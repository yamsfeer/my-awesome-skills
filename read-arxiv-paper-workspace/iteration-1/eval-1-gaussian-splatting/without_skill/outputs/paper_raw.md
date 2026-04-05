# Alpha-CLIP: A CLIP Model Focusing on Wherever You Want
**ArXiv:** 2312.03818 | **CVPR 2024** | Submitted December 6, 2023

**Authors:** Zeyi Sun, Ye Fang, Tong Wu, Pan Zhang, Yuhang Zang, Shu Kong, Yuanjun Xiong, Dahua Lin, Jiaqi Wang

**Resources:**
- Project page: https://aleafy.github.io/alpha-clip/
- Code: https://github.com/SunzeY/AlphaCLIP
- PDF: https://arxiv.org/pdf/2312.03818

---

## Abstract

Contrastive Language-Image Pre-training (CLIP) plays an essential role in extracting valuable content information from images across diverse tasks. It aligns textual and visual modalities to comprehend the entire image, including all the details, even those irrelevant to specific tasks. However, for finer understanding and controlled editing of images, it becomes crucial to focus on specific regions of interest, which can be indicated as points, masks, or boxes by humans or perception models.

Alpha-CLIP is an enhanced version of CLIP with an auxiliary alpha channel to suggest attentive regions, fine-tuned with millions of constructed RGBA region-text pairs. Alpha-CLIP not only preserves the visual recognition ability of CLIP but also enables precise control over the emphasis of image contents, proving effective across various tasks including open-world recognition, multimodal large language models, and conditional 2D/3D generation.

---

## Method

### Architecture

Alpha-CLIP modifies the CLIP image encoder to take an additional alpha channel along with RGB input. In the Vision Transformer (ViT) structure of the CLIP image encoder, **an additional Alpha Conv layer is added parallel to the existing RGB Conv layer**. This allows the encoder to accept an extra alpha channel input, where values range from 0 to 1, indicating background and foreground, respectively.

Initially, the Alpha Conv kernel weights are set to **zero** to ensure the alpha channel is ignored at the start of training (smooth initialization).

### Training Data Pipeline

Two data generation branches:

**1. Grounding pipeline:**
- Uses GRIT dataset which employs GLIP and CLIP to extract box region-text pairs
- Enhanced by using SAM (Segment Anything Model) to generate high-quality pseudo-masks for each box region
- Creates mask region-text pairs

**2. Classification pipeline:**
- Uses ImageNet dataset to generate region-text pairs with foreground objects highlighted
- SAM generates several masks per image; CLIP scores these masks with corresponding class labels
- Masks sorted by class scores; top-ranked masks selected
- Foreground objects placed on pure white background; BLIP-2 annotates with captions
- Fine-grained ImageNet class labels merged with BLIP-2 captions → millions of RGBA region-text pairs

Total: millions of RGBA region-text pairs using SAM and multimodal large models.

### Training Strategy

- **Text encoder:** Frozen throughout training
- **Image encoder:** Fully fine-tuned
- **Learning rates (AdamW, weight decay 2e-2):**
  - Alpha Conv layer: 2e-4
  - Remaining transformer blocks: 2e-6
  - Cosine learning rate scheduler
- **Loss function:** Contrastive loss (same as CLIP), temperature τ fixed to CLIP's trained value
- **Global recognition preservation:** Sample ratio r_s=0.1 — occasionally replace region pairs with full-image pairs (alpha=all ones)
- **Training duration:** GRIT-1M: 6–8 epochs; GRIT-20M: 2 epochs

---

## Key Results

### Image Recognition (ImageNet-S Zero-shot, ViT-L/14)

| Method | Top-1 Accuracy |
|--------|----------------|
| Original CLIP | 73.48% |
| MaskAdaptedCLIP | 63.50% |
| Alpha-CLIP (whole image) | 73.37% |
| Alpha-CLIP (box) | 75.62% |
| Alpha-CLIP (mask) | **77.41%** |

### Zero-shot Referring Expression Comprehension (RefCOCO)
- Surpasses ReCLIP by ~6.8%
- Surpasses RedCircle by ~3.0%
- Uses SAM-generated masks from box proposals

### Open Vocabulary Detection (OV-LVIS)
| Method | mAP_novel |
|--------|-----------|
| Detic-ImageNet (1.2M) | 24.6 |
| MaskImageNet + ori CLIP (460K) | 27.9 |
| MaskImageNet + Alpha-CLIP (460K) | **28.6** |

More data-efficient than Detic baseline.

### Region Captioning (LLaVA-1.5 fine-tuned)
| Model | RefCOCOg CIDEr | VG CIDEr |
|-------|----------------|----------|
| GLaMM | 105.0 | 157.8 |
| Alpha-CLIP + LLaVA-1.5 | **109.2** | **160.3** |

### 3D Generation (PureCLIPNeRF)
- R-Precision: 85.62 (original CLIP) → **88.89** (Alpha-CLIP)
- Alpha-CLIP without background augmentation matches or exceeds original CLIP with augmentation at 2x speed

---

## Ablation Studies

- **Sample ratio r_s:** Optimal at 0.1; too high degrades region focus; too low hurts global recognition
- **Unfreeze blocks:** More unfrozen blocks → better accuracy; full fine-tuning best; LoRA underperforms
- **Data volume:** More data consistently improves performance; larger ViT models benefit more
- **Whole-image setting:** Training and inference with alpha=all ones outperforms alpha=all zeros for global perception

---

## Downstream Applications

1. **MLLM** (BLIP-2, LLaVA-1.5): Region-focused VQA/captioning; reduces hallucinations; plug-in replacement
2. **2D Generation** (BLIP-Diffusion): Subject-driven generation in complex scenes; no retraining needed
3. **3D Generation** (Point-E, PureCLIPNeRF): Rectifies missing parts; improves text-3D alignment

---

## Limitations

- Cannot focus on multiple objects simultaneously or model inter-object relationships
- Alpha channel doesn't generalize well to intermediate values (between 0 and 1)
- Low input resolution limits small-object recognition (shared with original CLIP)

---

## Comparison vs. Alternative Region-Focusing Approaches

| Approach | Preserves Context | No Image Modification | Fine-grained |
|----------|-------------------|----------------------|--------------|
| Crop/Mask | ✗ | ✓ | ✗ |
| Red Circle overlay | ✓ | ✗ | ✗ |
| Feature masking | Partial | ✓ | ✗ |
| **Alpha-CLIP** | ✓ | ✓ | ✓ |

Key advantage: "does not change the image content and preserves the generalization performance" while enabling precise region control.

---

*Content retrieved from: arxiv.org/abs/2312.03818, ar5iv.labs.arxiv.org/html/2312.03818, aleafy.github.io/alpha-clip, huggingface.co/papers/2312.03818*
