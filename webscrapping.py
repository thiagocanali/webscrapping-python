import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import json
import time
from io import StringIO

# URL da página da web que contém a tabela de cotações de moedas do Yahoo Finance
url = "https://finance.yahoo.com/currencies"

def get_table_data():
    """
    Função para extrair dados de uma tabela da página da web
    Retorna um dicionário com os dados da tabela
    """
    try:
        # Encontrar o elemento da tabela na página usando XPath
        element = driver.find_element(By.XPATH, "//table")
        # Obter o conteúdo HTML completo da tabela
        html_content = element.get_attribute('outerHTML')

        # Analisar o conteúdo HTML usando BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find(name='table')  # Encontrar a tag <table> no HTML

        # Converter o conteúdo da tabela em um DataFrame do Pandas usando StringIO
        df_full = pd.read_html(StringIO(str(table)))[0]

        # Verificar as colunas presentes no DataFrame
        print("Colunas encontradas na tabela:", df_full.columns)

        # Atualizar o código para refletir as colunas corretas
        df = df_full[['Symbol', 'Last Price', 'Change', '% Change']]

        # Substituir valores NaN por valores vazios
        df = df.fillna('')

        # Verificar o DataFrame antes da conversão para JSON
        print("Dados do DataFrame:")
        print(df.head())  # Exibir as primeiras linhas do DataFrame

        # Renomear as colunas para correspondência desejada
        df.columns = ['symbol', 'price', 'change', 'percent_change']

        # Converter o DataFrame em um dicionário
        return df.to_dict('records')
    except Exception as e:
        # Imprimir mensagem de erro caso ocorra alguma exceção
        print(f"Error: {e}")
        return {}

# Configurar o WebDriver com opções específicas
option = Options()
option.headless = True  # Executar o navegador em modo headless (sem interface gráfica)
driver = webdriver.Firefox(options=option)  # Inicializar o WebDriver para Firefox com as opções configuradas

try:
    # Acessar a URL definida
    driver.get(url)
    # Pausar a execução por 10 segundos para garantir que a página carregue completamente
    time.sleep(10)
    # Definir um tempo máximo de espera de 10 segundos para encontrar elementos
    driver.implicitly_wait(10)
    
    # Obter o HTML da página atual e salvar em um arquivo para inspeção
    page_source = driver.page_source
    with open('page_source.html', 'w', encoding='utf-8') as f:
        f.write(page_source)
    print("Page source saved to page_source.html")  # Informar que o HTML da página foi salvo
    
    # Extrair os dados da tabela e armazenar em uma variável
    table_data = get_table_data()
finally:
    # Fechar o navegador
    driver.quit()

# Salvar os dados extraídos da tabela em um arquivo JSON
with open('currency_data.json', 'w', encoding='utf-8') as jp:
    js = json.dumps(table_data, indent=4)  # Converter os dados em uma string JSON formatada
    jp.write(js)  # Escrever a string JSON no arquivo

print("Currency data saved to currency_data.json")  # Informar que os dados foram salvos no arquivo JSON
