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

def le_gov2():
    dados = pd.read_sql_query('SELECT * FROM "GOVERNANCA"', conexao)
    pessoas = pd.read_sql_query('SELECT "id", "nome" FROM "PESSOAS"', conexao)

    dados = dados.merge(
        pessoas,
        left_on="responsavel",
        right_on="id",
        how="left",
        suffixes=("", "_pessoa")
    )
    dados = dados.drop(columns=["responsavel"]).rename(columns={"nome": "responsavel"})
    dados = dados.drop(columns=["id_pessoa","criado_em"])
    dados = dados.rename(columns={
    "id": "ID",
    "indicador": "Indicador",
    "meta":"Meta",
    "frequencia":"Frequência",
    "responsavel":"Responsável",
    "data_execucao":"Data Execução",
    "status":"Status",
    "observacoes":"Observações"
    })
    return dados

def le_infra():
    dados = pd.read_sql_query('SELECT * FROM "INFRAESTRUTURA"', conexao)
    pessoas = pd.read_sql_query('SELECT "id", "nome" FROM "PESSOAS"', conexao)

    dados = dados.merge(
        pessoas,
        left_on="responsavel",
        right_on="id",
        how="left",
        suffixes=("", "_pessoa")
    )
    dados = dados.drop(columns=["responsavel"]).rename(columns={"nome": "responsavel"})
    dados = dados.drop(columns=["id_pessoa","criado_em"])
    dados = dados.rename(columns={
    "id": "ID",
    "indicador": "Indicador",
    "meta":"Meta",
    "frequencia":"Frequência",
    "responsavel":"Responsável",
    "data_execucao":"Data Execução",
    "status":"Status",
    "observacoes":"Observações"
    })
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

def inserir_gov(indicador,meta,frequencia,responsavel,data_execucao,status,observacoes):
    cur = conexao.cursor()
    cur.execute(
        """
        INSERT INTO "GOVERNANCA" (indicador,meta,frequencia,responsavel,data_execucao,status,observacoes)
        VALUES (%s, %s,%s, %s,%s, %s,%s)
        """,
       (indicador,meta,frequencia,int(responsavel),data_execucao,status,observacoes) 
    )
    conexao.commit()
    cur.close()

def inserir_infra(indicador,meta,frequencia,responsavel,data_execucao,status,observacoes):
    cur = conexao.cursor()
    cur.execute(
        """
        INSERT INTO "INFRAESTRUTURA" (indicador,meta,frequencia,responsavel,data_execucao,status,observacoes)
        VALUES (%s, %s,%s, %s,%s, %s,%s)
        """,
       (indicador,meta,frequencia,int(responsavel),data_execucao,status,observacoes) 
    )
    conexao.commit()
    cur.close()



# ── Interface Streamlit ──────────────────────────────
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.jpeg", width=80)
with col2:
    st.markdown("""
    <h1 style='color: #00008B; text-align: center; font-family: sans-serif;'>
    EDUPOLIS-CIRCULAR
    </h1>
    """, unsafe_allow_html=True)
    
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
pessoas = le_pessoas()
nomes = pessoas["nome"]



gov, infra, curr, comm, pess = st.tabs(["Governança","Infraestrutura","Curriculo","Comunidade","Pessoas"])

with gov:
    Plan_GOV = le_gov2()
    st.dataframe(Plan_GOV)
#---------------------------------------- Metricas GOV ---------------------------------------------
    stat_gov = Plan_GOV["Status"]
    met_stat_gov = pd.Series(stat_gov).value_counts()
    st.dataframe(met_stat_gov)
     
#--------------------------------------- Nova Entrada ----------------------------------------------
    FORM = st.form('Novo Reg. Gov', clear_on_submit = True)
    FORM.subheader('Novo registro em Governança')
    col1, col2 = FORM.columns(2)
    with col1:
        indi = st.text_input('Indicador')
        freq = ["Diário","Semanal","Mensal","Semestral","Quinzenal","Anual"] 
        Freq = st.selectbox("Frequência",options=freq)
        data_exec = st.date_input("Data Execução",value="today",format="DD/MM/YYYY")

    with col2:
        mt = st.text_input('Meta')
        Pess = st.selectbox('Responsável', options = nomes)
        idx = pessoas[pessoas["nome"] == Pess].index
        idx_pess = pessoas.loc[idx,"id"].values[0]
        Stat = st.selectbox('Status', options = ("Não iniciado","Em andamento","Concluido"),)
    obs = FORM.text_area("Observações", value="")
    bt2 = FORM.form_submit_button('Inserir')
    if bt2:
        inserir_gov(indi,mt,Freq,idx_pess,data_exec,Stat,obs)
        
with infra:
    st.dataframe(le_infra())

    FORM = st.form('Novo Reg. Infra', clear_on_submit = True)
    FORM.subheader('Novo registro em Infraestrutura')
    col1, col2 = FORM.columns(2)
    with col1:
        indi = st.text_input('Indicador')
        freq = ["Diário","Semanal","Mensal","Semestral","Quinzenal","Anual"] 
        Freq = st.selectbox("Frequência",options=freq)
        data_exec = st.date_input("Data Execução",value="today",format="DD/MM/YYYY")

    with col2:
        mt = st.text_input('Meta')
        Pess = st.selectbox('Responsável', options = nomes)
        idx = pessoas[pessoas["nome"] == Pess].index
        idx_pess = pessoas.loc[idx,"id"].values[0]
        Stat = st.selectbox('Status', options = ("Não iniciado","Em andamento","Concluido"),)
    obs = FORM.text_area("Observações", value="")
    bt3 = FORM.form_submit_button('Inserir')
    if bt3:
        inserir_infra(indi,mt,Freq,idx_pess,data_exec,Stat,obs)

with pess:
    st.dataframe(le_pessoas())

    FORM = st.form('Inserir novo funcionário', clear_on_submit=True)
    FORM.subheader('Inserir novo funcionário:')
    nome = FORM.text_input("Nome:")
    cargo = FORM.text_input("Cargo:")
    bt1 = FORM.form_submit_button('Inserir')
    if bt1:
        inserir_pessoa(nome, cargo)
    


