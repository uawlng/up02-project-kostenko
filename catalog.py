"""Карточка товара."""
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from styles import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT,
    FONT_FAMILY, FONT_SIZE_NORMAL, FONT_SIZE_HEADER
)


_photos = []   # храним ссылки на картинки


def create_product_card(parent, product):
    """Создаёт карточку одного товара."""
    bg_color = _get_card_color(product.quantity)

    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=(5, 0))

    _add_image(card, product, bg_color)
    _add_text_info(card, product, bg_color)

    # --- Разделитель снизу ---
    separator = ttk.Separator(parent, orient="horizontal")
    separator.pack(fill="x", padx=10, pady=(0, 5))

    return card


def _get_card_color(qty):
    """Возвращает цвет фона карточки."""
    return COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG


def _add_image(card, product, bg_color):
    """Добавляет изображение товара (или заглушку)."""
    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    image_path = f"images/{product.image}" if product.image else "resources/picture.png"
    if not os.path.exists(image_path):
        image_path = "resources/picture.png"

    try:
        img = Image.open(image_path)
        img.thumbnail((100, 100))
        photo = ImageTk.PhotoImage(img)
        _photos.append(photo)
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo   # type: ignore
        img_label.pack()
    except Exception:
        _add_placeholder(img_frame, bg_color)


def _add_placeholder(img_frame, bg_color):
    """Заглушка, если нет фото."""
    placeholder = tk.Frame(img_frame, bg="#E0E0E0", width=100, height=100)
    placeholder.pack_propagate(False)
    placeholder.pack()

    tk.Label(placeholder, text="📷", bg="#E0E0E0",
             font=("Arial", 24)).pack(expand=True)
    tk.Label(placeholder, text="Нет фото", bg="#E0E0E0",
             font=(FONT_FAMILY, FONT_SIZE_NORMAL),
             fg="#666666").pack()


def _add_text_info(card, product, bg_color):
    """Добавляет текстовую информацию о товаре."""
    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    # Защита от пустого названия
    name = product.name if product.name else "[Без названия]"
    _add_label(text_frame, name, bg_color,
               bold=True, size=FONT_SIZE_HEADER)

    _add_label(text_frame, f"Категория: {product.category}", bg_color)

    # Количество с индикатором
    indicator = _indicator(product.quantity)
    _add_label(text_frame, f"Количество: {indicator} ({product.quantity})", bg_color)

    _add_label(text_frame, f"Материал: {product.material}", bg_color)
    _add_label(text_frame, f"{product.price_with_discount_auto():.2f} руб.",
               bg_color, bold=True, size=FONT_SIZE_HEADER, align="e")


def _add_label(parent, text, bg_color, bold=False,
               size=FONT_SIZE_NORMAL, align="w"):
    """Добавляет одну метку с текстом."""
    font_style = (FONT_FAMILY, size, "bold") if bold else (FONT_FAMILY, size)
    tk.Label(parent, text=text, font=font_style,
             bg=bg_color, anchor=align).pack(fill="x")


def _indicator(qty):
    """
    Индикатор «много/мало» (порог 5).

    :param qty: количество товара
    :return: «много» или «мало»
    """
    return "много" if qty > 5 else "мало"


