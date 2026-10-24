def validate_input_data(data):
    if not isinstance(data, dict):
        return False, "Входные данные должны быть JSON-объектом."

    if "tiers" not in data or not isinstance(data["tiers"], list):
        return False, "Отсутствует список ступеней тарифа 'tiers'."

    tiers = data["tiers"]
    if len(tiers) == 0:
        return False, "Список ступеней тарифа 'tiers' не может быть пустым."

    prev_limit = 0.0
    for idx, tier in enumerate(tiers):
        if not isinstance(tier, dict):
            return False, f"Ступень #{idx + 1} должна быть объектом."

        if "id" not in tier or "name" not in tier or "rate" not in tier:
            return False, f"Ступень #{idx + 1} должна содержать id, name и rate."

        rate = tier["rate"]
        if not isinstance(rate, (int, float)) or rate <= 0:
            return False, f"Тариф ступени #{tier.get('id', idx+1)} должен быть больше 0."

        limit = tier.get("limit")
        is_last = (idx == len(tiers) - 1)

        if limit is None:
            if not is_last:
                return False, f"Только последняя ступень может быть без лимита (null)."
        else:
            if not isinstance(limit, (int, float)) or limit <= 0:
                return False, f"Лимит ступени #{tier.get('id')} должен быть больше 0."
            if limit <= prev_limit:
                return False, f"Лимит ступени #{tier.get('id')} ({limit}) должен быть больше предыдущего ({prev_limit})."
            prev_limit = float(limit)

    if "consumers" not in data or not isinstance(data["consumers"], list):
        return False, "Отсутствует список потребителей 'consumers'."

    consumers = data["consumers"]
    if len(consumers) > 100:
        return False, f"Количество потребителей ({len(consumers)}) больше 100."

    seen_ids = set()
    for idx, c in enumerate(consumers):
        if not isinstance(c, dict):
            return False, f"Запись потребителя #{idx + 1} должна быть объектом."

        cid = c.get("id")
        if cid is None or str(cid).strip() == "":
            return False, f"У потребителя #{idx + 1} отсутствует id."

        str_cid = str(cid)
        if str_cid in seen_ids:
            return False, f"Дубликат id потребителя: '{str_cid}'."
        seen_ids.add(str_cid)

        volume = c.get("volume")
        if volume is None or not isinstance(volume, (int, float)):
            return False, f"У потребителя '{str_cid}' volume должен быть числом."
        if volume < 0:
            return False, f"У потребителя '{str_cid}' объём потребления не может быть отрицательным ({volume})."

    return True, None
