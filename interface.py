import customtkinter as ctk
from funcoes.operacoes import cadastrar_livro
from funcoes.operacoes import listar_livros
from funcoes.operacoes import buscar_livro_id
from funcoes.operacoes import buscar_livro_por_titulo
from funcoes.operacoes import editar_livro
from funcoes.operacoes import excluir_livro
from funcoes.operacoes import calcular_estatisticas
from funcoes.operacoes import relatorio_anual
from funcoes.api_livros import buscar_livros_api
from funcoes.validacoes import (
    validar_paginas,
    validar_data,
    validar_ano
)

from datetime import datetime
import re
from PIL import Image
from io import BytesIO
import requests



# Configuração da aparência
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")

# Criar a janela
janela = ctk.CTk()
largura_tela = janela.winfo_screenwidth()

if largura_tela < 1000:
    colunas = 1
else:
    colunas = 2

frame_principal = ctk.CTkFrame(
    master=janela
)

frame_principal.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)
frame_principal.grid_columnconfigure(0, weight=1)

frame_principal.grid_rowconfigure(0, weight=0)
frame_principal.grid_rowconfigure(1, weight=0)
frame_principal.grid_rowconfigure(2, weight=1)

frame_titulo = ctk.CTkFrame(
    master=frame_principal,
    fg_color="transparent"
)

frame_titulo.grid(
    row=0,
    column=0,
    sticky="ew",
    pady=(5, 5)
)

frame_menu =ctk.CTkFrame(
    master=frame_principal,
    fg_color="transparent"
)

frame_menu.grid(
    row=1,
    column=0,
    sticky="ew",
    pady=(5, 0)
)
frame_conteudo = ctk.CTkFrame(
    master=frame_principal,
    fg_color="transparent"
)

frame_conteudo.grid(
    row=2,
    column=0,
    sticky="nsew",
    padx=20,
    pady=(5, 10)
)


# Configurações da janela
janela.title("Biblioteca")
janela.geometry("800x600")
janela.after(0, lambda: janela.state("zoomed"))

titulo = ctk.CTkLabel(
    master=frame_titulo,
    text="Seu Mundinho!",
    font=("times new roman", 28, "bold")
)

titulo.pack(pady=10)

mensagem = ctk.CTkLabel(
    master=frame_menu,
    text="Bem-Vindo!!",
    font=("times new roman", 18, "bold")
)
mensagem.pack(pady=(15, 5))

def criar_card_livro(frame_lista, livro, acao=None):
    card_livro = ctk.CTkFrame(
        master=frame_lista,
        corner_radius=10,
        fg_color="#2b2b2b",
    )
    card_livro.pack(
        fill="x",
        padx=20,
        pady=20
    )
    # CAPA LIVRO
    imagem_capa = criar_imagem_capa(livro[8])
    if imagem_capa:
        label_capa = ctk.CTkLabel(
            master=card_livro,
            text="",
            image=imagem_capa
        )
        label_capa.pack(pady=10)
    #Menu Titulo
    label_titulo = ctk.CTkLabel(
        master=card_livro,
        text=f"📖 {livro[1]}",
        font=("times new roman", 12)
    )
    label_titulo.pack(
        pady=(10, 2),
        padx=20,
        anchor="w"
    )

    #Menu Autor
    label_autor = ctk.CTkLabel(
        master=card_livro,
        text=f"👤 {livro[2]}",
        font=("times new roman", 12)
    )
    label_autor.pack(
        pady=2,
        padx=20,
        anchor="w"
    )
    if livro[3]:
        status = livro[3]
    else:
        status = "Não informado!"
    label_status = ctk.CTkLabel(
        master=card_livro,
        text=f"📚 {status}",
        font=("times new roman", 12)
    )
    label_status.pack(
        pady=2,
        padx=20,
        anchor="w"
    )
    label_paginas = ctk.CTkLabel(
        master=card_livro,
        text=f"📄 {livro[4]} páginas",
        font=("times new roman", 12)
    )
    label_paginas.pack(
        pady=2,
        padx=20,
        anchor="w"
    )
    if livro[5]:
        data = livro[5]
    else:
        data = "Não Informado!"
        
    label_data = ctk.CTkLabel(
        master=card_livro,
        text=f"📅 {data}",
        font=("times new roman", 12)
    )
    label_data.pack(
        pady=2,
        padx=20,
        anchor="w"
    )
    label_formato = ctk.CTkLabel(
        master=card_livro,
        text=f"💻{livro[6]}",
        font=("times new roman", 12)
    )
    label_formato.pack(
        pady=2,
        padx=20,
        anchor="w"
    )
    label_anotacao = ctk.CTkLabel(
        master=card_livro,
        text=f"📋{livro[7]}",
        font=("times new roman", 12)
    )
    label_anotacao.pack(
        pady=2,
        padx=20,
        anchor="w"
    )      
    if acao == "editar":
        button_editar = ctk.CTkButton(
        master=card_livro,
        text="Editar",
        command=lambda: mostrar_formulario_edicao(livro)
        )

        button_editar.pack(
            pady=(10, 15),
            padx=20,
            anchor="e"
        )
    elif acao == "excluir":
        button_excluir = ctk.CTkButton(
        master=card_livro,
        text="Excluir",
        command=lambda: mostrar_confirmacao_exclusao(livro)
        )

        button_excluir.pack(
            pady=(10, 15),
            padx=20,
            anchor="e"
        )    
    elif acao == "adicionar":
        button_excluir = ctk.CTkButton(
        master=card_livro,
        text="Adicionar",
        command=lambda: cadastrar_livro(livro)
        )

        button_excluir.pack(
            pady=(10, 15),
            padx=20,
            anchor="e"
        ) 

def criar_card_livro_api(frame_lista, livro, acao=None):

    card_livro = ctk.CTkFrame(
        master=frame_lista,
        corner_radius=10,
        fg_color="#2b2b2b",
    )

    card_livro.pack(
        fill="x",
        padx=20,
        pady=20
    )
    # CAPA LIVRO
    imagem_capa = criar_imagem_capa(livro["capa"])
    if imagem_capa:
        label_capa = ctk.CTkLabel(
            master=card_livro,
            text="",
            image=imagem_capa
        )
        label_capa.pack(pady=10)
    label_titulo = ctk.CTkLabel(
        master=card_livro,
        text=f"📖 {livro['titulo']}",
        font=("times new roman", 12)
    )

    label_titulo.pack(
        pady=(10, 2),
        padx=20,
        anchor="w"
    )

    label_autor = ctk.CTkLabel(
        master=card_livro,
        text=f"👤 {livro['autores']}",
        font=("times new roman", 12)
    )

    label_autor.pack(
        pady=2,
        padx=20,
        anchor="w"
    )

    label_paginas = ctk.CTkLabel(
        master=card_livro,
        text=f"📄 {livro['paginas']} páginas",
        font=("times new roman", 12)
    )

    label_paginas.pack(
        pady=2,
        padx=20,
        anchor="w"
    )

    if acao == "adicionar":
        botao_adicionar = ctk.CTkButton(
            master=card_livro,
            text="Adicionar",
            command=lambda: mostrar_cadastro_livro_api(livro)
        )

        botao_adicionar.pack(
            pady=(10, 15),
            padx=20,
            anchor="e"
        )

def mostrar_cadastro_livro_api(livro):
    limpar_frame(frame_conteudo)

    frame_formulario = ctk.CTkScrollableFrame(
        master=frame_conteudo,
        fg_color="transparent"
    )

    frame_formulario.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    titulo_cadastro = ctk.CTkLabel(
        master=frame_formulario,
        text="Adicionar Livro",
        font=("times new roman", 20, "bold")
    )

    titulo_cadastro.pack(pady=20)

    entry_titulo = criar_campo(
        frame_formulario,
        "Título:",
        livro["titulo"]
    )

    entry_autor = criar_campo(
        frame_formulario,
        "Autor:",
        livro["autores"]
    )

    entry_status = criar_campo_selecao(
        frame_formulario,
        "Status:",
        ["Lido", "Lendo", "Não Lido"]
    )

    entry_paginas = criar_campo(
        frame_formulario,
        "Número de Páginas:",
        livro["paginas"]
    )

    entry_data = criar_campo(
        frame_formulario,
        "Data Leitura:"
    )

    entry_formato = criar_campo_selecao(
        frame_formulario,
        "Formato:",
        ["Físico", "E-book"]
    )
    entry_capa = criar_campo(frame_formulario, "Url capa: ", livro["capa"])
    entry_anotacao = criar_campo_anotacao(
        frame_formulario
    )

    button_cadastrar = ctk.CTkButton(
        master=frame_formulario,
        text="Cadastrar",
        command=lambda: clicar_cadastrar(
            entry_titulo,
            entry_autor,
            entry_status,
            entry_paginas,
            entry_data,
            entry_formato,
            entry_anotacao,
            entry_capa
        )
    )

    button_cadastrar.pack(
        pady=(10, 15),
        padx=20
    )
    criar_button(frame_formulario, pesquisar_livro_api)

def limpar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
    
def mostrar_menu():
    for widget in frame_conteudo.winfo_children():
        widget.destroy()

    opcoes = [
        ("Cadastrar", mostrar_tela_cadastro),
        ("Listar", mostrar_tela_listar),
        ("Buscar", mostrar_tela_buscar),
        ("Editar", mostrar_tela_editar),
        ("Excluir", mostrar_tela_excluir),
        ("Relátorio Anual", mostrar_tela_relatorio),
        ("Pesquisar Livro", pesquisar_livro_api)
    ]
    frame_formulario = ctk.CTkScrollableFrame(
        master=frame_conteudo,
        fg_color="transparent"
    )

    frame_formulario.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )
    mensagem = ctk.CTkLabel(
        master=frame_formulario,
        text="Menu do seu Mundinho Biblioteca!!",
        font=("times new roman", 14, "bold")
    )
    mensagem.pack(pady=(0, 10))

    lido, total, percentual = calcular_estatisticas()
    frame_estatisticas = ctk.CTkFrame(
        master=frame_formulario,
        corner_radius=10,
        width=400
    )
    frame_estatisticas.pack(
        padx=20,
        pady=20

    )
    label_estatisticas = ctk.CTkLabel(
    master=frame_estatisticas,
    text="Estatísticas",
    font=("times new roman", 18, "bold")
    )
    label_estatisticas.pack(
        pady=(15, 10),
        expand=True
        )

    label_total = ctk.CTkLabel(
        master=frame_estatisticas,
        text=f"📚 Total de livros: {total}"
    )
    label_total.pack(pady=5)

    label_lido = ctk.CTkLabel(
    master=frame_estatisticas,
    text=f"👀 Livros Lidos: {lido}"
    )
    label_lido.pack(pady=5)    

    label_percentual = ctk.CTkLabel(
        master=frame_estatisticas,
        text=f"✔ Concluído: {percentual:.1f}%"
    )
    label_percentual.pack(pady=5)

    barra_progresso = ctk.CTkProgressBar(
        master=frame_estatisticas
    )

    barra_progresso.pack(
        padx=30,
        pady=(5, 10)
    )
    barra_progresso.set(percentual / 100)

    frame_botoes = ctk.CTkFrame(
        master=frame_formulario,
        fg_color="transparent"
    )

    frame_botoes.pack(
        pady=20
    )
    # frame_botoes.grid_columnconfigure(0, weight=1)
    # frame_botoes.grid_columnconfigure(1, weight=1)

    for indice, (texto, funcao) in enumerate(opcoes):
        linha = indice // colunas
        coluna = indice % colunas
        botoes = ctk.CTkButton(
            master=frame_botoes,
            text=texto,
            command=funcao,
            width=250
        )

        botoes.grid(
            row=linha,
            column=coluna,
            padx=10,
            pady=10,
        )

def mostrar_tela_cadastro():
    limpar_frame(frame_conteudo)
    frame_formulario = ctk.CTkScrollableFrame(
        master=frame_conteudo,
        fg_color="transparent"
    )

    frame_formulario.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )
    titulo_cadastro = ctk.CTkLabel(
        master=frame_formulario,
        text="Cadastro de Livro",
        font=("times new roman", 20, "bold")
    )
    titulo_cadastro.pack(pady=20)

    entry_titulo = criar_campo(frame_formulario, "Titulo:")
    entry_autor = criar_campo(frame_formulario, "Autor:")
    entry_status = criar_campo_selecao(frame_formulario, "Status:", ["Lido","Lendo","Não Lido"])
    entry_paginas = criar_campo(frame_formulario, "Número de Páginas:")
    entry_data = criar_campo(frame_formulario, "Data Leitura:")
    entry_formato = criar_campo_selecao(frame_formulario, "Formato:", ["Físico", "E-book"])
    entry_anotacao = criar_campo_anotacao(frame_formulario)
    entry_capa = criar_campo(frame_formulario, "Insira o Url imagem: ")

    button_cadastrar = ctk.CTkButton(
        master=frame_conteudo,
        text="Cadastrar",
        command=lambda: clicar_cadastrar(entry_titulo, entry_autor, entry_status, entry_paginas, entry_data, entry_formato, entry_anotacao, entry_capa)
        
    )
    button_cadastrar.pack(
        pady=(10, 15),
        padx=20     
    )
    criar_button_voltar(frame_conteudo)

def mostrar_tela_listar():
    limpar_frame(frame_conteudo)

    label_livros = ctk.CTkLabel(
    master=frame_conteudo,
    text="Meus Livros",
    font=("times new roman", 20, "bold")

    )
    label_livros.pack(pady=20)

    frame_lista = ctk.CTkScrollableFrame(
        master=frame_conteudo,
        fg_color="transparent"
    )

    frame_lista.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    livros = listar_livros()

    for livro in livros:
        criar_card_livro(frame_lista, livro)

    criar_button_voltar(frame_conteudo)

def clicar_cadastrar(entry_titulo, entry_autor, entry_status, entry_paginas, entry_data, entry_formato, entry_anotacao, entry_capa):
    titulo = entry_titulo.get()
    autor = entry_autor.get()
    status = entry_status.get()
    paginas = entry_paginas.get()
    data = entry_data.get()
    formato = entry_formato.get()
    anotacao = entry_anotacao.get("1.0", "end").strip()
    capa = entry_capa.get()

    if not titulo.strip():
        mostrar_mensagem("❌ Insira um Título!")
        return
        
    valido, mensagem = validar_paginas(paginas)
    if not valido:
        mostrar_mensagem(mensagem)
        return
    valido, mensagem = validar_data(data)
    if not valido:
        mostrar_mensagem(mensagem)
        return

    paginas = int(paginas)           

    cadastrar_livro(titulo,autor,status,paginas,data,formato,anotacao,capa)
    
    mostrar_mensagem("✔Livro Cadastrado com Sucesso!")      
    mostrar_tela_cadastro()

def mostrar_menu_principal():
    limpar_frame(frame_menu)
    mostrar_menu()

def criar_button_voltar(frame):
    button_voltar = ctk.CTkButton(
    master=frame,
    text="Voltar",
    command=mostrar_menu_principal
    
    )
    button_voltar.pack(
        pady=(10, 15),
        padx=20        
    )

def criar_button(frame, fuct):
    button_voltar = ctk.CTkButton(
    master=frame,
    text="Voltar",
    command=fuct
    
    )
    button_voltar.pack(
        pady=(10, 15),
        padx=20        
    )

def button_voltar_editar(frame):
    button_voltar = ctk.CTkButton(
    master=frame,
    text="Voltar Editar",
    command=mostrar_tela_editar
    
    )
    button_voltar.pack(
        pady=(10, 15),
        padx=20,       
    )

def button_voltar(frame,text, comad):
    button_voltar = ctk.CTkButton(
    master=frame,
    text=text,
    command=comad
    
    )
    button_voltar.pack(
        pady=(10, 15),
        padx=20,       
    )    

def mostrar_tela_buscar():
    limpar_frame(frame_conteudo)
    # frame_formulario = ctk.CTkScrollableFrame(
    #     master=frame_conteudo,
    #     fg_color="transparent"
    # )

    # frame_formulario.pack(
    #     fill="both",
    #     expand=True,
    #     padx=20,
    #     pady=20
    # )
    label_titulo = ctk.CTkLabel(
        master=frame_conteudo,
        text="Título do Livro: ",
        font=("times new roman", 12, "bold")
    )
    label_titulo.pack(pady=(15, 5))

    entry_titulo_busca = ctk.CTkEntry(
        master=frame_conteudo
    )    
    entry_titulo_busca.pack(
        fill="x",
        pady=10,
        padx=30
        )

    label_id = ctk.CTkLabel(
        master=frame_conteudo,
        text="ID do Livro: ",
        font=("times new roman", 12, "bold")
    )
    label_id.pack(pady=(15, 5))

    entry_id_busca = ctk.CTkEntry(
        master=frame_conteudo
    )    
    entry_id_busca.pack(
        fill="x",
        pady=10,
        padx=30
        ) 
    frame_resultado = ctk.CTkFrame(
    master=frame_conteudo,
    fg_color="transparent"
    )

    frame_resultado.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(5, 0)
    )

    button_buscar = ctk.CTkButton(
        master=frame_conteudo,
        text="Buscar",
        command=lambda:clicar_buscar(entry_titulo_busca, entry_id_busca, frame_resultado) 
    )
    button_buscar.pack(
        pady=(10, 15),
        padx=20     
    )
    criar_button_voltar(frame_conteudo)

def clicar_buscar(entry_titulo_busca, entry_id_busca, frame_resultado):
    titulo = entry_titulo_busca.get()
    id_livro = entry_id_busca.get()
    id_exibidos = set()

    limpar_frame(frame_resultado)
    frame_lista = ctk.CTkScrollableFrame(
        master=frame_resultado,
        fg_color="transparent"
    )

    frame_lista.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    if id_livro:    
        if not id_livro.isdigit():
            mostrar_mensagem("❌Insira apenas número no ID!")
        else:
            id_livro = int(id_livro)        
            livro = buscar_livro_id(id_livro)  

            if not livro:
                mostrar_mensagem(f"❌Livro não encontrado pelo ID: {id_livro}")

            elif livro and livro[0] not in id_exibidos:
                criar_card_livro(frame_lista, livro)
                id_exibidos.add(livro[0])
    if titulo:
        if not titulo.strip():
            mostrar_mensagem("❌Insira o Titulo!")
            return
        livros = buscar_livro_por_titulo(titulo)
        if not livros:
            mostrar_mensagem(f"❌Livro não encontrado pelo Título: {titulo}!")
            return                          

        for livro in livros:
            if livro[0] not in id_exibidos:
                criar_card_livro(frame_lista, livro)                
                id_exibidos.add(livro[0])

def mostrar_confirmacao_exclusao(livro):
    limpar_frame(frame_conteudo)

    label_confirmacao = ctk.CTkLabel(
    master=frame_conteudo,
    text=f"Tem certeza que deseja excluir o livro:\n{livro[1]}",
    font=("times new roman", 24, "bold"),
    wraplength=400,
    justify="center"
    )
    label_confirmacao.pack(pady=40)

    button_confirmar = ctk.CTkButton(
    master=frame_conteudo,
    text="Confirmar",
    command=lambda:confirmar_exclusao(livro[0], livro[1])
    )

    button_confirmar.pack(
        pady=(10, 15),
        padx=20,
        anchor="n"
    )

    button_cancelar = ctk.CTkButton(
    master=frame_conteudo,
    text="Cancelar",
    command=mostrar_tela_excluir
    )

    button_cancelar.pack(
        pady=(10, 15),
        padx=20,
        anchor="n"
    )

def confirmar_exclusao(id_livro, titulo):
    excluir_livro(id_livro)

    limpar_frame(frame_menu)

    label_sucesso = ctk.CTkLabel(
        master=frame_menu,
        text=f"✔ Livro {titulo} excluído com sucesso!",
        font=("times new roman", 15, "bold")
    )
    label_sucesso.pack(pady=20)

    mostrar_tela_excluir()

def mostrar_tela_editar():
    limpar_frame(frame_conteudo)
  

    label_livros = ctk.CTkLabel(
    master=frame_conteudo,
    text="Editar Livros",
    font=("times new roman", 20, "bold")

    )
    label_livros.pack(pady=20)
    variavel_busca = ctk.StringVar()

    entry_busca = ctk.CTkEntry(
    master=frame_conteudo,
    placeholder_text="Digite o título do livro...",
    textvariable=variavel_busca
    )

    entry_busca.pack(
        fill="x",
        padx=30,
        pady=(5, 15)
    )
    variavel_busca.trace_add(
    "write",
        lambda *args: filtrar_livros(
            variavel_busca.get(),
            livros,
            frame_lista,
            "editar"
        )
    )
    frame_lista = ctk.CTkScrollableFrame(
        master=frame_conteudo,
        fg_color="transparent"
    )

    frame_lista.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    livros = listar_livros()

    for livro in livros:
        criar_card_livro(frame_lista, livro, "editar")

    criar_button_voltar(frame_conteudo)

def filtrar_livros(texto, livros, frame_lista, acao):
    limpar_frame(frame_lista)

    texto = texto.strip().lower()

    for livro in livros:
        titulo = livro[1].lower()

        if texto in titulo:
            criar_card_livro(frame_lista, livro, acao)
    criar_button_voltar(frame_conteudo)    

def mostrar_tela_excluir():
    limpar_frame(frame_conteudo)
  
    label_livros = ctk.CTkLabel(
    master=frame_conteudo,
    text="Meus Livros",
    font=("times new roman", 40, "bold")

    )
    label_livros.pack(pady=20)
    variavel_busca = ctk.StringVar()

    entry_busca = ctk.CTkEntry(
    master=frame_conteudo,
    placeholder_text="Digite o título do livro...",
    textvariable=variavel_busca
    )

    entry_busca.pack(
        fill="x",
        padx=30,
        pady=(5, 15)
    )
    variavel_busca.trace_add(
    "write",
        lambda *args: filtrar_livros(
            variavel_busca.get(),
            livros,
            frame_lista,
            "excluir"
        )
    )
    frame_lista = ctk.CTkScrollableFrame(
        master=frame_conteudo,
        fg_color="transparent"
    )

    frame_lista.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    livros = listar_livros()

    for livro in livros:
        criar_card_livro(frame_lista, livro, "excluir")
    criar_button_voltar(frame_conteudo)

def mostrar_formulario_edicao(livro):      
    limpar_frame(frame_conteudo)
    frame_formulario = ctk.CTkScrollableFrame(
        master=frame_conteudo,
        fg_color="transparent"
    )

    frame_formulario.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )
    titulo_editar = ctk.CTkLabel(
        master=frame_formulario,
        text="Editar de Livro",
        font=("times new roman", 20, "bold")
    )
    titulo_editar.pack(pady=20)
    entry_titulo = criar_campo(frame_formulario, "Titulo:", livro[1])
    entry_autor = criar_campo(frame_formulario, "Autor:", livro[2])
    entry_status = criar_campo_selecao(frame_formulario, "Status:", ["Lido","Lendo","Não Lido"], livro[3])
    entry_paginas = criar_campo(frame_formulario, "Número de Páginas:", livro[4])
    entry_data = criar_campo(frame_formulario, "Data Leitura:", livro[5])
    entry_formato = criar_campo_selecao(frame_formulario,"Formato:",["Físico", "E-book"],livro[6])
    entry_anotacao = criar_campo_anotacao(frame_formulario, livro[7])
    entry_capa = criar_campo(frame_formulario, "Insira o Url imagem:", livro[8])

    botao_salvar = ctk.CTkButton(
    master=frame_formulario,
    text="Salvar",
    command=lambda: clicar_editar(livro[0], entry_titulo, entry_autor, entry_status, entry_paginas, entry_data, entry_formato, entry_anotacao, entry_capa))
    botao_salvar.pack(
        pady=(10, 15),
        padx=20,       
    )
    button_voltar_editar(frame_formulario)

def clicar_editar(id_livro, entry_titulo, entry_autor, entry_status, entry_paginas, entry_data, entry_formato, entry_anotacao, entry_capa):
    titulo = entry_titulo.get()
    autor = entry_autor.get()
    status = entry_status.get()
    paginas = entry_paginas.get()
    data = entry_data.get()
    formato = entry_formato.get()
    anotacao = entry_anotacao.get("1.0", "end").strip()
    capa = entry_capa.get()

    if not titulo.strip():
        mostrar_mensagem("❌Insira um Título!")
        return
        
    valido, mensagem = validar_paginas(paginas)
    if not valido:
        mostrar_mensagem(mensagem)
        return

    valido, mensagem = validar_data(data)
    if not valido:
        mostrar_mensagem(mensagem)
        return

    paginas = int(paginas)            

    editar_livro(id_livro, titulo, autor, status, paginas, data, formato, anotacao, capa)

    mostrar_mensagem(f"✔Livro {titulo} Editado com Sucesso!")
    
def mostrar_mensagem(mensagem):
    limpar_frame(frame_menu)
    label_validacao = ctk.CTkLabel(
                master=frame_menu,
                text=mensagem,
                font=("times new roman", 20, "bold")
            )
    label_validacao.pack(pady=20)    

# def validar_paginas(paginas):
#     if not paginas.strip():
#         return False, "❌ Insira Páginas do Livro!"

#     if not paginas.isdigit():
#         return False, "❌ Insira Apenas Número de Páginas!"

#     if int(paginas) <= 0:
#         return False, "❌ Número de Páginas não pode ser Zero!"

#     return True, ""

# def validar_data(data):
#     if not data.strip():
#         return True, ""

#     if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", data):
#         return False, "❌ Formato inválido! Use DD/MM/AAAA. Exemplo: 13/08/2026."

#     try:
#         datetime.strptime(data, "%d/%m/%Y")
#     except ValueError:
#         return False, "❌ Data inválida! Digite uma data existente."

#     return True, ""

# def validar_ano(ano):
#     if not ano.strip():
#         return False, "❌ Insira o ano!"
#     if not ano.isdigit():
#         return False, "❌ Insira apenas números no ano!"
#     if not len(ano) == 4:
#         return False, "❌ Insira o ano com 4 caracteres!"
#     return True, ""

def criar_campo(master, texto, valor=None):
    label = ctk.CTkLabel(
        master=master,
        text=texto,
        font=("times new roman", 12, "bold")
    )
    label.pack(pady=(15, 5))

    entry = ctk.CTkEntry(
        master=master
    )
    entry.pack(
        fill="x",
        pady=10,
        padx=30
    )

    if valor is not None:
        entry.insert(0, str(valor))
    return entry

def criar_campo_selecao(master, texto, opcoes, valor=None):
    label = ctk.CTkLabel(
        master=master,
        text=texto,
        font=("times new roman", 12, "bold")
    )
    label.pack(pady=(15, 5))

    campo_selecao = ctk.CTkComboBox(
        master=master,
        values=opcoes
    )
    campo_selecao.pack(
        fill="x",
        pady=10,
        padx=30
    )

    if valor:
        campo_selecao.set(valor)

    return campo_selecao

def criar_campo_anotacao(master, valor=None):
    label = ctk.CTkLabel(
        master=master,
        text="Anotações:",
        font=("times new roman", 12, "bold")
    )
    label.pack(pady=(15, 5))

    textbox = ctk.CTkTextbox(
        master=master
    )
    textbox.pack(
        fill="x",
        pady=10,
        padx=30
    )

    if valor is not None:
        textbox.insert("1.0", valor)
    return textbox    

def mostrar_tela_relatorio():
    limpar_frame(frame_conteudo)
    frame_formulario = ctk.CTkScrollableFrame(
        master=frame_conteudo,
        fg_color="transparent"
    )

    frame_formulario.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )
    titulo_cadastro = ctk.CTkLabel(
        master=frame_formulario,
        text="Relatório Anual",
        font=("times new roman", 20, "bold")
    )
    titulo_cadastro.pack(pady=20)

    entry_ano = criar_campo(frame_formulario, "Ano:")


    button_cadastrar = ctk.CTkButton(
        master=frame_formulario,
        text="Pesquisar",
        command=lambda: clicar_pesquisar_relatorio(entry_ano)
        
    )
    button_cadastrar.pack(
        pady=(10, 15),
        padx=20     
    )
    criar_button_voltar(frame_formulario)

def clicar_pesquisar_relatorio(entry_ano):
    ano = entry_ano.get()
    limpar_frame(frame_conteudo)

    frame_formulario = ctk.CTkScrollableFrame(
        master=frame_conteudo,
        fg_color="transparent"
    )
    
    frame_formulario.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    valido, mensagem = validar_ano(ano)
    if not valido:
        mostrar_mensagem(mensagem)
        mostrar_tela_relatorio()
        return
   

    quantidade, livros = relatorio_anual(ano)   
    if quantidade == 0:
        mostrar_mensagem(f"Nenhum Livro encontrado no ano {ano}!")
        mostrar_tela_relatorio()
        return 
    mostrar_mensagem(f"Quantidade de Livros Lidos no ano de {ano}: {quantidade}")
        
    for livro in livros:
            criar_card_livro(frame_formulario, livro)

    button_voltar(frame_conteudo,"Voltar",mostrar_tela_relatorio)

def pesquisar_livro_api():
    limpar_frame(frame_conteudo)
    titulo = criar_campo(frame_conteudo, "Insira Título: ")
    
    frame_lista = ctk.CTkScrollableFrame(
        master=frame_conteudo,
        fg_color="transparent"
    )

    frame_lista.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )
    botao_pesquisar = ctk.CTkButton(
        master=frame_conteudo,
        text="Pesquisar",
        command=lambda: executar_busca_api(
            titulo,
            frame_lista
        )
    )

    botao_pesquisar.pack(
        pady=(10, 15),
        padx=20 
        )   
    criar_button_voltar(frame_conteudo)

def executar_busca_api(entry_titulo, frame_lista):
    titulo = entry_titulo.get().strip()

    if not titulo:
        mostrar_mensagem("❌ Insira um Título!")
        return
    limpar_frame(frame_lista)

    livros_api = buscar_livros_api(titulo)

    if not livros_api:
        mostrar_mensagem(
            f"❌ Nenhum livro encontrado para: {titulo}"
        )
        button_voltar(frame_conteudo, "Voltar a Pesquisar", pesquisar_livro_api)
        return
    for livro in livros_api:
        criar_card_livro_api(
            frame_lista,
            livro,
            "adicionar"
        )

    # criar_button(frame_conteudo, pesquisar_livro_api)

def criar_imagem_capa(url_capa, tamanho=(100, 150)):
    if not url_capa:
        return None

    try:
        resposta = requests.get(url_capa, timeout=5)

        imagem_pil = Image.open(
            BytesIO(resposta.content)
        )

        return ctk.CTkImage(
            light_image=imagem_pil,
            dark_image=imagem_pil,
            size=tamanho
        )

    except Exception as erro:
        print(f"Erro ao carregar capa: {erro}")
        return None

botao_entrar = ctk.CTkButton(
    master=frame_menu,
    text="Entrar",
    height=40,
    command=mostrar_menu_principal
)
botao_entrar.pack(pady=20)

# Manter a janela aberta
def iniciar_interface():
    janela.mainloop()