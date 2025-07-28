import sqlite3

conn = sqlite3.connect("carwrap.db")
cur = conn.cursor()

# ОЧИСТИТЬ ТОЛЬКО ТАБЛИЦУ cars (оставить отчёты, фото, пользователей)
cur.execute("DELETE FROM cars;")
conn.commit()
conn.close()

print("Готово! Таблица cars очищена.")