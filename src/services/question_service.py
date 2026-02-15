from pathlib import Path
from typing import Any, Dict, List

from src.core.data_manager import DataManager


class QuestionService:
    def __init__(self, exam_type: str):
        self.exam_type = exam_type
        self.base_path = Path(f"data/input/questions/{self.exam_type}")

    def get_available_years(self) -> List[int]:
        if not self.base_path.exists():
            return []

        years: List[int] = []
        for entry in self.base_path.iterdir():
            if entry.is_dir() and entry.name.isdigit():
                years.append(int(entry.name))
        return sorted(years)

    def get_subjects_by_year(self, year: int) -> List[str]:
        year_path = self.base_path / str(year)
        if not year_path.exists():
            return []

        return sorted([file.stem for file in year_path.glob("*.json")])

    def get_questions_by_year(self, year: int, subject: str) -> Dict[str, Any]:
        file_path = self.base_path / str(year) / f"{subject}.json"
        return DataManager.read_json(str(file_path))
