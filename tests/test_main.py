import unittest
from main import run_agent

class TestMain(unittest.TestCase):
    def test_run_agent(self):
        query = "What are the Wikipedia details for Henry Ford?"
        result = run_agent(query)
        self.assertIn("Henry Ford", result)

if __name__ == "__main__":
    unittest.main()
