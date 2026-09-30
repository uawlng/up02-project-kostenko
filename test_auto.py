"""Проверка метода price_with_discount_auto."""
from models import Product


товары = [
    Product(1, "Диван", "Угловой", "Велюр", 50000, 3, "sofa.png"),       # 3 шт. — без скидки
    Product(5, "Кровать", "Двуспальная", "Массив", 40000, 2, "bed.png"), # 2 шт. — со скидкой
]

for т in товары:
    print(f"{т.name}: {т.price} → {т.price_with_discount_auto()} руб.")