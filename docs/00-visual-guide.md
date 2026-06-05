# 看图速览 · 5 分钟版

> 如果你被一堆文字和公式绕晕了，只看这一页 + 图就行。

---

## Step 1 · 认识炮集

![炮集是什么](../assets/images/01-shot-gather.png)

把地震数据想成一张图：

- **横轴** = 检波道（一列一道）
- **纵轴** = 时间
- **颜色** = 振幅强弱

同相轴就是那些弯弯的条纹，地质解释全靠它连不连得上。

---

## Step 2 · 问题在哪

![缺道](../assets/images/02-missing-traces.png)

采集时经常会**丢道**（设备限制、近偏移距缺失等）。

我们做实验：人为竖向删掉 30% 的道，模拟真实情况。  
白色竖条 = 需要 AI 补出来的部分。

---

## Step 3 · 方案一句话

![CycleGAN](../assets/images/03-cyclegan-idea.png)

| 域 | 是什么 |
|----|--------|
| 域 X | 缺道的炮集图（一堆） |
| 域 Y | 完整的炮集图（一堆） |
| 生成器 G | X → Y，就是**插值补道** |
| 循环约束 | 补完再删道，应该回到原来的 X，防止胡编 |

**为什么不用 pix2pix？** 它要求「同一张炮集的缺道版 ↔ 完整版」严格配对，构造成本太高。

---

## Step 4 · 效果长什么样

![四种图对比](../assets/images/04-method-compare.png)

从左到右：缺道 → 双三次 → CycleGAN → 真值。

肉眼感受：

- 双三次：填上了，但抹平了
- CycleGAN：条纹更清楚

---

## Step 5 · 两个最关键的坑

### 坑 1：拼接有缝（overlap）

![overlap](../assets/images/05-overlap-stitch.png)

训练在 200×200 小图上做，大图要拼回来。

- **没 overlap**：中间一道亮缝，同相轴断开
- **有 overlap**：重叠区渐变融合，连续性好很多

> 这是部署问题，不是「多训几个 epoch」能解决的。

### 坑 2：颜色偏浅（振幅对齐）

![振幅](../assets/images/06-amplitude-align.png)

缺道图和完整图的灰度范围不一样，模型会学到「偏浅」的风格。

**修法**：训练前两域做同样的归一化。

---

## Step 6 · 完整流程

![流程](../assets/images/07-workflow.png)

比论文多出来的步骤：**切块 → 按文件名顺序预测 → overlap 拼回 → 转 SEG-Y 看频谱**。

---

## Step 7 · 怎么判断好不好

![频谱](../assets/images/08-spectrum.png)

| 看什么 | 为什么 |
|--------|--------|
| 波形变面积图 | 同相轴连不连 |
| 相减图 | 误差集中在哪 |
| 1D / 2D 频谱 | 高频有没有被抹掉 |

MSE 高不代表好 — 过度平滑反而 MSE 低。

---

## Step 8 · 实验迭代

![时间线](../assets/images/09-experiment-timeline.png)

```
v1 无 overlap     → 有缝
v2 振幅没对齐     → 颜色浅
v3 对齐振幅       → 颜色对了
v4 加 overlap     → 目前最好
```

---

## 想深入？

| 主题 | 文档 |
|------|------|
| 传统插值为啥不够 | [01-background.md](01-background.md) |
| 论文怎么选的 | [02-literature-review.md](02-literature-review.md) |
| 损失函数 / 网络结构 | [03-methodology.md](03-methodology.md) |
| tf.data 怎么加载 | [04-data-pipeline.md](04-data-pipeline.md) |
| 完整实验表 | [05-experiments.md](05-experiments.md) |
| 踩坑详情 | [07-troubleshooting.md](07-troubleshooting.md) |

---

## 关于图片

当前图是**合成示意图**（仓库里没有你 Word 里的原始截图）。

如果你手上有真实实验对比图，按 [../assets/images/README.md](../assets/images/README.md) 替换后，这份文档会更有说服力。
