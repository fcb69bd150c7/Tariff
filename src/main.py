import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from validator import validate_input_data
from calculator import calculate_tiered_bills
from storage import load_data, save_report

def format_console_output(report, tiers):
    unit = report.get("unit", "ед.")
    curr = report.get("currency", "руб.")
    service = report.get("service_name", "Услуга")

    print("\n" + "=" * 70)
    print(f"Отчет по начислениям: {service}")
    print("=" * 70)

    print("\nТарифная сетка:")
    prev_limit = 0.0
    for t in tiers:
        lim = t.get("limit")
        rate = t.get("rate")
        t_name = t.get("name")
        if lim is not None:
            print(f"  - Ступень {t.get('id')} ({t_name}): от {prev_limit} до {lim} {unit} - {rate:.2f} {curr}/{unit}")
            prev_limit = float(lim)
        else:
            print(f"  - Ступень {t.get('id')} ({t_name}): свыше {prev_limit} {unit} - {rate:.2f} {curr}/{unit}")

    print("\nДетализация начислений:")
    print("-" * 70)
    print(f"{'ID':<8} | {'Потребитель':<18} | {'Объем':<10} | {'По ступеням':<16} | {'Итог (' + curr + ')':>8}")
    print("-" * 70)

    if not report["details"]:
        print("  [Список потребителей пуст]")

    for d in report["details"]:
        cid = d["consumer_id"]
        cname = (d["name"][:16] + "..") if len(d["name"]) > 18 else d["name"]
        vol_str = f"{d['volume']:.1f} {unit}"
        tot_str = f"{d['total_cost']:.2f}"

        parts = []
        for b in d["tier_breakdown"]:
            if b["volume"] > 0:
                parts.append(f"{b['volume']:.0f}*{b['rate']:.1f}")
        parts_str = " + ".join(parts) if parts else "0"

        print(f"{cid:<8} | {cname:<18} | {vol_str:<10} | {parts_str:<16} | {tot_str:>8}")

    print("-" * 70)
    print(f"Итого абонентов: {report['total_consumers']} | "
          f"Общий объем: {report['total_volume']:.1f} {unit} | "
          f"К оплате: {report['total_cost']:.2f} {curr}")
    print("=" * 70 + "\n")


def main():
    default_input = os.path.join("data", "input_standard.json")
    default_output = os.path.join("data", "output_report.json")

    input_file = sys.argv[1] if len(sys.argv) > 1 else default_input
    output_file = sys.argv[2] if len(sys.argv) > 2 else default_output

    data, err = load_data(input_file)
    if err:
        print(f"Ошибка входа: {err}", file=sys.stderr)
        sys.exit(1)

    is_valid, val_err = validate_input_data(data)
    if not is_valid:
        print(f"Ошибка валидации: {val_err}", file=sys.stderr)
        sys.exit(2)

    service_name = data.get("service_name", "Коммунальная услуга")
    unit = data.get("unit", "ед.")
    currency = data.get("currency", "руб.")
    tiers = data["tiers"]
    consumers = data["consumers"]

    report = calculate_tiered_bills(tiers, consumers, service_name, unit, currency)

    format_console_output(report, tiers)

    success, save_err = save_report(report, output_file)
    if not success:
        print(f"Ошибка сохранения: {save_err}", file=sys.stderr)
        sys.exit(3)

    print(f"Результат сохранен в: '{output_file}'")
    sys.exit(0)


if __name__ == "__main__":
    main()
