def calculate_tiered_bills(tiers, consumers, service_name="Услуга", unit="ед.", currency="руб."):
    details = []
    total_volume = 0.0
    total_cost = 0.0

    for consumer in consumers:
        vol = float(consumer.get("volume", 0.0))
        rem = vol
        c_cost = 0.0
        prev_limit = 0.0
        breakdown = []

        for tier in tiers:
            limit = tier.get("limit")
            rate = float(tier["rate"])

            if limit is not None:
                cap = max(0.0, float(limit) - prev_limit)
                prev_limit = float(limit)
            else:
                cap = rem

            used = min(rem, cap)
            cost = round(used * rate, 2)

            rem = max(0.0, rem - used)
            c_cost = round(c_cost + cost, 2)

            breakdown.append({
                "tier_id": tier.get("id"),
                "tier_name": tier.get("name"),
                "volume": round(used, 2),
                "rate": rate,
                "cost": cost
            })

        total_volume = round(total_volume + vol, 2)
        total_cost = round(total_cost + c_cost, 2)

        details.append({
            "consumer_id": str(consumer.get("id")),
            "name": consumer.get("name", ""),
            "volume": round(vol, 2),
            "total_cost": c_cost,
            "tier_breakdown": breakdown
        })

    return {
        "service_name": service_name,
        "unit": unit,
        "currency": currency,
        "total_consumers": len(consumers),
        "total_volume": total_volume,
        "total_cost": total_cost,
        "details": details
    }
