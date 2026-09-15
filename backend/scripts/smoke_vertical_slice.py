"""Live smoke test of vertical slice 1 against a running API (local development only).

Usage (API running on http://127.0.0.1:8000, database seeded with --demo-users --demo-content):

    .venv/Scripts/python scripts/smoke_vertical_slice.py [email]

Answers every question with the first delivered option, so each synthetic account can run it once
(reassessment is not available). Prints status codes and results; never prints the password.
"""

from __future__ import annotations

import os
import sys

import httpx
from dotenv import dotenv_values

BASE = os.environ.get("SMOKE_BASE_URL", "http://127.0.0.1:8000")


def main() -> int:
    email = sys.argv[1] if len(sys.argv) > 1 else "training-manager01@example.invalid"
    password = os.environ.get("DEMO_USER_PASSWORD") or dotenv_values("../.env").get("DEMO_USER_PASSWORD")
    if not password:
        print("DEMO_USER_PASSWORD is not set")
        return 2
    with httpx.Client(base_url=BASE, timeout=30) as client:
        def show(label, response):
            print(f"{response.request.method:5} {response.request.url.path:60} -> {response.status_code}  {label}")
            if response.status_code >= 400:
                print("      problem:", response.json())
            return response

        show("health", client.get("/healthz"))
        show("ready", client.get("/readyz"))
        show("unauthenticated /me", client.get("/api/v1/me"))
        login = show("login", client.post("/api/v1/auth/login", json={"email": email, "password": password}))
        if login.status_code != 200:
            return 1
        headers = {"X-CSRF-Token": login.json()["csrf_token"]}
        me = show("me", client.get("/api/v1/me")).json()
        show("csrf missing", client.put("/api/v1/me/job-role", json={"job_role_id": "00000000-0000-0000-0000-000000000000"}))
        show("acknowledge notice", client.post("/api/v1/me/notice-acknowledgements",
                                               json={"notice_version": me["notice"]["version"]}, headers=headers))
        roles = show("job roles", client.get("/api/v1/job-roles")).json()
        demo_role = next(r for r in roles if r["is_demo"])
        requirements = show("role requirements", client.get(f"/api/v1/job-roles/{demo_role['id']}/competencies")).json()
        print("      requirements:", [(r["competency"]["code"], r["required_level"]) for r in requirements["requirements"]])
        show("select job role", client.put("/api/v1/me/job-role", json={"job_role_id": demo_role["id"]}, headers=headers))
        assessment = show("assessments", client.get("/api/v1/assessments")).json()[0]
        attempt = show("start attempt", client.post(f"/api/v1/assessments/{assessment['id']}/attempts", headers=headers))
        if attempt.status_code not in (200, 201):
            return 1
        attempt = attempt.json()
        for question in attempt["questions"]:
            client.put(f"/api/v1/attempts/{attempt['id']}/answers/{question['question_version_id']}",
                       json={"selected_option_id": question["options"][0]["id"]}, headers=headers).raise_for_status()
        print(f"      saved {len(attempt['questions'])} answers")
        submitted = show("submit", client.post(f"/api/v1/attempts/{attempt['id']}/submit", headers=headers)).json()
        print("      score_total:", submitted["score_total"], "baseline:", submitted["is_baseline"])
        result = show("result", client.get(f"/api/v1/attempts/{attempt['id']}/result")).json()
        for c in result["competencies"]:
            print(f"      {c['competency']['code']}: score {c['score']} level {c['level_number']} band {c['evidence_band']}")
        gaps = show("gaps", client.get("/api/v1/me/competency-gaps")).json()
        for g in gaps["items"]:
            print(f"      {g['competency']['code']}: status {g['status']} gap {g['gap']} (required {g['required_level']})")
        recs = show("recommendations", client.get("/api/v1/me/recommendations")).json()
        for r in recs["items"]:
            print(f"      #{r['rank']} {r['course']['title']} score {r['score']} demo={r['course']['is_demo']}")
        print("      gaps without approved content:", recs["gaps_without_approved_content"])
        show("submit again", client.post(f"/api/v1/attempts/{attempt['id']}/submit", headers=headers))
        show("logout", client.post("/api/v1/auth/logout", headers=headers))
        show("me after logout", client.get("/api/v1/me"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
