import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import pytz
import io

# ── Configurações via Secrets ────────────────────────
SUPABASE_URL    = st.secrets["SUPABASE_URL"]
SUPABASE_APIKEY = st.secrets["SUPABASE_APIKEY"]

HEADERS = {
    "apikey":        SUPABASE_APIKEY,
    "Authorization": f"Bearer {SUPABASE_APIKEY}",
    "Content-Type":  "application/json"
}


# ── Interface Streamlit ──────────────────────────────
st.set_page_config(page_title="Maturidade e Governança", page_icon="🏪", layout="wide")
