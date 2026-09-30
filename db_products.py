"""Загрузка товаров из БД в объекты класса Product."""
import sqlite3
from config import DB_PATH
from models import Product


def _row_to_product(row):
    """Преобразует строку из БД в объект Product."""
    return Product(
        product_id=row[0],   # id
        category=row[1],     # категория
        name=row[2],         # наименование
        material=row[3],     # материал
        price=row[4],        # цена
        quantity=row[5],     # количество
        image=row[6]         # фото
    )


def get_all_products():
    """Возвращает список всех товаров из БД."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    rows = cur.fetchall()
    conn.close()

    return [_row_to_product(row) for row in rows]


def get_products_by_category(category):
    """Возвращает список объектов Product по категории."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE категория = ?", (category,))
    rows = cur.fetchall()
    conn.close()

    return [_row_to_product(row) for row in rows]


def get_products_low_stock():
    """Возвращает товары с количеством ≤ 3."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE количество <= 3")
    rows = cur.fetchall()
    conn.close()

    return [_row_to_product(row) for row in rows]


def print_catalog_with_highlight(products):
    """Выводит каталог с подсветкой для товаров ≤3."""
    print(f"\n{'=' * 70}")
    print(f"КАТАЛОГ ({len(products)} товаров)")
    print("=" * 70)

    for p in products:
        highlight = "⚠️" if p.quantity <= 3 else "  "
        print(f"{highlight} {p.info()}")

    print("=" * 70)


if __name__ == "__main__":
    print("1. Все товары:")
    print_catalog_with_highlight(get_all_products())

    print("\n2. Товары категории «Диван»:")
    print_catalog_with_highlight(get_products_by_category("Диван"))

    print("\n3. Товары с низким остатком (≤3):")
    print_catalog_with_highlight(get_products_low_stock())