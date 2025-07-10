import sqlite3

conn = sqlite3.connect("demo.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    role TEXT,
    salary INTEGER
)
""")

employees = [
    (1, "Rick", "Científico", 10000),
    (2, "Morty", "Ayudante", 3000),
    (3, "Beth", "Veterinaria", 8000),
    (4, "Summer", "Estudiante", 2000)
]

cursor.executemany("INSERT OR REPLACE INTO employees VALUES (?, ?, ?, ?)", employees)
conn.commit()
conn.close()

print("✅ Base de datos demo.db creada.")
