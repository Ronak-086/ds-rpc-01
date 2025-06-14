import unittest
from app.services.rag_service import RagService

class TestRAGPipeline(unittest.TestCase):
    def setUp(self):
        self.rag = RagService()

    def test_engineering_role(self):
        query = "Explain microservices architecture"
        response = self.rag.ask(query, "engineering")
        self.assertTrue(len(response) > 0)

    def test_finance_role(self):
        query = "Explain financial risks"
        response = self.rag.ask(query, "finance")
        self.assertTrue(len(response) > 0)

    def test_invalid_role(self):
        query = "Test query"
        with self.assertRaises(KeyError):
            self.rag.ask(query, "invalid_role")

if __name__ == '__main__':
    unittest.main()
