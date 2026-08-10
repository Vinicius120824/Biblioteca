import sqlite3
conexao = sqlite3.connect("banco/biblioteca.db")
cursor = conexao.cursor()

print("banco criado com sucesso!")

cursor.execute("""
CREATE TABLE IF NOT EXISTS livros(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    status TEXT,
    numero_paginas INTEGER,
    data_leitura TEXT
)
""")
conexao.commit()

conexao.close()