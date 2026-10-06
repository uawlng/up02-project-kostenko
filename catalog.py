"""Карточка товара."""
import os
import tkinter as tk
from tkinter import ttk
from typing import Literal
from PIL import Image, ImageTk
from styles import (
    COLOR_MAIN_BG, COLOR_HIGHLIGHT,
    FONT_FAMILY, FONT_SIZE_NORMAL, FONT_SIZE_HEADER
)


AnchorType = Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]

_photos = []


def create_product_card(parent, product, refresh=None):
    """Создаёт карточку одного товара."""
    bg_color = _get_card_color(product.quantity)

    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=(5, 0))
    card.bind("<Button-1>", lambda e: _open_view(parent, product,refresh))

    _add_image(card, product, bg_color)
    _add_text_info(card, product, bg_color)

    separator = ttk.Separator(parent, orient="horizontal")
    separator.pack(fill="x", padx=10, pady=(0, 5))

    def _bind_recursive(widget):
        widget.bind("<Button-1>", lambda e: _open_view(parent, product,refresh))
        for child in widget.winfo_children():
            _bind_recursive(child)

    _bind_recursive(card)

    return card


def _open_view(parent, product,refresh=None):
    """Открывает форму просмотра товара."""
    from view_form import ViewForm
    ViewForm(parent, product, on_add_to_order=refresh)


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
        img_label.image = photo
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

    name = product.name if product.name else "[Без названия]"
    category = product.category if product.category else "[Без категории]"
    material = product.material if product.material else "[Не указан]"

    price = product.price if product.price is not None else 0
    final_price = _get_final_price(product.id, price)

    _add_label(text_frame, name, bg_color,
               bold=True, size=FONT_SIZE_HEADER)
    _add_label(text_frame, f"Категория: {category}", bg_color)

    indicator = _indicator(product.quantity)
    _add_label(text_frame, f"Количество: {indicator} ({product.quantity})", bg_color)

    _add_label(text_frame, f"Материал: {material}", bg_color)
    _add_label(text_frame, f"{final_price:.2f} руб.",
               bg_color, bold=True, size=FONT_SIZE_HEADER, align="e")


def _get_final_price(product_id, price):
    """Возвращает цену со скидкой или без (с защитой от None)."""
    try:
        from discount import calculate_price_with_discount
        return calculate_price_with_discount(product_id, price)
    except Exception:
        return price


def _add_label(parent, text, bg_color, bold=False,
               size=FONT_SIZE_NORMAL, align: AnchorType = "w"):
    """Добавляет одну метку с текстом."""
    font_style = (FONT_FAMILY, size, "bold") if bold else (FONT_FAMILY, size)
    tk.Label(parent, text=text, font=font_style,
             bg=bg_color, anchor=align).pack(fill="x")


def _indicator(qty):
    """
    Индикатор «много/мало» (порог 3).

    :param qty: количество товара
    :return: «много» или «мало»
    """
    return "много" if qty > 3 else "мало"