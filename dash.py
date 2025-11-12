import streamlit as st
import pandas as pd 
import plotly.express as px

st.set_page_config(layout = "wide")

st.title("Dashboard sobre a Escolaridade e Desemprego")

df = pd.read_csv("base-dados.csv", delimiter = ";", encoding = "utf-8")

regiao = st.sidebar.selectbox("Brasil e Regiões", df["Brasil e Grande Região"].unique())

df_filtro = df[df["Brasil e Grande Região"] == regiao]

df_filtro["Ano"] = df_filtro["Trimestre"].str.extract(r"(\d{4})")

df_filtro["Ano"] = df_filtro["Ano"].astype(int)

ano = st.sidebar.selectbox("Ano", df_filtro["Ano"].unique())

df_filtro = df_filtro[df_filtro["Ano"] == ano]

df_filtro["Pessoas de 14 anos ou mais de idade, desocupadas na semana de referência (Mil pessoas)"] = df_filtro["Pessoas de 14 anos ou mais de idade, desocupadas na semana de referência (Mil pessoas)"].astype(int)

total = df_filtro.groupby("Nível de instrução")[["Pessoas de 14 anos ou mais de idade, desocupadas na semana de referência (Mil pessoas)"]].sum().reset_index()

fig_total = px.pie(total, values = "Pessoas de 14 anos ou mais de idade, desocupadas na semana de referência (Mil pessoas)", names = "Nível de instrução")

st.plotly_chart(fig_total)