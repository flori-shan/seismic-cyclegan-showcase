# 图片说明

## 当前状态

| 文件 | 内容 | 类型 |
|------|------|------|
| `01-shot-gather.png` | 炮集是什么 | 合成示意 |
| `02-missing-traces.png` | 完整 vs 缺 30% 道 | 合成示意 |
| `03-cyclegan-idea.png` | CycleGAN 域映射 | 流程示意 |
| `04-method-compare.png` | 双三次 vs CycleGAN | 合成示意 |
| `05-overlap-stitch.png` | 有无 overlap 拼接 | 合成示意 |
| `06-amplitude-align.png` | 振幅对齐前后 | 合成示意 |
| `07-workflow.png` | 工程流程 | 流程示意 |
| `08-spectrum.png` | 波形 + 频谱 | 合成示意 |
| `09-experiment-timeline.png` | 实验迭代 | 流程示意 |

重新生成：`python3 scripts/generate_diagrams.py`

---

## 为什么没有真实项目截图？

原始 Word 文档（`.docx`）里的实验对比图、频谱图、相减图**没有随文本一起导出**，仓库里起初只有文字笔记。

---

## 如何换成你的真实截图

1. 从 Word 文档里导出实验图（右键图片 → 另存为 PNG）
2. 建议命名替换：

| 你的图 | 建议替换为 |
|--------|------------|
| 缺道 vs 完整炮集对比 | `02-missing-traces.png` |
| 无 overlap / 有 overlap 拼接 | `05-overlap-stitch.png` |
| 振幅修正前后 | `06-amplitude-align.png` |
| 双三次 vs CycleGAN 大图 | `04-method-compare.png` |
| 1D / 2D 频谱 | `08-spectrum.png` |
| 相减残差图 | 可新增 `10-residual.png` |

3. 替换后 commit 推送到 GitHub 即可

> 推送前确认图片**不含公司内部敏感信息**（井位、客户名、未公开数据等）。
