# 基于 CycleGAN 的地震道插值

> 把「缺失检波道的炮集」补回来。  
> 本仓库是技术复盘文档，**不含真实炮集数据**（商业资产）。文中的对比图均为**合成示意图**，用来帮助理解思路；你手头的 Word 实验截图可以按 [assets/images/README.md](assets/images/README.md) 说明替换进去。

**建议先看图：** [docs/00-visual-guide.md](docs/00-visual-guide.md) ← 5 分钟看完整个项目

---

## 一句话

炮集就是一张「道 × 时间」的图。删掉 30% 竖向道 → 用 CycleGAN 学会从「缺道图」变「完整图」→ 切块预测、重叠拼接 → 用波形和频谱看效果。

---

## 先看这三张图

### 1. 炮集是什么？

![炮集示意图](assets/images/01-shot-gather.png)

横轴每一列是一道检波器，纵轴是时间，颜色是振幅。**缺道 = 图上有白色竖条。**

---

### 2. 我们要干什么？

![缺失道对比](assets/images/02-missing-traces.png)

左边完整，右边删掉 30% 的道。**任务：把右边的白条补成左边那样。**

---

### 3. 为什么用 CycleGAN？

![CycleGAN 思路](assets/images/03-cyclegan-idea.png)

不需要「缺道图 ↔ 完整图」严格成对，只要两个域各有一批图，让模型学分布就行。详见 [docs/03-methodology.md](docs/03-methodology.md)。

---

## 效果对比（示意图）

![方法对比](assets/images/04-method-compare.png)

| 方法 | 直观感受 |
|------|----------|
| 双三次 | 能填上，但同相轴发糊 |
| CycleGAN | 纹理更锐，高频保留更好 |
| 关键坑 | 振幅没对齐 → 颜色偏浅；没 overlap → 拼接有缝 |

---

## 实验怎么一步步改过来的

![实验时间线](assets/images/09-experiment-timeline.png)

| 版本 | 改了什么 | 结果 |
|------|----------|------|
| v1 | 没做 overlap | 边缘道浅、拼接有缝 |
| v2 | 振幅没对齐 | 整张图颜色偏浅 |
| v3 | 对齐振幅 | 颜色对了，纹理还糊 |
| v4 | 加上 overlap | 缝隙没了，效果最好 |

![overlap 对比](assets/images/05-overlap-stitch.png)

![振幅对齐](assets/images/06-amplitude-align.png)

---

## 实际工程流程

![工程流程](assets/images/07-workflow.png)

论文里往往只写到「训练 CycleGAN」。落地时还多出：**切块 → 逐张预测（不能 shuffle）→ overlap 拼接 → 转 SEG-Y 做频谱**。

---

## 怎么评估好不好？

![频谱对比](assets/images/08-spectrum.png)

不能只看「像不像照片」。地震更关心：**同相轴断没断、高频还在不在。**

---

## 文档索引

| 想看什么 | 点这里 |
|----------|--------|
| **看图速览（推荐入口）** | [00-visual-guide.md](docs/00-visual-guide.md) |
| 问题从哪来 | [01-background.md](docs/01-background.md) |
| 为什么选 CycleGAN | [02-literature-review.md](docs/02-literature-review.md) |
| 原理怎么映射到地震 | [03-methodology.md](docs/03-methodology.md) |
| 数据怎么处理 | [04-data-pipeline.md](docs/04-data-pipeline.md) |
| 实验记录 | [05-experiments.md](docs/05-experiments.md) |
| 波形 / 频谱评估 | [06-evaluation.md](docs/06-evaluation.md) |
| 踩坑清单 | [07-troubleshooting.md](docs/07-troubleshooting.md) |

---

## 技术栈

TensorFlow 2 · `tf.data` / `tensorflow_datasets` · U-Net 生成器 · PatchGAN · GOM 2D + 山地自研数据

---

## 个人做了什么

- 传统插值调研 → GAN 论文选型 → CycleGAN 地震方案落地  
- TF2 数据管道 + overlap 切块推理拼接  
- 对照实验：overlap / epoch / U-Net vs ResNet / 振幅对齐  
- 解决：Mac MPS + Adam 崩溃、预测空图、测试集尺寸不一致、shuffle 乱序拼接  

---

## 说明

- 示意图由 `scripts/generate_diagrams.py` 生成，标注了「合成数据」  
- 你 Word 文档里的真实实验截图可以替换进 `assets/images/`（见该目录 README）  
- 通用 CycleGAN 学习：[pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)

---

## License

文档 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
