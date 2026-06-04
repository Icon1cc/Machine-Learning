# AI Engineer Mock

## Scenario

You are interviewing for an AI Engineer role. The prompt: "Our sales team spends hours after each
customer call writing summaries and follow-up emails. Design an AI feature inside our CRM that listens
to a call transcript and produces a structured summary plus a draft follow-up email. We have about
20,000 calls per day."

## Round Format

A 60-minute round: 5 minutes clarifying the product, 15 minutes on the pipeline and model choice, 20
minutes on evaluation and the failure modes that matter, 10 minutes on cost, latency, and safety, and
10 minutes on a rollout and improvement plan.

## Interviewer Prompt

Treat this as a product, not a model. Walk through the user, the output contract, the baseline, the
LLM pipeline, how you would measure quality, and how you would prevent embarrassing or unsafe drafts
from reaching customers.

## Expected Clarification Questions

- Does the email get sent automatically, or does the rep always review and edit it first?
- What fields must the structured summary contain (next steps, objections, deal stage, owner)?
- Are transcripts already available, or do we need speech-to-text first?
- What is the acceptable latency: real-time at call end, or a few minutes later?
- What are the privacy rules for call content (PII, recording consent, retention)?

## Expected Answer or Design

A strong candidate fixes the output contract first: a JSON summary with named fields plus a draft
email, never auto-sent, always rep-reviewed. The baseline is a single well-structured prompt over the
transcript with few-shot examples. Pipeline: transcript to chunking if long, a prompt that extracts
fields and drafts the email, schema validation on the JSON, and a safety pass that blocks promises
about pricing or legal terms. Because volume is 20k/day and not latency-critical, batch or
near-real-time processing is fine, and a mid-tier model with caching controls cost.

Evaluation is the heart of the answer: build a labeled set of ~200 calls with human-written gold
summaries, measure field-level extraction accuracy and a faithfulness check (does the summary invent
facts not in the transcript), track rep edit rate as the real-world quality signal, and keep a
regression set of hard calls (multi-speaker, accents, interrupted). Production controls: log model
version and prompt version, monitor edit rate and refusal rate, and roll back on a spike.

## Worked Strong Answer Outline

1. Output is a reviewed draft, never auto-sent. That single decision removes most risk.
2. Baseline: one prompt, few-shot, JSON schema. Ship and measure before adding retrieval or
   fine-tuning.
3. Metric: faithfulness (no invented facts) as primary, rep edit rate as the online proxy.
4. Cost: mid-tier model, batch processing, prompt caching for the static instruction block.
5. Safety: block commitments on price, legal, or dates; escalate uncertain calls.

## Scoring Rubric

| Area | Strong Signal | Weak Signal |
| --- | --- | --- |
| Product framing | Defines review step and output contract first | Jumps to "use the biggest model" |
| Pipeline | Baseline prompt before fine-tuning or RAG | Proposes fine-tuning on day one |
| Evaluation | Faithfulness + edit rate + hard-example set | "We will check if it looks good" |
| Cost and latency | Picks model and batching to fit 20k/day | Ignores cost entirely |
| Safety | Blocks unsafe commitments, escalates | Auto-sends customer emails |

## Red Flags

- Auto-sending emails to customers with no human review.
- No faithfulness or hallucination check on summaries.
- Fine-tuning before trying a prompt baseline.
- No handling of long or multi-speaker transcripts.
- No privacy plan for recorded call content.

## Follow-Up Questions

- A rep says the model invented a commitment that was never made. How do you debug and prevent it?
- Costs are 3x budget. What do you change first?
- How would you add company-specific product knowledge without fine-tuning?

## Self-Review Checklist

- Did I define the output contract and the human-review step before the model?
- Did I propose a prompt baseline before advanced methods?
- Did I name faithfulness and edit rate as concrete metrics?
- Did I address cost, latency, and privacy for 20k calls per day?
- Did I include monitoring and rollback?

---
## Navigation

[⬅ Previous](../interview-prep/15-final-revision-checklist.md) | [🏠 Home](../README.md) | [➡ Next](02-ml-engineer-mock.md)
