import unittest
from tools.graph_state import generate_answer, transform_query, perform_web_search, route_question

class TestTools(unittest.TestCase):
    def test_generate_answer(self):
        state = {"question": "What are the Wikipedia details for Henry Ford?", "context": ""}
        result = generate_answer(state)
        self.assertIn("generation", result)

    def test_transform_query(self):
        state = {"question": "What's happened recently with Macom?"}
        result = transform_query(state)
        self.assertIn("search_query", result)

    def test_perform_web_search(self):
        state = {"search_query": "Macom news"}
        result = perform_web_search(state)
        self.assertIn("context", result)

    def test_route_question(self):
        state = {"question": "What are the Wikipedia details for Henry Ford?"}
        next_step = route_question(state)
        self.assertIn(next_step, ["web_search", "generate_answer"])

if __name__ == "__main__":
    unittest.main
