# 校园物联网设备报修实验

组号：group01（仓库名 `iot-repair-group01`，请按实际组号替换）

成员A GitHub用户名：liuqilong676

成员B GitHub用户名：milkdragon12138

成员C GitHub用户名：434990788

本组选定语言：**Python**

## 范围

只分析查看设备、提交报修、更新状态，只编程实现状态判断函数。不接入真实硬件，
不实现数据库、网页、登录或 MQTT。设备数据取自 `data/devices.csv` 模拟清单。

## 固定规则

新工单为 PENDING。仅允许 PENDING 转 PROCESSING、PROCESSING 转 COMPLETED。
其他转换一律拒绝，包括状态跳级、回退、状态不变以及未知状态值。

## 分工

| 成员 | 任务分支 | 成果 |
| --- | --- | --- |
| A（组长） | `docs/requirements-a` | `docs/requirements.md`、`docs/usecase.md`、`docs/assets/usecase.png` 与 `usecase.svg`、仓库初始化与提交索引 |
| B | `docs/models-b` | `docs/models.md`、状态图与类图（`state.*`、`class.*`）、与需求的一致性检查 |
| C | `feat/status-c` | `src/python/status_rule.py`、`docs/test-results.md`、真实测试输出 |

三个主要 PR 合并后再由 A 开 `docs/submission-a` 分支整理 `docs/submission.md`。
图文件放 `docs/assets`，同时保留可编辑源文件（`.svg` 与 Mermaid 代码块）。

## 目录结构

```
README.md
data/devices.csv                 设备模拟清单（DEV-001～DEV-003）
docs/requirements.md             FR-01～FR-03 需求与验收条件（A）
docs/usecase.md                  用例图、角色说明与自查（A）
docs/models.md                   状态图、类图与一致性检查（B）
docs/test-results.md             真实测试记录（C）
docs/submission.md               最终提交索引（A，收尾 PR）
docs/assets/                     usecase/state/class 的 PNG 与 SVG 源文件
src/python/status_rule.py        规定的状态判断函数（实验二核心，C）
src/python/test_status_rule.py   规定的 4 项测试（不得修改预期值）
src/python/device.py             设备实体与 CSV 清单读取（扩展）
src/python/work_order.py         工单实体与状态迁移入口（扩展）
src/python/repair_service.py     FR-01～FR-03 业务校验（扩展）
src/python/cli.py                命令行演示程序（扩展）
src/python/test_repair_service.py 17 项补充测试（扩展）
src/java/                        Java 起始文件（本组未选用）
```

## 运行

Python（在 `src/python` 目录下）：

```
python test_status_rule.py          # 规定的 4 项测试
python -m unittest test_repair_service -v   # 17 项补充测试
python cli.py                       # 命令行演示：查看设备、提交报修、更新状态
```

也可以直接双击仓库根目录的 `run_tests.bat`：它自动查找可用的 Python（`py` 启动器 → PATH 中的
`python` → 随包提供的 `D:\rjgc1110\_tools\python-embed` 便携版），跑完 4 项规定测试与
17 项补充测试后停在窗口上，便于复制输出。

起始函数未实现时应为 2 项 PASS、2 项 FAIL、退出码 1；补齐规则后规定 4 项全部 PASS、
退出码 0。不要修改测试预期来获得通过，也不提交 `.class`、`__pycache__` 或整个 IDE 工程。

Java（本组未使用）：`javac StatusRule.java StatusRuleTest.java` 后 `java StatusRuleTest`。

## 协作

每人一个个人分支和主要 PR，交叉评审后合入 `main`；初始化之外不直接写 `main`。
评审顺序 A 审 B、B 审 C、C 审 A；四人组增加 D（`docs/acceptance-d`），按 A→B→C→D 合并。
操作详见配套《物联网设备报修实验_GitHub学生操作教程》。
