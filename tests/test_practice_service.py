import shutil
import unittest
from pathlib import Path

from src.services.practice_service import PracticeService
from src.services.question_service import QuestionService


class PracticeServiceTest(unittest.TestCase):
    def setUp(self):
        self.user_id = "unit_test_user"
        self.user_dir = Path("data/output/users") / self.user_id
        if self.user_dir.exists():
            shutil.rmtree(self.user_dir)

        self.question_service = QuestionService("세무사")
        self.practice_service = PracticeService("세무사")

    def tearDown(self):
        if self.user_dir.exists():
            shutil.rmtree(self.user_dir)

    def test_question_indexing(self):
        years = self.question_service.get_available_years()
        self.assertIn(2024, years)

        subjects = self.question_service.get_subjects_by_year(2024)
        self.assertIn("회계학", subjects)

    def test_grading_and_wrong_note_importance(self):
        question_set = self.question_service.get_questions_by_year(2024, "회계학")
        qid = question_set["questions"][0]["id"]

        for _ in range(3):
            self.practice_service.grade_submission(
                user_id=self.user_id,
                year=2024,
                subject="회계학",
                submitted_answers={qid: 3},
            )

        notes = self.practice_service.get_wrong_notes(self.user_id, minimum_importance="HIGH")
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["importance"], "HIGH")

        self.practice_service.grade_submission(
            user_id=self.user_id,
            year=2024,
            subject="회계학",
            submitted_answers={qid: 1},
        )

        medium_notes = self.practice_service.get_wrong_notes(self.user_id, minimum_importance="MEDIUM")
        self.assertEqual(len(medium_notes), 1)
        self.assertEqual(medium_notes[0]["importance"], "MEDIUM")


if __name__ == "__main__":
    unittest.main()
