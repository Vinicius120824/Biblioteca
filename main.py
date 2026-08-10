from funcoes.operacoes import cadastrar_livro
from funcoes.operacoes import listar_livros
from funcoes.operacoes import editar_livro
from funcoes.operacoes import excluir_livro
from funcoes.operacoes import buscar_livro_id
from funcoes.operacoes import buscar_livro_por_titulo

def ler_numero(mensagem):
    while True:

        texto = input(mensagem)

        if texto.isdigit():
            return int(texto)
        else:
            print("Digite apenas números!")
def menu():
    print("==================")
    print("   Biblioteca")
    print("==================")
    print("1 - Cadastrar Livro")
    print("2 - Listar Livro")
    print("3 - Editar Livro")
    print("4 - Excluir Livro")
    print("5 - Buscar Livro pelo Título")
    print("0 - Sair")
def mostrar_livro(livro):
        print("-" * 30)
        print("ID: ", livro[0])
        print("Título: ", livro[1])
        print("Autor: ", livro[2])
        print("Status: ", livro[3])
        print("Numero de Paginas: ", livro[4])
        print("Data de Leitura: ", livro[5])

while True:
    menu()
    opcao = input("Escolha uma opção: ")
############## CADASTRAR LIVROS ########################################
    if opcao == "1":
        titulo = input("Titulo do Livro: ")
        autor = input("Autor do Livro: ")
        status = input("Status: ")        
        numero_paginas = input("Número de Paginas: ")
        data_leitura = input("Data Leitura: ")        
        cadastrar_livro(titulo, autor, status, numero_paginas, data_leitura)
        
        busca = buscar_livro_por_titulo(titulo)
        if busca:
            for livro in busca:
                print("Livro Cadastrado com Sucesso!")
                print("\nLivro Cadastrado:")
                mostrar_livro(livro)

############## LISTAR LIVROS ##############################################
    elif opcao == "2":
        livros = listar_livros()
        for livro in livros:
            mostrar_livro(livro)
            print("=" * 30)           
############### EDITAR LIVROS ##############################################
    elif opcao == "3":
        #Listar os Livros
        print()
        print("Livros que você tem para Editar!!")
        print("=" * 30)
        livros = listar_livros()
        for livro in livros:
            mostrar_livro(livro)
            print("=" * 30)
        
        id_livro = ler_numero("Qual ID deseja alterar?: ")
        livro = buscar_livro_id(id_livro)
        if livro: 
            novo_titulo = input("Novo título (Pressione ENTER para manter): ")

            novo_autor = input("Novo autor (Pressione ENTER para manter): ")

            novo_status = input("Novo status (Pressione ENTER para manter): ")

            novo_numero_paginas = input("Novo Numero de Paginas (Pressione ENTER para manter): ")

            nova_data_leitura = input("Nova Data da Leitura (Pressione ENTER para manter): ")
            print()

            atualizou = editar_livro(id_livro, novo_titulo, novo_autor, novo_status, novo_numero_paginas, nova_data_leitura)
            if atualizou:
                livro_atualizado = buscar_livro_id(id_livro)

                print("Livro Atualizado com sucesso!")
                print("\nLivro Atualizado:")
                mostrar_livro(livro)
                print("=" * 30)
        else:
            print("Livro não encontrado!")
######################## EXLUIR LIVROS ##############################################
    elif opcao == "4":
        print("=" *30)
        print("Esta é a lista de livros para EXCLUIR!")
        livros = listar_livros()
        for livro in livros:
            mostrar_livro(livro)
            print("=" * 30)
        id_livro = ler_numero("Qual ID deseja Excluir?:")
        resposta = input ("Deseja excluir S/N: ")
        resultado = excluir_livro(id_livro, resposta)

        if resultado == "excluido":
            print("Livro excluido com sucesso!")
        elif resultado == "cancelado":
            print("Operação cancelada!")
        elif resultado == "nao_encontrado":
            print("Livro não encontrado!")
############### BUSCAR LIVRO ##############################################
    elif opcao == "5":
        titulo = input("Digite o titulo do livro: ")
        busca = buscar_livro_por_titulo(titulo)
        if busca:
            for livro in busca:
                mostrar_livro(livro)
        else:
            print("Livro não encontrado!")

############ ENCERRAR PROGRAMA ##############################################
    elif opcao == "0":
        print("Até logo!")
        break

    else:
        print("Opção Inválida!")
        print("Tente novamente>>>>")