import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

# URL base da API FastAPI
API_URL = os.getenv("API_URL")  # ajuste o host e a porta conforme necessário

def load_dataset(table_name):
    try:
        # Fazendo requisição GET para buscar os dados
        response = requests.get(f"{API_URL}/patrimonio/")
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida (status 200)
        
        # Converte os dados da resposta para um DataFrame
        data = response.json()
        df = pd.DataFrame(data)
        return df
    except requests.exceptions.RequestException as e:
        print(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro
