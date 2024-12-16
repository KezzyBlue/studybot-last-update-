import json
import os

def load_data(file_path, default=None):
    """Load dữ liệu từ file JSON."""
    if not os.path.exists(file_path):
        return default
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def save_data(file_path, data):
    """Lưu dữ liệu vào file JSON."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)