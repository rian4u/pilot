from src.services.question_service import QuestionService

if __name__ == "__main__":
    print("[INFO] 기출문제 서비스 테스트 시작...")
    
    # 1. 서비스 초기화 (세무사 시험용)
    service = QuestionService("세무사")
    
    # 2. 2024년 회계학 문제 불러오기
    questions = service.get_questions_by_year(2024, "회계학")
    
    # 3. 결과 확인
    if questions:
        print(f"[SUCCESS] 데이터를 찾았습니다: {questions['exam_metadata']}")
        print(f"첫 번째 문제: {questions['questions'][0]['question']}")
    else:
        print("[FAIL] 데이터를 불러오지 못했습니다. 경로를 확인하세요.")