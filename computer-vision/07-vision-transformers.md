# Vision Transformers

## Beginner-Friendly Intuition

A Vision Transformer (ViT) treats an image as a sequence of patches
(typically 16x16 pixels each) and processes them with a standard
transformer encoder. No convolutions; no spatial inductive biases
beyond the patch grid. Just self-attention over patches, the same
machinery that revolutionized NLP.

The intuition for why ViTs work: convolutions encode strong priors
about images (translation equivariance, locality). Those priors help
on small datasets but limit what the model can learn at scale.
Transformers have far weaker priors (just permutation invariance over
patches), so they cannot match CNNs on small data, but they scale
much better. Given hundreds of millions of training images, ViTs
match or exceed CNNs; given a few thousand, CNNs win comfortably.

In 2026, the picture is mixed. Pure ViTs work well for
foundation-model-style training (DINOv2, MAE-pretrained) but are
rarely the right choice for from-scratch training on a custom
dataset. Hybrid architectures (Swin, ConvNeXt, MaxViT) combine ViT
ideas with CNN priors and often dominate on real production tasks.

## Formal Explanation

### The ViT architecture

For a 224x224 RGB image:

1. **Patchify.** Split the image into 14x14 patches of size 16x16
   pixels. Each patch is flattened to a 768-dim vector (16 · 16 · 3 =
   768). 196 patches total.
2. **Linear projection.** Project each patch vector to model dim
   (768 in ViT-Base).
3. **Add positional encoding.** Learnable position embeddings, one
   per patch position. Without them, the transformer cannot tell
   which patch is which.
4. **Add a `[CLS]` token.** A learnable vector prepended to the
   sequence. Its final representation will be the image-level
   feature for classification.
5. **Transformer encoder.** Standard encoder layers (multi-head
   self-attention + MLP). 12 layers in ViT-Base, 24 in ViT-Large,
   32 in ViT-Huge.
6. **Classification head.** Linear layer over the `[CLS]` token's
   final embedding.

That is the entire architecture. No convolutions, no spatial
hierarchy, no specialized vision components.

### Variants

- **DeiT (2020).** ViT trained with strong augmentation and a
  distillation token. Showed ViT can train on ImageNet (1.3M images)
  alone, no need for 300M-image pretraining. The first practical
  ViT for the rest of us.
- **Swin Transformer (2021).** Hierarchical ViT with shifted windows.
  Computes attention only within local windows, which scales linearly
  with image size and recovers the spatial hierarchy of CNNs. The
  default ViT variant for many production tasks because it competes
  with CNNs at moderate data scale.
- **MaxViT (2022), CoAtNet (2021).** Hybrids of conv and attention.
- **MAE (Masked Autoencoder, 2022).** ViT pretrained by masking 75
  percent of patches and reconstructing them. Strong self-
  supervised features that transfer well.
- **DINO, DINOv2 (2021, 2023).** Self-distillation pretraining.
  Strong features without labels, often used as a frozen backbone
  with a linear classifier on top.

### CNN vs ViT inductive bias

- **CNN.** Translation equivariance (a feature in the corner is the
  same feature in the center) and locality (nearby pixels are more
  related than distant ones). Built into the architecture.
- **ViT.** Only permutation invariance over patches. The model has
  to learn translation equivariance and locality from data.

The implications:

- **Small data (< 10K images per class).** CNNs win. The inductive
  bias matches the data better than ViTs can learn from scratch.
- **Medium data (10K-1M).** Roughly comparable; depends on
  augmentation and recipe.
- **Large data (1M+ with pretraining).** ViTs and hybrids match or
  beat CNNs.

### Why pure ViTs need pretraining

The original ViT paper (Dosovitskiy et al., 2020) showed that ViT
trained on JFT-300M (300M images) reached state of the art, but ViT
trained only on ImageNet (1.3M) underperformed CNNs. The reason: ViT
needs to learn translation equivariance and locality from data, and
1.3M images is not enough.

DeiT showed that with strong augmentation, ViT can train on ImageNet
alone. Subsequent variants (Swin, ConvNeXt's ViT-style training)
made the architectures more data-efficient. The current rule of
thumb: pretrain on as much data as possible (ImageNet-21K with 14M
images at minimum, or large self-supervised corpora), then fine-tune.

### Scaling laws

ViTs scale gracefully. ViT-Huge at 632M parameters trained on JFT-
3B reached 90+ percent ImageNet accuracy. Scaling parameters,
data, and compute together produces predictable accuracy gains that
CNNs do not match at the same parameter count.

### Tasks beyond classification

ViTs are now used for:

- **Detection (DETR, Deformable DETR, DINO).** Encoder-decoder
  transformer over image features, with object queries.
- **Segmentation (Mask2Former, SAM).** Transformer decoder produces
  masks per query.
- **Self-supervised features (DINOv2).** Frozen ViT features plus a
  task head for many tasks.
- **Video (TimeSformer, ViViT).** Spatio-temporal attention.
- **Multimodal (CLIP, BLIP, LLaVA, GPT-4V).** ViT image encoder paired
  with a text model.

### Inference cost

ViT compute is `O(N² · d)` for N patches. At 224x224 with 16x16
patches, N = 196, attention is cheap. At 1024x1024 with 16x16
patches, N = 4096, attention becomes the bottleneck. Window-based
attention (Swin) and hierarchical designs handle high-resolution
images more efficiently.

## Why It Matters in Real Jobs

Three production reasons. First, **foundation models are mostly
ViTs**. CLIP, DINOv2, MAE, SAM, GPT-4V, and most modern multimodal
models use ViT-style image encoders. Using these models as
pretrained backbones is increasingly the default. Second, **scale
matters**: when you have a lot of data or can leverage massive
pretraining, ViTs deliver gains CNNs cannot. Third, **architectural
flexibility**: the transformer interface is the same as in NLP,
which makes multimodal work easier.

The cost: pure ViTs without massive pretraining underperform CNNs.
For most custom small-data tasks, fine-tuning a CNN backbone or a
hybrid (Swin, ConvNeXt) is still the right call.

## How It Works Step by Step

1. **Frame the task.** Classification, detection, segmentation,
   embeddings.
2. **Pick a pretrained model.** ViT-Base/16 or Swin-Base for
   classification. CLIP for zero-shot or image-text. DINOv2 for
   strong frozen features. SAM for promptable segmentation.
3. **Decide on linear probe vs fine-tune.** Linear probe (frozen
   backbone) is often within a few points of fine-tune and avoids
   overfitting on small data.
4. **Tokenize input.** Patchify the image; add positional encoding;
   prepend `[CLS]` if the model uses it.
5. **Train or fine-tune.** AdamW, lr=1e-4 to 3e-4, weight decay
   0.05, cosine LR with warmup. 30-300 epochs depending on data
   scale.
6. **Augment.** Strong augmentation (RandAugment, MixUp, CutMix)
   helps ViT in particular, since the model has weaker built-in
   priors.
7. **Stochastic depth (DropPath).** Standard for ViTs; rate
   typically 0.1-0.4 depending on depth.
8. **Evaluate per class** as always.
9. **Quantize and deploy.** ViTs are amenable to int8 quantization
   with similar accuracy preservation as CNNs.

## Real-World Example

A team builds a fashion item classifier (300 classes, 80K labeled
images). They benchmark.

- ResNet-50 pretrained, fine-tuned: top-1 0.78.
- ConvNeXt-tiny pretrained, fine-tuned: top-1 0.82.
- ViT-Base/16 pretrained on ImageNet-21K, fine-tuned: top-1 0.84.
- Swin-Base/4 pretrained on ImageNet-21K, fine-tuned: top-1 0.85.
- DINOv2-Base, frozen + linear classifier: top-1 0.83 (no fine-
  tune needed).

They ship Swin-Base. They quantize to int8; accuracy holds at 0.84.
For visual search (separate use case), they use DINOv2 frozen
features for embeddings; the embeddings transfer well across the
fashion domain without fine-tuning.

## Common Mistakes

- Training pure ViT from scratch on small data; needs massive
  pretraining or strong augmentation.
- Using ViT for tasks where CNN inductive bias matches better
  (small data, fine spatial detail, low-resolution dense
  prediction).
- Forgetting positional encoding; ViT cannot tell patch order
  without it.
- Using ImageNet-1K pretrained ViT and getting underwhelming
  results; ImageNet-21K or self-supervised pretraining is much
  stronger.
- Comparing ViT-Base with 86M parameters to ResNet-50 with 25M and
  concluding ViT is better; match parameter counts for fair
  comparison.
- Skipping stochastic depth for deep ViTs; they overfit otherwise.
- Using a single image-level `[CLS]` token for dense prediction
  tasks; per-patch outputs are needed for segmentation and detection.
- Forgetting that attention is `O(N²)` in patch count; high-resolution
  ViTs need window-based variants.

## Interview Angle

**Question:** Why do Vision Transformers need much more pretraining
data than CNNs to perform well, and when would you choose a CNN over
a ViT in 2026?

**Strong answer:** The difference is **inductive bias**. CNNs encode
strong priors about images directly into the architecture: weight
sharing across spatial positions (translation equivariance), local
receptive fields that grow with depth (locality), and a hierarchical
structure (low-level features at early layers, high-level features
later). These priors mean a CNN with a few million labeled images
can already learn meaningful representations.

ViTs have almost no built-in spatial priors. Each token is a 16x16
patch projected to a vector; self-attention treats them as a permutation-
invariant set, with order recovered only through learned positional
encodings. The model has to learn from scratch that nearby patches
are usually related, that translation produces predictable changes,
and that hierarchical features matter. Learning these priors needs
much more data than a model that has them built in.

The empirical evidence. The original ViT paper trained on JFT-300M (300
million images) and matched CNN state of the art; trained on
ImageNet-1K (1.3M), it underperformed. DeiT showed that strong
augmentation and distillation could close the gap on ImageNet-1K but
not entirely. The general rule: ViTs need 10-100x more data (or much
better pretraining) than CNNs to match them.

When to choose a CNN over a ViT in 2026.

- **Small to medium data (under 100K images per class).** CNN
  inductive bias dominates; ViT will overfit.
- **Edge or mobile inference.** EfficientNet, MobileNet, and
  ConvNeXt-tiny are typically faster than equally-sized ViTs.
- **Tasks needing fine spatial detail.** Medical imaging, defect
  detection, segmentation. CNNs and U-Nets handle these natively.
- **Limited compute for pretraining.** If you cannot afford
  ImageNet-21K or self-supervised pretraining, CNNs are easier.

When to choose a ViT (or hybrid).

- **Large pretraining available.** DINOv2, MAE-pretrained ViTs,
  CLIP. Foundation models are mostly transformer-based.
- **Multimodal work.** CLIP-style image-text alignment, multimodal
  LLMs. ViT interfaces cleanly with text transformers.
- **Self-supervised learning.** ViTs work especially well with masked-
  patch self-supervision.
- **Very large data.** When you have JFT-scale data, ViTs scale
  better than CNNs.
- **Hybrid models like Swin or ConvNeXt** when you want the best of
  both worlds and can afford moderate pretraining.

A senior engineer's instinct: in 2026, default to a hybrid (Swin,
ConvNeXt) pretrained on ImageNet-21K. Use a pure CNN (ResNet) for
small-data fast baselines or ViT (with massive pretraining) for
foundation-model-driven work.

**Weak answer:** "ViT needs more data" without explaining inductive
bias or naming when to choose CNN.

**Follow-up questions:**

- What is the difference between ViT and Swin Transformer?
- How does MAE pretraining work?
- When would you choose linear probe vs fine-tuning?
- What is DINOv2 and why is it useful?

## Mini Exercise

Take a small image classification dataset. Fine-tune a ViT-Base
pretrained on ImageNet-1K and a ResNet-50 pretrained on
ImageNet-1K with the same recipe. Compare validation accuracy. Then
do the same with ViT-Base pretrained on ImageNet-21K. Note the data-
scale effect.

## Diagram

```mermaid
flowchart LR
    I[Input image 224x224] --> P[Patchify into 14x14 patches of 16x16]
    P --> E[Linear projection + positional encoding + CLS token]
    E --> T[Transformer encoder: 12-32 layers]
    T --> C[CLS token's final embedding]
    C --> H[Linear classification head]
    H --> O[Predicted class]
```

---
## Navigation

[⬅ Previous](06-image-segmentation.md) | [🏠 Home](../README.md) | [➡ Next](08-multimodal-models.md)
