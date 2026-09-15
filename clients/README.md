# clients/

Thin, read-only clients. One module per source. A **live** client may be added
only after that source's API has been `VERIFIED` against official documentation.

## Contents

| Module | What it is | Status |
|---|---|---|
| `igot_client.py` | `IGotClient` interface, record types, errors, and `create_igot_client()` factory | Interface only. Contains no endpoints |
| `mock_igot_client.py` | `MockIGotClient` over `data/samples/mock/MOCK_igot_fixtures.json` | `MOCK` — every record is synthetic and labelled |

**There is no live iGOT client.** No public or partner API for iGOT Karmayogi is
documented, and no access has been authorized. See `../IGOT_ACCESS_STATUS.md`.
`create_igot_client()` returns the mock by default and raises
`AccessNotVerifiedError` if `IGOT_CLIENT_MODE=live`.

```python
from clients.igot_client import create_igot_client

client = create_igot_client()          # MockIGotClient
client.list_courses()
client.get_course("MOCK-COURSE-001")
client.get_user_enrollments("MOCK-USER-001")
client.get_user_completions("MOCK-USER-001")
client.get_learning_history("MOCK-USER-001")
```

Tests: `python -m unittest discover -s tests -t .`

## Rules for adding a live client

A live client may be added when, and only when:

- `API_REQUIREMENTS.md` has a `VERIFIED` row or section for the source,
- `SOURCE_AUDIT.md` carries a completed audit with a clean privacy screen,
- Gate C in `DATA_COLLECTION_CHECKLIST.md` is signed by two named people,
- for iGOT specifically, every precondition in `API_REQUIREMENTS.md` §6.4 is met.

Every client must satisfy constraints C-01 to C-12 in `../API_REQUIREMENTS.md`.
