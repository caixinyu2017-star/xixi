# a03 代码取向对照例 + 调试/审查方法摘要

> 从 SKILL.md 正文下沉的细节。正文保留决策要点与本文件指针，深用时读这里。

## 代码取向对照（最小够用 vs 过度工程；源头校验 vs 症状补丁）

```python
# Bad：过度工程——测试只要求重试 3 次，却预先堆了一堆没人用的旋钮(YAGNI)
def retry(fn, max_retries=3, backoff="exponential", on_retry=None, jitter=True): ...

# Good：刚好让当前测试通过，需求长出来再加参数
def retry(fn, attempts=3):
    for i in range(attempts):
        try:
            return fn()
        except Exception:
            if i == attempts - 1:
                raise
```

```python
# Bad：症状处补丁——坏值已传到下游，每个用到的地方各打一个补丁
def report(scores):
    scores = [0 if s != s else s for s in scores]  # 这里擦 NaN
    ...
# 别处又得再擦一次，根因(产生 NaN 的源头)没动，补丁会越长越多

# Good：在数据进入系统的源头校验/修复一次，下游干净(systematic-debugging Phase 1.5)
def load_scores(raw):
    scores = parse(raw)
    if any(s != s for s in scores):       # 源头发现即拒绝
        raise ValueError("输入含 NaN，拒绝在源头")
    return scores
```

## 调试与审查四法（正文摘要的展开）

- **系统化调试(systematic-debugging)**：动手前先定位根因——①逐字读错误/栈/行号 ②稳定复现 ③查最近改动(git diff/新依赖/环境) ④多组件系统在各边界加埋点定位是哪层断 ⑤反向追踪数据流到源头，在源头修而非症状处修。提单一假设、一次只改一个变量验证；先写失败测试再修。连修 3 次仍失败→停手质疑架构，这是结构问题不是 bug。四阶段+边界埋点详见 `references/debug_protocol.md`。
- **自我代码审查(requesting/receiving-code-review 视角)**：审查维度按严重度分级——Critical(立即修)/Important(下个任务前修)/Minor(记录待后)；评估每条建议的五查：对本库技术正确吗、会破坏现有功能吗、当前实现为何这么写、跨平台/版本可行吗、有完整上下文吗；加 YAGNI 检查(grep 实际用法，无人用就别加)。回应技术化、动作导向，不做表演性赞同。
- **改进架构(improve-codebase-architecture)**：用"删除测试"诊断——设想删掉某模块，复杂度消失=穿透层(浅，可吸收)，复杂度在多个调用方重现=深模块(值得留)。把浅模块改造成"小接口藏大实现"的深模块，集中知识、保证局部性；"接口即测试面"。
- **拆子任务(subagent-driven-development 思路)**：每任务给全新隔离上下文(只传必要信息不传会话史)，做完先过规格符合性审查再过代码质量审查(顺序不可乱)，发现问题回修复审循环；不并行派多个实现。
- **收尾分支(finishing-a-development-branch)**：合并前必须全测试通过；顺序为合并→在结果上重跑测试→移除 worktree→删分支(反了 `git branch -d` 会失败)；丢弃工作需显式确认，无请求不 force-push。
