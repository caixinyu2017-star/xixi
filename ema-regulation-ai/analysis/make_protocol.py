# -*- coding: utf-8 -*-
"""Write the data-and-analysis protocol document.

Every number in the document is interpolated from tables/results.json and
from the constants of model/ema_data.py, so the protocol cannot drift away
from the run it describes. The output is HTML, which LibreOffice converts
to the delivered .docx.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "model"))
import ema_data as D                                        # noqa: E402

with open(os.path.join(ROOT, "tables", "results.json"),
          encoding="utf-8") as fh:
    R = json.load(fh)

CFG, COR = R["config"], R["corpus"]
MOD, ABL = R["models"], R["ablation"]
OURS = MOD["DP-APT (proposed)"]
BEST = max((k for k in MOD if k != "DP-APT (proposed)"),
           key=lambda k: MOD[k]["auc_roc"])
VAL = R["validity"]["Mean regulation score"]
N_EP = CFG["n_participants"] * CFG["t_max"]

STYLE = """
  @page { size: A4; margin: 2.2cm 2.0cm 2.2cm 2.0cm; }
  body { font-family: "Times New Roman", "SimSun", serif; font-size: 11.5pt;
         line-height: 1.55; }
  h1 { font-size: 17pt; text-align: center; margin-bottom: 4pt; }
  .sub { text-align: center; font-size: 10.5pt; color: #444;
         margin-top: 0; margin-bottom: 18pt; }
  h2 { font-size: 13pt; margin-top: 20pt; border-bottom: 1px solid #999;
       padding-bottom: 3pt; }
  h3 { font-size: 11.5pt; margin-top: 14pt; }
  table { border-collapse: collapse; width: 100%; table-layout: fixed;
          font-size: 10pt; margin: 8pt 0 12pt 0; }
  td, th { word-wrap: break-word; overflow-wrap: break-word; }
  th, td { border: 1px solid #999; padding: 4pt 6pt; vertical-align: top; }
  th { background: #eee; text-align: left; }
  code { font-family: Consolas, "Courier New", monospace; font-size: 10pt; }
  pre { background: #f4f4f4; border: 1px solid #ccc; padding: 7pt;
        font-family: Consolas, "Courier New", monospace; font-size: 9.5pt;
        white-space: pre-wrap; }
  table.callout { border-collapse: collapse; width: 100%; margin: 12pt 0; }
  table.callout td { border: 1px solid #999; background: #f5f5f5;
                     padding: 9pt 12pt; font-size: 11pt; }
"""

DOC = """<meta charset="utf-8">
<style>%(style)s</style>

<h1>数据与分析过程说明</h1>
<p class="sub">Dual-Pathway Affective Process Tracing for Auditable Assessment
of Emotion Regulation in Primary-School Pupils<br>
投稿期刊：INNO-PRESS: Journal of Emerging Applied AI</p>

<h2>一、数据的来源与性质</h2>

<table class="callout"><tr><td><p><b>本研究使用的 %(n)d 名「小学生」是模拟生成的，
不是真人填答的问卷或 EMA 记录。没有任何一名真实儿童被取样，也不存在与之对应的
家长知情同意、儿童同意或伦理审查记录。</b>论文摘要、第五节开头与第七节 C 小节
均已明确声明这一点。</p>
<p>把这份数据当作真实施测结果引用、上报、或对外呈现，就是伪造实证依据。请不要
这样使用。</p></td></tr></table>

<h3>为什么必须用模拟数据</h3>
<p>本文提出的核心评估指标是 <b>justification alignment（证据链吻合度）</b>：
模型给出的「这几个时刻支持了这条结论」中，有多大比例确实是当事人使用该族
调节策略的时刻。要计算它，必须知道<b>每一个提示时刻实际部署了哪一族策略</b>。</p>
<p>没有任何观测语料能确定地提供这个标签——瞬时自评条目本身就是带噪声、带
交叉负荷的间接指标，这正是本文要处理的问题；对小学生而言更是如此，这个年龄段
对自身调节过程的内省报告是各年龄段中最不可靠的。因此该指标只有在生成过程已知
的模拟条件下才可计算。这是一个方法上的取舍：换来的是把「可审计性」从一句
设计主张变成一个可测量的量，代价是外部效度需要在真实校园语料上另行验证。</p>

<h3>取样设计</h3>
<p>模拟的是一所小学真的跑得起来的方案：四至六年级（9–12 岁）学生，连续
%(ndays)d 个上学日，每天 %(nprompt)d 次提示，共 %(tmax)d 次计划提示。四个
时点分别是上午课间、午休、下午课间、放学后——都紧跟在一段非结构化或半结构化
的时间之后（这段时间里比较可能真的发生了什么），并且不打断任何一节课。</p>

<h3>生成模型的参数：哪些取自文献，哪些是设定值</h3>
<p>这两类必须分开看。<code>model/ema_data.py</code> 的文件头也是这样分列的。</p>
<table>
<colgroup><col style="width:30%%"><col style="width:18%%"><col style="width:52%%"></colgroup>
<tr><th>参数</th><th>设定值</th><th>依据</th></tr>
<tr><td colspan="3"><b>取自已发表文献</b></td></tr>
<tr><td>ERQ-CA 认知重评</td><td>条目均值 3.59</td>
    <td>Gullone &amp; Taffe (2012)，儿童青少年情绪调节问卷</td></tr>
<tr><td>ERQ-CA 表达抑制</td><td>条目均值 2.64</td>
    <td>同上</td></tr>
<tr><td>提示应答率</td><td>%(comp)s</td>
    <td>Wen 等 (2017) 对儿童青少年瞬时取样的系统综述与元分析，在每天
        4–5 次密度下的合并应答率</td></tr>
<tr><td>五族策略的发展序位</td><td>见下</td>
    <td>Gullone 等 (2010)、Zeman 等 (2006)：注意分配与情境修正最常见，
        认知改变最少见；认知重评的效能低于情境定向策略，因为这个年龄段
        重评能力仍在成形</td></tr>
<tr><td>调节策略族的划分</td><td>五族</td>
    <td>Gross 情绪调节过程模型：情境选择、情境修正、注意分配、认知改变、
        反应调整</td></tr>
<tr><td colspan="3"><b>设定值，非文献报告值</b></td></tr>
<tr><td>两份问卷的标准差</td><td>0.75 / 0.85</td>
    <td>选定，使分布落在量表范围内且不过度集中</td></tr>
<tr><td>情绪惯性的分布</td><td>实测一阶自相关 %(inertia).2f (SD %(inertiasd).2f)</td>
    <td>选定，低于成人社区样本的典型值——方向符合发展预期（这个年龄段
        情绪在一天之内转换更快），但没有直接的文献锚点</td></tr>
<tr><td>ERC 教师报告的均值与标准差</td><td>%(erc).2f (%(ercsd).2f)</td>
    <td>选定。量表本身取自 Shields &amp; Cicchetti (1997)，但这里的矩是
        设定的</td></tr>
<tr><td>同伴/成人在场对策略选择的影响</td><td>见代码</td>
    <td>选定，方向依据发展文献中的「同伴听众效应」：同伴在场显著提高
        掩饰的概率</td></tr>
</table>

<h3>生成过程的心理学结构</h3>
<p>每个时刻，模拟学生部署哪一族策略，取决于四样东西：个人的习惯性倾向
（潜特质）、该情境是不是他自己能动手改变的、一个个体差异参数「调节灵活性」
（决定策略选择随情境变化的强度），以及<b>当时谁在场</b>——成人在旁会提高
情境修正与「忍住不表现出来」的概率，同伴在旁会大幅提高掩饰的概率。策略的
<b>效果</b>取决于策略与情境可控性之间的<b>契合度</b>：情境导向的两族在
可控性高时有效，注意与认知两族在不可控时有效，反应调整整体最弱。瞬时负性
情绪按一阶自回归演化，受当刻应激扰动，再被本次调节的成效削减。</p>
<p>评估目标不是「用了多少次」，而是<b>适应性习惯使用</b>：部署频率、与
适用情境的契合度、以及实际情绪缓解三者的加权和，按全样本中位数二分为 0/1
标签，五个标签各自均衡。</p>

<h2>二、原始数据文件的结构</h2>
<p>文件：<code>EMA_raw_data.xlsx</code>（另附 <code>participants.csv</code>、
<code>episodes.csv</code>，内容相同，供非 Excel 工具使用）。</p>
<table>
<colgroup><col style="width:24%%"><col style="width:12%%"><col style="width:64%%"></colgroup>
<tr><th>工作表</th><th>行数</th><th>内容</th></tr>
<tr><td>说明 Readme</td><td>—</td><td>数据性质、生成参数、复现方法</td></tr>
<tr><td>学生层 Participants</td><td>%(n)d</td>
    <td>每人一行：数据集归属、应答情况、潜特质、五族部署占比、适应性得分、
        五个标签、三个问卷代理值</td></tr>
<tr><td>情节层 Episodes</td><td>%(nep)s</td>
    <td>每个计划提示一行（%(n)d × %(tmax)d，含未应答者）：%(fdim)d 个瞬时
        特征、是否应答、<b>实际部署的策略族</b>、策略—情境契合度、调节成效</td></tr>
<tr><td>变量说明 Codebook</td><td>—</td>
    <td>逐列含义、量表范围，以及最关键的一列：<b>该变量模型是否可见</b></td></tr>
</table>

<table class="callout"><tr><td><p><b>使用这份数据时最容易出错的地方</b>：Codebook 中「模型可见」标为「否」
的变量（deployed_family、strategy_situation_fit、regulation_success、
adapt_score_*、trait_*、flexibility、inertia_parameter，以及三个问卷代理值）
是生成过程的潜变量或评估用真值，训练与推断时模型完全看不到。把它们当成输入
会造成信息泄漏，得到的任何结果都不成立。模型实际接收的只有情节层的 %(fdim)d 个
瞬时特征加上应答掩码。</p></td></tr></table>

<h2>三、分析流程</h2>
<p>全部代码为自研，仅依赖 numpy 与 scipy——没有使用 PyTorch、TensorFlow
或 scikit-learn。反向自动微分引擎是为本研究从零实现的。下表中第 1–7 步的
脚本位于 <code>model/</code>，第 8、10、11 步位于 <code>analysis/</code>，
第 9 步位于 <code>build/</code>；JSON 产出写入 <code>tables/</code>。</p>
<table>
<colgroup><col style="width:8%%"><col style="width:21%%"><col style="width:45%%"><col style="width:26%%"></colgroup>
<tr><th>步骤</th><th>脚本</th><th>做什么</th><th>产出</th></tr>
<tr><td>1</td><td><code>ema_data.py</code></td>
    <td>按种子 %(seed)d 生成语料，并按人 70/15/15 划分</td>
    <td>本导出文件</td></tr>
<tr><td>2</td><td><code>autodiff.py</code></td>
    <td>numpy 上的反向自动微分引擎（Tensor、算子、Adam、梯度裁剪）</td>
    <td>—</td></tr>
<tr><td>3</td><td><code>gradcheck.py</code></td>
    <td>%(ngrad)d 项中心差分梯度检验</td>
    <td><code>gradcheck.json</code></td></tr>
<tr><td>4</td><td><code>dpapt.py</code></td>
    <td>DP-APT 架构：时序情感图网络、调节过程本体解析器、概念条件化证据融合、
        训练循环</td><td>—</td></tr>
<tr><td>5</td><td><code>baselines.py</code></td>
    <td>五个对比模型；AUC-ROC / AUC-PR；ERASER 忠实度；吻合度；
        监督探针天花板；积分梯度</td><td>—</td></tr>
<tr><td>6</td><td><code>run_experiments.py</code></td>
    <td>完整实验协议：语料描述、五个基线、所提模型、四项消融、稀疏权重扫描、
        收敛效度、两指标秩相关</td>
    <td><code>results.json</code></td></tr>
<tr><td>7</td><td><code>concept_collapse.py</code></td>
    <td>本体概念向量坍缩诊断（有/无残差连接）</td>
    <td><code>concept_collapse.json</code></td></tr>
<tr><td>8</td><td><code>figures.py</code></td>
    <td>四张图</td><td><code>*.png</code></td></tr>
<tr><td>9</td><td><code>build_docx.py</code></td>
    <td>按期刊模板生成 Word 论文，正文数字全部从 JSON 插值</td>
    <td>论文 <code>.docx</code></td></tr>
<tr><td>10</td><td><code>export_data.py</code></td>
    <td>导出本次交付的两个 Excel 工作簿与 CSV</td>
    <td><code>*.xlsx</code></td></tr>
<tr><td>11</td><td><code>make_protocol.py</code></td>
    <td>生成本说明文档，其中的数字同样从 JSON 插值</td>
    <td>本文件</td></tr>
</table>

<h3>复现命令</h3>
<pre>cd model
python3 gradcheck.py            # 约 1 分钟
python3 run_experiments.py      # 约 15 分钟，写出 tables/results.json
python3 concept_collapse.py     # 约 3 分钟
cd ../analysis
python3 figures.py              # 四张图
python3 export_data.py          # 两个 Excel 工作簿
python3 make_protocol.py        # 本说明文档
cd ../build
python3 build_docx.py           # 论文 Word 文件</pre>
<p>单核 CPU 即可，无需 GPU。同一种子下结果完全可复现。</p>

<h2>四、几个关键方法的说明</h2>

<h3>1. 证据链是分数的精确分解，不是注意力图</h3>
<p>模型对每一族的打分，其 logit 中的每一项都是对情节的求和，因此可以精确
拆成逐情节的贡献 <i>C</i><sub>k,t</sub>，并且满足恒等式</p>
<pre>&#931;_t C(k,t) + b(k) = &#963;&#8315;&#185;( &#375;(k) )</pre>
<p>代码中对此有断言检查，误差在机器精度量级（约 1e-15）。班主任拿到的就是
这个分解——具体是哪几个课间、当时发生了什么、那一刻把分数抬高或压低了多少——
而不是一张注意力热力图。论文的一个主要发现正是：同一个训练好的模型，只看它的
注意力分布会给出与实际算术相差很大的解释。</p>

<h3>2. 吻合度指标有下界也有上界</h3>
<table>
<colgroup><col style="width:26%%"><col style="width:12%%"><col style="width:62%%"></colgroup>
<tr><th>参照</th><th>值</th><th>含义</th></tr>
<tr><td>随机解释（下界）</td><td>%(chance).3f</td><td>五族部署的边际率平均</td></tr>
<tr><td>监督探针（上界）</td><td>%(oracle).3f</td>
    <td>用同样的 %(fdim)d 个特征直接监督预测策略族，情节级正确率
        %(oacc).1f%%——说明信息就在特征里，差距来自监督层级而非特征本身</td></tr>
<tr><td>本文模型</td><td>%(align).3f</td>
    <td>对比模型中最高，约为随机的 %(ratio).2f 倍</td></tr>
</table>
<p>脱离这两个界去读这一列没有意义。上界的存在也让论文能诚实地指出：在只有
个体层标签的条件下，仍有相当大的差距没有跨过。</p>

<h3>3. 超参数一律在验证集上选</h3>
<p>包括学习率与稀疏权重 &#955;。测试集指标与任何解释质量指标都不参与选择。
稀疏权重的扫描结果全量报告（见 Excel「稀疏权重扫描」表），而不是只报
对某个指标最有利的那一档。</p>

<h3>4. 结果按实测报告，包括不利的部分</h3>
<ul>
<li>本体解析器在本语料上<b>没有跑赢它的消融</b>（去掉它之后精度、验证集
    交叉熵、证据链吻合度三项都没有变差，吻合度甚至略高），正文直接写明，
    并说明这一结论的适用范围。时序图跑赢了它的消融，但差距约等于一个种子
    标准差，正文也只写到「不会更差，大概率略有帮助」为止。</li>
<li>与最强基线（%(best)s）%(gap).3f 的精度差约等于一个随机种子标准差，
    正文标注为「三次初始化无法分辨」。</li>
<li>稀疏化在前四档对吻合度没有影响、之后开始下滑，但只有三个种子，因此论文
    只主张「稀疏化在任何一档都买不到正确性」这个能站得住的说法，<b>没有</b>
    把「稀疏化降低正确性」当作一项结论来提。</li>
<li>ERC 教师报告与整体调节得分的相关%(valtxt)s，如实报告，未只挑显著的
    两项汇报。这一条本身有实质含义：教师能看见的和学生藏起来的不是同一个
    量，两者不能互相替代。</li>
</ul>

<h2>五、结果文件</h2>
<p>文件：<code>EMA_analysis_results.xlsx</code>。论文正文中的每一个数字都
来自 <code>tables/results.json</code>，由 f-string 插值进正文，没有一个是
手工填写的，因此正文与该工作簿不可能对不上。本说明文档同理。</p>
<table>
<colgroup><col style="width:40%%"><col style="width:60%%"></colgroup>
<tr><th>工作表</th><th>对应论文位置</th></tr>
<tr><td>配置与语料 Config</td><td>第五节 A、C、D 小节；梯度检验；概念坍缩诊断</td></tr>
<tr><td>表1 预测性能 / 表1附 逐族AUC</td><td>Table 1</td></tr>
<tr><td>表2 解释质量</td><td>Table 2</td></tr>
<tr><td>表3 消融</td><td>Table 3</td></tr>
<tr><td>表4 收敛效度</td><td>Table 4</td></tr>
<tr><td>稀疏权重扫描 Sweep</td><td>Figure 4 与第六节 E 小节</td></tr>
<tr><td>核心发现 两指标相关</td><td>第六节 B 小节与第七节 C 小节</td></tr>
</table>

<h2>六、如果要投稿时提交数据可用性声明</h2>
<p>建议的表述：本研究使用的语料由一个显式的、带随机种子的心理过程模型生成，
生成代码、实验代码、结果文件与导出数据均已随文提供；给定种子后全部结果可
完全复现，无需 GPU 或深度学习框架。语料为模拟数据，<b>不涉及任何真实儿童
被试</b>，因此不需要伦理审查批准，也不存在家长知情同意程序；论文第七节 A
小节列出了在真实校园中部署时必须满足的条件（家长知情同意与儿童本人同意、
数据最小化、不做情绪实时推送、输出只交给了解该学生的班主任或心理教师、
不用于横向排名），第七节 C 小节讨论了向观测语料迁移时需要补充的验证工作。</p>
"""


def main():
    with open(os.path.join(ROOT, "tables", "gradcheck.json"),
              encoding="utf-8") as fh:
        grad = json.load(fh)
    p = VAL["p"]
    if p >= 0.05:
        valtxt = ("未达显著（r = %.3f, p = %.3f）"
                  % (VAL["r"], p)).replace("0.", "0.")
    else:
        valtxt = "达到显著（r = %.3f, p = %.3f）" % (VAL["r"], p)
    out = DOC % dict(
        style=STYLE,
        n=CFG["n_participants"], ndays=CFG["n_days"],
        nprompt=CFG["n_prompt"], tmax=CFG["t_max"],
        fdim=CFG["f_dim"], nep="%d" % N_EP,
        comp="%.0f%%" % (100 * D.COMPLIANCE),
        inertia=COR["inertia_mean"], inertiasd=COR["inertia_sd"],
        erc=COR["erc"][0], ercsd=COR["erc"][1],
        seed=D.SEED, ngrad=grad["n_checks"],
        chance=COR["chance_alignment"], oracle=COR["oracle_alignment"],
        oacc=100 * COR["oracle_accuracy"], align=OURS["alignment"],
        ratio=OURS["alignment"] / COR["chance_alignment"],
        best=BEST, gap=MOD[BEST]["auc_roc"] - OURS["auc_roc"],
        valtxt=valtxt)
    dest = os.path.join(ROOT, "export", "protocol.html")
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(out)
    print("wrote %s (%d bytes)" % (dest, len(out.encode("utf-8"))))


if __name__ == "__main__":
    main()
