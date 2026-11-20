import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()
EMAIL_REMETENTE = os.getenv("EMAIL_REMETENTE")
SENHA_APP = os.getenv("SENHA_APP")
SMTP_SERVER = "smtp.gmail.com"
PORT = 587





def enviar_relatorio(destinatario, caminho_pdf, nome_escola, cnpj_da_escola):
    if not EMAIL_REMETENTE or not SENHA_APP:
        print("\nErro: Configurações de e-mail não encontradas no arquivo .env")
        return
    
    msg = EmailMessage()
    msg["Subject"] = f"Relatório Escolar - {nome_escola}"
    msg["From"] = EMAIL_REMETENTE
    msg["To"] = destinatario

    texto_mensagem = f"""Olá!

Segue em anexo o relatório escolar atualizado referente à instituição: {nome_escola} de CNPJ: {cnpj_da_escola}.
Documento gerado automaticamente pelo Estoque Escolar Unificado - EEU.

Atenciosamente,
Equipe de Suporte"""

    msg.set_content(texto_mensagem)

    try:
        with open(caminho_pdf, "rb") as arquivo:
            dados_arquivo = arquivo.read()
            nome_arquivo = caminho_pdf.name

            msg.add_attachment(
                dados_arquivo,
                maintype="application",
                subtype="pdf",
                filename=nome_arquivo
            )
    except Exception as e:
        print(f"\nErro ao carregar o arquivo PDF: {e}")
        return

    try:
        print("\nConectando ao servidor de e-mail e enviando...")
        with smtplib.SMTP(SMTP_SERVER, PORT) as server:
            server.starttls()
            server.login(EMAIL_REMETENTE, SENHA_APP)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"\nErro ao enviar o e-mail: {e}")
        return