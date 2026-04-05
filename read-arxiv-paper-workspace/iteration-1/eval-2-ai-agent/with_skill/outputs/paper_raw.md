# Mixtral of Experts - 原文存档

> 来源：https://arxiv.org/abs/2401.04088
> 抓取时间：2026-03-22

---

## 摘要（Abstract）

We introduce Mixtral 8x7B, a Sparse Mixture of Experts (SMoE) language model. Mixtral has the same architecture as Mistral 7B, with the difference that each layer is composed of 8 feedforward blocks (i.e. experts). For every token, at each layer, a router network selects two experts to process the current state and combine their outputs. Even though each token only sees two experts, the selected experts can differ at each timestep. As a result, each token has access to 47B parameters, but only uses 13B active parameters during inference. Mixtral was trained with a context size of 32k tokens and it outperforms or matches Llama 2 70B and GPT-3.5 across all evaluated benchmarks. In particular, Mixtral vastly outperforms Llama 2 70B on mathematics, code generation, and multilingual benchmarks. We also provide a model fine-tuned to follow instructions, Mixtral 8x7B – Instruct, that surpasses GPT-3.5 Turbo, Claude-2.1, Gemini Pro, and Llama 2 70B – Chat model on human evaluation benchmarks. Both the base and instruct models are released under the Apache 2.0 license.

---

## 架构参数（Architecture Parameters）

| 参数 | 值 |
|------|----|
| dim | 4096 |
| n_layers | 32 |
| head_dim | 128 |
| hidden_dim | 14336 |
| n_heads | 32 |
| n_kv_heads | 8 |
| context_len | 32768 |
| vocab_size | 32000 |
| num_experts | 8 |
| top_k_experts | 2 |

---

## 性能对比（Performance Benchmarks）

### 综合基准测试
- Mixtral 8x7B 在 12 个主流基准中超越 Llama 2 70B 9 个，超越 GPT-3.5 5 个
- 推理速度比 Llama 2 70B 快约 6 倍

### MT-Bench（指令微调版本）
- Mixtral 8x7B Instruct: **8.30**
- 超越：GPT-3.5 Turbo, Claude-2.1, Gemini Pro, Llama 2 70B Chat

### Passkey Retrieval（长上下文）
- 在 32k 上下文内：**100% 准确率**，与 passkey 位置无关

### 数学与代码
- 在 GSM8K、HumanEval、MBPP 等任务上显著优于 Llama 2 70B

### 多语言
- 在 ARC Challenge、HellaSwag、MMLU 的法/德/西/意版本上全面超越 Llama 2 70B

---

## 专家分析（Expert Analysis）

- 大多数领域（生物、哲学、机器学习）文本上专家分配无明显规律
- DM Mathematics 合成数据集上出现显著专家偏好差异
- 语法层面（空白符、标点符号等）专家专业化最为明显
- 不同层之间，连续 token 通常被分配到相同专家

---

## 模型发布信息（Release Information）

- 基础模型：Mixtral 8x7B（Apache 2.0）
- 指令微调模型：Mixtral 8x7B – Instruct（Apache 2.0）
- 发布平台：Hugging Face, Mistral AI 官网
- 推理支持：vLLM + Megablocks CUDA 内核

---

## 引用信息（Citation）

```bibtex
@article{jiang2024mixtral,
  title={Mixtral of Experts},
  author={Albert Q. Jiang and Alexandre Sablayrolles and Antoine Roux and ...},
  journal={arXiv preprint arXiv:2401.04088},
  year={2024}
}
```
