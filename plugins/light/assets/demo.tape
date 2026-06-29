# Light README 演示动图录制脚本(vhs tape)
#
# 用法:安装 charmbracelet/vhs 后,在仓库根运行:
#   vhs assets/demo.tape
# 产出 assets/demo.gif。本机当前未装 vhs/asciinema,GIF 待后续在装有
# vhs 的环境渲染(见 PROGRESS R10 偏差日志:本轮以真实案例 PDF/九图作为
# "真的能跑"的证据,不放未经真实录制的动图)。
#
# 录制内容:场景 A 一句话触发文献检索 → 出综述骨架。
# 注意:tape 里的命令必须是真实可跑、离线安全的脚本演示;严禁伪造输出。

Output assets/demo.gif
Set FontSize 18
Set Width 1200
Set Height 660
Set Theme "Catppuccin Mocha"
Set Padding 20
Set TypingSpeed 60ms

Type "# 场景 A:一句话触发文献检索 → 综述骨架"
Enter
Sleep 800ms

Type "# Light 的 literature-search 技能内置可跑脚本,先看规范化检索"
Enter
Sleep 600ms

Type "python skills/light-literature-search/scripts/search_normalize.py --selftest"
Enter
Sleep 2500ms

Type "# PRISMA 流程留痕(系统综述筛选计数勾稽)"
Enter
Sleep 500ms
Type "python skills/light-literature-search/scripts/prisma_flow.py --selftest"
Enter
Sleep 2500ms

Type "# 全部离线 selftest 通过,产出可直接接入综述骨架"
Enter
Sleep 1500ms
