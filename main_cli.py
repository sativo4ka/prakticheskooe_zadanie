import argparse
from database import DeliveryDB
from data_export import export_orders_to_json


def main():
    parser = argparse.ArgumentParser(description="Система доставки CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    report_parser = subparsers.add_parser("report")

    export_parser = subparsers.add_parser("export")
    export_parser.add_argument("--file", required=True)

    args = parser.parse_args()
    db = DeliveryDB()

    if args.command == "report":
        rev = db.get_revenue_by_period()
        print(f"Общая выручка (выполненные заказы): {rev} руб.")
    elif args.command == "export":
        export_orders_to_json(args.file)


if __name__ == "__main__":
    main()