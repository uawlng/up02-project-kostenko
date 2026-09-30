"""Тестирование алгоритма скидки."""
from discount import calculate_price_with_discount, get_product_quantity


def run_tests():
    """Прогон тестов."""
    test_cases = [
        # (id, цена, ожидание, пояснение)
        (1, 50000, 50000, "Диван — 3 шт., скидки нет"),
        (2, 25000, 25000, "Стол — 5 шт., скидки нет"),
        (3, 5000,  5000,  "Стул — 20 шт., скидки нет"),
        (4, 35000, 35000, "Шкаф — 4 шт., скидки нет"),
        (5, 40000, 28000, "Кровать — 2 шт. → скидка 30%"),
        (6, 15000, 15000, "Комод — 6 шт., скидки нет"),
        (7, 3000,  3000,  "Полка — 15 шт., скидки нет"),

        #  5 новых тестов 
        (1, 10000, 10000, "Граница: 3 шт. — без скидки"),
        (5, 20000, 14000, "Кровать: 20000 → 14000"),
        (5, 10000, 7000,  "Кровать: 10000 → 7000"),
        (999, 5000, 3500, "Несуществующий товар → 0 шт. → скидка"),
        (3, 8000, 8000,   "Стул: 20 шт. — без скидки"),
    ]

    print("=" * 75)
    print("ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ (30% при количестве < 3)")
    print("=" * 75)

    passed = 0
    for product_id, price, expected, comment in test_cases:
        qty = get_product_quantity(product_id)
        result = calculate_price_with_discount(product_id, price)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} id={product_id} (кол-во: {qty}): "
              f"{price} → {result} (ожидалось {expected}) — {comment}")

    print("=" * 75)
    print(f"Пройдено: {passed} / {len(test_cases)}")


if __name__ == "__main__":
    run_tests()