#!/usr/bin/env python3
"""Generate images with OpenAI's GPT Image models (default: gpt-image-2).

The API key is read from the OPENAI_API_KEY environment variable — never
hard-code it in files or commit it to a repository.

Usage:
  python3 generate.py --prompt "..." [--out figure.png] [--model gpt-image-2]
                      [--size 1536x1024] [--quality high] [--n 1] [--transparent]

Sizes: 1024x1024, 1536x1024 (landscape), 1024x1536 (portrait), auto.
Quality: low / medium / high / auto (low is fine for drafts and much cheaper).
"""
import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request

API_URL = "https://api.openai.com/v1/images/generations"


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--prompt", required=True, help="detailed image description")
    p.add_argument("--out", default="image.png", help="output PNG path")
    p.add_argument("--model", default="gpt-image-2")
    p.add_argument("--size", default="1536x1024")
    p.add_argument("--quality", default="high")
    p.add_argument("--n", type=int, default=1, help="number of variants")
    p.add_argument("--transparent", action="store_true",
                   help="transparent background (PNG)")
    a = p.parse_args()

    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit(
            "OPENAI_API_KEY is not set.\n"
            "- Claude Code on the web: add it under your environment's "
            "environment variables (see https://code.claude.com/docs/en/claude-code-on-the-web).\n"
            "- Local Claude Code: export OPENAI_API_KEY=... in your shell profile, "
            'or add {"env": {"OPENAI_API_KEY": "..."}} to ~/.claude/settings.json.'
        )

    body = {"model": a.model, "prompt": a.prompt, "size": a.size,
            "quality": a.quality, "n": a.n}
    if a.transparent:
        body["background"] = "transparent"

    req = urllib.request.Request(
        API_URL, data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}",
                 "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            resp = json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        hint = ""
        if e.code in (403, 404) or "model" in detail.lower():
            hint = ("\nHint: if the error says the model is unknown or your account "
                    "lacks access, retry with --model gpt-image-1.")
        if e.code == 401:
            hint = "\nHint: the API key is invalid or was revoked — check/rotate it."
        sys.exit(f"OpenAI API error {e.code}: {detail}{hint}")
    except urllib.error.URLError as e:
        sys.exit(
            f"Network error reaching api.openai.com: {e.reason}\n"
            "In Claude Code remote environments, api.openai.com must be allowed in the "
            "environment's network policy (environment settings → network access)."
        )

    saved = []
    for i, item in enumerate(resp.get("data", [])):
        out = a.out if a.n == 1 else f"{os.path.splitext(a.out)[0]}-{i + 1}.png"
        with open(out, "wb") as f:
            f.write(base64.b64decode(item["b64_json"]))
        saved.append(out)
        print(out)
    if not saved:
        sys.exit(f"No image in response: {json.dumps(resp)[:500]}")
    usage = resp.get("usage")
    if usage:
        print(f"usage: {json.dumps(usage)}", file=sys.stderr)


if __name__ == "__main__":
    main()
