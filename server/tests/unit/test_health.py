from unittest import TestCase

from server.application import application as api


class TestHealth(TestCase):
    def setUp(self) -> None:
        self.app = api.test_client()
        self.app.testing = True

    def test_get(self):
        response = self.app.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "App is healthy"})

    def test_post(self):
        response = self.app.post("/api/health")
        self.assertEqual(response.status_code, 405)
