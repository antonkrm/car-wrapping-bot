-- Пользователи (сотрудники и админы)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_id INTEGER UNIQUE,
    name TEXT,
    is_admin BOOLEAN DEFAULT 0
);

-- Отчеты (один в день от сотрудника)
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Автомобили в отчете (могут быть несколько)
CREATE TABLE IF NOT EXISTS cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id INTEGER,
    license_plate TEXT,
    description TEXT,
    area REAL,
    cost INTEGER,
    labor_cost INTEGER DEFAULT 0,
    FOREIGN KEY(report_id) REFERENCES reports(id)
);

-- Фото, привязанные к отчету
CREATE TABLE IF NOT EXISTS photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id INTEGER,
    file_id TEXT,
    FOREIGN KEY(report_id) REFERENCES reports(id)
);

-- Таблица материалов (элементы и площадь)
CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    area REAL,
    active BOOLEAN DEFAULT 1
);
