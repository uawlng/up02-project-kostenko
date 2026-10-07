"""Главное окно с каталогом."""
import os
import tkinter as tk
from tkinter import ttk
from styles import COLOR_SECONDARY_BG, COLOR_ACCENT, FONT_FAMILY, FONT_SIZE_TITLE, FONT_SIZE_NORMAL, font
from config import APP_TITLE
import db_products as db
from catalog import create_product_card
from error_handler import safe_call
from resources import load_image_proportional, PATH_ICON, PATH_LOGO


class CatalogWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("900x700")

        self.set_icon()
        self.build_ui()
        self.load_products()

    def set_icon(self):
        """Устанавливает иконку приложения (кроссплатформенно)."""
        try:
            if os.name == "nt":
                self.root.iconbitmap(PATH_ICON)
            else:
                icon_img = load_image_proportional(
                    PATH_ICON.replace(".ico", ".png"),
                    max_size=(32, 32)
                )
                if icon_img:
                    self.root.iconphoto(True, icon_img)
        except Exception as e:
            print(f"Не удалось установить иконку: {e}")

    def build_ui(self):
        header = tk.Frame(self.root, bg=COLOR_SECONDARY_BG, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        logo = load_image_proportional(PATH_LOGO, max_size=(60, 60))
        if logo:
            logo_label = tk.Label(header, image=logo, bg=COLOR_SECONDARY_BG)
            logo_label.image = logo # type: ignore
            logo_label.pack(side="left", padx=15)
        else:
            tk.Label(header, text="[ЛОГОТИП]",
                     bg=COLOR_SECONDARY_BG).pack(side="left", padx=15)

        tk.Label(header, text="КАТАЛОГ ТОВАРОВ",
                 font=(FONT_FAMILY, 16, "bold"),
                 bg=COLOR_SECONDARY_BG).pack(expand=True)

        tk.Button(header, text="Заказы", command=self.open_orders,
          bg=COLOR_ACCENT, fg="white",
          font=font(FONT_SIZE_NORMAL),
          padx=10, pady=5).pack(side="right", padx=10)


        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical",
                                  command=self.canvas.yview)
        self.catalog_frame = tk.Frame(self.canvas, bg="white")
        self.catalog_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.catalog_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


    def open_orders(self):
        """Открывает окно списка заказов."""
        from orders_window import OrdersWindow
        OrdersWindow(self.root)


    def load_products(self):
        products = db.get_all_products()
        for p in products:
            create_product_card(self.catalog_frame, p, self.refresh_catalog)

    def refresh_catalog(self):
        """Очищает каталог и загружает заново."""
        for widget in self.catalog_frame.winfo_children():
            widget.destroy()
        self.load_products()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    CatalogWindow().run()