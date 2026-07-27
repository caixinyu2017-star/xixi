# -*- coding: utf-8 -*-
"""调用 image2（gpt-image-2）生成学术机制图。"""
import base64, json, os, subprocess, sys, tempfile, time

API = 'https://chedankj.com/v1/images/generations'
KEY = os.environ['CHEDANKJ_API_KEY']
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aifig')
os.makedirs(OUT, exist_ok=True)

STYLE = (
    'Style requirements: a clean, professional academic figure for a Chinese management '
    'journal. Pure white background. Flat vector look, NO 3D, NO gradients, NO shadows, '
    'NO icons, NO illustrations, NO photographs, NO decorative elements. '
    'Only rounded rectangles, thin arrows and thin connector lines. '
    'Restrained palette: dark navy (#2F4858), medium slate blue (#5B7C99), '
    'light blue-gray (#A8BFD0), pale blue (#DCE6ED), neutral gray (#7A7A7A) and white. '
    'All text must be rendered in Simplified Chinese, in a clean sans-serif '
    'font, horizontally, perfectly legible and correctly spelled, no garbled or invented '
    'characters. Text must never overflow its box and must never overlap any line or arrow. '
    'Generous white space. Balanced, symmetrical composition. High resolution, crisp edges.'
)


def gen(name, prompt, size='1536x1024', retries=3):
    path = os.path.join(OUT, name + '.png')
    body = json.dumps({
        'model': 'gpt-image-2',
        'prompt': prompt.strip() + '\n\n' + STYLE,
        'size': size,
        'n': 1,
    }).encode('utf-8')
    last = None
    for k in range(retries):
        try:
            with tempfile.NamedTemporaryFile('wb', suffix='.json', delete=False) as tf:
                tf.write(body); payload = tf.name
            res = subprocess.run(
                ['curl', '-sS', '--max-time', '900', API,
                 '-H', 'Authorization: Bearer ' + KEY,
                 '-H', 'Content-Type: application/json',
                 '--data-binary', '@' + payload],
                capture_output=True, timeout=920)
            os.unlink(payload)
            if res.returncode != 0:
                raise RuntimeError(res.stderr.decode('utf-8', 'ignore')[:200])
            d = json.loads(res.stdout.decode('utf-8'))
            if 'data' not in d:
                raise RuntimeError(json.dumps(d)[:300])
            item = d['data'][0]
            if 'b64_json' in item:
                open(path, 'wb').write(base64.b64decode(item['b64_json']))
            else:
                subprocess.run(['curl', '-sS', '--max-time', '300', '-o', path, item['url']],
                               check=True, timeout=320)
            print('OK  ', name, os.path.getsize(path) // 1024, 'KB')
            return path
        except Exception as e:
            last = e
            print('retry', k + 1, name, repr(e)[:160])
            time.sleep(4 * (k + 1))
    print('FAIL', name, repr(last)[:200])
    return None


if __name__ == '__main__':
    import importlib.util
    spec = importlib.util.spec_from_file_location('prompts', sys.argv[1])
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    only = sys.argv[2:] if len(sys.argv) > 2 else None
    for name, size, prompt in m.PROMPTS:
        if only and name not in only:
            continue
        gen(name, prompt, size)
