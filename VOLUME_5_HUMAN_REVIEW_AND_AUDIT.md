# UC02 Antigravity — Volume 5: Human Review + Audit

## Goal
Turn the AI pipeline into a reviewer-controlled workflow.

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


## Phase 26 — Reviewer actions
Support:
```text
APPROVE
REQUEST_INFORMATION
SEND_TO_NURSE
OVERRIDE_AI
```

Keep AI recommendation and human final action in separate fields.

## Phase 27 — Override
If reviewer action differs from AI recommendation, require:
- override reason,
- reviewer/demo user,
- timestamp.

Never overwrite the original AI output.

## Phase 28 — Audit trail
Store chronology for:
- request created,
- patient evidence reference/version,
- extraction,
- policy retrieval,
- policy/version,
- criteria,
- evidence match,
- AI recommendation,
- explanation,
- reviewer action,
- override reason.

Do not store secrets or unnecessary sensitive prompt payloads.

## Phase 29 — Evidence viewer
For each criterion show:
- criterion,
- patient evidence,
- patient source,
- policy text,
- policy name,
- section,
- page.

## Phase 30 — Request-information draft
Optional: OpenAI drafts a reviewer-editable request using only structured missing-evidence results. Never auto-send.

## Phase 31 — Dashboard metrics
Use actual stored prototype data:
- total requests,
- recommendation distribution,
- human action distribution,
- overrides,
- pending nurse review,
- waiting for information,
- prototype processing time.

## Phase 32 — UI error recovery
Every major page needs:
- loading,
- empty,
- API error,
- retry,
- invalid-ID state.

An OpenAI/RAG failure must never erase the authorization request.

## Completion gate
- [ ] human action separate from AI
- [ ] overrides require reason
- [ ] audit works
- [ ] evidence viewer works
- [ ] missing-info draft grounded
- [ ] dashboard uses stored data
- [ ] error states usable
