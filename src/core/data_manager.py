import json
import os
from typing import Any, Dict

class DataManager:
    @staticmethod
    def read_json(file_path: str) -> Dict[str, Any]:
        """JSON 파일을 읽어서 딕셔너리로 반환합니다."""
        if not os.path.exists(file_path):
            return {}
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_json(file_path: str, data: Dict[str, Any]):
        """딕셔너리 데이터를 JSON 파일로 저장합니다."""
        # 폴더가 없으면 생성
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)