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


def test_names_not_empty():
    """Проверяет, что у всех товаров есть название."""
    products = db.get_all_products()
    errors = 0

    for p in products:
        if not p.name or not p.name.strip():
            print(f"❌ Товар id={p.id}: пустое название")
            errors += 1

    if errors == 0:
        print("✅ У всех товаров есть название")


def run_all_tests():
    """Прогон всех тестов каталога."""
    tests = [
        ("Проверка полей", test_fields),
        ("Проверка цен", test_prices),
        ("Проверка количества", test_quantities),
        ("Проверка изображений", test_has_images),
        ("Дорогие товары (> 1 000 000)", test_expensive),
        ("Длинные названия (> 100)", test_long_names),
        ("Проверка кириллицы", test_cyrillic),
        ("Проверка названий (не пустые)", test_names_not_empty),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ КАТАЛОГА")
    print("=" * 60)

    passed = 0
    for name, func in tests:
        print(f"\n{name}")
        try:
            func()
            passed += 1
        except Exception as e:
            print(f"❌ Ошибка: {e}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(tests)}")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()