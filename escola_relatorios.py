import pathlib
from datetime import datetime
from fpdf import FPDF
import escolas_menus
import util
import envia_emails

pasta_jsons = pathlib.Path(__file__).parent / "Arquivos Json"
pasta_pdfs = pathlib.Path.home() / "Downloads"

ARQUIVO_ESTOQUE = pasta_jsons / "lista_de_estoques_escolares.json"
ARQUIVO_RETIRADAS = pasta_jsons / "lista_de_historico_retiradas.json"
ARQUIVO_ESCOLAS = pasta_jsons / "lista_de_escolas.json"
ARQUIVO_CREDES = pasta_jsons / "lista_de_credes.json"

def _obter_nome_escola(cnpj_escola):
    escolas = escolas_menus.carregar_dados(ARQUIVO_ESCOLAS)
    if isinstance(escolas, list):
        for escola in escolas:
            if escola.get("cnpj") == cnpj_escola:
                return escola.get("nome", "Escola")
    return "Escola"

def obter_email_crede(cnpj_escola):
    escolas = escolas_menus.carregar_dados(ARQUIVO_ESCOLAS)
    cnpj_crede_da_escola = None
    if isinstance(escolas, list):
        for escola in escolas:
            if escola.get("cnpj") == cnpj_escola:
                cnpj_crede_da_escola = escola.get("crede")
                break
    credes = escolas_menus.carregar_dados(ARQUIVO_CREDES)
    if isinstance(credes, list):
            for crede in credes:
                if crede.get("cnpj") == cnpj_crede_da_escola:
                    return crede.get("email")
    return None

def _adicionar_tabela_estoque(pdf, cnpj_escola):
    estoques = escolas_menus.carregar_dados(ARQUIVO_ESTOQUE)
    itens = estoques.get(cnpj_escola, [])

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "1. Estoque Atual", ln=True)

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(20, 8, "ID", border=1)
    pdf.cell(65, 8, "Produto", border=1)
    pdf.cell(45, 8, "Categoria", border=1)
    pdf.cell(25, 8, "Qtd.", border=1)
    pdf.cell(35, 8, "Validade", border=1, ln=True)

    pdf.set_font("Helvetica", "", 10)
    if not itens:
        pdf.cell(190, 8, "Nenhum produto cadastrado no estoque.", border=1, ln=True, align="C")
    else:
        for item in itens:
            pdf.cell(20, 8, f"{item['id']:03d}", border=1)
            pdf.cell(65, 8, str(item["nome"])[:30], border=1)
            pdf.cell(45, 8, str(item["categoria"])[:20], border=1)
            pdf.cell(25, 8, str(item["quantidade"]), border=1)
            pdf.cell(35, 8, str(item["validade"]), border=1, ln=True)
    pdf.ln(8)


def _adicionar_tabela_retiradas(pdf, cnpj_escola):
    retiradas = escolas_menus.carregar_dados(ARQUIVO_RETIRADAS)
    lista_retiradas = retiradas.get(cnpj_escola, [])

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "2. Histórico de Retiradas", ln=True)

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(25, 8, "ID Ret.", border=1)
    pdf.cell(25, 8, "ID Prod.", border=1)
    pdf.cell(65, 8, "Produto", border=1)
    pdf.cell(45, 8, "Setor", border=1)
    pdf.cell(30, 8, "Qtd. Retirada", border=1, ln=True)

    pdf.set_font("Helvetica", "", 10)
    if not lista_retiradas:
        pdf.cell(190, 8, "Nenhuma retirada registrada.", border=1, ln=True, align="C")
    else:
        for reg in lista_retiradas:
            pdf.cell(25, 8, f"{reg['id']:03d}", border=1)
            pdf.cell(25, 8, f"{reg['id_produto']:03d}", border=1)
            pdf.cell(65, 8, str(reg["nome_produto"])[:30], border=1)
            pdf.cell(45, 8, str(reg["setor"])[:20], border=1)
            pdf.cell(30, 8, str(reg["quantidade_retirada"]), border=1, ln=True)


def menu_baixar_pdf(cnpj_escola_logada):
    util.limpa_tela()
    print("\n--- Gerar Relatório em PDF ---")
    print("1 - Baixar PDF apenas do Estoque")
    print("2 - Baixar PDF apenas das Retiradas")
    print("3 - Baixar PDF Completo (Estoque + Retiradas)")
    print("0 - Voltar")

    opcao = input("\nEscolha uma opção: ").strip()
    if opcao == "0":
        util.limpa_tela()
        return
    if opcao not in ("1", "2", "3"):
        print("\nOpção inválida.")
        util.timer()
        util.limpa_tela()
        return

    pasta_pdfs.mkdir(parents=True, exist_ok=True)
    nome_escola = _obter_nome_escola(cnpj_escola_logada)
    data_hora = datetime.now().strftime("%d/%m/%Y às %H:%M")
    timestamp_arquivo = datetime.now().strftime("%Y%m%d_%H%M%S")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"Relatório Escolar - {nome_escola}", ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, f"CNPJ: {cnpj_escola_logada} | Gerado em: {data_hora}", ln=True, align="C")
    pdf.ln(8)

    if opcao == "1":
        _adicionar_tabela_estoque(pdf, cnpj_escola_logada)
        tipo = "estoque"
    elif opcao == "2":
        _adicionar_tabela_retiradas(pdf, cnpj_escola_logada)
        tipo = "retiradas"
    else:
        _adicionar_tabela_estoque(pdf, cnpj_escola_logada)
        _adicionar_tabela_retiradas(pdf, cnpj_escola_logada)
        tipo = "completo"

    caminho_pdf = pasta_pdfs / f"relatorio_{tipo}_{cnpj_escola_logada}_{timestamp_arquivo}.pdf"
    pdf.output(str(caminho_pdf))

    print(f"\nPDF gerado com sucesso!")
    print(f"Salvo em: {caminho_pdf.resolve()}")
    
    
    ### ESSA PARTE MANDA EMAILS PARA CREDE OU ESCOLA CASO O USUÁRIO QUEIRA
    mandar_email = input("\nPressione Enter para voltar ao menu.\nOu digite 1 para enviar esse relatório por email para a CREDE: ").strip()
    if mandar_email != "1":
        util.limpa_tela()
        return

    
    email_da_crede = obter_email_crede(cnpj_escola_logada)

    if email_da_crede:
            sucesso = envia_emails.enviar_relatorio(email_da_crede, caminho_pdf, nome_escola, cnpj_escola_logada)
            if sucesso:
                print("\nE-mail enviado para a CREDE com sucesso!")
            else:
                print("\nHouve um erro ao enviar o e-mail.")
    else:
        print("\nE-mail da CREDE não encontrado para esta escola.")
            
    input("\nPressione Enter para continuar...")
    util.limpa_tela()