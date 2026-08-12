# UC02 Antigravity — Volume 3: Policy RAG

## Goal
Build the policy intelligence layer.

RAG answers:
> Which policy sections apply to this diagnosis, requested procedure, and CPT code?

RAG does not make the final authorization decision.

## Antigravity rules for every phase
1. Read the current README and inspect the repository before editing.
2. Implement only the requested phase; preserve working features.
3. Before changing code, list files to create/modify.
4. After changes, run the relevant tests/build/smoke checks.
5. Never hard-code secrets or expose backend credentials to React.
6. Never invent missing datasets, keys, patient facts, or policy criteria.
7. Use deterministic Python for numeric/boolean/date/rule comparisons wherever possible.
8. Validate every AI JSON response with Pydantic before using or storing it.
9. Keep patient evidence separate from policy knowledge.
10. The AI gives triage support; the human reviewer makes the final action.

### Mandatory error-fixing loop
When a failure occurs:
1. Reproduce it.
2. Capture the exact error/stack trace/status code.
3. Identify the layer: frontend, API contract, backend, MongoDB, OpenAI, RAG, data, or environment.
4. State the root cause briefly.
5. Make the smallest safe fix.
6. Re-run the failed test.
7. Run a regression smoke test on previously working functionality.
8. Report root cause, files changed, fix, tests, and any remaining limitation.

Never “fix” an error by deleting the feature, weakening validation, adding broad silent exception handling, or inserting fake data.


## Phase 11 — Policy dataset
### Give policy PDFs now
Place public medical-policy PDFs in:
```text
backend/data/policies/
```

Start with 5–20 focused policies for planned demo procedures.

Preserve when available:
- policy name,
- payer/source,
- filename,
- page,
- section,
- effective date,
- policy/version ID,
- procedure/CPT metadata.

## Phase 12 — Parse PDFs
Use PyMuPDF.

Requirements:
- extract page-by-page,
- preserve page numbers,
- detect empty/scanned pages,
- log unreadable pages,
- avoid OCR unless truly needed.

## Phase 13 — Chunking
Use section-aware chunks with limited overlap.

Every chunk must carry metadata:
```json
{
  "policy_name": "Lumbar MRI Policy",
  "page_number": 6,
  "section": "Medical Necessity",
  "source_file": "lumbar_mri_policy.pdf"
}
```

Never merge unrelated policies.

## Phase 14 — OpenAI embeddings + FAISS
Pipeline:
```text
PDF → PyMuPDF → chunks → OpenAI embeddings → FAISS
```

Use the same backend OpenAI configuration from Volume 2.

Build index to a temporary location, validate it, then replace the active index. A failed rebuild must not destroy the last good index.

## Phase 15 — Retriever
Input:
- diagnosis
- requested procedure
- CPT code
- useful clinical context

Example query:
```text
Lumbar MRI medical necessity coverage criteria chronic lower back pain CPT 72148
```

Return:
- chunk text
- policy name
- page
- section
- source file
- retrieval score

## Phase 16 — Retrieval quality
Add:
- top-k config,
- relevance threshold,
- duplicate suppression,
- optional metadata filters.

If evidence is weak, return:
`INSUFFICIENT_POLICY_EVIDENCE`.

Never force a match.

## Phase 17 — Criteria extraction
Use OpenAI only after retrieval.

Output:
```json
{
  "policy_name": "Lumbar MRI Policy",
  "criteria": [
    {
      "criterion_id": "C1",
      "description": "Conservative therapy documented",
      "required": true,
      "operator": ">=",
      "required_value": 6,
      "unit": "weeks",
      "source_page": 6,
      "source_section": "Medical Necessity"
    }
  ]
}
```

Rules:
- only extract what retrieved text supports,
- never invent thresholds,
- preserve uncertainty,
- every criterion needs a source.

## Phase 18 — Policy evidence UI
Show source policy, page, section, excerpt, extracted criterion, and retrieval status.

## RAG failure cases
Handle:
- bad PDF,
- embedding failure,
- missing index,
- index/metadata mismatch,
- no relevant policy,
- invalid AI JSON.

## Completion gate
- [ ] PDFs parse
- [ ] metadata preserved
- [ ] FAISS persists
- [ ] retrieval is relevant
- [ ] no-match state works
- [ ] criteria grounded
- [ ] every criterion has source metadata
- [ ] RAG never issues final authorization outcome
