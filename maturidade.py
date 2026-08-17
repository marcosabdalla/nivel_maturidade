import streamlit as st
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import pandas as pd
import base64
import psycopg2

conexao = psycopg2.connect(
    host=st.secrets["db"]["host"],
    port=6543,  
    database=st.secrets["db"]["name"],
    user=st.secrets["db"]["user"],
    password=st.secrets["db"]["password"],
    sslmode="require"
)

# -- Funcoes ----------------------------------------
def le_pessoas():
    dados = pd.read_sql_query('''
    SELECT * FROM "PESSOAS"
    ''', conexao)
    return dados

def le_gov():
    dados = pd.read_sql_query('''
    SELECT * FROM "GOVERNANCA"
    ''', conexao)
    return dados

def inserir_pessoa(nome, cargo):
    cur = conexao.cursor()
    cur.execute(
        """
        INSERT INTO "PESSOAS" (nome, cargo)
        VALUES (%s, %s)
        """,
        (nome, cargo)
    )
    conexao.commit()
    cur.close()



# ── Interface Streamlit ──────────────────────────────
st.set_page_config(page_title="Maturidade e Governança", page_icon="🏪", layout="wide")


query = """
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
"""
tables_df = pd.read_sql(query, conexao)
#st.dataframe(tables_df)

#st.dataframe(le_pessoas())

gov, infra, curr, comm, pess = st.tabs(["Governança","Infraestrutura","Curriculo","Comunidade","Pessoas"])

with gov:
    FORM = st.form('Novo Reg. Gov', clear_on_submit = True)
    FORM.subheader('Novo registro em Governança')
    col1, col2 = FORM.columns(2)
    with col1:
        indi = FORM.text_input('Indicador')

    with col2:
        mt = FORM.text_input('Meta')
    bt2 = FORM.form_submit_button('Inserir')
    st.dataframe(le_gov())

with pess:
    st.dataframe(le_pessoas())

    FORM = st.form('Inserir novo funcionário', clear_on_submit=True)
    FORM.subheader('Inserir novo funcionário:')
    nome = FORM.text_input("Nome:")
    cargo = FORM.text_input("Cargo:")
    bt1 = FORM.form_submit_button('Inserir')
    if bt1:
        inserir_pessoa(nome, cargo)
    


