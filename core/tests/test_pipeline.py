import sqlite3
import tempfile
import unittest
from pathlib import Path

from legion_x.pipeline import guardian, guardian_media, oracle, run_pipeline


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

    def test_guardian_media_rejects_the_old_static_silent_pilot(self):
        review = guardian_media(
            {
                "has_real_motion": False,
                "has_voiceover": False,
                "has_licensed_music_or_sfx": False,
                "has_first_two_second_pattern_break": False,
                "has_subtitles": True,
                "is_1080x1920": True,
                "has_provider_watermark": False,
                "average_shot_length_seconds": 4,
                "distinct_visual_beats": 5,
            }
        )
        self.assertEqual(review.decision, "REJECTED")
        self.assertIn("static_or_insufficient_motion", review.reasons)
        self.assertIn("missing_voiceover", review.reasons)

    def test_guardian_media_rejects_provider_watermark_even_with_motion(self):
        review = guardian_media(
            {
                "has_real_motion": True,
                "has_voiceover": True,
                "has_licensed_music_or_sfx": True,
                "has_first_two_second_pattern_break": True,
                "has_subtitles": True,
                "is_1080x1920": True,
                "has_provider_watermark": True,
                "average_shot_length_seconds": 1.5,
                "distinct_visual_beats": 12,
            }
        )
        self.assertEqual(review.decision, "REJECTED")
        self.assertIn("provider_watermark", review.reasons)


if __name__ == "__main__":
    unittest.main()
