# Importar bibliotecas necessárias
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from time import sleep
import requests
import streamlit as st
import pdfplumber
import google.generativeai as genai


api_key = 'AIzaSyBu2R95Xa8xUBhDxcgC01xem0ZdRTtc7U8'

def setup_webdriver():
    """Configura e retorna o navegador Selenium."""
    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)
    return navegador

def get_pdf_url(navegador):
    """Navega no site do Senado e retorna a URL do PDF."""
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

def download_pdf(url, filename):
    """Faz o download do PDF a partir da URL e salva localmente."""
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

def extract_text(pdf_path):
    """Extrai texto de um arquivo PDF usando pdfplumber e o exibe no Streamlit e no console."""
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    
    # Exibe o texto extraído no Streamlit
    st.subheader("Texto Extraído do PDF:")
    st.text(text)

    # Exibe o texto extraído no console
    print("Texto extraído do PDF:")
    print(text)
    
    return text

def analyze_pl(text):

    prompt = """
    Forneça um resumo conciso do Projeto de Lei (PL), destacando seus principais objetivos e intenções. 
    Em seguida, analise de forma detalhada os potenciais impactos dessa lei na vida dos cidadãos brasileiros, 
    abordando tanto os aspectos positivos quanto os negativos. Considere as possíveis consequências de curto 
    e longo prazo, e explique como as diferentes classes sociais — baixa, média e alta — serão afetadas. 
    Por fim, explore se há implicações sociais que possam intensificar a desigualdade ou provocar mudanças 
    significativas no tecido social do país. Sobre a seguinte: 
    """ + text
    
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-1.5-flash')

    response = model.generate_content(prompt)
    print()
    
    # Retorna o texto gerado pela API
    return response.text


st.title("Análise de Projetos de Lei do Senado")

# Extrair URL do PDF usando Selenium
navegador = setup_webdriver()
pdf_url = get_pdf_url(navegador)

# Baixar PDF
pdf_filename = "downloaded_pl.pdf"
download_pdf(pdf_url, pdf_filename)

# Extrair texto do PDF
text = extract_text(pdf_filename)

# Analisar PL usando a nova API do Google Gemini
answer = analyze_pl(text)
st.write(answer)



