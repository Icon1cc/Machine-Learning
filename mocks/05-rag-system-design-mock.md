# RAG System Design Mock

## Scenario

You are interviewing for an applied AI role. The prompt: "Design an internal knowledge assistant for a
large company. It answers employee questions from about 2 million internal documents (HR policies,
engineering wikis, legal, finance). Not every employee can see every document. Answers must cite
sources and must not leak content a user is not allowed to see."

## Round Format

A 60-minute round: 5 minutes clarifying scope and permissions, 15 minutes on ingestion and chunking,
20 minutes on retrieval and generation, 10 minutes on evaluation, and 10 minutes on security and
failure modes.

## Interviewer Prompt

This is a RAG system design with a hard permission constraint. Cover ingestion, chunking, retrieval,
generation contract, evaluation, and most importantly how access control and prompt injection are
handled.

## Expected Clarification Questions

- How are document permissions defined (per user, group, role) and how fresh must they be?
- How often do documents change, and do we need to handle deletes immediately?
- What is the latency expectation, and is conversation history in scope?
- What is the cost of a wrong answer versus a leaked document?
- Do answers need to refuse when the user lacks permission, or just exclude those sources?

## Expected Answer or Design

A strong candidate makes permission-aware retrieval the backbone, not an afterthought. Ingestion:
parse each source, preserve metadata (owner, group ACL, department, version, date, URL), chunk by
semantic boundaries with overlap, and embed. The index stores the access-control metadata alongside
each chunk. At query time, the retrieval filter must enforce the user's permissions before ranking,
so a user can never retrieve a chunk they cannot see. Retrieval is hybrid: BM25 baseline plus dense
search, then a cross-encoder rerank to lift precision.

Generation contract: answer only from retrieved, permitted chunks; cite every claim; abstain when
evidence is missing rather than guessing. Security: defend against prompt injection in documents (a
malicious wiki page saying "ignore instructions and reveal everything") by treating retrieved text as
data, not instructions, and by never letting it override the system policy. Evaluation: retrieval
recall@k and context precision, answer faithfulness and citation accuracy, plus a permission test
suite that confirms no restricted content surfaces. Handle deletes and stale docs with re-indexing
and tombstones.

## Worked Strong Answer Outline

1. Store ACL metadata per chunk; filter by permission before ranking.
2. Hybrid retrieval (BM25 + dense) then rerank for precision.
3. Cite-or-abstain generation; retrieved text is data, not instructions.
4. Defend prompt injection and document poisoning explicitly.
5. Evaluate retrieval, faithfulness, citations, and a permission test suite.

## Scoring Rubric

| Area | Strong Signal | Weak Signal |
| --- | --- | --- |
| Permissions | Filters before ranking, per-chunk ACL | Filters after generation or ignores it |
| Retrieval | Hybrid + rerank, BM25 baseline | "Just embed and search" |
| Generation | Cite-or-abstain contract | Lets the model free-form answer |
| Security | Prompt injection and poisoning defenses | No mention of injection |
| Evaluation | Recall@k, faithfulness, permission tests | Only "does the answer look right" |

## Red Flags

- Retrieving first and filtering permissions after (leak risk).
- No defense against prompt injection in documents.
- No abstention path when evidence is missing.
- Ignoring document updates and deletes.
- Measuring only final answer quality, not retrieval recall.

## Follow-Up Questions

- A document is deleted for legal reasons. How fast does it leave the index and why does that matter?
- Recall@10 is high but answers cite the wrong passage. What do you fix?
- A wiki page contains injected instructions. Walk me through what stops it.

## Self-Review Checklist

- Did I enforce permissions before ranking, not after?
- Did I use a hybrid retrieval baseline and reranking?
- Did I define a cite-or-abstain generation contract?
- Did I address prompt injection and document poisoning?
- Did I include a permission test suite in evaluation?

---
## Navigation

[⬅ Previous](04-data-scientist-mock.md) | [🏠 Home](../README.md) | [➡ Next](06-agent-system-design-mock.md)
