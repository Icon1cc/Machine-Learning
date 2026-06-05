# Named Entity Recognition

## Beginner-Friendly Intuition

Named Entity Recognition (NER) finds and labels spans of text that refer
to specific entities: people, organizations, locations, dates, money
amounts, products. Given the sentence "Tim Cook met executives at Apple
in Cupertino last Tuesday," NER produces:

- "Tim Cook" -> PERSON
- "Apple" -> ORGANIZATION
- "Cupertino" -> LOCATION
- "last Tuesday" -> DATE

NER is one of the oldest and most-deployed information extraction tasks.
Search engines use it to understand queries, financial systems use it
to extract amounts and parties from contracts, healthcare systems extract
drug names from clinical notes, news pipelines populate knowledge graphs.

The challenge: entities are often ambiguous ("Washington" is a person,
a state, and a city), nested ("Bank of America Tower" contains "Bank
of America" as a sub-entity), and long-tail (every domain has its own
entity types). Traditional pipelines used hand-engineered features and
CRF decoding; modern systems fine-tune transformers on labeled examples
or prompt LLMs.

## Formal Explanation

### Tagging schemes

NER is a sequence labeling task: each input token gets one label.
Several tagging schemes mark span boundaries:

- **IO** (Inside, Outside). `O` for non-entity, `I-PER` for person
  tokens. Cannot mark adjacent entities of the same type.
- **BIO** (Begin, Inside, Outside). `B-PER` for first token of a
  person, `I-PER` for subsequent tokens, `O` for non-entity. Standard
  scheme.
- **BIOES** (Begin, Inside, Outside, End, Single). Adds `E-PER` for the
  last token of a multi-token entity and `S-PER` for single-token
  entities. Slightly more accurate than BIO; rarely worth the
  complexity.

The number of labels is `2K + 1` for BIO with `K` entity types (e.g.,
9 labels for 4 types), `4K + 1` for BIOES.

### Models

#### CRF on top of features

Pre-2018: CRF (Conditional Random Field) over hand-engineered features
(word identity, capitalization, prefix, suffix, gazetteer match,
neighboring word features). Strong baselines on standard benchmarks.

#### BiLSTM + CRF

A bidirectional LSTM produces per-token representations; a CRF on top
models label-to-label transitions, encouraging valid sequences (e.g.,
`I-PER` cannot follow `O`). State of the art before transformers.

#### Pretrained transformer + token classifier

Fine-tune BERT/RoBERTa/DeBERTa with a per-token classification head
(a linear layer over the BIO labels). The dominant approach in 2026.
Often achieves the same or better accuracy than BiLSTM + CRF, with
less feature engineering and faster training. Optionally add a CRF on
top for label coherence.

#### Span-based decoding

Instead of per-token labels, predict (start, end, type) triples for
spans. Naturally handles overlapping or nested entities, which BIO
cannot. Used by SpanBERT, span-based models, and most modern QA
systems.

#### LLM-based extraction

Prompt an LLM to extract entities and produce a structured output
(JSON). Works zero-shot or few-shot, handles novel entity types, but
slower and more expensive than fine-tuned encoders. Useful when label
budgets are small or entity types change frequently.

### Evaluation: span-level F1, not token-level

The right metric is **entity-level (span-level) F1**:

- A predicted entity is correct only if both its boundary and type
  match the gold annotation exactly.
- Precision = correct predicted entities / total predicted entities.
- Recall = correct predicted entities / total gold entities.
- F1 = harmonic mean.

Token-level F1 is misleading: a model that gets every token's `O`
label right scores high even if it misses every entity.

The standard evaluation library is `seqeval`, which implements span-
level metrics with various tagging schemes.

### Nested entities

In some domains (biomedical, finance), entities are nested. "Bank of
America Tower" contains "Bank of America" as a sub-entity. BIO cannot
represent nesting; you need:

- **Layered NER.** Run multiple BIO models, one per nesting level.
- **Span-based decoding.** Predict any (start, end, type) span.
- **Hypergraph models.** More expressive but more complex.

### Domain adaptation

Generic NER models (trained on news) often perform poorly on
specialized domains (biomedical, legal, code). Three options:

- **Continue pretraining.** Domain-adaptive pretraining on unlabeled
  domain text before fine-tuning on labeled NER.
- **Domain-specific pretrained models.** BioBERT, ClinicalBERT, SciBERT,
  Legal-BERT.
- **Few-shot prompting** of a large LLM.

### Long-tail entity types

For rare or new entity types (a new product, a slang term), few-shot
or zero-shot LLM extraction can outperform fine-tuned encoders that
have not seen the type. Hybrid pipelines route low-confidence
encoder predictions to the LLM.

## Why It Matters in Real Jobs

NER is the foundation of information extraction at scale. Three
production roles. First, **knowledge graph construction**: extract
entities from text and link them to a structured database. Second,
**search and query understanding**: identify entities in user queries
to route to specialized indexes. Third, **document processing**:
extract amounts, parties, dates from contracts, invoices, prescriptions,
or any structured-content document.

Production NER systems are rarely just a model; they include the
entity-linking step (mapping a span to a unique knowledge-base ID),
canonicalization (normalizing dates, amounts, addresses), and feedback
loops where reviewers correct errors.

## How It Works Step by Step

1. **Define the entity types.** Concrete, mutually exclusive (or pick
   a nesting strategy if not), and documented with examples. The label
   guidelines drive everything.
2. **Build labeled data.** Annotators label spans with types. Compute
   inter-annotator agreement; below 0.8 Cohen's kappa, the guidelines
   need work.
3. **Choose tagging scheme.** BIO for simple cases, BIOES for slightly
   better, span-based for nested.
4. **Pick a model.** Fine-tune a pretrained encoder for general
   accuracy. Domain-specific encoder for specialized text. Optionally
   add a CRF layer for label coherence.
5. **Tokenize carefully.** Subword tokenizers (BPE, WordPiece) split
   words into pieces; align labels to the first subword of each word.
6. **Train.** Standard transformer recipe. AdamW, `lr = 2e-5`, 3-5
   epochs.
7. **Evaluate with span-level F1.** Use `seqeval`. Per-type metrics
   reveal class-specific failures.
8. **Add post-processing.** Entity linking, canonicalization, business
   rule overrides.
9. **Monitor in production.** Per-type precision and recall. Drift in
   the distribution of input text often hits NER first.

## Real-World Example

A team builds an entity extractor for medical notes. They label 5,000
notes with 8 entity types: drug, dosage, frequency, condition,
procedure, anatomy, allergy, lab-value. Their first model is a
fine-tuned BERT-base; entity-level F1 is 0.71. They switch to
ClinicalBERT (BERT pretrained on medical text); F1 jumps to 0.79.
They add a CRF layer on top; F1 reaches 0.81 with cleaner span
boundaries. They build per-type evaluation; lab-value F1 is 0.93,
allergy F1 is 0.52 (rare class with high label noise). They
investigate; 30 percent of allergy labels are inconsistent with
guidelines. Re-labeling and re-training pushes allergy F1 to 0.78.
The lesson: per-type metrics drove the labeling improvement that drove
the accuracy improvement; aggregate F1 hid both.

## Common Mistakes

- Reporting token-level F1; it is misleading because most tokens are
  `O`.
- Using BIO for nested entities; switch to span-based.
- Forgetting to align subword tokens with word-level labels.
- Skipping per-type evaluation; aggregate metrics hide rare-class
  failures.
- Using generic pretrained models on specialized domains; domain-
  adaptive pretraining or domain-specific models help.
- Treating "entity boundary" as obvious; long entities and conjunctions
  ("Toronto and Vancouver") have ambiguous boundaries that the
  guidelines must resolve.
- Skipping the entity-linking step; raw spans are rarely the
  deliverable.
- Not handling acronyms ("CIA", "FBI") consistently with their full
  forms.
- Forgetting calibration; downstream systems often use entity scores.

## Interview Angle

**Question:** Walk through how you would build a production NER system,
including model choice, evaluation, and the post-processing steps.

**Strong answer:** Start with the entity types. Define them with
examples and counter-examples. Compute inter-annotator agreement on a
calibration set; if it is below 0.8 kappa, the guidelines need work.
Without good guidelines, no model can do well, and the metrics will be
misleading.

For the model. Default to fine-tuning a pretrained transformer with a
token classification head. RoBERTa-base or DeBERTa-v3-base for general
text. Domain-specific (BioBERT, Legal-BERT) for specialized text.
Tagging scheme: BIO for non-nested, span-based for nested. Optionally
add a CRF layer; it helps span coherence and adds 1-2 F1 points
typically. Train with AdamW at `lr = 2e-5`, 3-5 epochs, linear warmup
and cosine decay. Tokenization carefully aligned: subword tokenizers
split words; label only the first subword of each word, mark the rest
with a special "ignore" label that the loss masks.

For evaluation. Span-level (entity-level) F1 with `seqeval`. Both
boundary and type must match. Compute per-type F1 as well; aggregate
hides rare-class failures. Confusion analysis on validation set:
where does each type confuse with each other? That drives label
guideline iteration.

Post-processing. Entity linking: map each extracted span to a unique
knowledge-base ID (e.g., "Apple" -> Apple Inc, "Tim Cook" ->
Q312). Canonicalization for dates, money amounts, addresses (often a
regex layer or a small specialized model). Business rule overrides for
known patterns the model misses. Confidence thresholds: route low-
confidence predictions to human review.

Production concerns. Latency: fine-tuned BERT-base at int8 is ~10 ms
per sentence on CPU. Throughput: batch processing for offline
extraction, single-document for real-time. Drift: monitor per-type
precision and recall; entity vocabulary drifts faster than topic
classification. Retraining cadence: monthly or quarterly depending on
domain.

What I would not do. Use token-level F1 (misleading). Use a generic
model on specialized text without checking domain-specific
alternatives. Ship without per-type metrics. Skip entity linking; raw
spans are usually the input to a system that needs IDs.

**Weak answer:** "Fine-tune BERT for NER" without addressing tagging
scheme, span-level evaluation, or post-processing.

**Follow-up questions:**

- How do you handle nested entities?
- Why is span-level F1 the right metric instead of token-level?
- When would you use an LLM for NER instead of a fine-tuned encoder?
- How would you do entity linking after extraction?

## Mini Exercise

Take a labeled NER dataset (CoNLL-2003, OntoNotes, or a small custom
set). Fine-tune BERT-base for 3 epochs. Compute span-level F1 with
`seqeval`. Then add a CRF layer; compare F1. Note the boundary
improvements.

## Diagram

```mermaid
flowchart LR
    T[Text input] --> Tk[Tokenize]
    Tk --> E[Encoder: BERT/RoBERTa/Domain-specific]
    E --> H[Token classification head]
    H --> C[CRF layer (optional)]
    C --> P[BIO labels per token]
    P --> S[Decode spans]
    S --> L[Entity linking + canonicalization]
    L --> O[Structured entities with IDs]
```

---
## Navigation

[⬅ Previous](08-text-classification.md) | [🏠 Home](../README.md) | [➡ Next](10-semantic-search.md)
