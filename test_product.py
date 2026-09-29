"""Проверка класса Product."""
from models import Product


# Создаём один товар вручную (7 полей — как в БД)
p = Product(
    product_id=1,
    category="Диван",
    name="Угловой",
    material="Велюр",
    price=50000,
    quantity=3,
    image="sofa.png"
)

print(p.info())
print(f"Со скидкой 25%: {p.price_with_discount(25):.2f} руб.")
