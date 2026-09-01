// Build the Chinese design-plan Word document from plan.md
//
// Typography spec:
//   章标题(一级) 黑体 小三(15pt) 加粗 | 节标题(二级) 黑体 四号(14pt)
//   条标题(三级及以下) 黑体 小四(12pt) | 正文 宋体 小四(12pt)，无段前段后间距
//   图名置于图下方、表名置于表上方，均为五号(10.5pt)黑体；表格为三线表
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, ImageRun, Table, TableRow, TableCell,
  WidthType, AlignmentType, HeadingLevel, BorderStyle, ShadingType,
  PageBreak, Header, Footer, PageNumber, LevelFormat, LineRuleType,
  Tab, TabStopType, LeaderType,
  VerticalAlign, convertMillimetersToTwip,
} = require('docx');

const SRC = path.join(__dirname, 'plan.md');
const OUT = process.argv[2] || path.join(__dirname, '禾章智能体建设方案.docx');

// eastAsia fonts; ascii/hAnsi carry the Latin companion face
const SONG = { ascii: 'Times New Roman', eastAsia: '宋体', hAnsi: 'Times New Roman' };
const HEI = { ascii: 'Times New Roman', eastAsia: '黑体', hAnsi: 'Times New Roman' };
const MONO = { ascii: 'Consolas', eastAsia: '宋体', hAnsi: 'Consolas' };

// half-point sizes
const XIAOSAN = 30;   // 小三 15pt
const SIHAO = 28;     // 四号 14pt
const XIAOSI = 24;    // 小四 12pt
const WUHAO = 21;     // 五号 10.5pt

const BLACK = '000000';
const LINE_15 = 300;  // 两页简报：行距约 1.25 倍

function pngSize(file) {
  const b = fs.readFileSync(file);
  return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
}

// inline **bold** -> TextRun[]
function runs(text, opts = {}) {
  const base = { font: opts.font || SONG, size: opts.size || XIAOSI, color: BLACK };
  const out = [];
  text.split('**').forEach((seg, i) => {
    if (seg === '') return;
    out.push(new TextRun({ ...base, text: seg, bold: i % 2 === 1 || !!opts.bold }));
  });
  if (!out.length) out.push(new TextRun({ ...base, text: '' }));
  return out;
}

// 正文：宋体小四，段前段后 0，首行缩进 2 字
function body(text) {
  return new Paragraph({
    children: runs(text),
    spacing: { line: LINE_15, lineRule: LineRuleType.AUTO, before: 0, after: 0 },
    indent: { firstLine: 480 },
    alignment: AlignmentType.JUSTIFIED,
  });
}

function caption(text) {
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { line: LINE_15, lineRule: LineRuleType.AUTO, before: 60, after: 180 },
    children: [new TextRun({ text, font: HEI, size: WUHAO, color: BLACK })],
  });
}

let rawText = fs.readFileSync(SRC, 'utf8');

// ---- 图表符号编号解析：按文档出现顺序为 {{fig:key}} / {{tbl:key}} 分配序号 ----
{
  const figKeys = [], tblKeys = [];
  for (const line of rawText.split('\n')) {
    const t = line.trim();
    let m;
    if ((m = t.match(/^!\[\{\{fig:([^}]+)\}\}/))) { if (!figKeys.includes(m[1])) figKeys.push(m[1]); }
    else if ((m = t.match(/^TABLE:\s*\{\{tbl:([^}]+)\}\}/))) { if (!tblKeys.includes(m[1])) tblKeys.push(m[1]); }
  }
  const unresolved = [];
  rawText = rawText.replace(/\{\{fig:([^}]+)\}\}/g, (_, k) => {
    const i = figKeys.indexOf(k);
    if (i < 0) { unresolved.push('fig:' + k); return '图?'; }
    return '图' + (i + 1);
  }).replace(/\{\{tbl:([^}]+)\}\}/g, (_, k) => {
    const i = tblKeys.indexOf(k);
    if (i < 0) { unresolved.push('tbl:' + k); return '表?'; }
    return '表' + (i + 1);
  });
  if (unresolved.length) {
    console.error('未定义的图表引用：' + [...new Set(unresolved)].join(', '));
    process.exit(1);
  }
  console.log(`图表编号：图 1-${figKeys.length}，表 1-${tblKeys.length}`);
}

const raw = rawText.split('\n');
const children = [];
const gap = (n = 1) => { for (let i = 0; i < n; i++) children.push(new Paragraph({ children: [new TextRun({ text: '', size: XIAOSI })] })); };

// ===================== 页首标题 =====================
{
  const t0 = rawText.split('\n').find(l => l.startsWith('# ')) || '';
  const sub = (rawText.split('\n').find(l => l.startsWith('SUBTITLE:')) || '').replace(/^SUBTITLE:\s*/, '');
  children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 0, after: 120, line: LINE_15, lineRule: LineRuleType.AUTO },
    children: [new TextRun({ text: t0.replace(/^#\s*/, ''), font: HEI, size: XIAOSAN, bold: true, color: BLACK })],
  }));
  if (sub) children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: BLACK, space: 5 } },
    spacing: { before: 0, after: 200, line: LINE_15, lineRule: LineRuleType.AUTO },
    children: [new TextRun({ text: sub, font: SONG, size: WUHAO, color: BLACK })],
  }));
}
const tocEntries = [];
const PAGEMAP = {};

// ===================== 正文 =====================
let i = 0;
let firstChapter = true;
let numInstance = 0;
let figNo = 0, tblNo = 0;
let pendingTableTitle = null;
const mentions = [];          // running record of body text, for cross-reference checking
const xrefProblems = [];

function seenBefore(label) {
  return mentions.some(m => m.includes(label));
}

function threeLineTable(lines, tableLabel) {
  const rowsRaw = lines.map(l => l.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(c => c.trim()));
  const dataRows = rowsRaw.filter((_, idx) => idx !== 1);      // drop the |---| separator
  const nCols = rowsRaw[0].length;
  const TOTAL = 9600;

  // 列宽按各列内容的实际长度分配：窄列（序号、金额）不再占用等分宽度，
  // 长文本列获得更多空间，表格整体更矮，减少跨页与页尾空白。
  const cjkLen = t => [...String(t)].reduce((n, ch) => n + (/[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]/.test(ch) ? 2 : 1), 0);
  const weights = Array.from({ length: nCols }, (_, c) => {
    const lens = dataRows.map(r => cjkLen((r[c] || '').replace(/\*\*/g, '')));
    const mx = Math.max(...lens, 1);
    return Math.max(4, Math.min(mx, 46));         // 上限防止超长单元格独吞宽度
  });
  const MINW = 620;                                // 最窄列下限，保证表头不挤成竖排
  const colW = [];
  {
    let free = TOTAL - MINW * nCols;
    const wsum = weights.reduce((a, b) => a + b, 0);
    for (let c = 0; c < nCols; c++) colW.push(MINW + Math.floor(free * weights[c] / wsum));
    colW[nCols - 1] += TOTAL - colW.reduce((a, b) => a + b, 0);   // 补足取整误差
  }

  const THICK = { style: BorderStyle.SINGLE, size: 12, color: BLACK };
  const THIN = { style: BorderStyle.SINGLE, size: 6, color: BLACK };
  const NONE = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
  const last = dataRows.length - 1;

  const keepWhole = dataRows.length <= 5;   // 仅很小的表强制不跨页，避免孤行
  const rows = dataRows.map((cells, r) => new TableRow({
    tableHeader: r === 0,
    cantSplit: true,          // 单行不跨页，避免一行被从中间劈开

    children: Array.from({ length: nCols }, (_, c) => new TableCell({
      width: { size: colW[c], type: WidthType.DXA },
      // 三线表：仅表首粗线、表头分隔细线、表末粗线
      borders: {
        top: r === 0 ? THICK : NONE,
        bottom: r === 0 ? THIN : (r === last ? THICK : NONE),
        left: NONE,
        right: NONE,
      },
      verticalAlign: VerticalAlign.CENTER,
      margins: { top: 40, bottom: 40, left: 80, right: 80 },
      children: [new Paragraph({
        alignment: r === 0 ? AlignmentType.CENTER : AlignmentType.LEFT,
        keepNext: keepWhole ? r < last : r === 0,
        indent: { firstLine: 0, left: 0, right: 0 },   // 表格文字不首行缩进
        spacing: { line: 250, lineRule: LineRuleType.AUTO, before: 0, after: 0 },
        children: runs((cells[c] || '').replace(/<br\s*\/?>/g, ' '), { size: WUHAO, font: r === 0 ? HEI : SONG }),
      })],
    })),
  }));

  children.push(new Table({
    columnWidths: colW,
    width: { size: TOTAL, type: WidthType.DXA },
    alignment: AlignmentType.CENTER,
    borders: { top: THICK, bottom: THICK, left: NONE, right: NONE, insideHorizontal: NONE, insideVertical: NONE },
    rows,
  }));
  children.push(new Paragraph({ spacing: { before: 0, after: 200 }, children: [new TextRun({ text: '', size: 12 })] }));
  if (!seenBefore(tableLabel)) xrefProblems.push(`${tableLabel} 未在其之前的正文中被提及`);
}

while (i < raw.length) {
  const t = raw[i].trim();

  if (t === '' || t === '---') { i++; continue; }
  if (/^# /.test(t) || /^SUBTITLE:/.test(t)) { i++; continue; }               // doc title lives on the cover

  // ---- 图：图名置于图下方，五号黑体 ----
  const im = t.match(/^!\[([^\]]*)\]\(([^)]+)\)$/);
  if (im) {
    const file = path.join(__dirname, im[2]);
    const { w, h } = pngSize(file);
    // 很宽的图不必占满版心；很高的图压低上限，避免把整页挤空
    const MAXW = 340;
    const MAXH = 730;
    let dw = MAXW, dh = Math.round(MAXW * h / w);
    if (dh > MAXH) { dh = MAXH; dw = Math.round(MAXH * w / h); }
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER,
      keepNext: true,
      spacing: { before: 120, after: 40, line: 240, lineRule: LineRuleType.AUTO },
      children: [new ImageRun({ type: 'png', data: fs.readFileSync(file), transformation: { width: dw, height: dh } })],
    }));
    figNo++;
    const label = `图${figNo}`;
    const title = im[1].replace(/^图\s*\d+[　\s]*/, '');
    children.push(caption(`${label}　${title}`));
    if (!seenBefore(label)) xrefProblems.push(`${label} 未在其之前的正文中被提及`);
    i++; continue;
  }

  // ---- 表名指令：表名置于表上方，五号黑体 ----
  if (/^TABLE:/.test(t)) {
    pendingTableTitle = t.replace(/^TABLE:\s*/, '').replace(/^表\s*\d+[　\s]*/, '');
    i++; continue;
  }

  // ---- 标题 ----
  if (/^#### /.test(t) || /^##### /.test(t)) {
    const txt = t.replace(/^#+\s/, '');
    children.push(new Paragraph({
      heading: HeadingLevel.HEADING_4,
      spacing: { before: 200, after: 100, line: LINE_15, lineRule: LineRuleType.AUTO },
      children: [new TextRun({ text: txt, font: HEI, size: XIAOSI, bold: false, italics: false, color: BLACK })],
    }));
    mentions.push(txt); i++; continue;
  }
  if (/^### /.test(t)) {
    const txt = t.replace(/^### /, '');
    tocEntries.push({ level: 2, text: txt });
    children.push(new Paragraph({
      heading: HeadingLevel.HEADING_3,
      spacing: { before: 140, after: 60, line: LINE_15, lineRule: LineRuleType.AUTO },
      children: [new TextRun({ text: txt, font: HEI, size: SIHAO, bold: false, italics: false, color: BLACK })],
    }));
    mentions.push(txt); i++; continue;
  }
  if (/^## /.test(t)) {
    const title = t.replace(/^## /, '');
    firstChapter = false;   // 章标题不另起页
    tocEntries.push({ level: 1, text: title });
    children.push(new Paragraph({
      heading: HeadingLevel.HEADING_2,
      alignment: AlignmentType.CENTER,
      spacing: { before: 130, after: 100, line: LINE_15, lineRule: LineRuleType.AUTO },
      children: [new TextRun({ text: title, font: HEI, size: XIAOSAN, bold: true, italics: false, color: BLACK })],
    }));
    mentions.push(title); i++; continue;
  }

  // ---- 表格 ----
  if (/^\|/.test(t)) {
    const block = [];
    while (i < raw.length && /^\s*\|/.test(raw[i])) { block.push(raw[i]); i++; }
    tblNo++;
    const label = `表${tblNo}`;
    children.push(caption(`${label}　${pendingTableTitle || ''}`.trim()));
    // caption() adds after-spacing meant for figures; tighten it for a table title
    children[children.length - 1] = new Paragraph({
      alignment: AlignmentType.CENTER,
      keepNext: true,
      spacing: { line: LINE_15, lineRule: LineRuleType.AUTO, before: 180, after: 60 },
      children: [new TextRun({ text: `${label}　${pendingTableTitle || ''}`.trim(), font: HEI, size: WUHAO, color: BLACK })],
    });
    threeLineTable(block, label);
    pendingTableTitle = null;
    continue;
  }

  // ---- 代码块 ----
  if (/^```/.test(t)) {
    i++;
    const code = [];
    while (i < raw.length && !/^```/.test(raw[i].trim())) { code.push(raw[i]); i++; }
    i++;
    code.forEach(cl => children.push(new Paragraph({
      spacing: { line: 260, lineRule: LineRuleType.AUTO, before: 0, after: 0 },
      indent: { left: 420 },
      children: [new TextRun({ text: cl.replace(/\t/g, '    ') || ' ', font: MONO, size: 19, color: BLACK })],
    })));
    children.push(new Paragraph({ spacing: { before: 0, after: 200 }, children: [new TextRun({ text: '', size: 12 })] }));
    continue;
  }

  // ---- 项目符号 / 编号列表 ----
  if (/^- /.test(t)) {
    const txt = t.replace(/^- /, '');
    children.push(new Paragraph({
      numbering: { reference: 'hz-bullet', level: 0 },
      spacing: { line: LINE_15, lineRule: LineRuleType.AUTO, before: 0, after: 0 },
      alignment: AlignmentType.JUSTIFIED,
      children: runs(txt),
    }));
    mentions.push(txt); i++; continue;
  }
  if (/^\d+\.\s/.test(t)) {
    if (Number(t.match(/^(\d+)\./)[1]) === 1) numInstance++;
    const txt = t.replace(/^\d+\.\s/, '');
    children.push(new Paragraph({
      numbering: { reference: 'hz-num', level: 0, instance: numInstance },
      spacing: { line: LINE_15, lineRule: LineRuleType.AUTO, before: 0, after: 0 },
      alignment: AlignmentType.JUSTIFIED,
      children: runs(txt),
    }));
    mentions.push(txt); i++; continue;
  }

  // ---- 正文段落 ----
  children.push(body(t));
  mentions.push(t);
  i++;
}

fs.writeFileSync(path.join(__dirname, 'toc_headings.json'), JSON.stringify(tocEntries, null, 1));

// ===================== 文档 =====================
const doc = new Document({
  styles: { default: { document: { run: { font: SONG, size: XIAOSI, color: BLACK }, paragraph: { spacing: { line: LINE_15, lineRule: LineRuleType.AUTO, before: 0, after: 0 } } } } },
  numbering: {
    config: [
      { reference: 'hz-bullet', levels: [{ level: 0, format: LevelFormat.BULLET, text: '●', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 780, hanging: 300 } }, run: { size: 16, color: BLACK } } }] },
      { reference: 'hz-num', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 780, hanging: 360 } }, run: { color: BLACK } } }] },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: convertMillimetersToTwip(210), height: convertMillimetersToTwip(297) },
        margin: {
          top: convertMillimetersToTwip(16), bottom: convertMillimetersToTwip(16),
          left: convertMillimetersToTwip(20), right: convertMillimetersToTwip(20),
        },
      },
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ children: ['— ', PageNumber.CURRENT, ' —'], font: SONG, size: WUHAO, color: BLACK })],
        })],
      }),
    },
    children,
  }],
});

Packer.toBuffer(doc).then(b => {
  fs.writeFileSync(OUT, b);
  console.log(`wrote ${OUT}  ${(b.length / 1048576).toFixed(2)}MB | 图 ${figNo} 幅 | 表 ${tblNo} 张 | 块 ${children.length}`);
  if (xrefProblems.length) {
    console.log('交叉引用问题：');
    xrefProblems.forEach(p => console.log('  ! ' + p));
  } else {
    console.log('交叉引用检查：全部图表均已在正文中先行提及 ✓');
  }
});
