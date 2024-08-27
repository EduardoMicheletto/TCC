from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Configuração do WebDriver
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)

# Teste de Navegação
navegador.get("https://www.google.com")
print(navegador.title)
navegador.quit()