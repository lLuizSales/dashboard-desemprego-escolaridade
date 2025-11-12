import streamlit as st
import pandas as pd 
import plotly.express as px

st.set_page_config(layout = "wide")
st.set_page_config(page_title = "👨‍🎓👷‍♂️ Escolaridade e Desemprego")
st.title("Análise sobre a influência da escolaridade sobre o desemprego")

df = pd.read_csv("base-dados.csv", delimiter = ";", encoding = "utf-8")
df["Pessoas de 14 anos ou mais de idade, desocupadas na semana de referência (Mil pessoas)"] = df["Pessoas de 14 anos ou mais de idade, desocupadas na semana de referência (Mil pessoas)"].astype(int)
df["Ano"] = df["Trimestre"].str.extract(r"(\d{4})")
df["Ano"] = df["Ano"].astype(int)
df["Trimestre número"] = df["Trimestre"].str.extract(r"(\d+)")
df["Trimestre número"] = df["Trimestre número"].astype(int)

regiao = st.sidebar.selectbox("Brasil e Regiões", df["Brasil e Grande Região"].unique())
df_filtro_r = df[df["Brasil e Grande Região"] == regiao]

ano = st.sidebar.selectbox("Ano", df_filtro_r["Ano"].unique())
df_filtro = df_filtro_r[df_filtro_r["Ano"] == ano]

col1,col2 = st.columns(2)

total = df_filtro.groupby("Nível de instrução")[["Pessoas de 14 anos ou mais de idade, desocupadas na semana de referência (Mil pessoas)"]].sum().reset_index()
fig_total = px.pie(total, 
                   values = "Pessoas de 14 anos ou mais de idade, desocupadas na semana de referência (Mil pessoas)", 
                   names = "Nível de instrução",
                   title = f"Total do Desemprego por Nível de Instrução - {regiao}/{ano}")
fig_total.update_layout(legend_title = "Nível de instrução")
col1.plotly_chart(fig_total)

df_trimestre = df_filtro.groupby(["Trimestre", "Nível de instrução"])[["Pessoas de 14 anos ou mais de idade, desocupadas na semana de referência (Mil pessoas)"]].sum().reset_index()
fig_total_anos = px.line(df_trimestre, 
                        x = "Trimestre",
                        y = "Pessoas de 14 anos ou mais de idade, desocupadas na semana de referência (Mil pessoas)", 
                        color = "Nível de instrução",
                        title = f"Evolução do Desemprego por Nível de Instrução - {regiao}/{ano}")

fig_total_anos.update_layout(yaxis_title="Mil pessoas")

col2.plotly_chart(fig_total_anos)

df_anos = df_filtro_r.groupby(["Ano", "Trimestre número"])[["Pessoas de 14 anos ou mais de idade, desocupadas na semana de referência (Mil pessoas)"]].sum().reset_index()

fig_anos = px.bar(df_anos,
                  x = "Ano",
                  y = "Pessoas de 14 anos ou mais de idade, desocupadas na semana de referência (Mil pessoas)",
                  color = "Trimestre número",
                  title = f"Evolução do Desemprego por ano - {regiao}")

fig_anos.update_xaxes(type = "category")

fig_anos.update_layout(yaxis_title="Mil pessoas")

st.plotly_chart(fig_anos)