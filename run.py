from src.services.practice_service import PracticeService
from src.services.question_service import QuestionService


if __name__ == "__main__":
    user_id = "demo_user"
    exam_type = "세무사"

    question_service = QuestionService(exam_type)
    practice_service = PracticeService(exam_type)

    years = question_service.get_available_years()
    print(f"[INFO] 이용 가능한 연도: {years}")

    if not years:
        print("[FAIL] 기출 데이터가 없습니다.")
        raise SystemExit(1)

    selected_year = years[-1]
    subjects = question_service.get_subjects_by_year(selected_year)
    print(f"[INFO] {selected_year}년 과목 목록: {subjects}")

    if not subjects:
        print("[FAIL] 해당 연도 과목 데이터가 없습니다.")
        raise SystemExit(1)

    selected_subject = subjects[0]
    question_set = question_service.get_questions_by_year(selected_year, selected_subject)
    first_question = question_set["questions"][0]

    submitted_answers = {
        first_question["id"]: 3,
    }

    result = practice_service.grade_submission(
        user_id=user_id,
        year=selected_year,
        subject=selected_subject,
        submitted_answers=submitted_answers,
    )

    print(
        f"[RESULT] {result.subject} 점수: {result.correct_count}/{result.total_questions}"
        f" ({result.score_percent}%)"
    )
    print("[INFO] 중요도 MEDIUM 이상 오답노트")
    for note in practice_service.get_wrong_notes(user_id, minimum_importance="MEDIUM"):
        print(
            f"- {note['question_id']} | wrong_count={note['wrong_count']} | importance={note['importance']}"
        )
