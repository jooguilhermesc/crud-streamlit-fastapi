import requests

# URL base da API FastAPI
API_URL = "http://localhost:8000"  # ajuste o host e a porta conforme necessário

def insert_data(df, table_name):
    try:
        # Itera sobre as linhas do DataFrame e envia cada item para a API
        for index, row in df.iterrows():
            data = row.to_dict()  # Converte a linha para um dicionário
            response = requests.post(f"{API_URL}/patrimonio/", json=data)
            response.raise_for_status()  # Verifica se a requisição foi bem-sucedida
        print("Dados inseridos com sucesso!")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao inserir dados: {e}")
