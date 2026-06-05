# 参考文献

## 核心论文

1. **Zhu, J.-Y., et al.** (2017). *Unpaired Image-to-Image Translation using Cycle-Consistent Adversarial Networks.* ICCV.  
   — CycleGAN 原论文

2. **Isola, P., et al.** (2017). *Image-to-Image Translation with Conditional Adversarial Networks.* CVPR.  
   — pix2pix，U-Net 生成器 + PatchGAN

3. **Ledig, C., et al.** (2017). *Photo-Realistic Single Image Super-Resolution Using a Generative Adversarial Network.* CVPR.  
   — SRGAN，感知损失与频谱评估参考

4. **Seismic data interpolation using deep learning with GANs**  
   — 地震道插值 CycleGAN 方案（工作主要参考文献）

5. **Deep learning for 3D seismic compressive-sensing**  
   — 3D 地震压缩感知，VGG 感知损失参考

---

## 工具与数据

- **Madagascar** — `sfpatch` 等地震数据处理  
- **GOM 2D** — 公开二维炮集数据  
- **OpenCV** — `INTER_LINEAR` / `INTER_CUBIC` 传统插值基线  
- **TensorFlow 2** — `tf.data`, `tensorflow_datasets`  
- **pytorch-CycleGAN-and-pix2pix** — [junyanz/pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)

---

## 延伸阅读

- Goodfellow et al. — *Generative Adversarial Networks* (2014)  
- 双三次卷积插值原理 — 图像缩放经典算法  
- RNA（反褶积神经网络）相关文献 — 传统高级插值对标（待补充具体篇目）
