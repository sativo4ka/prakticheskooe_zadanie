import tkinter as tk
from tkinter import messagebox
from database import DeliveryDB


class DeliveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Быстрая доставка — Учёт")
        self.root.geometry("400x300")

        self.db = DeliveryDB()

        self.btn_report = tk.Button(root, text="Показать отчёт по выручке", command=self.show_report)
        self.btn_report.pack(pady=20)

        self.label = tk.Label(root, text="Список заказов (ID | Клиент ID | Дата | Статус | Сумма):")
        self.label.pack()

        self.text_area = tk.Text(root, height=10, width=45)
        self.text_area.pack(pady=10)

        self.refresh_orders()

    def refresh_orders(self):
        self.text_area.delete("1.0", tk.END)
        orders = self.db.get_orders()
        for o in orders:
            self.text_area.insert(tk.END, f"{o[0]} | {o[1]} | {o[2]} | {o[3]} | {o[4]} руб.\n")

    def show_report(self):
        rev = self.db.get_revenue_by_period()
        messagebox.showinfo("Отчёт", f"Общая выручка за всё время:\n{rev} руб.")


if __name__ == "__main__":
    root = tk.Tk()
    app = DeliveryApp(root)
    root.mainloop()