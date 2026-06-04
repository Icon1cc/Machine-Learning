# Deep Learning

## Folder Purpose

Neural networks, optimization, regularization, convolution, sequence models, attention, and transformers.

## Beginner Intuition

A neural network is a stack of simple differentiable layers trained by gradient descent. The forward
pass makes a prediction, a loss measures the error, backpropagation computes how each weight
contributed, and the optimizer nudges the weights. Most of deep learning practice is making that loop
train stably and generalize.

## Why It Matters

Deep learning dominates images, audio, text, and anything with rich unstructured signal. It is also
the foundation under transformers and LLMs, so this section is the bridge from classical ML to modern
generative AI. Knowing how to debug training is what separates practitioners from notebook runners.

## Who Should Read This Section

Read this if you work with unstructured data, are heading toward NLP, LLMs, or computer vision, or
interview for roles that probe backprop, optimizers, and regularization. It builds on the math
section.

## Recommended Reading Order

Read in order: neuron and MLP, then activations, forward pass, backprop, optimizers, regularization
and normalization, then CNNs and sequence models, then attention and transformers, then training and
debugging.

## Table of Contents

| Order | File |
| --- | --- |
| 1 | [What Is A Neural Network](01-what-is-a-neural-network.md) |
| 2 | [Perceptrons And Mlps](02-perceptrons-and-mlps.md) |
| 3 | [Activation Functions](03-activation-functions.md) |
| 4 | [Forward Propagation](04-forward-propagation.md) |
| 5 | [Backpropagation](05-backpropagation.md) |
| 6 | [Optimizers SGD Adam RMSprop](06-optimizers-sgd-adam-rmsprop.md) |
| 7 | [Regularization Dropout Weight Decay](07-regularization-dropout-weight-decay.md) |
| 8 | [Batch Normalization Layer Normalization](08-batch-normalization-layer-normalization.md) |
| 9 | [CNNs](09-cnns.md) |
| 10 | [RNNs LSTMs GRUs](10-rnns-lstms-grus.md) |
| 11 | [Attention Mechanism](11-attention-mechanism.md) |
| 12 | [Transformers](12-transformers.md) |
| 13 | [Training Deep Networks](13-training-deep-networks.md) |
| 14 | [Debugging Neural Networks](14-debugging-neural-networks.md) |
| 15 | [Deep Learning Interview Patterns](15-deep-learning-interview-patterns.md) |

## Real-World Examples

- A CNN detecting manufacturing defects from line-camera images.
- An LSTM (now usually a transformer) forecasting demand from sequential data.
- A transformer powering translation, search embeddings, and chat assistants.
- Transfer learning: fine-tuning a pretrained backbone on a few thousand labeled images.

## Pattern Recognition

- "Loss is NaN" points to learning rate too high or a data bug.
- "Loss flat from step one" points to dead ReLUs, a wiring bug, or LR too low.
- "Train good, validation bad" points to overfitting, so regularize or add data.
- "Deep net will not learn" points to vanishing gradients, so add residuals and normalization.

## Common Mistakes

- Forgetting to normalize inputs.
- Using a learning rate orders of magnitude off.
- Leaving BatchNorm in train mode or applying dropout at inference.
- Blaming the model when the data pipeline is broken.

## Interview Notes

Expect "why ReLU over sigmoid", "Adam vs SGD", "what BatchNorm does", "how residual connections help",
"why dropout reduces overfitting". Tie each to gradient flow or regularization.

## What You Should Know After Finishing

- The training loop: forward, loss, backprop, optimizer step.
- How activations, normalization, and residuals affect gradient flow.
- How CNNs, RNNs, and transformers differ and when each fits.
- A concrete procedure for debugging a model that will not learn.

## Suggested Exercises

- Overfit a single batch on purpose to prove your model can learn.
- Explain backprop using the chain rule in three sentences.
- List three causes of a NaN loss and the check for each.
- Compare a CNN and a transformer for the same sequence task and justify a choice.

## Navigation

[🏠 Home](../README.md)
