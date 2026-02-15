from src.core.data_manager import DataManager
import os

class QuestionService:
    def __init__(self, exam_type: str):
        self.exam_type = exam_type
        # 규약 준수: 모든 입력 데이터는 data/input에서 시작
        self.base_path = f"data/input/questions/{self.exam_type}"

    # src/services/question_service.py 내 함수 수정
    def get_questions_by_year(self, year: int, subject: str):
        file_path = f"{self.base_path}/{year}/{subject}.json"
        return DataManager.read_json(file_path)