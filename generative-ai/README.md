# Generative AI

## Folder Purpose

Autoregressive models, VAEs, GANs, diffusion, multimodal generation, and generative AI evaluation.

## Beginner Intuition

Generative models learn the distribution of data well enough to produce new samples that look like it:
new text, images, or audio. Different families reach that goal differently. Autoregressive models
predict the next piece; VAEs encode to a latent space and decode; GANs pit a generator against a
critic; diffusion models learn to reverse a noising process.

## Why It Matters

Generative AI underpins image generation, text-to-image tools, and the LLMs that dominate modern
products. Knowing the model families and, crucially, how to evaluate generation (which has no single
right answer) is increasingly core to AI engineering.

## Who Should Read This Section

Read this if you want to understand how image and text generators actually work, or you are heading
into LLM and multimodal work. It connects deep learning to the LLM and production-AI sections.

## Recommended Reading Order

Read in order: overview, autoregressive models, VAEs, GANs, diffusion, text-to-image, multimodal, then
evaluation last because judging generation ties the families together.

## Table of Contents

| Order | File |
| --- | --- |
| 1 | [Generative AI Overview](01-generative-ai-overview.md) |
| 2 | [Autoregressive Models](02-autoregressive-models.md) |
| 3 | [Variational Autoencoders](03-variational-autoencoders.md) |
| 4 | [GANs](04-gans.md) |
| 5 | [Diffusion Models](05-diffusion-models.md) |
| 6 | [Text To Image Systems](06-text-to-image-systems.md) |
| 7 | [Multimodal Generative AI](07-multimodal-generative-ai.md) |
| 8 | [Generative AI Evaluation](08-generative-ai-evaluation.md) |

## Real-World Examples

- Text-to-image tools (diffusion) generating art from a prompt.
- LLMs (autoregressive) drafting, summarizing, and answering.
- GAN-based super-resolution and face generation.
- Multimodal models that caption images or answer questions about a photo.

## Pattern Recognition

- "Predict the next token or pixel" points to autoregressive modeling.
- "Generate from a prompt with high fidelity images" points to diffusion.
- "Training is unstable, mode collapse" points to GANs.
- "How good is the output" with no single answer points to FID, human preference, and rubric eval.

## Common Mistakes

- Treating a single sample as proof of quality instead of measuring diversity and fidelity.
- Expecting GAN training to be as stable as supervised training.
- Ignoring evaluation because "it looks good" on a few examples.
- Forgetting safety filters and misuse risk on generative outputs.

## Interview Notes

Expect "VAE vs GAN vs diffusion", "how do you evaluate a generative model", "what is mode collapse",
"why is diffusion popular now". Strong answers connect the training objective to the failure mode and
the evaluation metric.

## What You Should Know After Finishing

- The four main generative families and how each samples.
- Why diffusion overtook GANs for high-quality image generation.
- How to evaluate generation with FID, human preference, and rubrics.
- Where safety and misuse risks enter generative systems.

## Suggested Exercises

- Compare VAE, GAN, and diffusion on training stability and sample quality.
- Propose an evaluation plan for a text-to-image model.
- Explain mode collapse and one mitigation.
- List two misuse risks of a generative system and a guardrail for each.

## Navigation

[🏠 Home](../README.md)
