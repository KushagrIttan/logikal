import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")


st.title("📊 Data Upload - Logiकल")

uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        st.switch_page("pages/val_true.py")
        st.experimental_rerun()
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
        st.switch_page("pages/val_true.py")
        st.experimental_rerun()
    else:
        st.switch_page("pages/val_false.py")
        st.experimental_rerun()
