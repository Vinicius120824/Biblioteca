from funcoes.validacoes import validar_paginas, validar_data, validar_ano

def test_paginas_validas():
    valido, mensagem = validar_paginas("300")

    assert valido is True
    assert mensagem == ""

def test_paginas_vazio():
    valido, mensagem = validar_paginas("")

    assert valido is False
    assert mensagem == "❌ Insira Páginas do Livro!"

def test_paginas_com_letras():
    valido, mensagem = validar_paginas("abc")

    assert valido is False
    assert mensagem == "❌ Insira Apenas Número de Páginas!"
def test_paginas_zero():
    valido, mensagem = validar_paginas("0")

    assert valido is False
    assert mensagem == "❌ Número de Páginas não pode ser Zero!"

def test_data_valida():
    valido, mensagem = validar_data("13/08/2026")

    assert valido is True
    assert mensagem == ""

def test_data_vazia():
    valido, mensagem = validar_data("")

    assert valido is True
    assert mensagem == ""

def test_data_formato_invalido():
    valido, mensagem = validar_data("2026-08-13")

    assert valido is False

def test_data_inexistente():
    valido, mensagem = validar_data("31/02/2026")

    assert valido is False