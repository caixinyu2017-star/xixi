# -*- coding: utf-8 -*-
"""禾创星 · 本地服务端

启动：
    python server.py
然后浏览器打开 http://127.0.0.1:8848
"""
import json
import re
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from hcx import config, docx_style, extract, llm
from hcx.corpus import CORPUS

app = FastAPI(title="禾创星 · 嘉兴创业智能体", version="1.0.0")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

# 内存态的附件仓库：{attachment_id: {"name", "text", "image"}}
ATTACHMENTS = {}


# ------------------------------------------------------------------ 模型 ---
class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    attachments: list[str] = []


class DocRequest(BaseModel):
    plan_text: str = ""
    attachments: list[str] = []
    kind: str = "improve"       # improve | landing


# ------------------------------------------------------------------ 工具 ---
def _gather_plan_text(plan_text: str, attachment_ids: list[str]) -> str:
    parts = []
    for aid in attachment_ids:
        item = ATTACHMENTS.get(aid)
        if item and item.get("text"):
            parts.append(f"【附件：{item['name']}】\n{item['text']}")
    if plan_text.strip():
        parts.append(plan_text.strip())
    return "\n\n".join(parts).strip()


def _safe_name(name: str) -> str:
    name = re.sub(r"[\\/:*?\"<>|\r\n]+", "_", name).strip()
    return name[:80] or "禾创星文档"


# ------------------------------------------------------------------ 接口 ---
@app.get("/api/status")
def status():
    return {
        "demo_mode": config.DEMO_MODE,
        "model": config.MODEL,
        "corpus_docs": len(CORPUS.docs),
        "corpus_titles": [d.title for d in CORPUS.docs],
        "policies": len(CORPUS.policies),
        "version": "1.0.0",
    }


@app.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    aid = uuid.uuid4().hex[:12]
    suffix = Path(file.filename or "file").suffix
    dest = config.UPLOAD_DIR / f"{aid}{suffix}"
    dest.write_bytes(await file.read())
    try:
        text, image = extract.extract(dest)
    except Exception as exc:                                   # noqa: BLE001
        text, image = f"[提示] 附件解析失败：{exc}", None
    ATTACHMENTS[aid] = {"name": file.filename, "text": text, "image": image,
                        "path": str(dest)}
    return {
        "id": aid,
        "name": file.filename,
        "chars": len(text or ""),
        "is_image": image is not None,
        "preview": (text or "")[:300],
    }


@app.post("/api/policies")
def policies(req: DocRequest):
    text = _gather_plan_text(req.plan_text, req.attachments)
    matched = CORPUS.match_policies(text or "创业", top_k=10)
    return {"matched": matched}


@app.post("/api/chat")
def chat(req: ChatRequest):
    msgs = []
    attach_text = ""
    for aid in req.attachments:
        item = ATTACHMENTS.get(aid)
        if not item:
            continue
        if item.get("text"):
            attach_text += f"\n\n【用户上传的附件：{item['name']}】\n{item['text']}"

    for i, m in enumerate(req.messages):
        content = m.content
        if i == len(req.messages) - 1 and m.role == "user":
            blocks = []
            for aid in req.attachments:
                item = ATTACHMENTS.get(aid)
                if item and item.get("image"):
                    blocks.append(item["image"])
            text_part = content + attach_text
            if blocks:
                blocks.append({"type": "text", "text": text_part})
                content = blocks
            else:
                content = text_part
        msgs.append({"role": m.role, "content": content})

    def event_stream():
        try:
            for chunk in llm.stream_chat(msgs, attach_text):
                yield f"data: {json.dumps({'delta': chunk}, ensure_ascii=False)}\n\n"
            yield f"data: {json.dumps({'done': True})}\n\n"
        except Exception as exc:                               # noqa: BLE001
            msg = f"\n\n[禾创星出错了] {exc}\n若是鉴权或网络问题，请检查 .env 里的 ANTHROPIC_API_KEY；也可以把 HCX_DEMO=1 打开离线演示模式。"
            yield f"data: {json.dumps({'delta': msg}, ensure_ascii=False)}\n\n"
            yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.post("/api/generate-doc")
def generate_doc(req: DocRequest):
    plan_text = _gather_plan_text(req.plan_text, req.attachments)
    if not plan_text:
        raise HTTPException(400, "请先上传创业计划书，或者在对话框里描述你的创业思路。")

    if req.kind == "landing":
        payload = llm.gen_landing_doc(plan_text)
    else:
        payload = llm.gen_improve_doc(plan_text)

    filename = _safe_name(payload.get("filename") or "禾创星文档")
    stamp = time.strftime("%Y%m%d-%H%M%S")
    out_path = config.OUTPUT_DIR / f"{filename}-{stamp}.docx"
    docx_style.render(payload["blocks"], str(out_path))
    return {
        "filename": out_path.name,
        "url": f"/api/download/{out_path.name}",
        "blocks": len(payload["blocks"]),
        "kind": req.kind,
    }


@app.get("/api/download/{name}")
def download(name: str):
    path = config.OUTPUT_DIR / name
    if not path.exists():
        path = config.SAMPLE_DIR / name
    if not path.exists():
        raise HTTPException(404, "文件不存在")
    return FileResponse(
        str(path),
        filename=path.name,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


@app.get("/api/samples")
def samples():
    if not config.SAMPLE_DIR.exists():
        return {"files": []}
    return {"files": [
        {"name": p.name, "url": f"/api/download/{p.name}", "size": p.stat().st_size}
        for p in sorted(config.SAMPLE_DIR.glob("*.docx"))
    ]}


app.mount("/", StaticFiles(directory=str(config.WEB_DIR), html=True), name="web")


if __name__ == "__main__":
    import uvicorn
    mode = "离线演示模式" if config.DEMO_MODE else f"实时模式（{config.MODEL}）"
    print("=" * 62)
    print("  禾创星 · 嘉兴本地化创业智能体")
    print(f"  运行模式：{mode}")
    print(f"  语料库：{len(CORPUS.docs)} 篇，结构化政策 {len(CORPUS.policies)} 条")
    print(f"  打开浏览器访问：http://{config.HOST}:{config.PORT}")
    print("=" * 62)
    uvicorn.run(app, host=config.HOST, port=config.PORT, log_level="warning")
