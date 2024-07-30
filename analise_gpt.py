import streamlit as st
import pdfpl
import gemini

# Função para extrair texto do PDF
def extract_text(pdf_path):
  with open(pdf_path, 'rb') as f:
    pdf_bytes = f.read()
  return pdfpl.get_text(pdf_bytes)

# Função para analisar PL usando Gemini
def analyze_pl(pdf_path):
  # Extrair texto do PDF
  text = extract_text(pdf_path)

  # Enviar texto para Gemini
  response = gemini.query(text, prompt="Um breve resumo sobre a PL, seguido por como esse projeto de lei poderá afetar a vida do cidadão brasileiro. Esclareça os pontos positivos e negativos dessa lei e suas consequencias futuras. Por fim disserte como afeta cada classe social (baixa, media e alta) e se for o caso impactos sociais que poderiam fomentar o aumento da Desigualdade")

  # Obter resposta do Gemini
  answer = response.text

  return answer

# Interface do Streamlit
st.title("Análise de Projetos de Lei do Senado")

# Carregar PDF
uploaded_file = st.file_uploader("Carregar PDF da PL")

if uploaded_file is not None:
  # Obter nome do arquivo
  filename = uploaded_file.name

  # Salvar PDF em diretório temporário
  with open(filename, 'wb') as f:
    f.write(uploaded_file.read())

  # Analisar PL
  answer = analyze_pl(filename)

  # Exibir resposta do Gemini
  st.write(answer)
else:
  # Exibir mensagem de erro
  st.error("Selecione um PDF de PL do Senado para análise.")
