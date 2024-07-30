# Instalar as bibliotecas necessárias
# pip install selenium
# pip install webdriver-manager
# pip install requests
# pip install streamlit
# pip install pdfplumber
# pip install gemini

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from time import sleep
import requests
import streamlit as st
import pdfplumber
import gemini

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
    """Extrai texto de um arquivo PDF usando pdfplumber."""
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

def analyze_pl(pdf_path):
    """Analisa o PDF utilizando o modelo Gemini e retorna a resposta."""
    text = extract_text(pdf_path)
    response = gemini.query(text, prompt="Um breve resumo sobre a PL, seguido por como esse projeto de lei poderá afetar a vida do cidadão brasileiro. Esclareça os pontos positivos e negativos dessa lei e suas consequencias futuras. Por fim disserte como afeta cada classe social (baixa, media e alta) e se for o caso impactos sociais que poderiam fomentar o aumento da Desigualdade")
    return response.text

def main():
    """Função principal que integra todas as etapas."""
    st.title("Análise de Projetos de Lei do Senado")

    # Carregar PDF manualmente
    uploaded_file = st.file_uploader("Carregar PDF da PL")

    if uploaded_file is not None:
        filename = uploaded_file.name
        with open(filename, 'wb') as f:
            f.write(uploaded_file.read())
        answer = analyze_pl(filename)
        st.write(answer)
    else:
        # Extrair URL do PDF usando Selenium
        navegador = setup_webdriver()
        pdf_url = get_pdf_url(navegador)
        
        # Baixar PDF
        pdf_filename = "downloaded_pl.pdf"
        download_pdf(pdf_url, pdf_filename)
        
        # Analisar PL
        answer = analyze_pl(pdf_filename)
        st.write(answer)

if __name__ == "__main__":
    main()
