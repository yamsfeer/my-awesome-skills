# Alpha-CLIP: A CLIP Model Focusing on Wherever You Want - 原文存档

> 来源：https://arxiv.org/abs/2312.03818
> 抓取时间：2026-03-22

---

## Title & Authors
**Alpha-CLIP: A CLIP Model Focusing on Wherever You Want**

Authors: Zeyi Sun, Ye Fang, Tong Wu, Pan Zhang, Yuhang Zang, Shu Kong, Yuanjun Xiong, Dahua Lin, Jiaqi Wang
Institutions: Shanghai Jiao Tong University, Fudan University, CUHK, Shanghai AI Lab, University of Macau, MThreads

---

## Abstract
CLIP aligns text and visual modalities to comprehend entire images, including irrelevant details. For finer understanding and controlled editing, focus on specific regions (points, masks, boxes) is needed. Alpha-CLIP adds an auxiliary alpha channel to indicate attentive regions, fine-tuned on millions of RGBA region-text pairs. It preserves CLIP's visual recognition while enabling precise content emphasis across open-world recognition, MLLMs, and 2D/3D generation.

---

## 1. Introduction

### Problem
CLIP captures whole-image content but lacks region-specific focus needed for:
- Finer understanding
- Controllable content generation
- Regions specified by points/masks/boxes (via SAM, GLIP, proposal networks)

### Prior Approaches & Limitations

**Strategy 1 – Exclusion:**
- Crop regions into patches or mask irrelevant parts
- Disrupts/omits contextual information critical for precise understanding

**Strategy 2 – Highlighting:**
- Red circles or mask contours overlaid on images
- Changes original image content → undesirable recognition/generation results

### Proposed Solution: Alpha-CLIP
- Additional alpha channel input alongside RGB
- Alpha range [0,1]: 1 = foreground, 0 = background
- Trained on RGBA-text pairs generated via SAM + BLIP-2 pipeline
- Mix of region-text and image-text pairs during training

### Key Contributions by Domain

| Domain | Components | Tasks | Advantage |
|--------|-----------|-------|-----------|
| Image Recognition | Alpha-CLIP | Zero-shot Classification, REC | +4.1% top-1 on ImageNet |
| MLLM | Alpha-CLIP + LLM | VQA, Captioning | Reduces hallucinations, bias |
| 2D Generation | Alpha-CLIP + Diffusion | Image Variation | Subject-driven gen in complex scenes |
| 3D Generation | Alpha-CLIP + Diffusion/NeRF | Point-E, PureCLIPNeRF | Rectifies missing parts, better alignment |

---

## 2. Related Work

### Region-Aware CLIP Methods
- **MaskCLIP [75]:** 1×1 conv on final 2D features for regional semantics; doesn't modify CLIP weights
- **SAN [64]:** Side network for local semantic perception
- **MaskCLIP [9] / ODISE [62]:** Attention masks for local focus
- **RegionCLIP [74]:** Box-text pairs, fine-tunes CLIP for box-level recognition
- **MaskAdaptedCLIP [31]:** Mask-text pseudo-labels; poor generalization beyond segmentation
- **ReCLIP [54] / OvarNet [7]:** Crop by bounding box; loses context
- **Red-Circle [52] / FGVP [66]:** Circles/contours on images; alters content, domain gap

Alpha-CLIP's approach: additional alpha channel—does not change image content, preserves generalization.

### Region-Level Annotation
- **LAION-400M/5B:** Large-scale pretraining data, no fine-grained mask labels
- **Kosmos-2 [41]:** GLIP-based pseudo-labeling → GRIT dataset
- **SAM [22]:** Strong zero-shot segmentation for pseudo-mask generation
- Alpha-CLIP builds on GRIT + SAM for RGBA region-text pair generation

### CLIP in MLLMs
- Widely used as vision backbone (BLIP-2, LLaVA, Kosmos-2, GPT4ROI, GLaMM)
- GPT4ROI uses ROI Align on CLIP features; GLaMM adds region encoder
- Alpha-CLIP achieves mask-level focusing using only the CLIP model

### CLIP in 2D/3D Generation
- DALLE-2, IP-Adapter, BLIP-Diffusion use CLIP image encoder
- Subject-driven methods (DreamBooth, ELITE) require single centered foreground objects
- Point-E conditions 3D diffusion on CLIP features; PureCLIPNeRF uses CLIP loss for NeRF optimization

---

## 3. Method

### 3.1 RGBA Region-Text Pair Generation

#### Grounding Data Pipeline
- Source: GRIT dataset [41] (box region-text pairs via GLIP + CLIP)
- Enhancement: SAM generates high-quality pseudo-masks for each box region
- Output: Natural images + foreground alpha channels + referring expressions

#### Classification Data Pipeline
- Source: ImageNet [8]
- Steps:
  1. SAM auto-generates masks per image
  2. Crop foreground, center, enlarge
  3. CLIP scores each mask against class label
  4. Sort by score, select top-ranked masks
  5. Place foreground on white background → BLIP-2 generates captions
  6. Merge fine-grained ImageNet class labels + BLIP-2 captions
- Output: Millions of RGBA region-text pairs

### 3.2 Alpha-CLIP Architecture

#### Model Structure
- Base: CLIP image encoder (ViT)
- Modification: Additional **Alpha Conv layer** parallel to RGB Conv layer in first layer
- Alpha channel input: range [0,1]
- Alpha Conv kernel initialized to **zero** → initial model ignores alpha channel
- Minimal structural change preserves CLIP's prior knowledge

#### Training Method
- Text encoder: **frozen**
- Image encoder: fully trained
- Learning rates:
  - Alpha Conv layer: **2e-4**
  - Remaining transformer blocks: **2e-6** (lower rate)
  - Scheduler: cosine
- **Whole-image sampling ratio** r_s = 0.1: 10% of training replaces RGBA pairs with original image-text pairs (alpha = all 1)
- Optimizer: AdamW, weight decay 2e-2
- Batch size: 4096 for all scales
- Hardware: 8 A100-80G (ViT-B/16), 64 GPUs (ViT-L/14), 128 GPUs (ViT-L/14@336px)
- Temperature τ: fixed to post-CLIP-training value

---

## 4. Experiments

### Training Data
- **GRIT-20M [41]:** Grounding data pipeline → zero-shot ImageNet classification
- **GRIT-20M + 460K ImageNet pairs:** Combined → all other tasks (REC, OVD, captioning, generation)

### 4.1 Image Recognition

#### Zero-Shot Classification (ImageNet-S [12], 919 classes)

| Method | ViT-B/16 Top-1 | ViT-B/16 Top-5 | ViT-L/14 Top-1 | ViT-L/14 Top-5 |
|--------|----------------|----------------|----------------|----------------|
| Original CLIP | 66.48 | 88.90 | 73.48 | 91.60 |
| MaskAdaptedCLIP | 57.86 | 79.12 | 63.50 | 86.34 |
| Red Circle | 65.37 | 88.68 | 73.37 | 92.09 |
| MaskCLIP* | 67.86 | 89.40 | 77.04 | 93.39 |
| **Alpha-CLIP** | **68.89** | **90.51** | **77.41** | **94.45** |

#### Alpha Map Granularity Study (ViT-L/14)

| Alpha Map | Top-1 | Top-5 |
|-----------|-------|-------|
| CLIP (no alpha) | 73.48 | 91.60 |
| Alpha-CLIP – whole image | 73.37 | 91.75 |
| Alpha-CLIP – rectangular box | 75.62 | 93.34 |
| Alpha-CLIP – mask | 77.41 | 94.45 |

#### Zero-Shot Referring Expression Comprehension (REC)

| Method | RefCOCO Val | TestA | TestB | RefCOCO+ Val | TestA | TestB | RefCOCOg Val | Test |
|--------|-------------|-------|-------|--------------|-------|-------|--------------|------|
| CPT | 32.2 | 36.1 | 30.3 | 31.9 | 35.2 | 28.8 | 36.7 | 36.5 |
| ReCLIP | 45.8 | 46.1 | 47.1 | 47.9 | 50.1 | 45.1 | 59.3 | 59.0 |
| Red Circle | 49.8 | 58.6 | 39.9 | 55.3 | 63.9 | 45.4 | 59.4 | 58.9 |
| **Alpha-CLIP** | **55.7** | **61.1** | **50.3** | **55.6** | **62.7** | **46.4** | **61.2** | **62.0** |

### 4.2 MLLM Integration

#### Region-Level Captioning (Alpha-CLIP+LLaVA fine-tuned on Visual Genome + RefCOCOg)

| Model | RefCOCOg METEOR | RefCOCOg CIDEr | VG METEOR | VG CIDEr |
|-------|----------------|----------------|-----------|----------|
| GRIT | 15.2 | 71.6 | 17.1 | 142.0 |
| Kosmos-2 | 14.1 | 62.3 | — | — |
| GPT4RoI | — | — | 17.4 | 145.2 |
| GLaMM | 16.2 | 105.0 | 18.6 | 157.8 |
| **Alpha-CLIP+LLaVA** | **16.7** | **109.2** | **18.9** | **160.3** |

### 4.3 2D Image Variation

- Integration: Replace ViT-L/14 in BLIP-Diffusion with Alpha-CLIP
- Alpha-CLIP: Fine-grained mask-level focus, background preserved

### 4.4 3D Object Generation

#### Alpha-CLIP in PureCLIPNeRF (Quantitative, 153 COCO prompts, R-Precision):

| Method | Resolution+Iterations | R-Precision | Time |
|--------|----------------------|-------------|------|
| PureCLIPNeRF (orig CLIP) | 168²+10k | 85.62 | ~34 min |
| α-PureCLIPNeRF | 168²+10k | **88.89** | ~36 min |

---

## 5. Limitations

1. Cannot simultaneously focus on multiple objects or model inter-object relationships
2. Alpha channel doesn't generalize to intermediate values (beyond binary 0/1)
3. Low resolution (shared with original CLIP) hinders small object recognition

---

## 6. Conclusion

Alpha-CLIP introduces an additional alpha channel to CLIP for region-of-interest specification. Trained on millions of RGBA region-text pairs, it maintains output space consistency with original CLIP, enabling seamless plug-and-play replacement across downstream tasks.

---

## Appendix A: Training Details

### Whole-image sample ratio search (ViT-B/16, GRIT, 4 epochs):

| r_s | 0.0 | 0.1 | 0.2 | 0.3 | 0.4 | 0.5 | 0.6 | 0.7 | 0.8 | 0.9 | 1.0 |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| Top-1 | 68.06 | **68.25** | 67.87 | 67.71 | 67.83 | 67.74 | 67.37 | 66.87 | 66.39 | 64.94 | 63.96 |

### Unfreeze block number search (ViT-B/16, GRIT-1M, 4 epochs):

| Blocks unfrozen | 0 | 2 | 4 | 6 | 8 | 10 | 12 | Full-tune orig CLIP |
|-----------------|---|---|---|---|---|----|----|--------------------|
| Top-1 | 63.61 | 64.73 | 65.63 | 66.59 | 67.09 | 68.07 | 68.27 | 66.52 |
