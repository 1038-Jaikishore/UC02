# UC02 Antigravity — Volume 2: Synthea + OpenAI Clinical Extraction

## Goal
Introduce synthetic patient evidence and structured clinical extraction.

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


## Prerequisite
Volume 1 must be stable.

## Phase 5 — Synthea ingestion
### Give the patient dataset now
Place files in:
```text
backend/data/synthea/
```

Recommended:
```text
patients.csv
conditions.csv
encounters.csv
procedures.csv
medications.csv
observations.csv
```

If files are missing, do not invent replacements. Report the exact missing files/columns.

Build an importer that:
1. validates file existence and columns,
2. normalizes IDs,
3. joins records by patient ID,
4. handles blanks safely,
5. upserts consolidated profiles into MongoDB,
6. reports processed/skipped/malformed rows.

Add:
```text
GET /api/patients/{patient_id}
GET /api/patients?search=
```

Important: Synthea stays in MongoDB/structured storage, not FAISS.

## Phase 6 — Link request to patient evidence
Keep historical procedures separate from `requested_procedure`.

Create a normalized patient evidence object from relevant:
- conditions,
- medications,
- procedures,
- encounters,
- observations.

## Phase 7 — OpenAI setup
### Give the OpenAI key now
Backend `.env`:
```env
OPENAI_API_KEY=
OPENAI_MODEL=
```

Do not put the key in React.

Handle:
- missing key,
- auth failure,
- timeout,
- rate limit,
- malformed JSON,
- schema failure.

## Phase 8 — Clinical extractor
Create:
```text
app/services/clinical_extractor.py
```

Suggested output:
```json
{
  "diagnosis": "Chronic lower back pain",
  "requested_procedure": "Lumbar MRI",
  "symptom_duration_weeks": 8,
  "physiotherapy_weeks": 3,
  "medications_attempted": ["Ibuprofen"],
  "previous_imaging": ["Lumbar X-Ray"],
  "relevant_conditions": [],
  "unknown_fields": []
}
```

Prompt rules:
- extract only supplied facts,
- never infer missing clinical facts,
- return null/empty when unknown,
- do not recommend approval,
- return machine-readable JSON.

Validate with Pydantic.

## Phase 9 — Persist extraction
Store:
- authorization_id
- patient_id
- structured extraction
- model
- timestamp
- extraction version
- validation status

Never overwrite raw patient data.

## Phase 10 — Clinical evidence UI
Show:
- source patient data,
- AI-extracted facts,
- unknown fields.

Do not show final triage yet.

## Tests
- complete note,
- missing duration → null,
- conflicting evidence → ambiguity,
- OpenAI unavailable,
- unknown patient ID.

## Completion gate
- [ ] Synthea import works
- [ ] patient API works
- [ ] request links to patient
- [ ] OpenAI backend-only
- [ ] AI JSON schema validated
- [ ] missing facts are not hallucinated
- [ ] errors handled
- [ ] extraction persisted
