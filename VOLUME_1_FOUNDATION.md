# UC02 Antigravity — Volume 1: Foundation

## Goal
Build a stable base before datasets, OpenAI, RAG, or CMS.

Target stack:
- React + Tailwind
- Python + FastAPI
- MongoDB Atlas
- Git/GitHub

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


## Phase 0 — Repository structure
Create:
```text
uc02-prior-auth/
├── frontend/src/{components,pages,services,types}
├── backend/app/{api,models,services,database,rag,utils}
├── backend/data/{synthea,policies,sample_requests}
├── backend/tests
├── backend/requirements.txt
├── backend/.env.example
└── README.md
```

Do not request Synthea, OpenAI, policy PDFs, or CMS yet.

Acceptance:
- React boots.
- FastAPI boots.
- `GET /health` returns 200.
- No external AI dependency is required to boot.

## Phase 1 — Reviewer UI with dummy data
Pages:
1. Dashboard
2. New Authorization
3. Authorization Details
4. Review Result placeholder

New Authorization fields:
- patient_id
- diagnosis
- diagnosis_code
- requested_procedure
- cpt_code
- clinical_notes
- priority
- supporting-document placeholder

Do not build a chatbot-first UI.

## Phase 2 — FastAPI
Implement:
```text
GET  /health
POST /api/authorizations
GET  /api/authorizations
GET  /api/authorizations/{authorization_id}
```

Use Pydantic and consistent API errors.

## Phase 3 — MongoDB Atlas
### Give MongoDB configuration now
Developer provides:
```env
MONGODB_URI=
DATABASE_NAME=prior_auth_db
```

Collections:
```text
patients
prior_authorizations
clinical_extractions
policy_matches
authorization_results
reviewer_actions
audit_logs
```

If MongoDB is unreachable, return a clear service error. Never silently switch to in-memory storage.

## Phase 4 — Frontend ↔ Backend
Flow:
```text
React form
→ FastAPI validation
→ MongoDB
→ authorization_id
→ details page
```

Acceptance:
- Create request in UI.
- Refresh and confirm persistence.
- Invalid form displays a useful error.
- Backend outage does not crash UI.

## Completion gate
- [ ] React works
- [ ] FastAPI works
- [ ] MongoDB works
- [ ] create/list/detail authorization works
- [ ] validation and error handling work
- [ ] `.env` is ignored
- [ ] no OpenAI/RAG/CMS required

Antigravity should end with `READY FOR VOLUME 2` only when all checks pass.
