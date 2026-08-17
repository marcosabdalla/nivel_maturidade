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
    SELECT * FROM PESSOAS
    ''', conexao)
    return dados



# ── Interface Streamlit ──────────────────────────────
st.set_page_config(page_title="Maturidade e Governança", page_icon="🏪", layout="wide")


funs = le_pessoas()

IDs = list(funs['id'])
Nomes = list(funs['nome'])
Cargos = list(funs['cargo'])

st.write(IDs)
st.write(Nomes)
st.write(Cargos)


