#python projeto_final.py

# Importar bibliotecas necessárias
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from time import sleep
import requests
import streamlit as st
import pdfplumber
import google.generativeai as genai
from selenium.webdriver.common.by import By

# Configurar a chave de API do Google Gemini
api_key = 'AIzaSyBu2R95Xa8xUBhDxcgC01xem0ZdRTtc7U8'
#Configuracao de acesso do threads
username = "ideiastiktok09@gmail.com"
password = "SenhaTeste!"

# Função para configurar e retornar o navegador Selenium
def setup_webdriver():
    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)
    return navegador

# Função para navegar no site do Senado e obter a URL do PDF
def get_pdf_url():
    navegador = setup_webdriver()
    navegador.get("https://www25.senado.leg.br/web/atividade/materias?p_p_id=materia_WAR_atividadeportlet&p_p_lifecycle=0&_materia_WAR_atividadeportlet_tipo=PL&_materia_WAR_atividadeportlet_ano=&_materia_WAR_atividadeportlet_numero=&_materia_WAR_atividadeportlet_siglasTipos=&_materia_WAR_atividadeportlet_pesquisaAvancada=true&_materia_WAR_atividadeportlet_p=1")
    navegador.find_element('xpath', '//*[@id="p_p_id_materia_WAR_atividadeportlet_"]/div/div/div/div/div[3]/div[1]/dl/dd[1]/div/div[1]/a').click()
    sleep(4)
    navegador.find_element('xpath', '//*[@id="secao-documentos"]/a').click()
    sleep(1)
    navegador.find_element('xpath', '//*[@id="materia_documentos_proposicao"]/div/div[1]/div[2]/span/a').click()
    sleep(4)
    urlPdf = navegador.current_url
    navegador.quit()
    return urlPdf

# Função para baixar o PDF
def download_pdf(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

# Função para extrair texto do PDF usando pdfplumber
def extrair_texto(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    st.subheader("Texto Extraído do PDF:")
    st.text(text)
    return text

# Função para análise do PL usando a API Gemini do Google
def analise_texto(text, url_pdf):
    prompt = f"""
    Forneça um resumo conciso do Projeto de Lei (PL), destacando seus principais objetivos e intenções. Em seguida, analise de forma detalhada os potenciais impactos dessa lei na vida dos cidadãos brasileiros, abordando tanto os aspectos positivos quanto os negativos. Considere as possíveis consequências de curto e longo prazo, e explique como as diferentes classes sociais — baixa, média e alta — serão afetadas. Por fim, explore se há implicações sociais que possam intensificar a desigualdade ou provocar mudanças significativas no tecido social do país. Esse resumo será postado no Threads, e cada thread pode conter até 529 caracteres. Sempre que finalizar de explicar um tópico, utilize '**' para indicar o encerramento de um bloco de ideias.

    Resumo sobre o seguinte: {text}
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text+" Download Documento Original:"+url_pdf

def dividir_em_threads(texto, limite=529):
    palavras = texto.split()
    threads = []
    thread_atual = ""

    for palavra in palavras:
        # Adiciona a palavra à thread atual se não ultrapassar o limite de caracteres
        if len(thread_atual) + len(palavra) + 1 <= limite:
            if thread_atual:
                thread_atual += " " + palavra
            else:
                thread_atual = palavra
        else:
            # Se atingir o limite, adiciona a thread atual e começa uma nova
            threads.append(thread_atual + " **")
            thread_atual = palavra

    # Adiciona a última thread
    if thread_atual:
        threads.append(thread_atual + " **")

    return threads

def setup_webdriver():
    """Configura e retorna o navegador Selenium."""
    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)
    return navegador

# Função para postar no Threads
def post_on_threads(username, password, threads):
    """Faz login no Threads e realiza uma postagem."""
    
    # Configurando o WebDriver
    navegador = setup_webdriver()

    # Acessar a página de login
    navegador.get("https://www.threads.net/login/")
    sleep(2)

    # Preencher o campo de login
    login_input = navegador.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div/div/div[1]/div[1]/div[3]/form/div/div[1]/input')
    login_input.send_keys(username)

    # Preencher o campo de senha
    password_input = navegador.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div/div/div[1]/div[1]/div[3]/form/div/div[2]/input')
    password_input.send_keys(password)

    # Clicar no botão de login
    login_button = navegador.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div/div/div[1]/div[1]/div[3]/form/div/div[3]/div[2]')
    login_button.click()
    
    sleep(4)  # Espera 2 segundos para garantir que o login foi realizado
    
    # Clicar no local onde será feita a postagem
    post_area_button = navegador.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div[1]/div[2]/div[3]/div/div/div[2]')
    post_area_button.click()

    sleep(3)  # Espera 2 segundos para o carregamento

    # Inserir o texto gerado no campo de postagem
    post_input = navegador.find_element(By.XPATH, '/html/body/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[3]/div[1]/div[1]/p')
    post_input.send_keys(mensagem)
    
    # Clicar no botão para postar
    post_button = navegador.find_element(By.XPATH, '/html/body/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div[2]/div/div[1]/div/div')
    post_button.click()
    
    # Espera 2 segundos e fecha o navegador
    sleep(2)
    navegador.quit()


# Função principal do aplicativo Streamlit
def main():
    pdf_url = get_pdf_url()
    pdf_filename = "downloaded_pl.pdf"
    download_pdf(pdf_url, pdf_filename)
    text = extrair_texto(pdf_filename)
    mensagem = analise_texto(text, pdf_url)
    threads = dividir_em_threads(mensagem)
    post_on_threads(username, password, threads)


# Rodar a função principal
main()
