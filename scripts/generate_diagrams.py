#!/usr/bin/env python3
"""生成项目说明用示意图（合成数据，非真实炮集）。"""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "assets" / "images"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams["font.sans-serif"] = ["PingFang SC", "Heiti SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def synthetic_gather(n_traces=48, n_samples=80, seed=0):
    """合成类似炮集的二维图：多条双曲线同相轴。"""
    rng = np.random.default_rng(seed)
    img = np.zeros((n_samples, n_traces))
    t = np.linspace(0, 1, n_samples)
    for _ in range(12):
        trace0 = rng.integers(0, n_traces)
        v = rng.uniform(0.08, 0.25)
        for tr in range(n_traces):
            t0 = abs(tr - trace0) * v
            if t0 < 1:
                phase = (t - t0) * 40
                amp = np.exp(-((t - t0) ** 2) / 0.002) * (0.6 + 0.4 * np.sin(phase))
                img[:, tr] += amp
    img += rng.normal(0, 0.02, img.shape)
    img = (img - img.min()) / (img.max() - img.min() + 1e-8)
    return img


def remove_traces(img, ratio=0.3, seed=1):
    """竖向删道，模拟缺失检波道。"""
    rng = np.random.default_rng(seed)
    n_traces = img.shape[1]
    n_remove = int(n_traces * ratio)
    remove_idx = set(rng.choice(n_traces, n_remove, replace=False))
    out = img.copy()
    for i in remove_idx:
        out[:, i] = 0.05
    return out, sorted(remove_idx)


def smooth2d(img, k=5):
    """简单均值模糊，替代 scipy gaussian_filter。"""
    k = max(3, int(k) | 1)  # 奇数核
    pad = k // 2
    padded = np.pad(img, pad, mode="edge")
    out = np.zeros_like(img)
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            block = padded[y : y + k, x : x + k]
            out[y, x] = block.mean()
    return out


def fill_missing_traces(img):
    filled = img.copy()
    for i in range(filled.shape[1]):
        if filled[:, i].std() < 0.02:
            left = max(i - 1, 0)
            right = min(i + 1, filled.shape[1] - 1)
            filled[:, i] = 0.5 * filled[:, left] + 0.5 * filled[:, right]
    return filled


def fake_interp(img_missing, blur=3):
    """模拟 CycleGAN 补全：比双三次略锐。"""
    filled = fill_missing_traces(img_missing)
    return np.clip(smooth2d(filled, k=blur), 0, 1)


def bicubic_like(img_missing):
    filled = img_missing.copy()
    for i in range(filled.shape[1]):
        if filled[:, i].std() < 0.02:
            left = max(i - 2, 0)
            right = min(i + 2, filled.shape[1] - 1)
            filled[:, i] = filled[:, left : right + 1].mean(axis=1)
    return smooth2d(filled, k=7)


def save_panel(images, titles, path, figsize=(12, 3.2), cmap="seismic"):
    n = len(images)
    fig, axes = plt.subplots(1, n, figsize=figsize)
    if n == 1:
        axes = [axes]
    for ax, im, title in zip(axes, images, titles):
        ax.imshow(im, aspect="auto", cmap=cmap, vmin=0, vmax=1)
        ax.set_title(title, fontsize=11, pad=8)
        ax.set_xlabel("检波道 →")
        ax.set_ylabel("时间 ↓")
        ax.tick_params(labelsize=8)
    fig.suptitle("示意图 · 合成数据（非真实项目炮集）", fontsize=9, color="#666", y=1.02)
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig01_what_is_shot_gather():
    img = synthetic_gather()
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.imshow(img, aspect="auto", cmap="seismic", vmin=0, vmax=1)
    ax.axhline(0, color="white", lw=0)
    ax.annotate("", xy=(0.92, 0.08), xytext=(0.92, 0.92),
                xycoords="axes fraction",
                arrowprops=dict(arrowstyle="->", color="yellow", lw=2))
    ax.text(0.94, 0.5, "时间", transform=ax.transAxes, color="yellow", fontsize=11, va="center")
    ax.annotate("", xy=(0.08, 0.08), xytext=(0.92, 0.08),
                xycoords="axes fraction",
                arrowprops=dict(arrowstyle="->", color="yellow", lw=2))
    ax.text(0.5, 0.02, "检波道（每一列 = 一道波形）", transform=ax.transAxes,
            color="yellow", fontsize=11, ha="center")
    ax.set_title("炮集图长什么样？\n横轴是道，纵轴是时间，颜色是振幅", fontsize=12)
    fig.text(0.5, 0.01, "示意图 · 合成数据", ha="center", fontsize=8, color="#888")
    fig.tight_layout()
    fig.savefig(OUT / "01-shot-gather.png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig02_missing_traces():
    full = synthetic_gather()
    missing, idx = remove_traces(full)
    vis = missing.copy()
    for i in idx:
        vis[:, i] = np.nan
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8))
    axes[0].imshow(full, aspect="auto", cmap="seismic", vmin=0, vmax=1)
    axes[0].set_title("完整炮集（域 Y）")
    axes[1].imshow(vis, aspect="auto", cmap="seismic", vmin=0, vmax=1)
    axes[1].set_title("删掉 30% 竖向道（域 X）\n白色竖条 = 缺失道")
    for ax in axes:
        ax.set_xlabel("检波道 →")
        ax.set_ylabel("时间 ↓")
    fig.suptitle("我们要解决的问题：把右边的「白条」补回来", fontsize=12, y=1.05)
    fig.text(0.5, -0.02, "示意图 · 合成数据", ha="center", fontsize=8, color="#888")
    fig.tight_layout()
    fig.savefig(OUT / "02-missing-traces.png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig03_cyclegan_idea():
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3)
    ax.axis("off")
    boxes = [
        (0.3, 1.2, "域 X\n缺失道炮集", "#ffe0e0"),
        (2.5, 1.2, "G\n补全", "#fff3cd"),
        (4.5, 1.2, "域 Y\n完整炮集", "#d4edda"),
        (6.5, 1.2, "F\n反向", "#fff3cd"),
        (8.5, 1.2, "回到 X\n循环一致", "#e2e3e5"),
    ]
    for x, y, text, color in boxes:
        ax.add_patch(mpatches.FancyBboxPatch((x, y), 1.4, 1.0, boxstyle="round,pad=0.05",
                                             facecolor=color, edgecolor="#333"))
        ax.text(x + 0.7, y + 0.5, text, ha="center", va="center", fontsize=10)
    for x1, x2 in [(1.7, 2.5), (3.9, 4.5), (5.9, 6.5), (7.9, 8.5)]:
        ax.annotate("", xy=(x2, 1.7), xytext=(x1, 1.7),
                    arrowprops=dict(arrowstyle="->", lw=1.8))
    ax.text(5, 2.6, "CycleGAN 核心：不需要「缺失图-完整图」严格成对，只要两个域的分布",
            ha="center", fontsize=11)
    fig.savefig(OUT / "03-cyclegan-idea.png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig04_results_compare():
    full = synthetic_gather(seed=2)
    missing, _ = remove_traces(full, seed=3)
    bicubic = bicubic_like(missing)
    cyclegan = fake_interp(missing, blur=3)
    save_panel(
        [missing, bicubic, cyclegan, full],
        ["缺失 30% 道", "双三次插值\n（偏糊）", "CycleGAN 补全\n（纹理更锐）", "完整真值"],
        OUT / "04-method-compare.png",
        figsize=(13, 3.2),
    )


def fig05_overlap():
    """示意 overlap 拼接缝隙。"""
    patch = synthetic_gather(n_traces=32, n_samples=60, seed=4)
    mid = patch.shape[1] // 2
    left, right = patch[:, :mid], patch[:, mid:]
    right_shallow = right * 0.55 + 0.15

    no_overlap = np.hstack([left, right_shallow])
    # 中间画一条亮缝表示断层
    seam = mid
    no_overlap[:, seam - 1 : seam + 1] = 0.95

    overlap_w = 3
    w = np.linspace(0, 1, overlap_w)
    blend_zone = left[:, -overlap_w:] * (1 - w) + right_shallow[:, :overlap_w] * w
    with_overlap = np.hstack([left[:, :-overlap_w], blend_zone, right_shallow[:, overlap_w:]])

    save_panel(
        [no_overlap, with_overlap],
        ["无 overlap 硬拼\n→ 中间亮缝 = 拼接断层", "有 overlap 渐变融合\n→ 同相轴更连续"],
        OUT / "05-overlap-stitch.png",
        figsize=(9, 3.5),
    )


def fig06_amplitude():
    full = synthetic_gather(seed=5)
    missing, _ = remove_traces(full, ratio=0.3, seed=6)
    # 模拟振幅不一致：域 X 整体偏浅
    missing_shallow = missing * 0.45 + 0.1
    pred_wrong = fake_interp(missing_shallow) * 0.5 + 0.1
    pred_right = fake_interp(missing_shallow)
    pred_right = (pred_right - pred_right.min()) / (pred_right.max() - pred_right.min())
    pred_right = pred_right * (full.max() - full.min()) + full.min()
    save_panel(
        [full, missing_shallow, pred_wrong, pred_right],
        ["完整炮集", "缺失道炮集\n（振幅偏浅）", "未对齐振幅时预测\n→ 颜色偏浅", "对齐振幅后预测\n→ 深度接近真值"],
        OUT / "06-amplitude-align.png",
        figsize=(13, 3.2),
    )


def fig07_workflow():
    steps = [
        "炮集数据", "删 30% 道", "切块+训练", "逐块预测", "overlap 拼接", "波形+频谱评估"
    ]
    fig, ax = plt.subplots(figsize=(11, 2.2))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 2)
    ax.axis("off")
    colors = ["#cfe2ff", "#ffe5b4", "#ffd6e7", "#d1e7dd", "#e2d9f3", "#cff4fc"]
    for i, (s, c) in enumerate(zip(steps, colors)):
        x = 0.4 + i * 1.75
        ax.add_patch(mpatches.FancyBboxPatch((x, 0.6), 1.5, 0.8, boxstyle="round,pad=0.04",
                                             facecolor=c, edgecolor="#444"))
        ax.text(x + 0.75, 1.0, s, ha="center", va="center", fontsize=9)
        if i < len(steps) - 1:
            ax.annotate("", xy=(x + 1.55, 1.0), xytext=(x + 1.45, 1.0),
                        arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.set_title("实际工程流程（比论文多出来的部分）", fontsize=12, pad=10)
    fig.savefig(OUT / "07-workflow.png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig08_spectrum():
    full = synthetic_gather(n_traces=1, n_samples=256, seed=7).flatten()
    t = np.linspace(0, 1, len(full))
    trace_sharp = full
    trace_blur = np.convolve(full, np.ones(15) / 15, mode="same")
    fft_sharp = np.abs(np.fft.rfft(trace_sharp))
    fft_blur = np.abs(np.fft.rfft(trace_blur))
    freq = np.fft.rfftfreq(len(trace_sharp), d=1 / 250)

    fig, axes = plt.subplots(1, 2, figsize=(9, 3.5))
    axes[0].plot(t, trace_sharp, label="CycleGAN 补全道", lw=1)
    axes[0].plot(t, trace_blur, label="双三次补全道", lw=1, alpha=0.8)
    axes[0].set_title("单道波形对比")
    axes[0].set_xlabel("时间")
    axes[0].legend(fontsize=8)
    axes[1].plot(freq, fft_sharp, label="CycleGAN")
    axes[1].plot(freq, fft_blur, label="双三次", alpha=0.8)
    axes[1].set_title("一维频谱：高频谁保留得多？")
    axes[1].set_xlabel("频率")
    axes[1].set_xlim(0, 80)
    axes[1].legend(fontsize=8)
    fig.suptitle("评估不只看「像不像」，还要看频谱高频", fontsize=11, y=1.02)
    fig.text(0.5, -0.02, "示意图 · 合成波形", ha="center", fontsize=8, color="#888")
    fig.tight_layout()
    fig.savefig(OUT / "08-spectrum.png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig09_experiment_timeline():
    """实验迭代时间线。"""
    items = [
        ("v1", "无 overlap", "边缘道浅、有缝隙", "#f8d7da"),
        ("v2", "振幅未对齐", "整体颜色偏浅", "#fff3cd"),
        ("v3", "振幅对齐", "颜色对了，纹理仍糊", "#cff4fc"),
        ("v4", "加 overlap", "缝隙消失，效果最好", "#d1e7dd"),
    ]
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis("off")
    for i, (ver, change, result, color) in enumerate(items):
        y = 3.8 - i * 0.9
        ax.add_patch(mpatches.FancyBboxPatch((0.5, y - 0.25), 8.5, 0.7, boxstyle="round,pad=0.03",
                                             facecolor=color, edgecolor="#999"))
        ax.text(1.0, y + 0.1, ver, fontsize=10, fontweight="bold")
        ax.text(2.0, y + 0.1, change, fontsize=10)
        ax.text(5.5, y + 0.1, f"→ {result}", fontsize=10)
    ax.set_title("实验是怎么一步步改过来的", fontsize=12)
    fig.savefig(OUT / "09-experiment-timeline.png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main():
    fig01_what_is_shot_gather()
    fig02_missing_traces()
    fig03_cyclegan_idea()
    fig04_results_compare()
    fig05_overlap()
    fig06_amplitude()
    fig07_workflow()
    fig08_spectrum()
    fig09_experiment_timeline()
    print(f"Generated {len(list(OUT.glob('*.png')))} images in {OUT}")


if __name__ == "__main__":
    main()
