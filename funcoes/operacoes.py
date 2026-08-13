import sqlite3

def conexao_banco():
    conexao = sqlite3.connect("banco/biblioteca.db")
    cursor = conexao.cursor()
    return conexao, cursor

def cadastrar_livro(titulo,autor,status,numero_paginas,data_leitura, formato,anotacao):

    conexao, cursor = conexao_banco()

    cursor.execute("""
    INSERT INTO livros(
        titulo,
        autor,
        status,
        numero_paginas,
        data_leitura,
        formato,
        anotacao
    )
    VALUES(?, ?, ?, ?, ?, ?, ?)
    """, (titulo, autor, status, numero_paginas, data_leitura, formato, anotacao))

    conexao.commit()
    
    conexao.close()

def listar_livros():
    conexao, cursor = conexao_banco()

    cursor.execute("""
    SELECT * FROM livros
    """)

    livros = cursor.fetchall()

    conexao.close()
    return livros

def buscar_livro_por_titulo(titulo):

    conexao, cursor = conexao_banco()

    cursor.execute("""
        SELECT * FROM livros WHERE titulo = ?
    """, (titulo,))
    livro = cursor.fetchall()
    
    conexao.close()
    return livro

def editar_livro(id_livro, novo_titulo, novo_autor, novo_status, novo_numero_paginas, nova_data_leitura, novo_formato,novo_anotacao):
    conexao, cursor = conexao_banco()

    livro = buscar_livro_id(id_livro)

    if livro:
        if novo_titulo == "":
            novo_titulo = livro[1]
        if novo_autor == "":
            novo_autor = livro[2]
        if novo_status == "":
            novo_status = livro[3]
        if novo_numero_paginas == "":
            novo_numero_paginas = livro[4]          
        else:
            novo_numero_paginas = int(novo_numero_paginas)
        if nova_data_leitura == "":
            nova_data_leitura = livro[5]              

        cursor.execute("""
                UPDATE livros
            SET
                titulo = ?,
                autor = ?,
                status = ?,
                numero_paginas = ?,
                data_leitura = ?,
                formato = ?,
                anotacao = ?
            WHERE id = ?

        """, (novo_titulo, novo_autor, novo_status, novo_numero_paginas, nova_data_leitura,novo_formato, novo_anotacao, id_livro))
        conexao.commit()
        conexao.close()
        return True
    
    
    conexao.close()
    return False

def excluir_livro(id_livro):

    livro = buscar_livro_id(id_livro)

    if not livro:
        return "nao_encontrado"

    conexao, cursor = conexao_banco()

    cursor.execute("""
        DELETE FROM livros
        WHERE id = ?
    """, (id_livro,))

    conexao.commit()
    conexao.close()

    return "excluido"

def buscar_livro_id(id_livro):
    
    conexao, cursor = conexao_banco()
    #verificar ID 
    cursor.execute("""
        SELECT * FROM livros
        WHERE id = ?    
    """, (id_livro,))
    livro = cursor.fetchone()

    conexao.close()

    return livro

def calcular_estatisticas():
    livros = listar_livros()
    total = len(livros)
    lidos = 0

    if livros:
        for livro in livros:
            if livro[3] == "Lido":
                lidos += 1

        percentual = lidos / total * 100
        return lidos, total, percentual

    return 0, 0, 0