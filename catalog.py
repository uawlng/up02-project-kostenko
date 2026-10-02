"""Карточка товара."""
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from styles import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT,
    FONT_FAMILY, FONT_SIZE_NORMAL, FONT_SIZE_HEADER,
    font
)


_photos = []   # храним ссылки на картинки


def create_product_card(parent, product):
    """Создаёт карточку одного товара."""
    bg_color = COLOR_HIGHLIGHT if product.quantity <= 3 else COLOR_MAIN_BG

    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=(5, 0))

    # --- Картинка (слева) ---
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    # Проверяем: есть ли у товара фото и существует ли файл
    image_path = f"images/{product.image}" if product.image else "resources/picture.png"
    if not os.path.exists(image_path):
        image_path = "resources/picture.png"

    try:
        img = Image.open(image_path)
        img.thumbnail((100, 100))          # сохраняем пропорции
        photo = ImageTk.PhotoImage(img)
        _photos.append(photo)               # сохраняем ссылку
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo             # type: ignore
        img_label.pack()
    except Exception:
        placeholder = tk.Frame(img_frame, bg="#E0E0E0", width=100, height=100)
        placeholder.pack_propagate(False)
        placeholder.pack()
        tk.Label(placeholder, text="📷", bg="#E0E0E0",
                 font=("Arial", 24)).pack(expand=True)

        tk.Label(placeholder, text="Нет фото", bg="#E0E0E0",
                 font=(FONT_FAMILY, FONT_SIZE_NORMAL),
                 fg="#666666").pack()

    # --- Цена (справа) ---
    price_frame = tk.Frame(card, bg=bg_color)
    price_frame.pack(side="right", padx=15, pady=10)

    tk.Label(price_frame,
             text=f"{product.price_with_discount_auto():.2f} руб.",
             bg=bg_color, font=(FONT_FAMILY, 14, "bold")).pack(anchor="e")

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

    # --- Разделитель снизу ---
    separator = ttk.Separator(parent, orient="horizontal")
    separator.pack(fill="x", padx=10, pady=(0, 5))

    return card