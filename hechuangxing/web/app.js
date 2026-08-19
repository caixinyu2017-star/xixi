/* 禾创星前端：聊天、附件上传、流式渲染、Word 生成 */
const $ = (s) => document.querySelector(s);
const chatEl = $("#chat"), inputEl = $("#input"), attachBar = $("#attach-bar");
let messages = [];          // 发给后端的对话历史
let attachments = [];       // [{id,name,chars,is_image}]
let busy = false;

/* --------------------------------------------------------- 小工具 --- */
function toast(text) {
  const el = document.createElement("div");
  el.className = "toast"; el.textContent = text;
  document.body.appendChild(el);
  requestAnimationFrame(() => el.classList.add("on"));
  setTimeout(() => { el.classList.remove("on"); setTimeout(() => el.remove(), 300); }, 2600);
}
const esc = (s) => s.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));

/* 轻量 Markdown 渲染：标题、粗体、行内代码、列表、表格、分隔线 */
function md(src) {
  const lines = src.replace(/\r/g, "").split("\n");
  let out = "", i = 0;
  const inline = (t) => esc(t)
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/`([^`]+)`/g, "<code>$1</code>");

  while (i < lines.length) {
    const line = lines[i];

    // 表格
    if (/^\s*\|.*\|\s*$/.test(line) && /^\s*\|[\s:|-]+\|\s*$/.test(lines[i + 1] || "")) {
      const cells = (r) => r.trim().replace(/^\||\|$/g, "").split("|").map((c) => c.trim());
      const head = cells(line); i += 2;
      let body = "";
      while (i < lines.length && /^\s*\|.*\|\s*$/.test(lines[i])) {
        body += "<tr>" + cells(lines[i]).map((c) => `<td>${inline(c)}</td>`).join("") + "</tr>";
        i++;
      }
      out += `<table><thead><tr>${head.map((h) => `<th>${inline(h)}</th>`).join("")}</tr></thead><tbody>${body}</tbody></table>`;
      continue;
    }
    // 标题
    let m = line.match(/^(#{1,6})\s+(.*)$/);
    if (m) { const lv = Math.min(m[1].length + 1, 4); out += `<h${lv}>${inline(m[2])}</h${lv}>`; i++; continue; }
    // 分隔线
    if (/^\s*(-{3,}|\*{3,})\s*$/.test(line)) { out += "<hr>"; i++; continue; }
    // 有序 / 无序列表
    if (/^\s*(\d+\.|[-*])\s+/.test(line)) {
      const ordered = /^\s*\d+\./.test(line);
      let items = "";
      while (i < lines.length && /^\s*(\d+\.|[-*])\s+/.test(lines[i])) {
        items += `<li>${inline(lines[i].replace(/^\s*(\d+\.|[-*])\s+/, ""))}</li>`; i++;
      }
      out += ordered ? `<ol>${items}</ol>` : `<ul>${items}</ul>`;
      continue;
    }
    // 空行
    if (!line.trim()) { i++; continue; }
    // 普通段落
    let buf = [];
    while (i < lines.length && lines[i].trim() && !/^\s*(#{1,6}\s|\||\d+\.\s|[-*]\s|-{3,})/.test(lines[i])) {
      buf.push(lines[i]); i++;
    }
    if (buf.length) out += `<p>${inline(buf.join(" "))}</p>`;
    else { out += `<p>${inline(line)}</p>`; i++; }
  }
  return out;
}

/* --------------------------------------------------------- 渲染 --- */
function clearWelcome() { const w = chatEl.querySelector(".welcome"); if (w) w.remove(); }

function addMsg(role, text, files) {
  clearWelcome();
  const wrap = document.createElement("div");
  wrap.className = `msg ${role === "user" ? "user" : "bot"}`;
  const avatar = role === "user"
    ? `<div class="avatar">我</div>`
    : `<div class="avatar"><img src="logo.svg" alt="禾创星"></div>`;
  const fileTags = (files && files.length)
    ? `<div class="files">${files.map((f) => `<span class="tag">${esc(f.name)}</span>`).join("")}</div>` : "";
  wrap.innerHTML = `${avatar}<div class="bubble">
      <div class="who">${role === "user" ? "我" : "禾创星"}</div>
      <div class="body">${role === "user" ? esc(text) + fileTags : md(text)}</div>
    </div>`;
  chatEl.appendChild(wrap);
  chatEl.scrollTop = chatEl.scrollHeight;
  return wrap.querySelector(".body");
}

/* ------------------------------------------------------- 附件区 --- */
function renderAttachments() {
  attachBar.innerHTML = attachments.map((a, idx) => `
    <div class="att"><b>${esc(a.name)}</b>
      <small>${a.is_image ? "图片" : a.chars + " 字"}</small>
      <button class="x" data-i="${idx}">×</button></div>`).join("");
  attachBar.querySelectorAll(".x").forEach((b) =>
    b.onclick = () => { attachments.splice(+b.dataset.i, 1); renderAttachments(); refreshRadar(); });
}

async function uploadFiles(fileList) {
  for (const file of fileList) {
    const fd = new FormData(); fd.append("file", file);
    try {
      const res = await fetch("/api/upload", { method: "POST", body: fd });
      const data = await res.json();
      attachments.push(data);
      toast(`已读取 ${data.name}${data.is_image ? "" : "，" + data.chars + " 字"}`);
    } catch (e) { toast("上传失败：" + e.message); }
  }
  renderAttachments(); refreshRadar();
}

/* --------------------------------------------------------- 发送 --- */
async function send(textOverride) {
  if (busy) return;
  const text = (textOverride ?? inputEl.value).trim();
  if (!text && !attachments.length) return;

  const usedFiles = attachments.slice();
  addMsg("user", text || "（已上传附件，请分析）", usedFiles);
  messages.push({ role: "user", content: text || "请分析我上传的创业计划书。" });
  inputEl.value = ""; inputEl.style.height = "auto";
  refreshRadar();

  busy = true; $("#btn-send").disabled = true;
  const body = addMsg("bot", "");
  body.innerHTML = '<span class="cursor"></span>';
  let acc = "";

  try {
    const res = await fetch("/api/chat", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages, attachments: usedFiles.map((f) => f.id) }),
    });
    const reader = res.body.getReader(), dec = new TextDecoder();
    let buf = "";
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buf += dec.decode(value, { stream: true });
      const parts = buf.split("\n\n"); buf = parts.pop();
      for (const part of parts) {
        const line = part.trim();
        if (!line.startsWith("data:")) continue;
        const payload = JSON.parse(line.slice(5));
        if (payload.delta) {
          acc += payload.delta;
          body.innerHTML = md(acc) + '<span class="cursor"></span>';
          chatEl.scrollTop = chatEl.scrollHeight;
        }
      }
    }
    body.innerHTML = md(acc);
    messages.push({ role: "assistant", content: acc });
  } catch (e) {
    body.innerHTML = md("[连接出错] " + e.message);
  } finally {
    busy = false; $("#btn-send").disabled = false; inputEl.focus();
  }
}

/* --------------------------------------------------- 文档生成 --- */
async function genDoc(kind, btn) {
  const planText = messages.filter((m) => m.role === "user").map((m) => m.content).join("\n\n");
  if (!planText && !attachments.length) { toast("先上传创业计划书，或先描述一下你的项目"); return; }
  const old = btn.innerHTML;
  btn.disabled = true;
  btn.innerHTML = "<b>正在生成…</b><span>按排版规范渲染 Word，请稍候</span>";
  try {
    const res = await fetch("/api/generate-doc", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ kind, plan_text: planText, attachments: attachments.map((a) => a.id) }),
    });
    if (!res.ok) throw new Error((await res.json()).detail || res.statusText);
    const data = await res.json();
    const a = document.createElement("a");
    a.href = data.url; a.textContent = data.filename; a.download = data.filename;
    $("#downloads").prepend(a);
    toast("已生成：" + data.filename);
    addMsg("bot", `**Word 已生成：${data.filename}**\n\n共 ${data.blocks} 个内容块，排版已按规范设置：一级标题黑体小三居中、二级标题黑体四号、三级标题宋体加粗小四、正文宋体加 Times New Roman、无段前段后间距、首行缩进 2 字符，表格单倍行距居中。右侧可下载。`);
  } catch (e) { toast("生成失败：" + e.message); }
  finally { btn.disabled = false; btn.innerHTML = old; }
}

/* --------------------------------------------------- 政策雷达 --- */
let radarTimer = null;
function refreshRadar() {
  clearTimeout(radarTimer);
  radarTimer = setTimeout(async () => {
    const text = messages.filter((m) => m.role === "user").map((m) => m.content).join(" ")
      + " " + attachments.map((a) => a.name).join(" ") + " " + inputEl.value;
    if (!text.trim()) return;
    try {
      const res = await fetch("/api/policies", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ plan_text: text, attachments: attachments.map((a) => a.id) }),
      });
      const { matched } = await res.json();
      if (!matched.length) return;
      $("#radar-note").textContent = `命中 ${matched.length} 条政策，按匹配度排序`;
      $("#radar").innerHTML = matched.map((p) => `
        <div class="pol"><span class="n">${esc(p.name)}</span>
          <span class="a">${esc(p.amount)}</span>
          <div class="d">${esc(p.level)} · ${esc(p.dept)}</div></div>`).join("");
    } catch (e) { /* 静默 */ }
  }, 400);
}

/* ------------------------------------------------------- 初始化 --- */
(async function init() {
  try {
    const s = await (await fetch("/api/status")).json();
    $("#mode-text").textContent = s.demo_mode ? "离线演示模式" : "实时模式 · Claude";
    if (!s.demo_mode) $("#mode-badge").classList.add("live");
    $("#corpus-docs").textContent = s.corpus_docs;
    $("#corpus-pol").textContent = s.policies;
    $("#corpus-list").innerHTML = s.corpus_titles.map((t) => `<li>${esc(t)}</li>`).join("");
  } catch (e) { $("#mode-text").textContent = "后端未连接"; }

  try {
    const { files } = await (await fetch("/api/samples")).json();
    $("#samples").innerHTML = files.map((f) =>
      `<a href="${f.url}" download="${esc(f.name)}">${esc(f.name)}</a>`).join("")
      || '<div class="panel-note">暂无示例文件</div>';
  } catch (e) { /* 忽略 */ }
})();

/* 事件绑定 */
$("#btn-send").onclick = () => send();
$("#btn-attach").onclick = () => $("#file-input").click();
$("#file-input").onchange = (e) => { uploadFiles(e.target.files); e.target.value = ""; };
$("#btn-improve").onclick = (e) => genDoc("improve", e.currentTarget);
$("#btn-landing").onclick = (e) => genDoc("landing", e.currentTarget);
$("#btn-clear").onclick = () => {
  messages = []; attachments = []; renderAttachments();
  chatEl.innerHTML = ""; location.reload();
};
inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); send(); }
});
inputEl.addEventListener("input", () => {
  inputEl.style.height = "auto";
  inputEl.style.height = Math.min(inputEl.scrollHeight, 190) + "px";
  refreshRadar();
});
document.querySelectorAll(".chip").forEach((c) => c.onclick = () => send(c.dataset.q));
document.querySelectorAll("#chain-list li").forEach((li) => li.onclick = () => send(li.dataset.q));

/* 拖拽与粘贴上传 */
const mask = $("#drop-mask");
let dragDepth = 0;
window.addEventListener("dragenter", (e) => { e.preventDefault(); dragDepth++; mask.classList.add("on"); });
window.addEventListener("dragleave", () => { if (--dragDepth <= 0) mask.classList.remove("on"); });
window.addEventListener("dragover", (e) => e.preventDefault());
window.addEventListener("drop", (e) => {
  e.preventDefault(); dragDepth = 0; mask.classList.remove("on");
  if (e.dataTransfer.files.length) uploadFiles(e.dataTransfer.files);
});
window.addEventListener("paste", (e) => {
  const files = [...(e.clipboardData?.files || [])];
  if (files.length) { e.preventDefault(); uploadFiles(files); }
});
