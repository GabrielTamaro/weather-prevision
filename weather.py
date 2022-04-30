import requests
import csv
from datetime import timedelta, date

def cria_csv(cabecalho, dados, nome):
    # cria ou abre o arquivo csv para escrita
    with open(nome, 'w') as f:
        # cria uma variável para escrever no arquivo csv
        escrever = csv.writer(f)

        # escreve no arquivo
        escrever.writerow(cabecalho)
        # escreve os dados que pegou da url
        escrever.writerow(dados)

dia_hoje = str(date.today().strftime("%d-%m-%Y"))
# dia de amanhã
dia_1 = str((date.today() + timedelta(days=1)).strftime("%d-%m-%Y"))
# dia depois de amanhã
dia_2 = str((date.today() + timedelta(days=2)).strftime("%d-%m-%Y"))

capitais = ('Rio Branco', 'Maceió', 'Macapá', 'Manaus', 'Salvador', 'Fortaleza', 'Vitória', 'Goiânia', 'São Luís', 'Cuiabá',
'Campo Grande', 'Belo Horizonte', 'Belém', 'João Pessoa', 'Curitiba', 'Recife', 'Teresina', 'Rio de Janeiro', 'Natal',
'Porto Alegre', 'Porto Velho', 'Boa Vista', 'Florianópolis', 'São Paulo', 'Aracaju', 'Palmas', 'Brasília')

cabecalho = ('Cidade', dia_hoje, dia_1, dia_2)

for cap in capitais:
    # retira o espaço para o nome do arquivo e pesquisa na url
    c = cap.replace(' ', '-')    
    # preenche o nome do arquivo com a capital e o dia de hoje
    csv_arquivo = str(c + '-' + dia_hoje + '.csv')

    # url onde vai pegar os dados de acordo com cada capital
    URL = 'https://goweather.herokuapp.com/weather/' + c
    
    # fazendo requisição get para pegar os dados da url
    req = requests.get(url = URL)
    # valida se a requisição retornou código 200, sem erros
    if req.status_code == requests.codes.ok:
        # transforma o dado da url em um json
        dado = req.json()

        #temperatura do dia de hoje
        temp = dado['temperature']

        # pega as informações de previsão
        prev = dado['forecast']
        # temperatura dia de amanhã
        temp_prev1 = '0'
        # temperatura do dia depois de amanhã
        temp_prev2 = '0'
        # procura dentro das previsões os dados para 1 e 2 dias
        for dia in prev:
            # caso seja a previsão de 1 dia
            if dia['day'] == '1':
                temp_prev1 = dia['temperature']
            # caso seja a previsão de 2 dia
            if dia['day'] == '2':
                temp_prev2 = dia['temperature']
            # caso as variáveis já estejam preenchidas, pode para o loop
            if temp_prev1 != '0' and temp_prev2 != '0':
                break
        dados = (cap, temp, temp_prev1, temp_prev2)
        cria_csv(cabecalho, dados, csv_arquivo)
        #print(cabecalho, dados)
    # caso tenha retornado erro, deixar as temperaturas tudo com zero
    else:
        dados = (cap, 0, 0, 0)
        cria_csv(cabecalho, dados, csv_arquivo)