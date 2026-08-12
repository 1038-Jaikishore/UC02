# UC02 Antigravity README Series

Use the volumes in order:

1. `VOLUME_1_FOUNDATION.md`
2. `VOLUME_2_PATIENT_DATA_AND_OPENAI.md`
3. `VOLUME_3_POLICY_RAG.md`
4. `VOLUME_4_EVIDENCE_AND_TRIAGE.md`
5. `VOLUME_5_HUMAN_REVIEW_AND_AUDIT.md`
6. `VOLUME_6_CMS_TESTING_AND_HARDENING.md`

## When to provide external inputs
- MongoDB Atlas URI → Volume 1, Phase 3.
- Synthea dataset → Volume 2, Phase 5.
- OpenAI API key → Volume 2, Phase 7.
- Policy PDFs → Volume 3, Phase 11.
- OpenAI embeddings → Volume 3, Phase 14, using the backend OpenAI configuration.
- CMS API/data → Volume 6, Phase 33, only after local RAG works.

## How to use with Antigravity
Open the current volume and say:

> Read this README and inspect the repository. Implement only the next incomplete phase. Before editing, tell me which files you will modify. After implementation, run tests/build checks, fix errors using the mandatory error-fixing loop, and stop at the phase completion gate. Do not proceed to the next phase unless I explicitly ask.

Each volume includes error recovery, acceptance gates, and rules preventing Antigravity from hiding failures with fake data or broad exception handling.
