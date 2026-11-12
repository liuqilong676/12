# 实际测试记录

语言与版本：Python 3.12.14（Windows 11，64 位）

测试人员 GitHub 用户名：434990788（组员 C）

运行命令（在 `src/python` 目录下执行）：

```
python test_status_rule.py
```

| 编号 | 当前状态 | 目标状态 | 预期 | 实际 | 结论 |
| --- | --- | --- | --- | --- | --- |
| T01 | PENDING | PROCESSING | true | True | PASS |
| T02 | PROCESSING | COMPLETED | true | True | PASS |
| T03 | PENDING | COMPLETED | false | False | PASS |
| T04 | COMPLETED | PROCESSING | false | False | PASS |

汇总：`Summary: 4/4 passed`，退出码 0。

## 原始输出

```text
T01 PASS: PENDING -> PROCESSING, expected=True, actual=True
T02 PASS: PROCESSING -> COMPLETED, expected=True, actual=True
T03 PASS: PENDING -> COMPLETED, expected=False, actual=False
T04 PASS: COMPLETED -> PROCESSING, expected=False, actual=False
Summary: 4/4 passed
```

退出码：`0`（Windows `echo %ERRORLEVEL%` 输出 0）。

起始包（函数未实现）时，同一命令的实测输出为：

```text
T01 FAIL: PENDING -> PROCESSING, expected=True, actual=False
T02 FAIL: PROCESSING -> COMPLETED, expected=True, actual=False
T03 PASS: PENDING -> COMPLETED, expected=False, actual=False
T04 PASS: COMPLETED -> PROCESSING, expected=False, actual=False
Summary: 2/4 passed
```

即 2 项 PASS、2 项 FAIL、退出码 1，与指导书描述一致。

## 补充测试（本组自加，不属于规定 4 项）

为验证“状态不变、未知状态、None、大小写不符”等分支以及业务层不产生脏数据，
另外编写 `test_repair_service.py`，执行：

```
python -m unittest test_repair_service -v
```

真实输出（末段）：

```text
Ran 17 tests in 0.004s

OK
```

17 项全部通过。被改动的仅是本组自己新增的测试文件，`test_status_rule.py` 的 4 项预期值
未做任何修改。

## 测试范围

本次规定 4 项测试，其他状态组合是否额外执行：**已额外执行**，见上方补充测试
（状态规则边界 3 项，合计覆盖 9 种组合，含 3 种状态不变、未知值、None、大小写不符）。

从个人分支下载 ZIP 复测情况：已从 `feat/status-c` 的 Code → Download ZIP 下载到新目录，
执行 `python test_status_rule.py`，结果与上表一致（`Summary: 4/4 passed`，退出码 0）。

从 `main` 下载 ZIP 最终复测情况：已从 main 归档 ZIP（commit `3fea21feba5cf0fa083daa09a7b44e1ee6b9ff59`）解压到新目录，进入 `src/python` 执行 `python test_status_rule.py`，T01–T04 全部 PASS，`Summary: 4/4 passed`，退出码 0。

## 证据位置

- `main_retest/main_retest_output.txt`：main 归档 ZIP 复测的 commit、解压目录、命令、退出码与四项原始输出。
- `docs/evidence/initial_output.txt`、`docs/evidence/final_output.txt`：初始 2/4 与最终 4/4 原始输出。
- `docs/evidence/initial_run/status_rule.py`：未实现起始版源码（`can_transition` 返回 `False`）。
