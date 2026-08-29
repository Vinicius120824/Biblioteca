import re
from datetime import datetime

def validar_paginas(paginas):
    if not paginas.strip():
        return False, "❌ Insira Páginas do Livro!"

    if not paginas.isdigit():
        return False, "❌ Insira Apenas Número de Páginas!"

    if int(paginas) <= 0:
        return False, "❌ Número de Páginas não pode ser Zero!"

    return True, ""

def validar_data(data):
    if not data.strip():
        return True, ""

    if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", data):
        return False, "❌ Formato inválido! Use DD/MM/AAAA. Exemplo: 13/08/2026."

    try:
        datetime.strptime(data, "%d/%m/%Y")
    except ValueError:
        return False, "❌ Data inválida! Digite uma data existente."

    return True, ""

def validar_ano(ano):
    if not ano.strip():
        return False, "❌ Insira o ano!"
    if not ano.isdigit():
        return False, "❌ Insira apenas números no ano!"
    if not len(ano) == 4:
        return False, "❌ Insira o ano com 4 caracteres!"
    return True, ""