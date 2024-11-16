import streamlit as st
import numpy as np
import requests
import pandas as pd
from src.load import load_dataset
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("API_URL")

# Função para carregar os dados diretamente da API
# @st.cache_data
def load_data():
    try:
        response = requests.get(f"{API_URL}/patrimonio/")
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error("Erro ao carregar dados.")
            return pd.DataFrame()
    except Exception as e:
        st.error("Erro ao conectar com a API.")
        return pd.DataFrame()

st.title('KDBENS')

# Cadastro de novo item de patrimônio
with st.form("my_form"):
    st.write("Cadastre um novo item de patrimônio")
    item = st.text_input("Item")
    col1, col2, col3 = st.columns(3)
    setor = col1.selectbox("Setor", ("Setor 1", "Setor 2", "Setor 3", "Setor 4", "Setor 5"))
    filial = col2.selectbox("Filial", ("Filial A", "Filial B", "Filial C"))
    tipo = "Exclusivo" if col3.checkbox("Exclusivo") else "Comum"
    patrimonio = np.random.randint(10000, 99999)

    cadastro = {
        "Item": item,
        "Setor": setor,
        "Filial": filial,
        "Tipo": tipo,
        "Patrimonio": patrimonio
    }

    submitted = st.form_submit_button("Enviar")
    if submitted:
        response = requests.post(f"{API_URL}/patrimonio/", json=cadastro)
        if response.status_code == 200:
            st.success("Item cadastrado com sucesso!")
        else:
            st.error("Erro ao cadastrar o item.")

# st.divider()

# Exibição do inventário
# st.subheader("Inventário")
df_patrimonio = load_data()
# st.dataframe(df_patrimonio, use_container_width=True)

st.divider()

# Editar ou excluir itens de patrimônio
st.subheader("Editar ou Excluir Item de Patrimônio")

# Seleção do item para edição ou exclusão
item_id = st.selectbox("Selecione um item para editar ou excluir", df_patrimonio['Patrimonio'] if not df_patrimonio.empty else [])
if item_id:
    item_data = df_patrimonio[df_patrimonio['Patrimonio'] == item_id].iloc[0]

    st.write(f"Editando {item_data['Item']}")
    new_item = st.text_input("Item", item_data['Item'])
    col1, col2, col3 = st.columns(3)
    new_setor = col1.selectbox("Setor", ["Setor 1", "Setor 2", "Setor 3", "Setor 4", "Setor 5"], index=["Setor 1", "Setor 2", "Setor 3", "Setor 4", "Setor 5"].index(item_data['Setor']) if item_data['Setor'] in ["Setor 1", "Setor 2", "Setor 3", "Setor 4", "Setor 5"] else 0)
    new_filial = col2.selectbox("Filial", ["Filial A", "Filial B", "Filial C"], index=["Filial A", "Filial B", "Filial C"].index(item_data['Filial']) if item_data['Filial'] in ["Filial A", "Filial B", "Filial C"] else 0)
    new_tipo = "Exclusivo" if col3.checkbox("Exclusivo", item_data['Tipo'] == "Exclusivo") else "Comum"

    # Função para atualizar os dados via API (PUT)
    def update_data(item, setor, filial, tipo, patrimonio):
        payload = {
            "Item": item,
            "Setor": setor,
            "Filial": filial,
            "Tipo": tipo,
            "Patrimonio": patrimonio
        }
        response = requests.put(f"{API_URL}/patrimonio/{patrimonio}", json=payload)
        return response.status_code == 200

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    atualizar = col1.button("Atualizar")
    excluir = col2.button("Excluir")

    # Atualizar ou excluir o item e recarregar o dataframe
    if atualizar:
        if update_data(new_item, new_setor, new_filial, new_tipo, item_id):
            st.success("Item atualizado com sucesso!")
            df_patrimonio = load_data()  # Recarrega os dados após a atualização
        else:
            st.error("Erro ao atualizar o item.")

    if excluir:
        response = requests.delete(f"{API_URL}/patrimonio/{item_id}")
        if response.status_code == 200:
            st.success("Item excluído com sucesso!")
            df_patrimonio = load_data()  # Recarrega os dados após a exclusão
        else:
            st.error("Erro ao excluir o item.")
        
    # Exibição do dataframe atualizado
    st.divider()
    st.subheader("Inventário")
    st.dataframe(df_patrimonio, use_container_width=True)
