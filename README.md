# conferenciaReprovada
Este projeto automatiza o envio de e-mails de notificação para compradores sobre conferências XML reprovadas no ERP TOTVS Moda, utilizando um banco de dados Oracle.

## Descrição

O script Python realiza as seguintes tarefas:

1. Conecta-se a um bloco de dados Oracle para consultar conferências XML reprovadas, listadas no componente FISFC063.
2. Formata os dados das conferências reprovadas em um e-mail HTML.
3. Envia o e-mail para os compradores.
4. Agenda a execução da rotina para ser executada a cada 1 hora usando Agendador de tarefas do Windows.

## Pré-requisitos

* Python 3.x
* Conta de e-mail SMTP para envio de e-mails.
* Acesso a um banco de dados Oracle.

## Instalação

1. Clone o repositório: 
```bash
https://github.com/Edson-Padilha/conferenciaReprovada.git
```

2. Crie um ambiente virtual (recomendado):

```bash
python -m venv env
```

3. Ative o ambiente virtual:
    
    * No Windows:
        
        ```bash
        venv\Scripts\activate
        ```

4. Instale as dependências:

```bash
pip install -r requirements.txt
```

5. Crie um arquivo '.env' na raiz do projeto com as seguintes variáveis de ambiente:
    
    ```
    ORACLE_USUARIO=<seu_usuario_oracle>
    ORACLE_SENHA=<sua_senha_oracle>
    ORACLE_DSN=<seu_dsn_oracle>
    EMAIL_REMETENTE=<seu_email_remetente>
    SENHA_EMAIL=<sua_senha_email>
    SERVIDOR_SMTP=<seu_servidor_smtp>
    PORTA_SMTP=<sua_porta_smtp>
    ```

    * Substitua os valores entre '<>' pelas suas credenciais.
    * Adicione o arquivo '.env' ao '.gitignore' para evitar o envio de informações sensíveis para o repositório.

## Configuração
1. Configure as variáveis de ambiente no arquivo '.env'.
2. Agende a execução do script 'conferencia_reprovada.py' usando Agendador de Tarefas do Windows.

## Execução
1. Ative o ambiente virtual (se estiver usando).
2. Execute o script 'conferencia_reprovada.py':

    ```bash
    python conferencia_reprovada.py
    ```

## Observações

* Certifique-se que o Oracle Client esteja instalado e configurado corretamente. 
* O script verifica se há conferências reprovadas antes de enviar o e-mail. Se não houver conferências, o script encerra sem enviar um e-mail.
* As informações sensíveis (credenciais) são lidas de variáveis de ambiente para evitar exposição no código.

## Contribuição

Contribuição são bem-vindas! Sinta-se á vontade para abrir uma issue ou enviar um pull request.

## Licença

Este projeto está sob a licença [MIT](LICENSE).

## Autor
* Edson Padilha