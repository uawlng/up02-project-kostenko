"""Окно списка заказов с проверкой прав доступа."""
import tkinter as tk
from tkinter import ttk, messagebox

from styles import (
    COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)


class OrdersWindow:
    ALLOWED_ROLES = ("Менеджер", "Администратор")

    def __init__(self, parent, current_user=None):
        self.current_user = current_user

        if not self._check_access():
            return

        self.win = tk.Toplevel(parent)
        self.win.title("Заказы")
        self.win.geometry("800x500")
        self.win.configure(bg="white")

        header = tk.Frame(self.win, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="СПИСОК ЗАКАЗОВ",
            font=font(FONT_SIZE_TITLE, bold=True),
            bg=COLOR_SECONDARY_BG, fg="white"
        ).pack(side="left", padx=15, pady=15)

        if current_user:
            fio = f"{current_user[1]} {current_user[2]}"
            tk.Label(
                header, text=f"{fio} ({current_user[5]})",
                font=font(FONT_SIZE_NORMAL),
                bg=COLOR_SECONDARY_BG, fg="white"
            ).pack(side="right", padx=15)

        self.build_table()
        self.load_orders()

    def _check_access(self):
        if self.current_user is None:
            messagebox.showwarning("Доступ запрещён", "Необходимо авторизоваться.")
            return False

        role = self.current_user[5]
        if role not in self.ALLOWED_ROLES:
            messagebox.showerror(
                "Доступ запрещён",
                f"Роль «{role}» не имеет доступа к заказам.\n"
                f"Разрешено: {', '.join(self.ALLOWED_ROLES)}."
            )
            return False

        return True

    def build_table(self):
        columns = ("id", "дата", "клиент", "сумма")
        self.tree = ttk.Treeview(self.win, columns=columns, show="headings")

        self.tree.heading("id", text="№")
        self.tree.heading("дата", text="Дата")
        self.tree.heading("клиент", text="Клиент")
        self.tree.heading("сумма", text="Сумма")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("дата", width=150, anchor="center")
        self.tree.column("клиент", width=250)
        self.tree.column("сумма", width=120, anchor="e")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load_orders(self):
        try:
            import database as db
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute("""
                SELECT Заказ.id, Заказ.дата, Заказ.клиент,
                       IFNULL(SUM(Состав_заказа.количество *
                                  Состав_заказа.цена), 0)
                FROM Заказ
                LEFT JOIN Состав_заказа
                       ON Заказ.id = Состав_заказа.заказ_id
                GROUP BY Заказ.id
                ORDER BY Заказ.id
            """)
            rows = cur.fetchall()
            conn.close()

            for row in rows:
                self.tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Ошибка БД", str(e))


