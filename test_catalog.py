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
    else:
        print(f"❌ Найдено ошибок: {errors}")


if __name__ == "__main__":
    test_fields()
