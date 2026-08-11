import sqlite3
import os

def criar_banco():
    os.makedirs("banco", exist_ok=True)
    conexao = sqlite3.connect("banco/biblioteca.db")
    cursor = conexao.cursor()



    cursor.execute("""
    CREATE TABLE IF NOT EXISTS livros(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autor TEXT NOT NULL,
        status TEXT,
        numero_paginas INTEGER,
        data_leitura TEXT,
        formato TEXT,
        anotacao TEXT
    )
    """)
    conexao.commit()
    conexao.close()