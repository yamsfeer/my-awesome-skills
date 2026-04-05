# Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks - 原文存档

> 来源：https://arxiv.org/abs/2005.11401
> 抓取时间：2026-03-22

---

# Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

**arXiv:2005.11401v4 [cs.CL] 12 Apr 2021**

## Authors
Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, Douwe Kiela

*Facebook AI Research; University College London; New York University*

---

## Abstract

The paper introduces RAG — models combining pre-trained parametric and non-parametric memory for language generation. The parametric memory is a pre-trained seq2seq model (BART); the non-parametric memory is a dense vector index of Wikipedia accessed via a neural retriever (DPR). Two variants are compared: one conditioning on the same retrieved passages across the full output sequence, another using different passages per token.

---

## 1. Introduction

Pre-trained language models store factual knowledge in parameters but struggle to update, explain, or precisely access that knowledge. Prior hybrid models (REALM, ORQA) combined masked LMs with differentiable retrievers but only for extractive QA. This work brings hybrid memory to seq2seq models.

RAG uses:
- **Retriever**: Dense Passage Retriever (DPR)
- **Generator**: BART-large
- Both jointly trained end-to-end

Key claim: RAG achieves state-of-the-art on Natural Questions, WebQuestions, CuratedTrec, and strong results on TriviaQA, "outperforming parametric seq2seq models and task-specific retrieve-and-extract architectures."

---

## 2. Methods

### 2.1 Models

**RAG-Sequence**: Same retrieved document used for the entire output sequence:

p_RAG-Sequence(y|x) ≈ Σ_{z∈top-k} p_η(z|x) · Π_i p_θ(y_i|x,z,y_{1:i-1})

**RAG-Token**: A different document can be used per output token:

p_RAG-Token(y|x) ≈ Π_i Σ_{z∈top-k} p_η(z|x) · p_θ(y_i|x,z,y_{1:i-1})

### 2.2 Retriever: DPR

Bi-encoder architecture:
- Document encoder: BERT_d(z)
- Query encoder: BERT_q(x)
- Retrieval via Maximum Inner Product Search (MIPS) using FAISS

### 2.3 Generator: BART

BART-large (400M parameters), a denoising seq2seq transformer. Input and retrieved document are simply concatenated.

### 2.4 Training

Jointly trained by minimizing negative marginal log-likelihood of targets. The document encoder is kept **frozen**; only the query encoder and BART generator are fine-tuned.

### 2.5 Decoding

- **RAG-Token**: Standard beam search with marginalized transition probabilities.
- **RAG-Sequence**: Separate beam search per document, then hypotheses are aggregated ("Thorough Decoding" or "Fast Decoding").

---

## 3. Experiments

All experiments use a December 2018 Wikipedia dump (~21M 100-word chunks), indexed with FAISS HNSW.

| Task | Dataset(s) |
|------|-----------|
| Open-domain QA | NQ, TriviaQA, WebQuestions, CuratedTrec |
| Abstractive QA | MS-MARCO NLG |
| Question Generation | Jeopardy (SearchQA splits) |
| Fact Verification | FEVER (3-way and 2-way) |

---

## 4. Results

### 4.1 Open-domain QA (Exact Match)

| Model | NQ | TQA | WQ | CT |
|-------|-----|-----|-----|-----|
| T5-11B | 34.5 | 50.1 | 37.4 | — |
| T5-11B+SSM | 36.6 | 60.5 | 44.7 | — |
| REALM | 40.4 | — | 40.7 | 46.8 |
| DPR | 41.5 | 57.9 | 41.1 | 50.6 |
| RAG-Token | 44.1 | 55.2/66.1 | 45.5 | 50.0 |
| RAG-Sequence | **44.5** | 56.8/**68.0** | **45.2** | **52.2** |

RAG achieves state-of-the-art without expensive salient span masking pre-training. Notably, RAG scores 11.8% accuracy on NQ even when the correct answer is absent from all retrieved documents.

### 4.2 Abstractive QA (MS-MARCO)

RAG-Sequence outperforms BART by 2.6 BLEU and 2.6 Rouge-L points, approaching models that use gold passages.

### 4.3 Jeopardy Question Generation

RAG-Token outperforms RAG-Sequence on Q-BLEU-1. Human evaluation (452 pairs):

| Judgment | Factuality | Specificity |
|----------|-----------|-------------|
| BART better | 7.1% | 16.8% |
| RAG better | 42.7% | 37.4% |

RAG-Token benefits from combining content across multiple documents per token — illustrated by document posterior analysis on the "Hemingway" example.

### 4.4 Fact Verification (FEVER)

RAG achieves within 4.3% of state-of-the-art pipeline systems (which use retrieval supervision) on 3-way classification, and within 2.7% on 2-way classification without any retrieval supervision.

### 4.5 Additional Results

**Generation Diversity** (distinct trigram ratio):

| Model | MSMARCO | Jeopardy |
|-------|---------|---------|
| Gold | 89.6% | 90.0% |
| BART | 70.7% | 32.4% |
| RAG-Token | 77.8% | 46.8% |
| RAG-Sequence | 83.5% | 53.8% |

**Retrieval Ablations**: Learned (dense) retrieval outperforms frozen retrieval and BM25 on most tasks; BM25 is competitive on FEVER due to entity-centric claims.

**Index Hot-Swapping**: Replacing the 2016 Wikipedia index with a 2018 index updates world knowledge without retraining. Accuracy with mismatched indices drops dramatically (to ~4–12%).

**Effect of k (documents retrieved)**: More documents monotonically improve RAG-Sequence on QA; RAG-Token peaks at k=10.

---

## 5. Related Work

- **Single-Task Retrieval**: Prior work showed retrieval helps QA, dialogue, translation, etc. individually.
- **General-Purpose NLP**: BART, T5 achieve strong results without retrieval.
- **Learned Retrieval**: DPR, REALM, ORQA use differentiable retrievers for specific tasks.
- **Memory-based Architectures**: Memory networks, entity memory models. RAG's raw-text memory is human-readable and human-writable.
- **Retrieve-and-Edit**: RAG differs by aggregating across multiple retrieved documents and learning latent retrieval.

---

## 6. Discussion

RAG demonstrates that combining parametric and non-parametric memory yields state-of-the-art knowledge-intensive NLP performance. The retrieval index can be hot-swapped for knowledge updates without retraining. Future directions include joint pre-training of both components.

**Broader Impact**: RAG is more grounded and less prone to hallucination than purely parametric models, but shares risks of other LMs (misinformation, impersonation). The knowledge source (Wikipedia) may contain bias.

---

## Key Appendix Details

- **Parameters**: ~626M trainable (110M DPR query encoder + 406M BART-large); much smaller than T5-11B (11B).
- **Non-parametric index**: 21M vectors of dimension 728 (~15.3B values), stored on CPU (~100GB raw, ~36GB compressed).
- **Training**: 8× 32GB NVIDIA V100 GPUs, mixed precision, Fairseq; ported to HuggingFace Transformers.
- **Retrieval Collapse**: Observed on story generation tasks — retriever learns to retrieve same documents regardless of input, reducing RAG to BART-equivalent behavior.

---

## Selected References

- Lewis et al. (2019) — BART
- Karpukhin et al. (2020) — DPR
- Guu et al. (2020) — REALM
- Raffel et al. (2019) — T5
- Devlin et al. (2019) — BERT
- Johnson et al. (2017) — FAISS
- Thorne et al. (2018) — FEVER
- Kwiatkowski et al. (2019) — Natural Questions
- Joshi et al. (2017) — TriviaQA
- Wolf et al. (2019) — HuggingFace Transformers
