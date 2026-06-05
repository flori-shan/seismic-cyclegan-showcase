# 图文总览

本文档配合 README 中的示意图，对项目背景、方法选择和主要实验结论作简要说明。图中数据为合成示意，非原始实验输出。

---

## 1. 炮集数据表示

![炮集是什么](../assets/images/01-shot-gather.png)

炮集可按二维图像理解：

| 维度 | 含义 |
|------|------|
| 横轴 | 检波道编号 |
| 纵轴 | 时间采样点 |
| 像素值 | 地震振幅 |

插值效果需结合同相轴连续性判断，不能仅依据视觉相似度。

---

## 2. 问题定义

![缺道](../assets/images/02-missing-traces.png)

地震采集过程中存在检波道缺失。实验中采用竖向删除 30% 检波道的方式模拟缺失情形：

- 左图：完整炮集（域 Y）
- 右图：缺道炮集（域 X），空白竖条为缺失位置

任务目标为根据已有道信息重建缺失检波道。

---

## 3. 方法概述

![CycleGAN](../assets/images/03-cyclegan-idea.png)

采用 CycleGAN 将缺道炮集与完整炮集建模为两个图像域：

| 组件 | 作用 |
|------|------|
| 域 X | 缺道炮集集合 |
| 域 Y | 完整炮集集合 |
| 生成器 G | X → Y，执行道插值 |
| 循环一致性损失 | 约束 F(G(x)) ≈ x，限制不合理映射 |

未采用 pix2pix 的原因：该方法要求同一炮点的缺道图与完整图严格成对，数据构造成本较高。

---

## 4. 与传统插值对比

![四种图对比](../assets/images/04-method-compare.png)

对比顺序：缺道输入、双三次插值、CycleGAN 输出、完整真值。

| 方法 | 现象 |
|------|------|
| 双三次插值 | 缺失道可填补，但同相轴平滑，高频细节损失 |
| CycleGAN | 同相轴纹理相对清晰，高频保留优于双三次 |

最终效果与数据集、训练轮数及预处理设置有关。

---

## 5. 工程问题

### 5.1 Overlap 切块与拼接

![overlap](../assets/images/05-overlap-stitch.png)

训练在 200×200 patch 上进行，全尺寸炮集需切块推理后拼接。

| 处理方式 | 现象 |
|----------|------|
| 无 overlap | patch 边界处振幅偏弱，拼接位置易出现缝隙 |
| 有 overlap | 重叠区域加权融合，同相轴连续性改善 |

该问题主要与推理流程相关，增加训练轮数无法替代 overlap 处理。

### 5.2 振幅归一化

![振幅](../assets/images/06-amplitude-align.png)

域 X 与域 Y 的振幅统计量不一致时，预测结果会出现整体偏深或偏浅。

处理方式：训练前对两域执行统一归一化，推理后做反变换用于显示和分析。

---

## 6. 处理流程

![流程](../assets/images/07-workflow.png)

```
数据准备 → 缺失道构造 → patch 切块与训练 → 逐 patch 推理 → overlap 拼接 → 波形与频谱评估
```

推理阶段需关闭 `shuffle`，按文件名排序输出，否则拼接顺序会错乱。

---

## 7. 评估方法

![频谱](../assets/images/08-spectrum.png)

| 评估项 | 说明 |
|--------|------|
| 波形变面积显示 | 检查同相轴是否连续 |
| 相减图 | 观察预测与真值的误差分布 |
| 一维 / 二维频谱 | 比较高频能量是否保留 |

MSE 不宜作为唯一指标。SRGAN 相关研究指出，基于 MSE 的优化倾向于产生过度平滑的结果。

---

## 8. 实验迭代记录

![时间线](../assets/images/09-experiment-timeline.png)

| 轮次 | 调整项 | 结果 |
|------|--------|------|
| 第一轮 | 未使用 overlap | 拼接缝隙明显 |
| 第二轮 | 振幅未对齐 | 预测图整体偏浅 |
| 第三轮 | 完成振幅对齐 | 颜色接近真值，细节仍不足 |
| 第四轮 | 增加 overlap | 缝隙减轻，为目前较好配置 |

详细参数与截图说明见 [05-experiments.md](05-experiments.md)。

---

## 9. 文档索引

| 文档 | 内容 |
|------|------|
| [01-background.md](01-background.md) | 问题背景与传统插值 |
| [02-literature-review.md](02-literature-review.md) | 文献调研 |
| [03-methodology.md](03-methodology.md) | CycleGAN 原理与场景映射 |
| [04-data-pipeline.md](04-data-pipeline.md) | 数据预处理与加载 |
| [05-experiments.md](05-experiments.md) | 实验记录 |
| [07-troubleshooting.md](07-troubleshooting.md) | 问题与处理 |

---

## 10. 图示说明

当前图示由 `scripts/generate_diagrams.py` 生成。如有原始实验截图，可按 [../assets/images/README.md](../assets/images/README.md) 中的命名规则替换。
