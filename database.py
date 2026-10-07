"""Работа с базой данных: роли, пользователи, заказы, авторизация."""
import sqlite3
from config import DB_PATH


def get_connection():
    """Возвращает соединение с базой данных."""
    return sqlite3.connect(DB_PATH)


def create_tables():
    """Создаёт таблицы Роль и Пользователь."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Роль (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            название TEXT NOT NULL UNIQUE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Пользователь (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            фамилия TEXT NOT NULL,
            имя TEXT NOT NULL,
            отчество TEXT,
            логин TEXT NOT NULL UNIQUE,
            роль_id INTEGER NOT NULL,
            FOREIGN KEY (роль_id) REFERENCES Роль(id)
        )
    """)

    conn.commit()
    conn.close()


def create_order_tables():
    """Создаёт таблицы Заказ и Состав_заказа."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Заказ (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            дата TEXT NOT NULL,
            клиент TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Состав_заказа (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            заказ_id INTEGER NOT NULL,
            товар_id INTEGER NOT NULL,
            количество INTEGER NOT NULL,
            цена REAL NOT NULL,
            FOREIGN KEY (заказ_id) REFERENCES Заказ(id),
            FOREIGN KEY (товар_id) REFERENCES Товар(id)
        )
    """)

    conn.commit()
    conn.close()


def fill_roles():
    """Добавляет базовые роли."""
    conn = get_connection()
    cur = conn.cursor()

    roles = ["Администратор", "Менеджер", "Клиент"]
    for role in roles:
        cur.execute("INSERT OR IGNORE INTO Роль (название) VALUES (?)", (role,))

    conn.commit()
    conn.close()


def fill_test_users():
    """Добавляет тестовых пользователей."""
    conn = get_connection()
    cur = conn.cursor()

    users = [
        ("Иванов", "Иван", "Иванович", "admin", 1),
        ("Петров", "Пётр", None, "manager", 2),
        ("Сидоров", "Сидор", None, "client", 3),
    ]
    for u in users:
        cur.execute("""
            INSERT OR IGNORE INTO Пользователь
            (фамилия, имя, отчество, логин, роль_id)
            VALUES (?, ?, ?, ?, ?)
        """, u)

    conn.commit()
    conn.close()


def fill_test_orders():
    """Добавляет тестовые заказы и состав заказов."""
    conn = get_connection()
    cur = conn.cursor()

    orders = [
        (1, "2025-01-15", "Иванов"),
        (2, "2025-02-03", "Петров"),
    ]
    for o in orders:
        cur.execute("INSERT OR IGNORE INTO Заказ (id, дата, клиент) VALUES (?, ?, ?)", o)

    items = [
        (1, 1, 2, 15000.0),
        (1, 2, 1, 8000.0),
        (2, 3, 4, 3500.0),
    ]
    for i in items:
        cur.execute("""
            INSERT OR IGNORE INTO Состав_заказа
            (заказ_id, товар_id, количество, цена)
            VALUES (?, ?, ?, ?)
        """, i)

    conn.commit()
    conn.close()


def get_user_by_login(login):
    """Ищет пользователя по логину.
    :return: (id, фамилия, имя, отчество, логин, роль) или None
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT Пользователь.id, Пользователь.фамилия,
               Пользователь.имя, Пользователь.отчество,
               Пользователь.логин, Роль.название
        FROM Пользователь
        JOIN Роль ON Пользователь.роль_id = Роль.id
        WHERE Пользователь.логин = ?
    """, (login,))
    row = cur.fetchone()
    conn.close()
    return row


def init_db():
    """Инициализация БД: таблицы + тестовые данные."""
    create_tables()
    create_order_tables()
    fill_roles()
    fill_test_users()
    fill_test_orders()


if __name__ == "__main__":
    init_db()
    print("База данных готова.\n")

    for login in ("admin", "manager", "client", "unknown"):
        user = get_user_by_login(login)
        if user:
            print(f"✔ {login}: {user[1]} {user[2]} — роль: {user[5]}")
        else:
            print(f"✘ {login}: пользователь не найден")