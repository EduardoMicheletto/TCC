from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from time import sleep
import requests
import streamlit as st
import pdfplumber
import google.generativeai as genai
from selenium.webdriver.common.by import By

def setup_webdriver():
    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)
    return navegador

# Função para postar no Threads
# def post_on_threads(username, password, threads):
#     """Faz login no Threads e realiza postagens de várias threads."""
    
#     # Configurando o WebDriver
#     navegador = setup_webdriver()

#     # Acessar a página de login
#     navegador.get("https://www.threads.net/login/")
#     sleep(2)

#     # Preencher o campo de login
#     login_input = navegador.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div/div/div[1]/div[1]/div[3]/form/div/div[1]/input')
#     login_input.send_keys(username)

#     # Preencher o campo de senha
#     password_input = navegador.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div/div/div[1]/div[1]/div[3]/form/div/div[2]/input')
#     password_input.send_keys(password)

#     # Clicar no botão de login
#     login_button = navegador.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div/div/div[1]/div[1]/div[3]/form/div/div[3]/div[2]')
#     login_button.click()
    
#     sleep(4)  # Espera para garantir que o login foi realizado
    
#     # Clicar no local onde será feita a primeira postagem
#     post_area_button = navegador.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div[1]/div[2]/div[3]/div/div/div[2]')
#     post_area_button.click()

#     sleep(3)  # Espera para o carregamento da área de postagem
    
#     # Itera sobre cada thread e faz a postagem
#     for idx, thread in enumerate(threads):
#         # Inserir o texto gerado no campo de postagem
#         post_input = navegador.find_element(By.XPATH, '/html/body/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[3]/div[1]/div[1]/p')
#         post_input.send_keys(thread)
        
#         # Caso não seja a última thread, clicar no botão "Adicionar mais uma thread"
#         if idx < len(threads) - 1:
#             if idx == 0:
#                 # Primeiro botão "Adicionar mais uma thread"
#                 next_thread_button = navegador.find_element(By.XPATH, '/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div[1]/div/div/div[5]/div[2]/span')
#             else:
#                 # Botão "Adicionar mais uma thread" para as threads subsequentes
#                 next_thread_button = navegador.find_element(By.XPATH, f'/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/div[5]/div[2]/span')
#             next_thread_button.click()
#             sleep(3)  # Espera para carregar o próximo campo de texto
    
#     # Clicar no botão para postar todas as threads
#     post_button = navegador.find_element(By.XPATH, '/html/body/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div[2]/div/div[1]/div/div')
#     post_button.click()

#     # Espera e fecha o navegador
#     sleep(2)
#     navegador.quit()

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
    post_input.send_keys("testge")
    
    # Clicar no botão para postar
    post_button = navegador.find_element(By.XPATH, '/html/body/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div[2]/div/div[1]/div/div')
    post_button.click()
    
    # Espera 2 segundos e fecha o navegador
    sleep(2)
    navegador.quit()

texto_exemplo = """
PL 3632/2024: Responsabilidade Administrativa de Notários e Registradores

O PL 3632/2024, de autoria do Senador Rodrigo Cunha, visa incluir a responsabilidade administrativa dos notários e registradores na Lei nº 8.935/1994. O objetivo é estabelecer um prazo prescricional de 3 anos para a apuração de infrações disciplinares cometidas por esses profissionais. A proposta se baseia na legislação que já prevê prazo prescricional para a improbidade administrativa, buscando garantir segurança jurídica e eficiência no sistema notarial e registral.

Impactos Potenciais:

Positivos:

* Segurança Jurídica: O prazo definido para a apuração de infrações disciplinares garante segurança jurídica tanto para os profissionais quanto para os usuários dos serviços notariais e de registro.
* Eficiência: A delimitação do prazo evita a perpetuação de processos disciplinares, tornando o sistema mais ágil e eficiente.
* Transparência: A criação do prazo contribui para a transparência do sistema, incentivando a investigação e a aplicação de sanções em tempo hábil.

Negativos:

* Risco de impunidade: A existência de um prazo limite para a apuração de infrações pode criar um risco de impunidade para condutas graves, caso não sejam investigadas e punidas dentro do prazo.
* Complexidade na aplicação: A aplicação prática do prazo prescricional pode gerar complexidades, especialmente em casos que envolvam investigações complexas.

Impacto nas Classes Sociais:

* Baixa renda:  A lei pode ter impacto positivo, pois garante um processo mais justo e ágil, beneficiando aqueles que buscam serviços notariais e de registro.
* Classe média: A lei pode trazer segurança jurídica para as transações imobiliárias e outros serviços notariais, beneficiando a classe média.
* Classe alta: A lei pode impactar a classe alta, especialmente aqueles que atuam no ramo imobiliário, por garantir a segurança jurídica de seus negócios.

Implicações Sociais:

A lei não deve intensificar a desigualdade social, mas sim garantir maior justiça e segurança jurídica para todos os cidadãos, independentemente da classe social. A proposta, se aprovada, pode contribuir para a consolidação de um sistema notarial e registral mais eficaz e transparente, o que pode ter impacto positivo no tecido social brasileiro. No entanto, é importante monitorar a aplicação da lei para garantir que não haja falhas na investigação e punição de infrações graves.

Fim do tópico.
"""

# Função para dividir o texto em threads
def dividir_em_threads(texto, limite_caracteres=500):
    threads = []
    palavras = texto.split()
    thread_atual = ""

    for palavra in palavras:
        # Verifica se a próxima palavra excederia o limite de caracteres
        if len(thread_atual) + len(palavra) + 1 > limite_caracteres:
            threads.append(thread_atual.strip())
            thread_atual = palavra
        else:
            thread_atual += " " + palavra
    
    # Adiciona a última thread
    if thread_atual:
        threads.append(thread_atual.strip())
    
    return threads

# Dividindo o texto exemplo em threads com limite de 500 caracteres
threads_geradas = dividir_em_threads(texto_exemplo)

username = "ideiastiktok09@gmail.com"
password = "SenhaTeste!"
post_on_threads(username, password, threads_geradas)