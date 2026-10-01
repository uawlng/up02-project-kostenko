"""Модели данных для проекта УП.02."""
from discount import calculate_price_with_discount


class Product:
    """Класс Товар."""

    def __init__(self, product_id, category, name, material, price, quantity, image):
        """
        Инициализация товара.

        :param product_id: идентификатор
        :param category: категория
        :param name: название
        :param material: материал
        :param price: цена
        :param quantity: количество
        :param image: имя файла фото
        """
        self.id = product_id
        self.category = category
        self.name = name
        self.material = material
        self.price = price
        self.quantity = quantity
        self.image = image

    def total(self):
        """Общая стоимость (цена × количество)."""
        return self.price * self.quantity

    def price_with_discount(self, discount_percent):
        """Цена со скидкой."""
        return self.price * (1 - discount_percent / 100)

    def price_with_discount_auto(self):
        """Цена со скидкой по алгоритму (30%, если товара < 3)."""
        return calculate_price_with_discount(self.id, self.price)

    def indicator(self):
        """Индикатор «много/мало» (порог 5)."""
        return "много" if self.quantity > 5 else "мало"

    def is_available(self):
        """Есть ли товар в наличии."""
        return self.quantity > 0

    def info(self):
        """Строка с информацией о товаре."""
        return (
            f"{self.name} ({self.category}) — "
            f"{self.price} руб. × {self.quantity} = {self.total()} руб. "
            f"({self.indicator()})"
        )
    def discounted_price(self):
        """Цена со скидкой"""
        return self.price * 0.90


class Order:
    """Класс Заказ."""

    def __init__(self, order_id, date, client, product, quantity):
        """
        Инициализация заказа.

        :param order_id: идентификатор заказа
        :param date: дата
        :param client: ФИО клиента
        :param product: объект Product
        :param quantity: количество
        """
        self.id = order_id
        self.date = date
        self.client = client
        self.product = product      # объект Product
        self.quantity = quantity

    def total(self):
        """Стоимость заказа."""
        return self.product.price * self.quantity

    def info(self):
        """Строка с информацией о заказе."""
        return (
            f"Заказ №{self.id} от {self.date}: {self.client} — "
            f"{self.product.name} × {self.quantity} = {self.total()} руб."
        )