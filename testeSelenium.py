from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

# Função para configurar e retornar o navegador Selenium
def setup_webdriver():
    """Configura e retorna o navegador Selenium."""
    servico = Service(ChromeDriverManager().install())
    navegador = webdriver.Chrome(service=servico)
    return navegador

# Função para postar no Threads
def post_on_threads(username, password, message):
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
    post_input.send_keys(message)
    
    # Clicar no botão para postar
    post_button = navegador.find_element(By.XPATH, '/html/body/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div[2]/div/div[1]/div/div')
    post_button.click()
    
    # Espera 2 segundos e fecha o navegador
    sleep(2)
    navegador.quit()

# Parâmetros de exemplo
username = "ideiastiktok09@gmail.com"
password = "SenhaTeste!"
message = "Esta é uma postagem automatizada de teste no Threads usando Selenium!2"

# Chamar a função para postar no Threads
post_on_threads(username, password, message)
