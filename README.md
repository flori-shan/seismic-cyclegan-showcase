# 基于 CycleGAN 的地震道插值研究

> **面试展示仓库** — 梳理本人在工业场景下探索「深度学习地震道插值」的完整技术路线。  
> 本仓库**不包含**原始地震数据与训练代码（数据属项目/商业资产），重点呈现：**问题定义 → 文献调研 → 方案设计 → 实验对比 → 问题排查 → 改进方向**。

---

## 一句话介绍

将炮集图中**缺失检波道**的重建问题，建模为**不完整炮集 ↔ 完整炮集**之间的图像域翻译；在 TensorFlow 2 上实现 CycleGAN 训练流程，系统对比 overlap 切分、生成器结构（U-Net / ResNet）、训练轮数等因素，并用**波形显示 + 频谱分析**评估插值质量。

---

## 项目背景

| 维度 | 说明 |
|------|------|
| **业务问题** | 地震采集存在道缺失（近偏移距丢失、不规则采样），需在炮集（shot gather）上补全缺失道 |
| **传统基线** | 双线性 / 双三次卷积插值 — 边缘模糊、高频细节损失 |
| **深度学习路线** | GAN 系列 → 超分思路（SRGAN）→ **地震道专用 CycleGAN 论文** → 工程落地 |
| **技术栈** | TensorFlow 2、`tf.data` / `tensorflow_datasets`、U-Net 生成器、PatchGAN 判别器 |

---

## 整体技术路线

```mermaid
flowchart LR
    A[业务需求：炮集道缺失] --> B[传统插值基线调研]
    B --> C[GAN / pix2pix / CycleGAN 调研]
    C --> D[论文：Seismic interpolation with GANs]
    D --> E[数据构造：删减30%检波道]
    E --> F[CycleGAN 训练与推理]
    F --> G[重叠切块拼接 + 频谱评估]
    G --> H[问题排查与迭代优化]
```

---

## 核心思路（面试 2 分钟版）

1. **域定义**  
   - 域 A：删减 30% 检波道后的炮集图（模拟缺失）  
   - 域 B：完整炮集图  
   - 无需严格像素对齐的成对标签，适合 **unpaired CycleGAN**

2. **数据工程**  
   - GOM 2D 数据集：Madagascar `sfpatch` 重叠切块  
   - 自研山地数据集：200×200 / 1024×1024 patch，`overlap` 缓解边缘效应  
   - 删除前 5 道模拟近偏移缺失；振幅归一化对齐两域

3. **模型**  
   - 生成器：U-Net（pix2pix 风格）为主，对比 ResNet 残差生成器  
   - 判别器：70×70 PatchGAN  
   - 损失：对抗损失 + 循环一致性损失（λ=10）

4. **关键实验结论**（详见 [docs/05-experiments.md](docs/05-experiments.md)）  
   - **overlap 切块**显著减轻边缘道生成过浅、拼接缝隙问题  
   - 两域**振幅不一致**会导致颜色深度偏差，需预处理对齐  
   - 40 epoch 与 200 epoch、U-Net vs ResNet 均做对比记录

5. **评估**  
   - 视觉：波形变面积显示、大图对比、相减残差图  
   - 定量：一维 / 二维频谱分析（转 SEG-Y 后分析）  
   - 对标：工业软件处理结果、RNA 等传统方法（规划中）

---

## 文档目录

| 文档 | 内容 |
|------|------|
| [01-background.md](docs/01-background.md) | 问题定义、插值算法调研 |
| [02-literature-review.md](docs/02-literature-review.md) | GAN 演进、相关论文笔记 |
| [03-methodology.md](docs/03-methodology.md) | CycleGAN 原理与地震场景映射 |
| [04-data-pipeline.md](docs/04-data-pipeline.md) | 数据集、预处理、切块与加载 |
| [05-experiments.md](docs/05-experiments.md) | 实验设计与结果分析 |
| [06-evaluation.md](docs/06-evaluation.md) | 频谱与波形评估方法 |
| [07-troubleshooting.md](docs/07-troubleshooting.md) | 工程踩坑（Mac MPS、空图、尺寸不匹配等） |
| [08-interview-guide.md](docs/08-interview-guide.md) | 面试话术与高频追问 |

---

## 为什么本仓库没有数据和代码？

- 地震炮集数据属于**项目/商业数据**，无法公开  
- 本仓库定位为 **Technical Portfolio**：展示调研深度、工程化能力和问题拆解思路  
- 通用 CycleGAN 复现可参考：[pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)（本机学习用）

---

## 个人贡献摘要（可写入简历）

- 独立完成从**传统插值 → GAN 论文调研 → CycleGAN 地震插值**的技术选型与方案设计  
- 实现完整 **TF2 数据管道**（`tensorflow_datasets` / `tf.data`）及炮集**重叠切块—推理—拼接**流程  
- 设计多组对照实验（overlap、epoch、生成器结构、振幅对齐），形成可复现的实验记录  
- 排查并解决 **Mac MPS + Adam 崩溃、预测空图、测试集尺寸不匹配、图片乱序拼接** 等工程问题  
- 建立**波形 + 频域**双重评估框架，为后续与 RNA / 商业软件对标奠定基础

---

## 参考文献

见 [docs/references.md](docs/references.md)

---

## License

文档内容采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。  
代码与数据未包含在本仓库中。
