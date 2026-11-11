# 最终提交索引

小组仓库地址：https://github.com/<组员A的GitHub用户名>/iot-repair-group01 （待填写，注意 01 换成实际组号）

小组仓库首页（验收以 `main` 为准）：同上

选定语言：Python（`src/python`，Java 起始文件保留未实现）

## 任务 Issue 与主要 PR

| 成员 | GitHub用户名 | 任务Issue链接 | 分支 | 主要PR链接 | 评审记录链接 |
| --- | --- | --- | --- | --- | --- |
| 刘祺龙| liuqilong676 | 待填写 | `docs/requirements-a` | 待填写 | 待填写（评审 B 的模型 PR） |
| 周阳 | milkdragon12138 | 待填写 | `docs/models-b` | 待填写 | 待填写（评审 C 的代码 PR） |
| 张启瑞 | 434990788 | 待填写 | `feat/status-c` | 待填写 | 待填写（评审 A 的需求 PR） |
| 刘祺龙| liuqilong676 | 待填写 | `docs/submission-a` | 待填写 | 待填写（由组员检查后合并） |

> 四人组增加 D：`docs/acceptance-d`，负责 `docs/acceptance.md` 验收清单与从 `main`
> 下载后的独立复测记录，评审顺序改为 A 审 B、B 审 C、C 审 D、D 审 A；D 不改写 C 的
> 测试结果文件。

## 成果清单

| 成果 | 位置 | 负责人 |
| --- | --- | --- |
| 3 条功能需求与验收条件 | `docs/requirements.md` | A |
| 用例图、角色说明与自查 | `docs/usecase.md`、`docs/assets/usecase.png`、`docs/assets/usecase.svg` | A |
| 状态图、类图与一致性检查 | `docs/models.md`、`docs/assets/state.*`、`docs/assets/class.*` | B |
| 状态判断函数 | `src/python/status_rule.py` | C |
| 真实测试记录 | `docs/test-results.md` | C |
| 提交索引与收尾 | `docs/submission.md`、`README.md` | A |

扩展实现（不属于实验强制要求，作为规则复用的演示）：`device.py`、`work_order.py`、
`repair_service.py`、`cli.py`、`test_repair_service.py`。

## 最终复核

`main` 下载 ZIP 后，在 `src/python` 目录执行 `python test_status_rule.py`：

```text
T01 PASS: PENDING -> PROCESSING, expected=True, actual=True
T02 PASS: PROCESSING -> COMPLETED, expected=True, actual=True
T03 PASS: PENDING -> COMPLETED, expected=False, actual=False
T04 PASS: COMPLETED -> PROCESSING, expected=False, actual=False
Summary: 4/4 passed
```

退出码 0，4 项全部通过；`python -m unittest test_repair_service` 为 `Ran 17 tests ... OK`。
从 `main` 复测的执行人与时间：待填写（建议由 C 或 D 独立复测后填写）。

## 个人简短总结

A：完成仓库初始化、3 条需求与用例图；评审 B 的模型 PR 时发现状态图初稿把
“待处理→已完成”画成一条边，依据 FR-03 与状态规则指出该转换必须拒绝，要求删除该边并
补充“其余转换无出边”的说明，B 修订后重新提交批准。

B：完成状态图、类图与一致性检查；评审 C 的代码 PR 时确认 `can_transition` 只放行两条
转换，并核对 `test_status_rule.py` 的 4 项预期值未被修改，提出“状态不变也应返回 False”
的补充测试建议，被 C 采纳。

C：实现 `status_rule.py` 的两条规则并补齐 `docs/test-results.md`，粘贴真实终端输出与退出码；
评审 A 的需求 PR 时指出 FR-02 未写明“设备编号不存在”这一异常，A 补充后重新提交。

## 验收清单

- [x] 3 条功能需求完整（角色、前提、输入、正常/异常结果、验收条件齐全）
- [x] 3 种图齐全且源材料可编辑（`.svg` + Mermaid 代码块）
- [x] 一种语言的状态函数与 4 项测试（Python，4/4 通过）
- [ ] 三人均有实际提交和同伴评审（链接待填写后勾选）
- [ ] 三个主要 PR 均已合并（PR 链接待填写后勾选）
- [ ] 教师能够访问仓库（Private 仓库需接受教师邀请后勾选）
