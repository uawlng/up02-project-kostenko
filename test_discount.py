"""Тестирование алгоритма скидки."""
from discount import calculate_price_with_discount, get_product_quantity


def run_tests():
    """Прогон тестов."""
    # Ожидаемые результаты взяты из текущей БД.
    # Если данные в БД изменятся — поменяй ожидания.
    test_cases = [
        # (id, цена, ожидание, пояснение)
        (1, 50000, 50000, "Диван — 3 шт., скидки нет (не меньше 3)"),
        (2, 25000, 25000, "Стол — 5 шт., скидки нет"),
        (3, 5000,  5000,  "Стул — 20 шт., скидки нет"),
        (4, 35000, 35000, "Шкаф — 4 шт., скидки нет"),
        (5, 40000, 28000, "Кровать — 2 шт. → скидка 30%"),
        (6, 15000, 15000, "Комод — 6 шт., скидки нет"),
        (7, 3000,  3000,  "Полка — 15 шт., скидки нет"),
    ]

    print("=" * 70)
    print("ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ (30% при количестве < 3)")
    print("=" * 70)

    passed = 0
    for product_id, price, expected, comment in test_cases:
        qty = get_product_quantity(product_id)
        result = calculate_price_with_discount(product_id, price)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} Товар {product_id} (кол-во: {qty}): "
              f"{price} → {result} (ожидалось {expected}) — {comment}")

    print("=" * 70)
    print(f"Пройдено: {passed} / {len(test_cases)}")


if __name__ == "__main__":
    run_tests()