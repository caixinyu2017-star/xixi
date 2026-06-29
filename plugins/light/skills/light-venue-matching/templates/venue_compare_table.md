<!-- venue 对比表模板（核心交付物起手骨架）
约定字段见 ../../../CONVENTIONS.md §3；铁律见 SKILL.md。
铁律：① 凡指标值必带(来源,年份)；② 无官方接收率一律填「待核查—无官方公开数据」，禁编百分比；
      ③ 三套分区(JCR/中科院/CCF 等)各标来源+年份，不可混用；④ 数据以 db01 为准、投前重核。 -->

# 候选 venue 对比

## 一、对比矩阵（横向速览，只放关键决策列）

| venue_name | venue_type | 档位(CCF·中科院·北大核心) | impact_factor(来源,年) | jcr_quartile | review_cycle | apc_fee | indexing | 推荐档位 | 录用可能性 | last_checked |
|---|---|---|---|---|---|---|---|---|---|---|
| _示例期刊A_ | 期刊 | CCF-B·中科院2区 | 5.2 (JCR,2024) | Q1 | 约12周 | $2000 | SCIE | 稳妥 | 中 | 2026-06-06 |
|  |  |  |  |  |  |  |  |  |  |  |

<!-- 推荐档位：冲刺/稳妥/保底  ｜  录用可能性：高/中/低（定性，禁百分比） -->

## 二、逐 venue 详情卡（承载完整字段与分级理由）

### <venue_name>
- **基本**：venue_type / publisher / subject_area / level
- **收录与档位**：indexing(WoS: SCIE/SSCI/ESCI；Scopus: Y/N) ｜ ccf_level ｜ cas_quartile(大类/小类,年) ｜ jcr_quartile(年) ｜ 北大核心/CSSCI/CSCD
- **指标**（必标来源+年份，不可混用）：impact_factor(JCR,YYYY) ｜ CiteScore(Scopus,YYYY) ｜ SJR(Scimago,YYYY)
- **周期/费用/OA**：review_cycle ｜ apc_fee ｜ is_OA / DOAJ(有无 Seal)
- **投稿信息**：reference_style ｜ template_url ｜ submission_url
- **代表作**（db01）：……
- **录用可能性（定性分级，全程无百分比）**：<高/中/低>
  - 作者实力 = __（来源）
  - 方向匹配 = __
  - 方法规模 = __
  - 官方接收率 = 待核查—无官方公开数据
  - 创新性 = 作者自评 __（主观）
- **风险预警**：risk_note（预警名单命中 / 异常自引 / 超快审稿 等）
- **last_checked_date**：YYYY-MM-DD
