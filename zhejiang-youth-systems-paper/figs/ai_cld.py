import os, json, base64, urllib.request
key = os.environ.get('CHEDANKJ_API_KEY')
prompt = (
"Reproduce EXACTLY the following causal loop diagram as a clean academic figure. Do not add, remove or "
"rename any node or arrow. Pure white background, flat vector style, thin dark-navy rounded rectangles, "
"straight or gently curved arrows, a small + or - sign beside every arrow, loop identifiers in small "
"circles. Serif-free crisp text, no shadows, no icons, no gradients.\n"
"NODES (place on a 3-row grid):\n"
"row 1 left to right: 'Digital transformation', 'Employer skill threshold', 'Mismatched employment'\n"
"row 2 left to right: 'Open searchers', 'Skill-threshold gap', 'Hiring rate', 'Market tightness'\n"
"row 3 left to right: 'Exam queue', 'Employability capital', 'Aspiration level', 'Offer quality'\n"
"ARROWS (source -> target, sign):\n"
"Digital transformation -> Employer skill threshold (+)\n"
"Mismatched employment -> Employer skill threshold (+)\n"
"Employer skill threshold -> Skill-threshold gap (-)\n"
"Employability capital -> Skill-threshold gap (+)\n"
"Skill-threshold gap -> Hiring rate (+)\n"
"Hiring rate -> Mismatched employment (-)\n"
"Hiring rate -> Open searchers (-)\n"
"Open searchers -> Hiring rate (+)\n"
"Open searchers -> Market tightness (-)\n"
"Market tightness -> Offer quality (+)\n"
"Offer quality -> Hiring rate (+)\n"
"Open searchers -> Employability capital (-)\n"
"Employability capital -> Hiring rate (+)\n"
"Open searchers -> Exam queue (+)\n"
"Exam queue -> Open searchers (+)\n"
"Exam queue -> Employability capital (-)\n"
"Skill-threshold gap -> Aspiration level (+)\n"
"Aspiration level -> Hiring rate (-)\n"
"LOOP LABELS: R1 between Open searchers and Employability capital; R2 between Open searchers and Exam "
"queue; R3 between Mismatched employment and Employer skill threshold; B1 between Skill-threshold gap "
"and Aspiration level; B2 between Open searchers, Market tightness and Offer quality.")
body = json.dumps({'model':'gpt-image-2','prompt':prompt,'size':'1536x1024','quality':'high'}).encode()
req = urllib.request.Request('https://www.chedankj.com/v1/images/generations', data=body,
    headers={'Authorization': f'Bearer {key}', 'Content-Type':'application/json'})
with urllib.request.urlopen(req, timeout=420) as r:
    data = json.load(r)
b64 = data['data'][0].get('b64_json')
img = base64.b64decode(b64) if b64 else urllib.request.urlopen(data['data'][0]['url'], timeout=300).read()
open('ai_cld.png','wb').write(img); print('ok', len(img)//1024,'KB')
