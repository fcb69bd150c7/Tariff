import json
import os

def load_data(file_path):
    if not os.path.exists(file_path):
        return None, f"Входной файл не найден: '{file_path}'"

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data, None
    except json.JSONDecodeError as e:
        return None, f"Ошибка синтаксиса JSON в файле '{file_path}': строка {e.lineno}, колонка {e.colno} ({e.msg})"
    except Exception as e:
        return None, f"Не удалось прочитать файл '{file_path}': {str(e)}"


def save_report(report_data, file_path):
    try:
        dir_name = os.path.dirname(file_path)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        return True, None
    except Exception as e:
        return False, f"Не удалось сохранить отчёт в '{file_path}': {str(e)}"
