# 状态规则初始运行与最终运行证据

本目录保存组员 C 在实验二中“起始 2/4 → 补齐规则 4/4”的原始输出和未实现起始版源码，供教师核对。

## 文件

| 文件 | 内容 |
| --- | --- |
| `initial_run/status_rule.py` | 未实现起始版：保留状态常量，`can_transition` 对所有输入返回 `False` |
| `initial_run/test_status_rule.py` | 规定的 4 项测试，预期值未修改 |
| `initial_output.txt` | 在未实现版上执行 `python test_status_rule.py` 的原始输出：2/4 passed，退出码 1 |
| `final_output.txt` | 补齐两条允许转换后的原始输出：4/4 passed，退出码 0 |

## 运行方式

在 `src/python` 目录下执行：

```text
python test_status_rule.py
```

初始版可直接在 `docs/evidence/initial_run` 目录复现：

```text
cd docs/evidence/initial_run
python test_status_rule.py
```

初始版对应 T01、T02 FAIL，T03、T04 PASS，`Summary: 2/4 passed`；最终版四项全部 PASS，`Summary: 4/4 passed`。

## 关于仓库起点

仓库初始提交 `7a2a8a6` 的 `src/python/status_rule.py` 已是完成版（已含两条允许转换），与本人实验时使用的起始包不是同一份文件。为避免“仓库起点”和“本地起始包”混淆，本目录保留未实现版源码及两次运行的原始输出。

最终代码以 `src/python/status_rule.py` 为准；`test_status_rule.py` 只把比较运算符 `actual is expected` 改为 `actual == expected`，四项预期值未做任何修改。

## 相关记录

- 测试记录：`docs/test-results.md`
- 代码 PR：#5（合并 commit `794b840c496e2fc0cd3f5fca175e8a831bd47458`）
- C 的提交：`0f534e48bf4990365266b713c02094aa76b26d31`
- main 复测：`main_retest/main_retest_output.txt`
