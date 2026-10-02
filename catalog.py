"""Карточка товара."""
import os
import tkinter as tk
from PIL import Image, ImageTk
from config import FONT_FAMILY, COLOR_BG, COLOR_HIGHLIGHT


# Список для хранения ссылок на картинки (иначе Python их удалит)
_photos = []


def create_product_card(parent, product):
    """
    Создаёт карточку одного товара.

    :param parent: родительский виджет (куда положить карточку)
    :param product: объект Product
    """
    # Если товара мало — используем подсветку
    bg_color = COLOR_HIGHLIGHT if product.quantity <= 3 else COLOR_BG

    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    # --- Картинка с защитой от отсутствия файла ---
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    # Определяем путь к картинке
    image_path = f"images/{product.image}" if product.image else "resources/picture.png"
    if not os.path.exists(image_path):
        image_path = "resources/picture.png"

    try:
        img = Image.open(image_path)
        img.thumbnail((120, 120))          # сохраняем пропорции
        photo = ImageTk.PhotoImage(img)
        _photos.append(photo)               # сохраняем ссылку
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo             # type: ignore
        img_label.pack()
    except Exception:
        tk.Label(img_frame, text="[нет фото]", bg=bg_color,
                 font=(FONT_FAMILY, 10), width=12, height=6).pack()

    # --- Тексты ---
    info = tk.Frame(card, bg=bg_color)
    info.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    tk.Label(info, text=product.name, bg=bg_color,
             font=(FONT_FAMILY, 14, "bold")).pack(anchor="w")

    tk.Label(info, text=f"Категория: {product.category}", bg=bg_color,
             font=(FONT_FAMILY, 11)).pack(anchor="w")
    tk.Label(info, text=f"Количество: {product.quantity} ({product.indicator()})",
             bg=bg_color, font=(FONT_FAMILY, 11)).pack(anchor="w")
    
    tk.Label(info, text=f"Материал: {product.material}", bg=bg_color,
             font=(FONT_FAMILY, 11)).pack(anchor="w")
    # --- Цена справа ---
    price_frame = tk.Frame(card, bg=bg_color)
    price_frame.pack(side="right", padx=15, pady=10)

    tk.Label(price_frame,
             text=f"{product.price_with_discount_auto():.2f} руб.",
             bg=bg_color, font=(FONT_FAMILY, 14, "bold")).pack(anchor="e")

    return card