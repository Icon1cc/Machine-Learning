# Computer Vision

## Folder Purpose

Image tensors, convolution, classification, detection, segmentation, vision transformers, and multimodal models.

## Beginner Intuition

An image is just a grid of numbers (pixels across color channels). Computer vision teaches a model to
turn that grid into meaning: what is in the image, where it is, and which pixels belong to it.
Convolutions detect local patterns (edges, textures) and stack into higher-level features; vision
transformers do the same job with attention over image patches.

## Why It Matters

Vision powers defect detection, medical imaging, self-driving perception, document processing, and
content moderation. It is also where transfer learning shines: you rarely train from scratch, you
fine-tune a pretrained backbone on a few thousand labeled images.

## Who Should Read This Section

Read this if you work with images, or want to understand CNNs and vision transformers for interviews.
It builds on the deep-learning section and connects to multimodal generative AI.

## Recommended Reading Order

Read in order: overview, images as tensors, convolution, CNNs for classification, then the harder
tasks (detection, segmentation), then vision transformers and multimodal models.

## Table of Contents

| Order | File |
| --- | --- |
| 1 | [Computer Vision Overview](01-computer-vision-overview.md) |
| 2 | [Images As Tensors](02-images-as-tensors.md) |
| 3 | [Convolution](03-convolution.md) |
| 4 | [CNNs For Classification](04-cnns-for-classification.md) |
| 5 | [Object Detection](05-object-detection.md) |
| 6 | [Image Segmentation](06-image-segmentation.md) |
| 7 | [Vision Transformers](07-vision-transformers.md) |
| 8 | [Multimodal Models](08-multimodal-models.md) |

## Real-World Examples

- Defect detection on a factory line from camera images.
- Object detection drawing bounding boxes around pedestrians and cars.
- Medical segmentation outlining a tumor pixel by pixel.
- Multimodal models that caption an image or answer questions about it.

## Pattern Recognition

- "What is in the image" points to classification.
- "Where is it" points to detection (boxes), measured by mAP and IoU.
- "Which pixels are it" points to segmentation (masks).
- "Small labeled dataset" points to transfer learning from a pretrained backbone.

## Common Mistakes

- Training a large network from scratch on a small dataset.
- Forgetting data augmentation when images are scarce.
- Using accuracy on imbalanced classes (rare defects) instead of recall and PR-AUC.
- Ignoring inference latency on the deployment device.

## Interview Notes

Expect "how does a convolution work", "CNN vs vision transformer", "classification vs detection vs
segmentation", "how do you handle a small dataset". Connect the task to its metric (accuracy, mAP,
IoU).

## What You Should Know After Finishing

- How images are represented and how convolution extracts features.
- The difference between classification, detection, and segmentation.
- When vision transformers beat CNNs and why.
- How transfer learning and augmentation handle small datasets.

## Suggested Exercises

- Explain a convolution and pooling step on a small pixel grid.
- For a 5,000-image defect task, write your transfer-learning and augmentation plan.
- Match each task (classify, detect, segment) to its metric.
- Compare a CNN and a vision transformer for the same problem.

## Navigation

[🏠 Home](../README.md)
