"""一个假的「WebVPN + CAS + 博达后台」站点，只为测试用。

复刻了真实环境里最难对付的几个特征：
  * CAS 登录页有图形验证码，点图片会换一张
  * 密码错和验证码错返回**不同**的提示（这样才能验证程序真的能区分）
  * 后台是多层 iframe：主文档 → 菜单 frame → 内容 frame
  * 左侧菜单默认折叠，必须先点「访问统计」才能看见「最近访问记录」
  * 会话可以被服务端主动作废，用来测试自动重登
"""
from __future__ import annotations

import random
import re
import string
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Optional

CORRECT_USER = "00008227"
CORRECT_PASSWORD = "correct-horse-battery"

RECORDS_ROWS = [
    ("2026-08-27 15:32:11", "223.104.3.77", "/2026/0824/c1001a12345/page.htm", "“文化魔方”亮相长三角高校"),
    ("2026-08-27 15:32:14", "223.104.3.77", "/2026/0729/c1001a12346/page.htm", "推荐单位意见"),
    ("2026-08-27 15:32:41", "106.11.159.22", "/index.htm", "首页"),
    ("2026-08-27 15:41:02", "36.24.88.190", "/2026/0728/c1001a12347/page.htm", "主要完成单位"),
]

LOGIN_PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>统一身份认证</title></head>
<body><h2>统一身份认证</h2>
{error}
<form method="post" action="/cas/login">
  <input type="hidden" name="execution" value="{execution}">
  <input type="hidden" name="_eventId" value="submit">
  <input type="hidden" name="service" value="{service}">
  <p>账号 <input type="text" name="username" id="username"></p>
  <p>密码 <input type="password" name="password" id="password"></p>
  {captcha_field}
  <button type="submit">登 录</button>
</form></body></html>"""

ADMIN_SHELL = """<!doctype html><html><head><meta charset="utf-8"><title>博达网站群</title></head>
<body><div id="topnav">
  <a href="#" id="deskTop">我的桌面</a>
  <a href="#" id="opCenter" onclick="document.getElementById('mainframe').src='/main.jsp';return false;">运营中心</a>
</div>
<iframe id="mainframe" name="mainframe" src="/blank.jsp" width="100%" height="600"></iframe>
</body></html>"""

MENU_FRAME = """<!doctype html><html><head><meta charset="utf-8"></head><body>
<div id="tree">
  <div>网站统计</div>
  <a href="#" id="visitStat" onclick="document.getElementById('sub').style.display='block';return false;">访问统计</a>
  <div id="sub" style="display:none">
    <a href="#" id="recent"
       onclick="document.getElementById('content').src='/records.jsp';return false;">最近访问记录</a>
    <a href="#" id="pv">页面浏览数</a>
  </div>
</div>
<iframe id="content" name="content" src="/blank.jsp" width="100%" height="500"></iframe>
</body></html>"""


def _records_html(rows) -> str:
    body = "".join(
        f"<tr><td>{i+1}</td><td>{t}</td><td>{ip}</td>"
        f"<td><a href='{url}' title='{title}'>{title}</a></td>"
        f"<td>-</td><td>Chrome 128</td><td>Windows 10</td><td>浙江</td></tr>"
        for i, (t, ip, url, title) in enumerate(rows)
    )
    # 外面故意套两层布局表格，和真实的博达后台一样
    return f"""<!doctype html><html><head><meta charset="utf-8"></head><body>
<table width="100%"><tr><td>
  <table width="100%"><tr><td class="title">运营中心 &gt; 网站统计 &gt; 访问统计 &gt; 最近访问记录</td></tr></table>
  <table width="100%" class="listTable" border="1">
    <tr class="tableHead"><th>序号</th><th>访问时间</th><th>来访IP</th><th>访问页面</th>
        <th>来源页面</th><th>浏览器</th><th>操作系统</th><th>来访地区</th></tr>
    {body}
  </table>
</td></tr></table></body></html>"""


class FakeSite:
    """开在随机端口上的假站点，用完记得 stop()。"""

    def __init__(self, require_captcha: bool = True):
        self.require_captcha = require_captcha
        self.captcha_code = self._new_code()
        self.valid_session: Optional[str] = None
        self.login_posts = 0            # 关键指标：表单被提交了几次
        self.captcha_fetches = 0
        self.rows = list(RECORDS_ROWS)
        self._server = ThreadingHTTPServer(("127.0.0.1", 0), self._make_handler())
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()

    @property
    def base(self) -> str:
        host, port = self._server.server_address[:2]
        return f"http://{host}:{port}"

    @property
    def login_url(self) -> str:
        return f"{self.base}/cas/login?service={urllib.parse.quote(self.base + '/system/caslogin.jsp')}"

    @property
    def target_url(self) -> str:
        return f"{self.base}/system/caslogin.jsp"

    def expire_session(self) -> None:
        """模拟 WebVPN 把会话踢掉。"""
        self.valid_session = None

    def stop(self) -> None:
        self._server.shutdown()
        self._server.server_close()

    @staticmethod
    def _new_code() -> str:
        return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))

    def _make_handler(self):
        site = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, *args):    # 别把测试输出刷满
                pass

            # -------- 工具 --------
            def _send(self, body: str, status: int = 200, ctype: str = "text/html; charset=utf-8",
                      headers=None):
                raw = body.encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(raw)))
                for k, v in (headers or {}):
                    self.send_header(k, v)
                self.end_headers()
                self.wfile.write(raw)

            def _logged_in(self) -> bool:
                cookie = self.headers.get("Cookie") or ""
                m = re.search(r"FAKESESSION=([^;]+)", cookie)
                return bool(m and site.valid_session and m.group(1) == site.valid_session)

            def _login_page(self, error: str = "", service: str = ""):
                captcha_field = ("""<p>验证码 <input type="text" name="captcha" id="captcha">
     <img id="captchaImg" src="/captcha.svg?t=0" width="110" height="40"
          onclick="this.src='/captcha.svg?t='+Date.now()"></p>"""
                                 if site.require_captcha else "")
                self._send(LOGIN_PAGE.format(
                    error=f"<p class='error' style='color:red'>{error}</p>" if error else "",
                    execution=f"e1s{random.randint(1, 9999)}",
                    service=service or (site.base + "/system/caslogin.jsp"),
                    captcha_field=captcha_field,
                ))

            # -------- GET --------
            def do_GET(self):
                path, _, query = self.path.partition("?")
                params = urllib.parse.parse_qs(query)
                if path in ("/", "/cas/login"):
                    self._login_page(service=(params.get("service") or [""])[0])
                elif path == "/captcha.svg":
                    site.captcha_fetches += 1
                    site.captcha_code = site._new_code()
                    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="110" height="40">'
                           f'<rect width="110" height="40" fill="white"/>'
                           f'<text x="8" y="30" font-family="DejaVu Sans, Arial" font-size="28" '
                           f'fill="black" letter-spacing="4">{site.captcha_code}</text></svg>')
                    self._send(svg, ctype="image/svg+xml")
                elif path == "/system/caslogin.jsp":
                    if not self._logged_in():
                        self.send_response(302)
                        self.send_header("Location", site.login_url)
                        self.send_header("Content-Length", "0")
                        self.end_headers()
                        return
                    self._send(ADMIN_SHELL)
                elif path == "/main.jsp":
                    self._send(MENU_FRAME if self._logged_in() else "<html><body>请重新登录</body></html>")
                elif path == "/records.jsp":
                    if not self._logged_in():
                        self.send_response(302)
                        self.send_header("Location", site.login_url)
                        self.send_header("Content-Length", "0")
                        self.end_headers()
                        return
                    self._send(_records_html(site.rows))
                elif path == "/blank.jsp":
                    self._send("<html><body></body></html>")
                else:
                    self._send("<html><body>404</body></html>", status=404)

            # -------- POST --------
            def do_POST(self):
                length = int(self.headers.get("Content-Length") or 0)
                form = urllib.parse.parse_qs(self.rfile.read(length).decode("utf-8"))
                if not self.path.startswith("/cas/login"):
                    self._send("<html><body>404</body></html>", status=404)
                    return
                site.login_posts += 1
                username = (form.get("username") or [""])[0]
                password = (form.get("password") or [""])[0]
                captcha = (form.get("captcha") or [""])[0]
                service = (form.get("service") or [""])[0]

                if username != CORRECT_USER or password != CORRECT_PASSWORD:
                    self._login_page("用户名或密码错误，请重新输入", service)
                    return
                if site.require_captcha and captcha.upper() != site.captcha_code.upper():
                    self._login_page("验证码错误，请重新输入", service)
                    return

                site.valid_session = "".join(random.choice(string.hexdigits) for _ in range(16))
                self.send_response(302)
                self.send_header("Set-Cookie", f"FAKESESSION={site.valid_session}; Path=/")
                self.send_header("Location", service or (site.base + "/system/caslogin.jsp"))
                self.send_header("Content-Length", "0")
                self.end_headers()

        return Handler
