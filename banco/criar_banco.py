import sqlite3
def criar_banco():
    conexao = sqlite3.connect("banco/biblioteca.db")
    cursor = conexao.cursor()



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