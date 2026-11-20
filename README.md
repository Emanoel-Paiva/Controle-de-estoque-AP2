# Sistema de Controle de Estoque Escolar - CREDE

Este projeto é um sistema de gerenciamento de estoque desenvolvido para a rede municipal de ensino (com foco inicial no município de Juazeiro do Norte). Ele conecta as escolas municipais à CREDE, digitalizando e otimizando o controle de materiais para garantir transparência e eficiência no uso do dinheiro público.

## Objetivo do Projeto

Atualmente, o controle de estoque em muitas escolas públicas é feito de forma manuscrita, o que abre margem para erros de contagem, perda de produtos por vencimento e desvio de materiais. 

O objetivo principal deste sistema é **manter o estoque de materiais atualizado**, evitando desperdícios e desvios de verbas. Através da plataforma, é possível:
* Rastrear a entrada e saída de produtos (incluindo quem solicitou a retirada).
* Monitorar a validade dos itens.
* Agilizar o processo de compras por meio do envio de pesquisas de preço para aprovação da CREDE.

## Funcionalidades

O sistema é dividido em dois módulos principais, atendendo às necessidades de cada nível da administração:

### Módulo das Escolas (Colégios)
* **Entrada de produtos:** Registro detalhado dos materiais recebidos.
* **Saídas de produtos:** Controle de retirada com identificação do solicitante.
* **Solicitações à CREDE:** Funcionalidade para encaminhar pesquisas de preços e solicitar a compra de novos materiais com o recurso destinado à escola.
* **Relatórios em PDF:** Geração de relatórios do estoque e do histórico de retiradas, com opção de envio por e-mail para a CREDE.
* **Sistema de Alertas *(planejado, ainda não implementado)*:** Notificações automáticas para **estoque mínimo** e **produtos próximos ao vencimento**.

### Módulo da CREDE
* **crede_autorizacao:** Análise das pesquisas de preço enviadas pelas escolas e indicação/autorização dos locais de compra.
* **crede_fiscalizacao:** Acesso em tempo real ao inventário de cada colégio da rede.
* **crede_login_e_cadastro:** Capacidade de entrar em CREDEs já existentes e criar novas.
* **crede_menus:** Apresentação das ações da CREDE.
* **Arquivos Json/lista_de_credes.json:** Armazenamento das credenciais das CREDEs.

### Ajuda
* **geral_login_cadastro:** Alteração de senha e de e-mail de CREDEs e escolas (requer a senha de administrador).

## Benefícios Esperados

* **Para as Escolas:** Maior agilidade e resposta rápida nas futuras compras de materiais de uso diário.
* **Para a CREDE:** Maior controle sobre o uso das verbas públicas, auditoria facilitada e garantia de um melhor investimento financeiro.
* **Para a Sociedade:** Transparência, redução de desperdícios e melhoria na infraestrutura de suporte à educação.


## Bibliotecas
* Para gerar os PDFs, é necessário instalar o **fpdf2**. No terminal: `pip install fpdf2`
  * Se a biblioteca antiga `fpdf` estiver instalada, remova-a antes (`pip uninstall fpdf`), pois as duas usam o mesmo nome de importação.
* Para enviar os relatórios por e-mail, é necessário instalar o **python-dotenv**. No terminal: `pip install python-dotenv`

## Configuração do e-mail
O envio de relatórios por e-mail lê as credenciais de um arquivo `.env` na pasta do projeto (esse arquivo não vai para o Git):

```
EMAIL_REMETENTE = seu_email@gmail.com
SENHA_APP = sua_senha_de_app_do_gmail
```

A `SENHA_APP` é uma senha de app gerada na conta Google, não a senha normal do e-mail.

## Como executar
Na pasta do projeto, rode no terminal:

```
python main.py
```

**Ordem de cadastro:** cadastre primeiro a CREDE. Ao cadastrar uma escola, o sistema pede o CNPJ da CREDE vinculada e só aceita uma CREDE que já esteja cadastrada.
