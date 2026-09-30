catalog = [
    {"name": "Кроссовки", "price": 8500, "qty": 3},
    {"name": "Ботинки", "price": 15000, "qty": 1},
    {"name": "Туфли", "price": 12000, "qty": 5},
    {"name": "Сандалии", "price": 4500, "qty": 8},
    {"name": "Кеды", "price": 6000, "qty": 2},
]

catalog.sort(key=lambda item: item["qty"] <= 5)

print("Каталог с индикатором:")

for i, item in enumerate(catalog, start=1):
    mark = "много" if item["qty"] > 5 else "мало"
    print(f'{i}. {item["name"]:<12} — {item["qty"]} шт. → {mark}')