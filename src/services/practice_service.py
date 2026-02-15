from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Any

from src.core.data_manager import DataManager
from src.services.question_service import QuestionService


IMPORTANCE_ORDER = {
    "LOW": 1,
    "MEDIUM": 2,
    "HIGH": 3,
}


@dataclass
class GradingResult:
    user_id: str
    exam_type: str
    year: int
    subject: str
    total_questions: int
    correct_count: int
    score_percent: float
    details: List[Dict[str, Any]]


class PracticeService:
    def __init__(self, exam_type: str):
        self.exam_type = exam_type
        self.question_service = QuestionService(exam_type)

    def grade_submission(
        self,
        user_id: str,
        year: int,
        subject: str,
        submitted_answers: Dict[str, int],
    ) -> GradingResult:
        question_set = self.question_service.get_questions_by_year(year, subject)
        questions = question_set.get("questions", [])

        details: List[Dict[str, Any]] = []
        correct_count = 0

        for item in questions:
            question_id = item["id"]
            correct_answer = item["answer"]
            submitted_answer = submitted_answers.get(question_id)
            is_correct = submitted_answer == correct_answer

            if is_correct:
                correct_count += 1

            details.append(
                {
                    "question_id": question_id,
                    "concept_id": item.get("concept_id"),
                    "submitted_answer": submitted_answer,
                    "correct_answer": correct_answer,
                    "is_correct": is_correct,
                }
            )

        total_questions = len(questions)
        score_percent = (correct_count / total_questions * 100) if total_questions else 0.0

        result = GradingResult(
            user_id=user_id,
            exam_type=self.exam_type,
            year=year,
            subject=subject,
            total_questions=total_questions,
            correct_count=correct_count,
            score_percent=round(score_percent, 2),
            details=details,
        )

        self._save_attempt(result)
        self._update_wrong_note(user_id, year, subject, details)
        return result

    def get_wrong_notes(self, user_id: str, minimum_importance: str = "LOW") -> List[Dict[str, Any]]:
        file_path = self._wrong_note_path(user_id)
        payload = DataManager.read_json(file_path)
        notes = payload.get("wrong_notes", [])
        minimum_level = IMPORTANCE_ORDER[minimum_importance]

        return [
            note
            for note in notes
            if IMPORTANCE_ORDER.get(note.get("importance", "LOW"), 1) >= minimum_level
        ]

    def _save_attempt(self, result: GradingResult):
        file_path = self._history_path(result.user_id)
        payload = DataManager.read_json(file_path)
        attempts = payload.get("attempts", [])
        attempts.append(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "exam_type": result.exam_type,
                "year": result.year,
                "subject": result.subject,
                "total_questions": result.total_questions,
                "correct_count": result.correct_count,
                "score_percent": result.score_percent,
            }
        )
        DataManager.save_json(file_path, {"attempts": attempts})

    def _update_wrong_note(
        self,
        user_id: str,
        year: int,
        subject: str,
        details: List[Dict[str, Any]],
    ):
        file_path = self._wrong_note_path(user_id)
        payload = DataManager.read_json(file_path)
        notes_by_question = {note["question_id"]: note for note in payload.get("wrong_notes", [])}

        for item in details:
            question_id = item["question_id"]
            if question_id not in notes_by_question:
                notes_by_question[question_id] = {
                    "question_id": question_id,
                    "concept_id": item.get("concept_id"),
                    "year": year,
                    "subject": subject,
                    "wrong_count": 0,
                    "last_submitted_answer": None,
                    "last_correct_answer": item["correct_answer"],
                    "last_result": "UNSEEN",
                    "importance": "LOW",
                    "updated_at": datetime.utcnow().isoformat(),
                }

            note = notes_by_question[question_id]
            note["last_submitted_answer"] = item["submitted_answer"]
            note["last_correct_answer"] = item["correct_answer"]
            note["last_result"] = "CORRECT" if item["is_correct"] else "WRONG"
            note["updated_at"] = datetime.utcnow().isoformat()

            if item["is_correct"]:
                note["wrong_count"] = max(note["wrong_count"] - 1, 0)
            else:
                note["wrong_count"] += 1

            note["importance"] = self._importance_from_wrong_count(note["wrong_count"])

        DataManager.save_json(file_path, {"wrong_notes": list(notes_by_question.values())})

    @staticmethod
    def _importance_from_wrong_count(wrong_count: int) -> str:
        if wrong_count >= 3:
            return "HIGH"
        if wrong_count >= 1:
            return "MEDIUM"
        return "LOW"

    def _history_path(self, user_id: str) -> str:
        return f"data/output/users/{user_id}/history.json"

    def _wrong_note_path(self, user_id: str) -> str:
        return f"data/output/users/{user_id}/wrong_notes.json"
