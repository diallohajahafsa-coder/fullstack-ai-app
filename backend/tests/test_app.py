import unittest

from app import create_app


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app(
            {
                "TESTING": True,
                "MONGO_URI": "",
                "MONGO_DB_NAME": "test_database",
                "FRONTEND_ORIGIN": "http://localhost:5173",
            }
        ).test_client()

    def test_health_reports_api_and_optional_database(self):
        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")
        self.assertEqual(response.json["database"], "not_configured")

    def test_sentiment_requires_non_empty_text(self):
        response = self.client.post("/api/sentiment", json={"text": "  "})

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json)

    def test_sentiment_returns_demo_result_without_database(self):
        response = self.client.post(
            "/api/sentiment",
            json={"text": "This is a great and wonderful app"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["label"], "positive")
        self.assertEqual(response.json["mode"], "demo_rules")
        self.assertFalse(response.json["stored"])
        self.assertEqual(response.json["storage"], "not_configured")

    def test_sentiment_rejects_text_over_limit(self):
        response = self.client.post(
            "/api/sentiment",
            json={"text": "a" * 5001},
        )

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
