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

从个人分支下载 ZIP 复测情况：本地按 `feat/status-c` 的同一目录结构打包并解压到新目录，
执行 `python test_status_rule.py`，结果为 `Summary: 4/4 passed`，退出码 0；
GitHub 网页的 `Code → Download ZIP` 复测由组员 C 在推送后确认。

从 `main` 下载 ZIP 最终复测情况：待合并后填写，或在 `docs/submission.md` 记录。
