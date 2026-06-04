# Deep Learning Mock

## Scenario

You are interviewing for a deep learning role. The prompt: "We are building a vision model to detect
surface defects on a manufacturing line. We have 8,000 labeled images, only 4 percent of which show a
defect. Early training runs either do not learn or overfit instantly. Walk me through how you would
build and debug this."

## Round Format

A 60-minute round: 5 minutes clarifying the data and constraint, 15 minutes on the model and training
setup, 20 minutes on debugging the training failures, 10 minutes on evaluation under class imbalance,
and 10 minutes on deployment on the line.

## Interviewer Prompt

This is a practical deep learning problem with small, imbalanced data and real training pathologies.
Cover transfer learning, the imbalance, how you debug "not learning" versus "overfitting", and how you
evaluate when defects are rare.

## Expected Clarification Questions

- Is the cost of a missed defect much higher than a false alarm (recall-heavy)?
- What is the image resolution and inference latency budget on the line?
- Are defects visually localized, so detection or segmentation might beat classification?
- Can we collect more defect images, or augment the rare class?
- Is labeling reliable, or do inspectors disagree on borderline cases?

## Expected Answer or Design

A strong candidate does not train from scratch on 8,000 images. Use transfer learning: a pretrained
backbone, freeze early layers, fine-tune the head, then unfreeze gradually. The 4 percent imbalance
needs handling: weighted loss or focal loss, oversampling defects, and heavy augmentation
(rotations, flips, crops, brightness) since defects are scarce. The metric is not accuracy; with 4
percent positives, predicting "no defect" scores 96 percent. Use recall at a fixed precision, PR-AUC,
and tune the threshold to the cost of a missed defect.

Debugging is the core of the answer. "Not learning" (flat loss): check the learning rate, verify the
data pipeline actually feeds correct labels, confirm the loss is wired correctly, and overfit a tiny
batch deliberately to prove the model can learn at all. "Overfits instantly": too little data or too
much capacity, so add augmentation, regularization, and freeze more of the backbone. Deployment: meet
the latency budget with a compact model, monitor the defect rate and score distribution for drift,
and keep humans reviewing low-confidence predictions.

## Worked Strong Answer Outline

1. Transfer learning, not from scratch, on 8,000 images.
2. Handle imbalance: focal/weighted loss, oversampling, augmentation.
3. Metric: recall at fixed precision and PR-AUC, never raw accuracy.
4. Debug "not learning" by overfitting one batch and checking the data pipeline.
5. Deploy compact, monitor score drift, human-review low confidence.

## Scoring Rubric

| Area | Strong Signal | Weak Signal |
| --- | --- | --- |
| Data strategy | Transfer learning + augmentation | Trains a big net from scratch |
| Imbalance | Focal/weighted loss, threshold tuning | Uses accuracy on 4 percent positives |
| Debugging | Overfit one batch, check pipeline | "Train longer" |
| Evaluation | PR-AUC, recall at precision | Reports accuracy |
| Deployment | Latency budget, drift monitoring | Ignores production constraints |

## Red Flags

- Training a large network from scratch on tiny data.
- Using accuracy as the metric under heavy imbalance.
- "Just train more epochs" as the debugging answer.
- No augmentation despite scarce defect images.
- Leaving BatchNorm in train mode or applying dropout at inference.

## Follow-Up Questions

- Loss is flat from step one. List three checks in priority order.
- Validation recall is high but the line still misses defects. What is wrong?
- Inspectors disagree on 15 percent of labels. How does that change your plan?

## Self-Review Checklist

- Did I use transfer learning instead of training from scratch?
- Did I handle the 4 percent imbalance explicitly?
- Did I choose a metric that survives imbalance?
- Did I give a concrete debugging procedure for not-learning and overfitting?
- Did I cover latency and drift monitoring on the line?

---
## Navigation

[⬅ Previous](07-statistics-mock.md) | [🏠 Home](../README.md) | [➡ Next](09-mlops-mock.md)
