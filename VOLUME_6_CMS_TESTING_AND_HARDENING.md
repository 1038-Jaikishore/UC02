# UC02 Antigravity — Volume 6: CMS + Testing + Hardening + Demo

## Goal
Add CMS as an optional policy source only after local Policy RAG is stable, then harden the entire application.

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


## Phase 33 — CMS integration
### Use CMS API/data now
First inspect the exact current CMS coverage source/API documentation chosen by the team before implementation.

Backend config may include:
```env
CMS_API_URL=
CMS_API_KEY=
```
Only require a key if the chosen endpoint actually needs one.

Architecture:
```text
Local Policy RAG ─┐
                  ├→ normalized policy object → criteria pipeline
CMS source ───────┘
```

Local RAG must remain available if CMS fails.

## Phase 34 — Normalize CMS output
Convert CMS responses into the same internal policy schema used by local RAG. Add `source_type = LOCAL_POLICY | CMS`.

## Phase 35 — CMS error handling
Handle:
- timeout,
- rate limit,
- 4xx/5xx,
- schema change,
- empty result,
- outage.

Fallback:
- valid local policy if available,
- otherwise human review / insufficient-policy state,
- never LLM memory as a substitute.

## Phase 36 — End-to-end tests
Test:
1. authorization creation,
2. MongoDB,
3. patient retrieval,
4. Synthea import,
5. clinical extraction,
6. policy ingestion,
7. retrieval,
8. criteria extraction,
9. evidence matching,
10. triage,
11. explanation,
12. human review,
13. audit,
14. CMS failure fallback.

Mock external APIs where appropriate.

## Phase 37 — Security/config review
Check:
- `.env` ignored,
- no secrets in frontend,
- file upload validation,
- input validation,
- logs do not leak secrets,
- MongoDB access configured appropriately,
- sensible CORS for demo/development.

Do not claim regulatory compliance unless separately assessed.

## Phase 38 — Cost/performance
- do not re-embed unchanged PDFs,
- bound top-k,
- do not send unnecessary patient history to OpenAI,
- prevent duplicate analysis jobs,
- cache stable policy retrieval where appropriate.

## Phase 39 — Demo cases
Prepare:
- APPROVE,
- REQUEST MORE INFORMATION,
- PEND FOR NURSE REVIEW,
- optional POLICY UNAVAILABLE.

## Phase 40 — Demo flow
1. dashboard,
2. prior-auth request,
3. Synthea evidence,
4. clinical extraction,
5. RAG retrieval,
6. exact policy source/page,
7. evidence matching,
8. AI recommendation,
9. missing evidence,
10. human action,
11. audit trail.

## Phase 41 — Final self-repair pass
Antigravity must run:
- backend tests,
- frontend build,
- lint if configured,
- API smoke checks,
- MongoDB connectivity,
- OpenAI failure path,
- missing FAISS path,
- RAG no-match,
- CMS outage fallback,
- three demo cases.

For every failure, use the mandatory error-fixing loop.

## Final checklist
- [ ] React/Tailwind
- [ ] FastAPI
- [ ] MongoDB Atlas
- [ ] Synthea
- [ ] OpenAI clinical extraction
- [ ] policy PDFs
- [ ] OpenAI embeddings
- [ ] FAISS
- [ ] grounded criteria
- [ ] evidence matcher
- [ ] triage engine
- [ ] explanations + citations
- [ ] human review
- [ ] audit
- [ ] optional CMS
- [ ] fallback behavior
- [ ] three demo cases
- [ ] frontend build passes
- [ ] backend tests pass
- [ ] no secrets committed
