import smtplib
import time
import random
import re
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_sender.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class MassEmailSender:
    def __init__(self):
        # Conta empresarial
        self.contas = [
            {
                "email": "secretariairpf@regularizacaoirpf2025online.site",
                "senha": "Sdnei841419@",
                "nome_empresa": "Receita Federal BR"
            },
        ]

        # Configurações SMTP (godaddy/ microsoft 365
        self.smtp_config = {
    "default": {
        "email": "secretariairpf@regularizacaoirpf2025online.site",
        "senha" : "Sdnei841419@",
        "host": "smtp.secureserver.net", 
        "port": 587,
        "user": 
        "secretariairpf@regularizacaoirpf2025online.site",
        "password": "Sdnei841419@",
        "encryption":"starttls",
}
}

        self.dominios_validos = {
            "gmail.com", "hotmail.com", "outlook.com", "live.com", "msn.com", "yahoo.com",
            "yahoo.com.br", "ymail.com", "rocketmail.com", "bol.com.br", "uol.com.br",
            "ig.com.br", "terra.com.br", "globo.com", "r7.com", "oi.com.br", "zipmail.com.br",
            "empresarial.com.br", "comercial.com.br", "negocio.com.br", "empresa.com",
            "company.com", "corp.com", "business.com",
            ".com.br", ".com", ".net", ".org", ".biz", ".info"
        }

        self.aceitar_todos_emails = True
        self.emails_enviados = 0
        self.emails_falharam = 0
        self.prazo_regularizacao = (datetime.now() + timedelta(days=3)).strftime("%d/%m/%Y")

        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        ]

    def get_smtp_config(self, email):
        dominio = email.split('@')[-1].lower()
        return self.smtp_config.get(dominio, self.smtp_config["default"])

    def detectar_formato_arquivo(self, linha_exemplo):
        partes = linha_exemplo.strip().split(',')
        if len(partes) >= 2:
            primeiro = partes[0].strip()
            segundo = partes[1].strip()
            if '@' in primeiro and '.' in primeiro:
                return 'email_primeiro'
            elif '@' in segundo and '.' in segundo:
                return 'nome_primeiro'
        return 'nome_primeiro'

    def processar_arquivo_txt(self, caminho_arquivo):
        if not os.path.exists(caminho_arquivo):
            logging.error(f"Arquivo não encontrado: {caminho_arquivo}")
            return []
        pessoas = []
        formato_detectado = None
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                linhas = arquivo.readlines()
                for linha in linhas:
                    if linha.strip() and ',' in linha:
                        formato_detectado = self.detectar_formato_arquivo(linha)
                        break
                logging.info(f"Formato detectado: {'Email,Nome' if formato_detectado == 'email_primeiro' else 'Nome,Email'}")
                for i, linha in enumerate(linhas, 1):
                    linha = linha.strip()
                    if not linha or ',' not in linha:
                        continue
                    try:
                        partes = [p.strip() for p in linha.split(',')]
                        if len(partes) < 2:
                            continue
                        if formato_detectado == 'email_primeiro':
                            email = partes[0]
                            nome = partes[1] if len(partes) > 1 else "Cliente"
                        else:
                            nome = partes[0]
                            email = partes[1] if len(partes) > 1 else ""
                        if self.validar_email_basico(email):
                            pessoas.append({"nome": nome, "email": email})
                        else:
                            logging.warning(f"Email inválido na linha {i}: {email}")
                    except Exception as e:
                        logging.warning(f"Erro na linha {i}: {linha} - {e}")
                        continue
            logging.info(f"{len(pessoas)} emails válidos carregados do arquivo")
            return pessoas
        except Exception as e:
            logging.error(f"Erro ao processar arquivo: {e}")
            return []

    def validar_email_basico(self, email):
        if not email or '@' not in email:
            return False
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(padrao, email):
            return False
        if self.aceitar_todos_emails:
            return True
        try:
            dominio = email.split("@")[-1].lower()
            return any(dominio == d or dominio.endswith(d) for d in self.dominios_validos)
        except Exception:
            return False

    def gerar_protocolo_aleatorio(self):
        protocolo = f"85563{random.randint(100000, 999999)}"
        return {
            "protocolo": protocolo,
            "valor_darf": "R$172,20",
            "assunto": f"Aviso de Irregularidade Protocolo - IRPF Nº {protocolo}"
        }

    def criar_mensagem_html(self, nome, dados_protocolo):
        saudacoes = ["Prezado.(a)", "Caro(a)", "Sr.(a)"]
        orgao = random.choice(["Receita Federal do Brasil", "Receita Federal", "RFB"])
        return f"""
        <html>
        <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="font-family: Arial, sans-serif; background-color: #f6f6f6; margin: 0; padding: 0;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 20px;">
        <div style="text-align: center;">
        <a href="https://imgbb.com/"><img src="https://i.ibb.co/S41cPQVJ/Imagem-do-gov.jpg" alt="Imagem-do-gov" border="0"></a>
        <div style="background-color: #0c3c72; color: white; padding: 18px; border-radius: 10px;">
        <p style="margin-top: 0;">{random.choice(saudacoes)} {nome},</p>
        <p>Informamos que foram identificadas pendências vinculadas ao seu CPF junto à Receita Federal, em razão do não recolhimento de tributos obrigatórios.</p>
        <p>Essa situação pode gerar restrições em diversos serviços, incluindo:</p>
        <ul>
        <li>Emissão de passaporte</li>
        <li>Solicitação de financiamentos</li>
        <li>Participação em concursos públicos</li>
        <li>Abertura de contas bancárias</li>
        </ul>
        <p>Além disso, podem ser aplicadas multas e encargos adicionais conforme a legislação vigente.</p>
        <p>Caso já tenha realizado o pagamento, desconsidere esta mensagem.</p>
        <p>Atenciosamente,<br>{orgao},<br>Governo Federal.</p>
        </div>
        <div style="margin-top: 20px;">
        <p><strong>- Situação do seu CPF:</strong> Irregular</p>
        <p><strong>- Valor do DARF 2025:</strong> {dados_protocolo["valor_darf"]}</p>
        <p><strong>- Prazo para regularização:</strong> {self.prazo_regularizacao}</p>
        <p><strong>- Protocolo:</strong> {dados_protocolo["protocolo"]}</p>
        </div>
        <div style="text-align: center; margin-top: 30px;">
        <a href="https://ibb.co/35GM2nQX"><img src="https://i.ibb.co/hxhZbSw5/imagem-receita-fed.jpg" alt="imagem-receita-fed" border="0"></a>
        </div>
        <div style="text-align: center; margin-top: 20px;">
        <table role="presentation" style="margin: auto;">
        <tr>
        <td>
        <a href="https://regularizacaoirpf2025online.site/" style="background-color: #28a745; color: white; padding: 15px 25px; text-decoration: none; border-radius: 5px; font-size: 16px; display: inline-block;"> REALIZAR CONSULTA </a>
        </td>
        </tr>
        </table>
        </div>
        <p style="text-align: center; margin-top: 10px; font-weight: bold;">CLIQUE NO BOTÃO ACIMA PARA CONSULTAR</p>
        <hr>
        <p style="font-size: 11px; color: gray; text-align: center;">
        Esta é uma mensagem automática. Por favor, não responda.
        </p>
        </div>
        </body>
        </html>
        """

    def enviar_email(self, conta, pessoa):
        email = conta["email"]
        senha = conta["senha"]
        nome_empresa = conta["nome_empresa"]
        smtp_conf = self.get_smtp_config(email)
        host = smtp_conf["host"]
        port = smtp_conf["port"]

        protocolo_info = self.gerar_protocolo_aleatorio()
        assunto = protocolo_info["assunto"]

        mensagem = MIMEMultipart("alternative")
        mensagem["From"] = f"{nome_empresa} <{email}>"
        mensagem["To"] = pessoa["email"]
        mensagem["Subject"] = assunto
        mensagem.attach(MIMEText(self.criar_mensagem_html(pessoa["nome"], protocolo_info), "html"))

        try:
            server = smtplib.SMTP(host, port)
            server.starttls()
            server.login(email, senha)
            server.sendmail(email, pessoa["email"], mensagem.as_string())
            server.quit()
            self.emails_enviados += 1
            logging.info(f"Email enviado para: {pessoa['email']}")
            return True
        except Exception as e:
            self.emails_falharam += 1
            logging.error(f"Falha ao enviar para {pessoa['email']}: {e}")
            return False

    def enviar_em_lote(self, lista_pessoas, delay=30, max_threads=5):
        total = len(lista_pessoas)
        logging.info(f"Iniciando envio para {total} destinatários...")

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = []
            for pessoa in lista_pessoas:
                conta = random.choice(self.contas)
                futures.append(executor.submit(self.enviar_email, conta, pessoa))
                time.sleep(delay)
            for future in as_completed(futures):
                future.result()

        logging.info(
            f"Envio finalizado. Enviados: {self.emails_enviados}, "
            f"Falhas: {self.emails_falharam}"
        )

# ---- fora da classe ----
def main():
    sender = MassEmailSender()
    lista = sender.processar_arquivo_txt("emails.txt")

    if lista:
        sender.enviar_em_lote(lista, delay=50, max_threads=5)
    else:
        print("Lista de destinatários vazia. Nada a enviar.")


if __name__ == "__main__":
    main()
