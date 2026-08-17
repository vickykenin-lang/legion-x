import sqlite3
import tempfile
import unittest
from pathlib import Path

from legion_x.pipeline import guardian, oracle, run_pipeline


class PipelineTests(unittest.TestCase):
    def test_oracle_is_reproducible(self):
        self.assertEqual(oracle("same-seed"), oracle("same-seed"))

    def test_guardian_rejects_incomplete_package(self):
        score, reasons = guardian({"character": "unknown", "scenes": []})
        self.assertLess(score, 80)
        self.assertIn("invalid_story_structure", reasons)

    def test_pipeline_approves_and_persists_valid_package(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "legion.sqlite3"
            result = run_pipeline("test-seed", database)
            self.assertEqual(result.status, "APPROVED")
            with sqlite3.connect(database) as connection:
                row = connection.execute(
                    "SELECT status, qa_score FROM content WHERE content_id = ?",
                    (result.content_id,),
                ).fetchone()
            self.assertEqual(row, ("APPROVED", 100))


if __name__ == "__main__":
    unittest.main()
