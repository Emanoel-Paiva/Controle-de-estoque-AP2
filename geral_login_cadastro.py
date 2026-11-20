import util
import pathlib

pasta_jsons = pathlib.Path(__file__).parent / "Arquivos Json"

ARQUIVO_CREDE = pasta_jsons / 'lista_de_credes.json'
ARQUIVO_ESCOLAS = pasta_jsons / 'lista_de_escolas.json'

def menu_ajuda():
    util.limpa_tela()
    util.cabecalho()
    print("Bem-vindo ao menu de ajuda, o que você precisa?\n" \
    "" \
    "1 - Mudar Senha\n" \
    "2 - Mudar Email\n" \
    "0 - Voltar\n" \
    "")
    opcao = input('Selecione uma opção: ')

    if opcao == "1":
        mudar_senha()
    elif opcao == "2":
        mudar_email()
    elif opcao == "0":
        return
    else:
        print("Opção inválida!")
        util.timer()
        util.limpa_tela()


def escolher_tipo_usuario():
    usuario = input("Qual usuário deseja alterar?\n" \
    "1 - CREDE\n" \
    "2 - Escola\n" \
    "Digite um número: ")
    if usuario == "1":
        return ARQUIVO_CREDE
    elif usuario == "2":
        return ARQUIVO_ESCOLAS
    else:
        print("Opção inválida!")
        util.timer()
        return None

def encontra_usuario():
    arquivo_do_usuario = escolher_tipo_usuario()
    if arquivo_do_usuario is None:
        return None, None, None
    cnpj_do_usuario = util.padronizar_cnpj(input("Digite o CNPJ do usuário: "))
    if cnpj_do_usuario is not None:
        usuarios = util.carregar_dados(arquivo_do_usuario)
        for usuario in usuarios:
            if usuario["cnpj"] == cnpj_do_usuario:
                print(f"Usuário {usuario["nome"]},encontrado!")
                return arquivo_do_usuario, usuarios, usuario
    print(f"CNPJ não encontrado!")
    util.timer()
    return None, None, None


def mudar_senha():
    util.limpa_tela()
    util.cabecalho()
    permissao = util.senha_administrador()
    if not permissao:
        return
    
    arquivo_do_usuario, usuarios, usuario = encontra_usuario()
    if arquivo_do_usuario is None:
        return
      
    print("Digite a nova senha de acesso.")
    nova_senha = input("Nova senha: ")
    i = 0
    while i < 3 and nova_senha.strip() == "":
        print("A nova senha não pode ser vazia!")
        nova_senha = input("Nova senha: ")
        i += 1
    if nova_senha.strip() == "":
        print("Operação cancelada!")
        util.timer()
        return
    
    novo_salt, nova_senha_hash = util.gerar_hash_senha(nova_senha)
    confirma = input("Digite 1 pra confirmar e 0 para cancelar: ")
    
    if confirma != "1":
        print("Operação cancelada!")
        util.timer()
        return
    else:
        usuario["salt"] = novo_salt
        usuario["senha_hash"] = nova_senha_hash
        util.salvar_dados(arquivo_do_usuario, usuarios)
        print("Mudança feita com sucesso!")
        util.timer()
            
def mudar_email():
    util.limpa_tela()
    util.cabecalho()
    permissao = util.senha_administrador()
    if not permissao:
        return
    
    arquivo_do_usuario, usuarios, usuario = encontra_usuario()
    if arquivo_do_usuario is None:
        return
      
    print("Digite o novo email.")
    novo_email = input("Novo e-mail: ")
    
    confirma = input("Digite 1 pra confirmar e 0 para cancelar: ")
    
    if confirma != "1":
        print("Operação cancelada!")
        util.timer()
        return
    else:
        usuario["email"] = novo_email
        util.salvar_dados(arquivo_do_usuario, usuarios)
        print("Mudança feita com sucesso!")
        util.timer()
