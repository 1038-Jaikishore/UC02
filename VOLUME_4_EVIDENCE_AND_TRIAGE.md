# UC02 Antigravity — Volume 4: Evidence Matching + Triage + Explainability

## Goal
Compare structured patient evidence against RAG-derived policy criteria.

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


## Phase 19 — Normalize evidence
Normalize:
- weeks/months/days,
- booleans,
- dates,
- codes,
- medication/procedure lists,
- explicit unknown values.

Never convert unknown to false.

## Phase 20 — Evidence matcher
Create:
```text
app/services/evidence_matcher.py
```

Allowed statuses:
```text
MET
NOT_MET
UNCLEAR
MISSING
```

Example:
```json
{
  "criterion_id": "C1",
  "criterion": "Conservative therapy >= 6 weeks",
  "patient_evidence": "Physical therapy documented for 3 weeks",
  "normalized_patient_value": 3,
  "required_value": 6,
  "unit": "weeks",
  "status": "NOT_MET",
  "policy_source_page": 6
}
```

Use deterministic Python for numeric/boolean/date comparisons.

## Phase 21 — Triage engine
Create:
```text
app/services/decision_engine.py
```

Allowed recommendations:
```text
APPROVE
PEND_NURSE_REVIEW
REQUEST_MORE_INFO
```

Base behavior:
- required MISSING → REQUEST_MORE_INFO
- required UNCLEAR/conflicting → PEND_NURSE_REVIEW
- all mandatory MET → APPROVE
- NOT_MET must not automatically become a final denial; route to human review when policy/workflow requires judgment.

Return reason codes.

## Phase 22 — Missing evidence detector
Derive missing documentation from matcher results. Never invent a requirement.

## Phase 23 — Explanation
OpenAI may translate the structured result into reviewer-friendly prose.

The explanation must not change the deterministic result. If prose conflicts with structured output, reject/regenerate the prose.

## Phase 24 — Result UI
Show table:
| Criterion | Patient Evidence | Status | Policy Source |

Also show:
- recommendation,
- missing evidence,
- policy citations,
- warnings.

## Phase 25 — Reliability
Prefer HIGH/MEDIUM/LOW based on observable signals:
- retrieval quality,
- extraction completeness,
- direct evidence coverage,
- unresolved ambiguity.

Do not fabricate percentages.

## Test matrix
- all met,
- missing evidence,
- ambiguous evidence,
- no reliable policy,
- threshold boundary,
- 42 days vs 6 weeks,
- contradictory evidence.

## Completion gate
- [ ] normalization works
- [ ] matching traceable
- [ ] missing ≠ false
- [ ] triage only allowed states
- [ ] deterministic comparisons used where possible
- [ ] explanation cannot override result
- [ ] all three UC02 outcomes demo correctly
