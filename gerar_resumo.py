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
from requests_oauthlib import OAuth1Session
import os
import json

# Configurar a chave de API do Google Gemini
api_key = 'AIzaSyCCPVPdu7IWJ-MHXPWgZapIiRpjKIF9QUc'

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
    Forneça um resumo conciso do Projeto de Lei (PL), destacando seus principais objetivos e intenções. 
    Em seguida, analise de forma detalhada os potenciais impactos dessa lei na vida dos cidadãos brasileiros, 
    abordando tanto os aspectos positivos quanto os negativos. Considere as possíveis consequências de curto e longo prazo, 
    e explique como as diferentes classes sociais — baixa, média e alta — serão afetadas. Por fim,
    explore se há implicações sociais que possam intensificar a desigualdade ou provocar mudanças significativas no tecido social do país.
    Cada bloco de ideia deve ter no máximo 360 caracteres incluindo o titulo, ao final de cada bloco de ideia coloque '**' apenas o ultimo 
    não precisa, o titulo e subtitulo deve fazer parte do bloco de ideia ao qual ele faz parte.


    segue exemplo de como deve usar os **:

    Titulo PL
    O Projeto de Lei proposto pela Senadora Ana Paula Lobato visa alterar o Código de Defesa do Consumidor, proibindo a cobrança de preços mais altos para produtos ou serviços destinados ao[...] .** [não deve passar 350 caracteres, a contagem inclui o titulo]

    Potenciais Impactos na Vida dos Cidadãos Brasileiros
    A lei pode ter impactos positivos, como a redução da desigualdade de preços e maior equidade no mercado. As mulheres, que frequentemente pagam mais por produtos similares, se beneficiariam diretamente[...]** [não deve passar 350 caracteres, a contagem inclui o titulo]

    Consequências de Curto e Longo Prazo
    No curto prazo, espera-se um aumento na conscientização sobre práticas discriminatórias de preços. A longo prazo, a lei poderia incentivar mudanças na cultura empresarial, forçando uma reavaliação de preços[...]** [não deve passar 350 caracteres, a contagem inclui o titulo]

    Efeitos nas Diferentes Classes Sociais
    Mulheres de classes baixas e médias provavelmente experimentarão benefícios diretos, enquanto as de classe alta poderão ver um impacto menor, dado seu maior poder aquisitivo. No entanto, se as empresas decidirem[...]** [não deve passar 350 caracteres, a contagem inclui o titulo]

    Implicações Sociais e Desigualdade
    Embora a lei busque promover igualdade, a forma como as empresas reagem pode intensificar desigualdades. Se a pressão por preços justos levar a aumentos generalizados, a lei pode não alcançar seu objetivo de equidade[...]** [não deve passar 350 caracteres, a contagem inclui o titulo]

    
    
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

def quebrar_texto(texto):
    return  texto.split('**')

# Função principal do aplicativo Streamlit
def gerar_tweets():
    pdf_url = get_pdf_url()
    pdf_filename = "downloaded_pl.pdf"
    download_pdf(pdf_url, pdf_filename)
    text = extrair_texto(pdf_filename)
    mensagem = analise_texto(text, pdf_url)
    return quebrar_texto(mensagem)


# Rodar a função principal
tweets = gerar_tweets()
print(tweets)