import pathlib
import util
import os, json
import escolas_menus

pasta_jsons = pathlib.Path(__file__).parent / "Arquivos Json"

ARQUIVO_ESCOLAS = pasta_jsons / 'lista_de_escolas.json'
ARQUIVO_CREDES = pasta_jsons / 'lista_de_credes.json'


# Cadastro de Escolas protegido por senha de administrador
def adm_cadastro_escola():
    util.limpa_tela()
    util.cabecalho()

    print("\n- Cadastro Escola -\n")
    print("Apenas para usuários autorizados.\n")

    prosseguir = util.senha_administrador()

    if prosseguir:
        cadastro_escola()




# Cadastro de Escola
def cadastro_escola():
    util.limpa_tela()
    util.cabecalho()

    lista_escolas = carregar_escolas()


    print("\n- Cadastro Escola -\n")

    ########### BLOCO PRO CNPJ ###########
    cnpj = input("Digite o CNPJ da Escola: ")
    cnpj = util.padronizar_cnpj(cnpj)
    i = 0
    while i < 3:
            if cnpj is not None:
                break
            else:
                print("\nCNPJ inválido! Por favor, digite um CNPJ válido.\n")
                cnpj = input("Digite o CNPJ da Escola: ")
                cnpj = util.padronizar_cnpj(cnpj)
                i += 1
    if cnpj is None:
        print("Operação cancelada!")
        util.timer()
        return

    for cadastro in lista_escolas:
            if cadastro["cnpj"] == cnpj:
                print("CNPJ já cadastrado.")
                util.timer()
                return
    ############################################
    
    crede_vinculada = util.padronizar_cnpj(input("Digite o CNPJ da CREDE vinculada a esta escola: "))
    i = 0
    while i < 3:
        if crede_vinculada is not None:
            break
        else:
            print("\nCNPJ inválido! Por favor, digite um CNPJ válido.\n")
            crede_vinculada = input("Digite o CNPJ da CREDE: ")
            crede_vinculada = util.padronizar_cnpj(crede_vinculada)
            i +=1
    if crede_vinculada is None:
        print("Operação cancelada!")
        util.timer()
        return
    
    credes = util.carregar_dados(ARQUIVO_CREDES)
    crede_nao_cadastrada = True
    for crede_cadastrada in credes:
        if crede_vinculada == crede_cadastrada['cnpj']:
            crede_nao_cadastrada = False
            break
    if crede_nao_cadastrada:
        print("CREDE ainda não cadastrada!\nSua CREDE precisa estar cadastrada para usar o sistema.")
        util.timer()
        return

    nome = input("Digite o nome da Escola: ")
    email = input("Digite o email responsável: ")
    senha = input("Crie a senha de acesso: ")


    salt, senha_hash = util.gerar_hash_senha(senha)

    util.limpa_tela()
    util.cabecalho()

    print("\n- Confira os dados inseridos: -\n")
    print("CNPJ: {}".format(cnpj))
    print("Nome: {}".format(nome))
    print(f"Email: {email}")
    print("CREDE: {}".format(crede_vinculada))

    opcao = input("\nEscreva 1 para confirmar ou 0 para cancelar: \n")

    if opcao == '1':
        lista_escolas.append({
            "cnpj": cnpj,
            "nome": nome,
            "email": email,
            "crede": crede_vinculada,
            "salt": salt,
            "senha_hash": senha_hash
        })

        salvar_escolas(lista_escolas)

        print("\nCadastro realizado com sucesso!\n")
    
    elif opcao == '0':
        print("\nCadastro cancelado.\n")

    else:
        print("\nOpção inválida. Cadastro não realizado.\n")

    util.timer()








# Carrega os cadastros de Escolas
def carregar_escolas():
    if not os.path.exists(ARQUIVO_ESCOLAS):
        return []

    with open(ARQUIVO_ESCOLAS, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read().strip()

    if not conteudo:
        return []

    return json.loads(conteudo)






def salvar_escolas(escolas):
    with open(ARQUIVO_ESCOLAS, "w", encoding="utf-8") as arquivo:
        json.dump(
            escolas,
            arquivo,
            indent=4,
            ensure_ascii=False
        )




# Entrada da Escola
def entrar_escola():
    util.limpa_tela()
    util.cabecalho()

    print("\n- Entrar como Escola -\n")

    cnpj = input("Digite o CNPJ da Escola: ")
    cnpj = util.padronizar_cnpj(cnpj)
    while True:
            if cnpj is not None:
                break
            else:
                print("\nCNPJ inválido! Por favor, digite um CNPJ válido.\n")
                cnpj = input("Digite o CNPJ da Escola: ")
                cnpj = util.padronizar_cnpj(cnpj)
    senha = input("Digite a senha de acesso: ")
    lista_escolas = carregar_escolas()
    for cadastro in lista_escolas:
        if cadastro["cnpj"] == cnpj:
            if util.verificar_senha(
                senha,
                cadastro["salt"],
                cadastro["senha_hash"]
            ):
                print("\nLogin realizado com sucesso!\n")
                util.timer()
                escolas_menus.menu_principal(cnpj)
                return

    print("\nCNPJ ou senha incorretos! Tente novamente.\n")
    util.timer()
    return
