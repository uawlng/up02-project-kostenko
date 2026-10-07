"""Главное окно приложения с авторизацией."""
import tkinter as tk
from tkinter import ttk

from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
from config import APP_TITLE
from resources import load_image_proportional, PATH_LOGO

import db_products as db          # товары берём отсюда
from catalog import create_product_card


class MainWindow:
    """Главное окно приложения."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("900x700")
        self.root.configure(bg=COLOR_MAIN_BG)

        self.current_user = None
        self.user_label = None

        self.build_ui()
        self.load_products()
        self.require_auth()

    # ---------- Интерфейс ----------

    def build_ui(self):
        """Строит интерфейс окна."""
        # Шапка
        header = tk.Frame(self.root, bg=COLOR_SECONDARY_BG, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Логотип (если есть)
        logo = load_image_proportional(PATH_LOGO, max_size=(60, 60))
        if logo:
            logo_label = tk.Label(header, image=logo, bg=COLOR_SECONDARY_BG)
            logo_label.image = logo  # сохраняем ссылку, иначе исчезнет
            logo_label.pack(side="left", padx=15)

        # Заголовок
        tk.Label(
            header, text="КАТАЛОГ ТОВАРОВ",
            font=font(FONT_SIZE_TITLE, bold=True),
            bg=COLOR_SECONDARY_BG, fg="white"
        ).pack(side="left", expand=True)

        # ФИО пользователя (правый верхний угол)
        self.user_label = tk.Label(
            header, text="Не авторизован",
            font=font(FONT_SIZE_NORMAL),
            bg=COLOR_SECONDARY_BG, fg="white"
        )
        self.user_label.pack(side="right", padx=15)

        # Область с прокруткой
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical",
                                  command=self.canvas.yview)
        self.catalog_frame = tk.Frame(self.canvas, bg="white")
        self.catalog_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.catalog_frame,
                                  anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ---------- Авторизация ----------

    def require_auth(self):
        """Запрашивает авторизацию через отдельное окно."""
        from auth import AuthWindow
        AuthWindow(self.root, self.on_auth_success)

    def on_auth_success(self, user):
        """
        Обработчик успешной авторизации.
        :param user: кортеж (id, фамилия, имя, отчество, логин, роль)
        """
        self.current_user = user

        # ФИО + роль в шапке
        fio = f"{user[1]} {user[2]} {user[3] or ''}".strip()
        self.user_label.config(text=f"{fio} ({user[5]})")

        # Кнопки в зависимости от роли
        self.add_role_buttons(user[5])

    def add_role_buttons(self, role):
        """Добавляет кнопки в зависимости от роли."""
        header = self.user_label.master

        if role in ("Менеджер", "Администратор"):
            tk.Button(
                header, text="Заказы",
                command=self.open_orders,
                bg=COLOR_ACCENT, fg="white",
                font=font(FONT_SIZE_NORMAL),
                padx=10, pady=5
            ).pack(side="right", padx=10)

        if role == "Администратор":
            tk.Button(
                header, text="Админ-панель",
                command=self.open_admin,
                bg=COLOR_ACCENT, fg="white",
                font=font(FONT_SIZE_NORMAL),
                padx=10, pady=5
            ).pack(side="right", padx=10)

    # ---------- Действия ----------

    def open_orders(self):
        """Открывает окно списка заказов."""
        from orders_window import OrdersWindow
        OrdersWindow(self.root, self.current_user)

    def open_admin(self):
        """Открывает админ-панель."""
        from admin_panel import AdminPanel
        AdminPanel(self.root, self.current_user)

    # ---------- Каталог ----------

    def load_products(self):
        """Загружает товары в каталог."""
        products = db.get_all_products()
        for p in products:
            create_product_card(self.catalog_frame, p,
                                refresh=self.refresh_catalog)

    def refresh_catalog(self):
        """Обновляет каталог."""
        for widget in self.catalog_frame.winfo_children():
            widget.destroy()
        self.load_products()

    # ---------- Запуск ----------

    def run(self):
        """Запускает приложение."""
        self.root.mainloop()


if __name__ == "__main__":
    MainWindow().run()