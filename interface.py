import customtkinter as ctk
from funcoes.operacoes import cadastrar_livro
from funcoes.operacoes import listar_livros
from funcoes.operacoes import buscar_livro_id
from funcoes.operacoes import buscar_livro_por_titulo
from funcoes.operacoes import editar_livro
from funcoes.operacoes import excluir_livro

# Configuração da aparência
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")

# Criar a janela
janela = ctk.CTk()

frame_principal = ctk.CTkFrame(
    master=janela
)

frame_principal.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)

frame_titulo = ctk.CTkFrame(
    master=frame_principal,
    fg_color="transparent"
)

frame_titulo.pack(
    fill="x",
    pady=(20, 10)
)

frame_menu =ctk.CTkFrame(
    master=frame_principal,
    fg_color="transparent"
)

frame_menu.pack(
    fill="x",
    pady=20
)

frame_conteudo = ctk.CTkFrame(
    master=frame_principal,
    fg_color="transparent"
)

frame_conteudo.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)


# Configurações da janela
janela.title("Biblioteca")
janela.geometry("800x600")

titulo = ctk.CTkLabel(
    master=frame_titulo,
    text="Seu Mundinho!",
    font=("times new roman", 28, "bold")
)

titulo.pack(pady=40)

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
        ("Excluir", mostrar_tela_excluir)
    ]

    mensagem = ctk.CTkLabel(
        master=frame_conteudo,
        text="Menu do seu Mundinho Biblioteca!!",
        font=("times new roman", 14, "bold")
    )
    mensagem.pack(pady=20)

    for texto, funcao in opcoes:
        botoes = ctk.CTkButton(
            master=frame_conteudo,
            text=texto,
            command=funcao
        )
        botoes.pack(
        pady=(10, 15),
        padx=20  
        )

def mostrar_tela_cadastro():
    limpar_frame(frame_conteudo)

    titulo_cadastro = ctk.CTkLabel(
        master=frame_conteudo,
        text="Cadastro de Livro",
        font=("times new roman", 20, "bold")
    )
    titulo_cadastro.pack(pady=20)
    entry_titulo = criar_campo(frame_conteudo, "Titulo:")
    entry_autor = criar_campo(frame_conteudo, "Autor:")
    entry_status = criar_campo_status(frame_conteudo)
    entry_paginas = criar_campo(frame_conteudo, "Número de Páginas:")
    entry_data = criar_campo(frame_conteudo, "Data Leitura:")

    button_cadastrar = ctk.CTkButton(
        master=frame_conteudo,
        text="Cadastrar",
        command=lambda: clicar_cadastrar(entry_titulo, entry_autor, entry_status, entry_paginas, entry_data)
        
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

def clicar_cadastrar(entry_titulo, entry_autor, entry_status, entry_paginas, entry_data):
    titulo = entry_titulo.get()
    autor = entry_autor.get()
    status = entry_status.get()
    paginas = entry_paginas.get()
    data = entry_data.get()

    if not titulo.strip():
        mostrar_mensagem("❌ Insira um Título!")
        return
        
    valido, mensagem = validar_paginas(paginas)

    if not valido:
        mostrar_mensagem(mensagem)
        return

    paginas = int(paginas)           

    cadastrar_livro(titulo,autor,status,paginas,data)
    
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

def mostrar_tela_buscar():
    limpar_frame(frame_conteudo)

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
        pady=20
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

def criar_card_editar(frame_lista, livro):
    criar_card_livro(frame_lista, livro, "editar")

def criar_card_excluir(frame_lista, livro):
    criar_card_livro(frame_lista, livro, "excluir")

def mostrar_confirmacao_exclusao(livro):
    limpar_frame(frame_conteudo)

    label_confirmacao = ctk.CTkLabel(
    master=frame_conteudo,
    text=f"Tem Certeza que deseja excluir: {livro[1]}",
    font=("times new roman", 40, "bold")
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
        font=("times new roman", 20, "bold")
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
        criar_card_editar(frame_lista, livro)

    criar_button_voltar(frame_conteudo)

def mostrar_tela_excluir():
    limpar_frame(frame_conteudo)
  
    label_livros = ctk.CTkLabel(
    master=frame_conteudo,
    text="Meus Livros",
    font=("times new roman", 40, "bold")

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
        criar_card_excluir(frame_lista, livro)
    criar_button_voltar(frame_conteudo)

def mostrar_formulario_edicao(livro):
    limpar_frame(frame_conteudo)

    titulo_editar = ctk.CTkLabel(
        master=frame_conteudo,
        text="Editar de Livro",
        font=("times new roman", 20, "bold")
    )
    titulo_editar.pack(pady=20)
    entry_titulo = criar_campo(frame_conteudo, "Titulo:", livro[1])
    entry_autor = criar_campo(frame_conteudo, "Autor:", livro[2])
    entry_status = criar_campo_status(frame_conteudo, livro[3])
    entry_paginas = criar_campo(frame_conteudo, "Número de Páginas:", livro[4])
    entry_data = criar_campo(frame_conteudo, "Data Leitura:", livro[5])

    botao_salvar = ctk.CTkButton(
    master=frame_conteudo,
    text="Salvar",
    height=20,
    command=lambda: clicar_editar(livro[0], entry_titulo, entry_autor, entry_status, entry_paginas, entry_data)
    )
    botao_salvar.pack(pady=20)
    button_voltar_editar(frame_conteudo)

def clicar_editar(id_livro, entry_titulo, entry_autor, entry_status, entry_paginas, entry_data):
    titulo = entry_titulo.get()
    autor = entry_autor.get()
    status = entry_status.get()
    paginas = entry_paginas.get()
    data = entry_data.get()

    if not titulo.strip():
        mostrar_mensagem("❌Insira um Título!")
        return
        
    valido, mensagem = validar_paginas(paginas)

    if not valido:
        mostrar_mensagem(mensagem)
        return

    paginas = int(paginas)            

    editar_livro(id_livro, titulo, autor, status, paginas, data)

    mostrar_mensagem(f"✔Livro {titulo} Editado com Sucesso!")
    
def mostrar_mensagem(mensagem):
    limpar_frame(frame_menu)
    label_validacao = ctk.CTkLabel(
                master=frame_menu,
                text=mensagem,
                font=("times new roman", 20, "bold")
            )
    label_validacao.pack(pady=20)    

def validar_paginas(paginas):
    if not paginas.strip():
        return False, "❌ Insira Páginas do Livro!"

    if not paginas.isdigit():
        return False, "❌ Insira Apenas Número de Páginas!"

    if int(paginas) <= 0:
        return False, "❌ Número de Páginas não pode ser Zero!"

    return True, ""

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

def criar_campo_status(master, valor=None):
    label = ctk.CTkLabel(
        master=master,
        text="Status:",
        font=("times new roman", 12, "bold")
    )
    label.pack(pady=(15, 5))

    combo_status = ctk.CTkComboBox(
        master=master,
        values=["Lido", "Lendo", "Não Lido"]
    )
    combo_status.pack(
        fill="x",
        pady=10,
        padx=30
    )

    if valor:
        combo_status.set(valor)

    return combo_status

botao_entrar = ctk.CTkButton(
    master=frame_menu,
    text="Entrar",
    height=40,
    command=mostrar_menu_principal
)
botao_entrar.pack(pady=20)

# Manter a janela aberta
janela.mainloop()