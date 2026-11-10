# 模型文件目录

保存用例图、状态图、类图的图片和可编辑源文件。

| 文件 | 说明 |
| --- | --- |
| `usecase.png` | 用例图导出图（供 `docs/usecase.md` 引用） |
| `usecase.svg` | 用例图可编辑矢量源文件 |
| `state.png` | 工单状态图导出图（供 `docs/models.md` 引用） |
| `state.svg` | 状态图可编辑矢量源文件 |
| `class.png` | 设备与工单类图导出图（供 `docs/models.md` 引用） |
| `class.svg` | 类图可编辑矢量源文件 |

命名保持小写英文，`docs/*.md` 中一律使用相对路径引用（如 `assets/usecase.png`），
不得写成 `C:\...` 形式的本机磁盘路径。修改图时请同步更新 PNG 与 SVG，并在 PR 说明中
注明改动内容。
