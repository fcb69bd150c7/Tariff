import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from validator import validate_input_data
from calculator import calculate_tiered_bills
from storage import load_data

def run_all_tests():
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    test_cases = [
        {
            "id": 1,
            "name": "Обычный случай",
            "file": "input_standard.json",
            "expected_type": "valid",
            "check": lambda res: (
                res["total_consumers"] == 4 and
                res["total_volume"] == 775.0 and
                res["total_cost"] == 2250.0 and
                res["details"][0]["total_cost"] == 350.0 and
                res["details"][1]["total_cost"] == 200.0
            )
        },
        {
            "id": 2,
            "name": "Пустая коллекция",
            "file": "input_empty.json",
            "expected_type": "valid",
            "check": lambda res: (
                res["total_consumers"] == 0 and
                res["total_volume"] == 0.0 and
                res["total_cost"] == 0.0 and
                len(res["details"]) == 0
            )
        },
        {
            "id": 3,
            "name": "Одна запись",
            "file": "input_single.json",
            "expected_type": "valid",
            "check": lambda res: (
                res["total_consumers"] == 1 and
                res["total_volume"] == 60.0 and
                res["total_cost"] == 120.0 and
                res["details"][0]["tier_breakdown"][0]["volume"] == 60.0 and
                res["details"][0]["tier_breakdown"][1]["volume"] == 0.0
            )
        },
        {
            "id": 4,
            "name": "Точная граница правила",
            "file": "input_boundary.json",
            "expected_type": "valid",
            "check": lambda res: (
                res["details"][0]["volume"] == 100.0 and
                res["details"][0]["total_cost"] == 200.0 and
                res["details"][0]["tier_breakdown"][1]["volume"] == 0.0 and
                res["details"][1]["volume"] == 300.0 and
                res["details"][1]["total_cost"] == 800.0 and
                res["details"][1]["tier_breakdown"][2]["volume"] == 0.0
            )
        },
        {
            "id": 5,
            "name": "Неверное значение (отрицательный объем)",
            "file": "input_invalid.json",
            "expected_type": "invalid",
            "check": lambda err: "не может быть отрицательным" in err
        },
        {
            "id": 6,
            "name": "Сложный случай (0, дробь, крупное)",
            "file": "input_complex.json",
            "expected_type": "valid",
            "check": lambda res: (
                res["details"][0]["volume"] == 0.0 and res["details"][0]["total_cost"] == 0.0 and
                res["details"][1]["volume"] == 125.5 and res["details"][1]["total_cost"] == 276.5 and
                res["details"][2]["volume"] == 1000.0 and res["details"][2]["total_cost"] == 4300.0 and
                res["total_cost"] == 4576.5
            )
        }
    ]

    print("\n" + "-" * 65)
    print("Проверка 6 обязательных сценариев:")
    print("-" * 65)

    all_passed = True
    for tc in test_cases:
        fpath = os.path.join(data_dir, tc["file"])
        data, err = load_data(fpath)
        passed = False

        if not err:
            is_valid, val_err = validate_input_data(data)
            if tc["expected_type"] == "invalid":
                if not is_valid and tc["check"](val_err):
                    passed = True
            elif tc["expected_type"] == "valid":
                if is_valid:
                    report = calculate_tiered_bills(
                        data["tiers"],
                        data["consumers"],
                        data.get("service_name", ""),
                        data.get("unit", ""),
                        data.get("currency", "")
                    )
                    passed = tc["check"](report)

        status_str = "OK" if passed else "FAIL"
        if not passed:
            all_passed = False
        print(f"Тест {tc['id']}: {tc['name']:<42} -> {status_str}")

    print("-" * 65)
    if all_passed:
        print("Все тесты пройдены успешно.\n")
        return 0
    else:
        print("Есть ошибки в тестах!\n")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
