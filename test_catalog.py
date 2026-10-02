"""Проверка вывода полей."""
import db_products as db


def test_fields():
    """Проверяет, что все поля на месте."""
    products = db.get_all_products()
    print(f"Всего товаров: {len(products)}")

    required_fields = ["id", "category", "name", "material", "price", "quantity"]
    errors = 0

    for p in products:
        missing = [f for f in required_fields if getattr(p, f, None) in (None, "")]
        if missing:
            print(f"❌ Товар id={p.id}: отсутствуют поля {missing}")
            errors += 1

    if errors == 0:
        print("✅ Все товары содержат нужные поля")


def test_prices():
    """Проверяет, что у всех товаров есть цена (не None)."""
    products = db.get_all_products()
    errors = 0

    for p in products:
        if p.price is None:
            print(f"❌ Товар id={p.id}: нет цены")
            errors += 1

    if errors == 0:
        print("✅ У всех товаров есть цена")


def test_quantities():
    """Проверяет, что у всех товаров количество ≥ 0."""
    products = db.get_all_products()
    errors = 0

    for p in products:
        if p.quantity is None or p.quantity < 0:
            print(f"❌ Товар id={p.id}: некорректное количество ({p.quantity})")
            errors += 1

    if errors == 0:
        print("✅ У всех товаров количество ≥ 0")


def test_has_images():
    """Проверяет, что хотя бы у одного товара есть изображение."""
    products = db.get_all_products()
    count_with_image = sum(1 for p in products if p.image)

    if count_with_image > 0:
        print(f"✅ Есть товары с изображением: {count_with_image}")
    else:
        print("❌ Ни у одного товара нет изображения")


def test_expensive():
    """Товары с ценой больше 1 000 000 руб."""
    products = db.get_all_products()
    found = [p for p in products if p.price and p.price > 1_000_000]

    if found:
        print(f"⚠️ Найдено {len(found)} товаров с ценой > 1 000 000:")
        for p in found:
            print(f"   id={p.id}, {p.name}, {p.price} руб.")
    else:
        print("✅ Товаров с ценой > 1 000 000 нет")


def test_long_names():
    """Товары с названием длиннее 100 символов."""
    products = db.get_all_products()
    found = [p for p in products if p.name and len(p.name) > 100]

    if found:
        print(f"⚠️ Найдено {len(found)} товаров с длинным названием")
    else:
        print("✅ Товаров с названием >100 символов нет")


def test_cyrillic():
    """Проверяет, что все названия на кириллице."""
    products = db.get_all_products()
    errors = 0

    for p in products:
        if p.name and not any("а" <= ch.lower() <= "я" for ch in p.name):
            print(f"❌ Товар id={p.id}: название не на кириллице")
            errors += 1

    if errors == 0:
        print("✅ Все названия на кириллице")


if __name__ == "__main__":
    print("=== 1. Поля ===")
    test_fields()
    print("\n=== 2. Цены ===")
    test_prices()
    print("\n=== 3. Количество ===")
    test_quantities()
    print("\n=== 4. Изображения ===")
    test_has_images()
    print("\n=== 5. Дорогие (> 1 000 000) ===")
    test_expensive()
    print("\n=== 6. Длинные названия ===")
    test_long_names()
    print("\n=== 7. Кириллица ===")
    test_cyrillic()