import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from clients.igot_client import (
    AccessNotVerifiedError,
    AuthorizationRequiredError,
    IGotClient,
    NotFoundError,
    create_igot_client,
)
from clients.mock_igot_client import DEFAULT_FIXTURES, MockIGotClient


class MockIGotClientTest(unittest.TestCase):
    def setUp(self):
        self.client = MockIGotClient()

    def test_implements_interface(self):
        self.assertIsInstance(self.client, IGotClient)

    def test_list_courses_default_call(self):
        page = self.client.list_courses()
        self.assertEqual(page.total, 4)
        self.assertEqual(len(page.courses), 4)
        self.assertEqual(page.data_status, "MOCK")

    def test_list_courses_pagination_and_filters(self):
        page = self.client.list_courses(limit=1, offset=1)
        self.assertEqual([c.course_id for c in page.courses], ["MOCK-COURSE-002"])
        self.assertEqual(page.total, 4)
        by_provider = self.client.list_courses(provider="MOCK Provider B")
        self.assertEqual({c.course_id for c in by_provider.courses}, {"MOCK-COURSE-003", "MOCK-COURSE-004"})
        by_competency = self.client.list_courses(competency="MOCK: Survey methodology")
        self.assertEqual({c.course_id for c in by_competency.courses}, {"MOCK-COURSE-001", "MOCK-COURSE-004"})

    def test_list_courses_rejects_bad_paging(self):
        with self.assertRaises(ValueError):
            self.client.list_courses(limit=0)

    def test_get_course(self):
        course = self.client.get_course("MOCK-COURSE-003")
        self.assertTrue(course.title.startswith("MOCK"))
        self.assertEqual(course.data_status, "MOCK")
        with self.assertRaises(NotFoundError):
            self.client.get_course("NOPE")

    def test_enrollments_and_completions_are_consistent(self):
        enrollments = self.client.get_user_enrollments("MOCK-USER-002")
        completions = self.client.get_user_completions("MOCK-USER-002")
        self.assertEqual(len(enrollments), 3)
        completed = {e.course_id for e in enrollments if e.status == "completed"}
        self.assertEqual({c.course_id for c in completions}, completed)
        self.assertTrue(all(c.completed_on for c in completions))

    def test_learning_history_sorted_oldest_first(self):
        history = self.client.get_learning_history("MOCK-USER-002")
        times = [e.occurred_at for e in history]
        self.assertEqual(times, sorted(times))
        self.assertEqual(len(history), 5)

    def test_user_with_no_activity_returns_empty_lists(self):
        self.assertEqual(self.client.get_user_enrollments("MOCK-USER-003"), [])
        self.assertEqual(self.client.get_user_completions("MOCK-USER-003"), [])
        self.assertEqual(self.client.get_learning_history("MOCK-USER-003"), [])

    def test_unknown_user(self):
        for method in (self.client.get_user_enrollments, self.client.get_user_completions, self.client.get_learning_history):
            with self.assertRaises(NotFoundError):
                method("MOCK-USER-999")

    def test_acting_user_authorization(self):
        client = MockIGotClient(acting_user_id="MOCK-USER-001")
        self.assertEqual(len(client.get_user_enrollments("MOCK-USER-001")), 2)
        with self.assertRaises(AuthorizationRequiredError):
            client.get_user_completions("MOCK-USER-002")

    def test_every_record_is_labelled_mock(self):
        records = list(self.client.list_courses().courses)
        for uid in ("MOCK-USER-001", "MOCK-USER-002"):
            records += self.client.get_user_enrollments(uid)
            records += self.client.get_user_completions(uid)
            records += self.client.get_learning_history(uid)
        self.assertTrue(records)
        self.assertTrue(all(r.data_status == "MOCK" for r in records))

    def test_refuses_fixtures_not_marked_mock(self):
        data = json.loads(DEFAULT_FIXTURES.read_text(encoding="utf-8"))
        data["enrollments"][0]["data_status"] = "VERIFIED"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "fixtures.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(ValueError):
                MockIGotClient(fixtures_path=path)


class FactoryTest(unittest.TestCase):
    def test_default_is_mock(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            self.assertIsInstance(create_igot_client(), MockIGotClient)

    def test_live_is_refused(self):
        with mock.patch.dict(os.environ, {"IGOT_CLIENT_MODE": "live"}):
            with self.assertRaises(AccessNotVerifiedError):
                create_igot_client()


if __name__ == "__main__":
    unittest.main()
