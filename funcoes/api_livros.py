import os
import requests
from dotenv import load_dotenv

load_dotenv()

chave= os.getenv("GOOGLE_BOOKS_API_KEY")

def buscar_livros_api(titulo):
    url = "https://www.googleapis.com/books/v1/volumes"

    parametros = {
        "q":f"intitle:{titulo}",
        "key": chave
    }

    resposta = requests.get(url, params=parametros)
    if resposta.status_code != 200:
        return []

    dados = resposta.json()
    livros = dados.get("items", [])

    resultado = []

    for livro in livros:
        informacoes = livro["volumeInfo"]

        titulo = informacoes.get("title", "Título não informado")
        autores = informacoes.get("authors")
        paginas = informacoes.get("pageCount", "Não informado")
        if autores:
            autores_texto = ", ".join(autores)
        else:
            autores_texto = "Autores Não Encontrado!"
        livro_tratado = {
            "titulo": titulo,
            "autores": autores_texto,
            "paginas": paginas
        }
        resultado.append(livro_tratado)
    return resultado