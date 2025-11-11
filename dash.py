import streamlit as st
import pandas as pd 
import plotly.express as px

st.set_page_config(layout = "wide")

st.title("Dashboard sobre a Escolaridade e Desemprego")

df = pd.read_csv("base-dados2.csv", delimiter = ";", encoding = "utf-8")

df["Brasil e Grande Região"].unique()

regiao = st.sidebar.selectbox("Brasil e Regiões", df["Brasil e Grande Região"].unique())

df_filtro = df[df["Brasil e Grande Região"] == regiao]

total = df_filtro.groupby("Nível de instrução")[["Variável - Pessoas de 14 anos ou mais de idade, desocupadas na semana de referência (Mil pessoas)"]].sum().reset_index()

fig_total = px.pie(total, values = "Variável - Pessoas de 14 anos ou mais de idade, desocupadas na semana de referência (Mil pessoas)", names = "Nível de instrução")

st.plotly_chart(fig_total)