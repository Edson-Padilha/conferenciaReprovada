import cx_Oracle
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

usuario_oracle = os.getenv("ORACLE_USUARIO")
senha_oracle = os.getenv("ORACLE_SENHA")
email_remetente = os.getenv("REMETENTE")
senha_email = os.getenv("REMETENTE_SENHA")
servidor_smtp = os.getenv("SERVIDOR_SMTP")
porta_smtp = os.getenv("PORTA_SMTP")
servidor = os.getenv("SERVIDOR")
porta_servidor = os.getenv("PORTA_SERVIDOR")
name = os.getenv("NAME")
destinatario = os.getenv("DESTINATARIO")

print(usuario_oracle)
class ConexaoOracle:
    def __init__(self, usuario, senha, dsn):
        self.usuario = usuario
        self.senha = senha
        self.dsn = dsn
        self.conexao = None
    
    def conectar(self):
        try:
            self.conexao = cx_Oracle.connect(self.usuario, self.senha, self.dsn)
            return self.conexao
        except cx_Oracle.Error as erro:
            print(f"Erro ao conectar ao Oracle: {erro}")
            return None
    
    def desconectar(self):
        if self.conexao:
            self.conexao.close()

class ConferenciaXML:
    def __init__(self, conexao):
        self.conexao = conexao

    def consultar_conferencias(self):
        cursor = self.conexao.cursor()
        sql = """
            select f.nr_conferencia, f.dt_conferencia, f.nr_fatura, i.DS_CHAVEACESSO, i.DS_CAMPOCMP, i.DS_CAMPONF, i.CD_PRODUTO 
            from FIS_CONFC f
            join V_FIS_NFCONFC i on f.nr_fatura = i.NR_FATURA
            where f.cd_empresa = 2 and f.tp_situacao = 2 and f.dt_cadastro > '01/01/2025'
        """
        cursor.execute(sql)
        resultados = []
        for linha in cursor.fetchall():
            resultados.append({
                'nr_conferencia': linha[0],
                'dt_conferencia': linha[1],
                'nr_fatura': linha[2],
                'ds_chaveacesso': linha[3],
                'ds_campocmp': linha[4],
                'ds_camponf': linha[5],
                'cd_produto': linha[6]
            })
        return resultados
    
    def formatar_email(self, resultados):
        corpo_email ="""
            <html>
            <head><title>Conferências XML Reprovadas</title></head>
            <body>
                <h1>Conferências XML Reprovadas</h1>
                <p>Prezado Comprador,</p>
                <p>As seguintes conferências de XML foram reprovadas devido a divergências nos valores dos campos:</p>
                <table border="1">
                    <tr>
                        <th>Nr. Conferência</th>
                        <th>Dt. Conferência</th>
                        <th>Nr. Fatura</th>
                        <th>Chave Acesso</th>
                        <th>Código Produto</th>
                        <th>Valor CMP</th>
                        <th>Valor NF</th>
                    </tr>
        """
        for resultado in resultados:
            # Formata a data
            data_conferencia = resultado['dt_conferencia']
            data_formatada = data_conferencia.strftime("%d/%m/%Y")

            # Formata os valores
            valor_cmp = (resultado['ds_campocmp'])
            valor_nf = (resultado['ds_camponf'])

            corpo_email += f"""
                <tr>
                    <td>{resultado['nr_conferencia']}</td>
                    <td>{data_formatada}</td>
                    <td>{resultado['nr_fatura']}</td>
                    <td>{resultado['ds_chaveacesso']}</td>
                    <td>{resultado['cd_produto']}</td>
                    <td>{valor_cmp}</td>
                    <td>{valor_nf}</td>
                </tr>
        """
        corpo_email += """
            </table>
            <p>Por favor, verifique as divergências e tome as ações necessárias.</p>
            <p>E-mail automático.</p>
        </body>
        </html>
        """
        return corpo_email

class EmailSender:
    def __init__(self, email_remetente, senha_email, servidor_smtp,porta_smtp):
        self.email_remetente = email_remetente
        self.senha_email = senha_email
        self.servidor_smtp = servidor_smtp
        self.porta_smtp = porta_smtp
    
    def enviar_email(self, destinatario, assunto, corpo_email):
        msg = MIMEMultipart()
        msg['From'] = email_remetente
        msg['To'] = destinatario
        msg['Subject'] = assunto

        msg.attach(MIMEText(corpo_email, 'html'))

        try:
            servidor = smtplib.SMTP(servidor_smtp, porta_smtp)
            servidor.starttls()
            servidor.login(email_remetente, senha_email)
            texto = msg.as_string()
            servidor.sendmail(email_remetente, destinatario, texto)
            servidor.quit()
            print(f"E-mail enviado para {destinatario}")
        except Exception as erro:
            print(f"Erro ao enviar e-mail: {erro}")

dsn_oracle = cx_Oracle.makedsn(servidor, porta_servidor, service_name=name)

conexao_oracle = ConexaoOracle(usuario_oracle, senha_oracle, dsn_oracle)
conexao = conexao_oracle.conectar()

if conexao:
    conferencia_xml = ConferenciaXML(conexao)
    resultados = conferencia_xml.consultar_conferencias()

    if not resultados:
        print("Nenhuma conferência XML reprovada encontrada.")
        conexao_oracle.desconectar()
        exit()
        
    corpo_email = conferencia_xml.formatar_email(resultados)

    email_sender = EmailSender(email_remetente, senha_email, servidor_smtp, porta_smtp)
    email_sender.enviar_email(destinatario,'Conferências XML Reprovadas', corpo_email)

    conexao_oracle.desconectar()