# -*- coding: utf-8 -*-
"""用 OpenAI 图像模型（image 2 / gpt-image 系列）生成书稿概念图/示意图。

用法（需环境变量 OPENAI_API_KEY，新会话中生效）：
    python3 openai_figures.py --list                 # 查看可生成清单
    python3 openai_figures.py fig_cover              # 生成指定图
    python3 openai_figures.py --all                  # 生成全部清单项
    python3 openai_figures.py fig_cover --model gpt-image-1   # 指定模型

说明：
- 默认依次尝试模型 gpt-image-2、gpt-image-1（以账户实际可用为准）。
- 输出 PNG 到 figs_ai/ 目录（不覆盖 figs/ 下的矢量图；替换书稿中的图需
  修改对应章节 content_chNN.py 的 fig 路径后重新 assemble）。
- 中文文字渲染是图像模型的弱项，提示词默认要求“无文字/极少文字”，
  文字性标注仍建议由矢量图承担。
"""
import argparse
import base64
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'figs_ai')

# 待生成清单：key -> (文件名, 提示词)。可按需增删。
PROMPTS = {
    'fig_cover': (
        'cover_concept.png',
        '学术专著封面概念图：中国绿色低碳转型主题，抽象的碳分子与标准文件符号交织，'
        '深蓝与青绿渐变配色，简洁现代的扁平插画风格，大量留白，无任何文字。'),
    'fig1_concept': (
        'ch01_concept.png',
        '概念插图：三个相互咬合的齿轮分别象征政策、技术、市场三重驱动力，'
        '推动一座由标准文件构成的桥梁伸向低碳地球，扁平矢量插画风格，'
        '蓝绿主色调，白色背景，无文字。'),
    'fig3_concept': (
        'ch03_concept.png',
        '概念插图：全球绿色规则博弈，地球两侧分别是欧盟旗帜色调的关税之门与'
        '东方色调的绿色工厂，中间是天平与标准文件，扁平插画，克制配色，无文字。'),
    'fig9_concept': (
        'ch09_concept.png',
        '概念插图：五根绿色支柱托起一个透明穹顶（象征五大功能模块支撑标准体系），'
        '穹顶上方有上升的箭头与叶片，简洁等距插画风格，白底，无文字。'),
}


def generate(key, model_pref):
    fname, prompt = PROMPTS[key]
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        sys.exit('错误：环境变量 OPENAI_API_KEY 未配置（需在配置后新启动的会话中运行）。')
    os.makedirs(OUT, exist_ok=True)
    last_err = None
    for model in model_pref:
        body = json.dumps({'model': model, 'prompt': prompt,
                           'size': '1536x1024', 'quality': 'high'}).encode()
        req = urllib.request.Request(
            'https://api.openai.com/v1/images/generations', data=body,
            headers={'Authorization': f'Bearer {api_key}',
                     'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                data = json.load(r)
            b64 = data['data'][0].get('b64_json')
            if b64 is None:  # 部分模型返回 url
                url = data['data'][0]['url']
                with urllib.request.urlopen(url, timeout=300) as r2:
                    img = r2.read()
            else:
                img = base64.b64decode(b64)
            path = os.path.join(OUT, fname)
            with open(path, 'wb') as f:
                f.write(img)
            print(f'ok {key} -> {path}  (model={model}, {len(img)//1024}KB)')
            return
        except Exception as e:  # noqa: BLE001
            last_err = e
            msg = getattr(e, 'read', lambda: b'')()
            print(f'  模型 {model} 失败：{e} {msg[:200] if msg else ""}', file=sys.stderr)
    sys.exit(f'全部模型均失败：{last_err}')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('keys', nargs='*')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--model', help='强制指定模型，如 gpt-image-2')
    a = ap.parse_args()
    if a.list or (not a.keys and not a.all):
        for k, (f, p) in PROMPTS.items():
            print(f'{k:14s} -> figs_ai/{f}\n    {p[:60]}…')
        sys.exit(0)
    pref = [a.model] if a.model else ['gpt-image-2', 'gpt-image-1']
    for k in (list(PROMPTS) if a.all else a.keys):
        generate(k, pref)
