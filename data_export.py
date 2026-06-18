import json
from database import DeliveryDB


def export_orders_to_json(filepath="data/orders_backup.json"):
    db = DeliveryDB()
    orders = db.get_orders()

    orders_list = []
    for o in orders:
        orders_list.append({
            "id": o[0],
            "customer_id": o[1],
            "order_date": o[2],
            "status": o[3],
            "total": o[4]
        })

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(orders_list, f, ensure_ascii=False, indent=4)
    print(f"Успешно экспортировано в {filepath}")