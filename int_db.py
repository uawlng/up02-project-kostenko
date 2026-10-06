import sqlite3
from config import DB_PATH

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("PRAGMA foreing_keys = ON;")

cur.execute('''CREATE TABLE IF NOT EXISTS Состав_заказа (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    заказ_id INTEGER NOT NULL,
    товар_id INTEGER NOT NULL,
    количество INTEGER NOT NULL,
    цена REAL NOT NULL,
    FOREIGN KEY (заказ_id) REFERENCES Заказ(id) ON DELETE CASCADE,
    FOREIGN KEY (товар_id) REFERENCES Товар(id)
);
''')

conn.commit()
conn.close()
