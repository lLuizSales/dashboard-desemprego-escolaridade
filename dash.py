import streamlit as st
import pandas as pd 
import plotly.express as px
import json

st.set_page_config(layout = "wide")
st.set_page_config(page_title = "👨‍🎓Escolaridade e Desemprego👨‍💼")
st.title("Análise sobre a influência da escolaridade sobre o desemprego")

st.markdown("""
A escolaridade exerce um papel central na estrutura do mercado de trabalho brasileiro, influenciando diretamente a taxa de desemprego 
e as oportunidades de inserção profissional. No entanto, essa relação não é simples: diferentemente de muitos países desenvolvidos, 
onde o desemprego diminui conforme a escolaridade aumenta, o Brasil apresenta um comportamento não linear.
Com base em dados nacionais e estudos recentes, esta análise busca compreender como diferentes níveis de instrução impactam as taxas 
de desocupação, considerando assimetrias de informação, diferenças regionais, desafios de qualificação e dinâmicas do mercado de trabalho.
""")

df_desemprego = pd.read_csv("base-dados-desempregos.csv", delimiter = ";", encoding = "utf-8")
df_desemprego["Pessoas de 14 anos ou mais de idade (Mil pessoas)"] = df_desemprego["Pessoas de 14 anos ou mais de idade (Mil pessoas)"].astype(int)
df_desemprego["Ano"] = df_desemprego["Trimestre"].str.extract(r"(\d{4})")
df_desemprego["Ano"] = df_desemprego["Ano"].astype(int)

df_escolaridade = pd.read_csv("base-dados-escolaridade.csv", delimiter = ";", encoding = "utf-8")
df_escolaridade["Variável - População (Mil pessoas)"] = df_escolaridade["Variável - População (Mil pessoas)"].astype(int)
df_escolaridade["Ano"] = df_escolaridade["Trimestre"].str.extract(r"(\d{4})")
df_escolaridade["Ano"] = df_escolaridade["Ano"].astype(int) 

df = pd.read_csv("base-dados.csv", delimiter = ";", encoding = "utf-8")
df["Pessoas de 14 anos ou mais de idade, desocupadas na semana de referência (Mil pessoas)"] = df["Pessoas de 14 anos ou mais de idade, desocupadas na semana de referência (Mil pessoas)"].astype(int)
df["Ano"] = df["Trimestre"].str.extract(r"(\d{4})")
df["Ano"] = df["Ano"].astype(int)
df["Trimestre número"] = df["Trimestre"].str.extract(r"(\d+)")
df["Trimestre número"] = df["Trimestre número"].astype(int)

ano = st.sidebar.selectbox("Ano:", df["Ano"].unique())
df_filtro = df[df["Ano"] == ano]
df_filtro2 = df_desemprego[df_desemprego["Ano"] == ano]

regiao = st.sidebar.selectbox("Brasil e Regiões:", df_filtro["Brasil e Grande Região"].unique())
df_filtro_r = df_filtro[df_filtro["Brasil e Grande Região"] == regiao]
df_filtro_r2 = df[df["Brasil e Grande Região"] == regiao]
df_filtro_r3 = df_escolaridade[df_escolaridade["Brasil e Grande Região"] == regiao]
df_filtro_r4 = df_desemprego[df_desemprego["Brasil e Grande Região"] == regiao]
 
graf_linha = st.sidebar.selectbox("Gráfico Evolução Anual:", ["Escolaridade/Desemprego", "Escolaridade"])
if graf_linha == "Escolaridade/Desemprego":
    coluna = "Pessoas de 14 anos ou mais de idade, desocupadas na semana de referência (Mil pessoas)"
    df_escolhido = df_filtro_r2
    titulo = f"Evolução do Desemprego por Nível de Instrução - {regiao}"
elif graf_linha == "Escolaridade":
    coluna = "Variável - População (Mil pessoas)"
    df_escolhido = df_filtro_r3
    titulo = f"Evolução do Nível de Instrução - {regiao}"

col1,col2 = st.columns(2)

total = df_filtro_r.groupby("Nível de instrução")[["Pessoas de 14 anos ou mais de idade, desocupadas na semana de referência (Mil pessoas)"]].sum().reset_index()
fig_total = px.pie(total, 
                   values = "Pessoas de 14 anos ou mais de idade, desocupadas na semana de referência (Mil pessoas)", 
                   names = "Nível de instrução",
                   title = f"Total do Desemprego por Nível de Instrução - {regiao}/{ano}")
fig_total.update_layout(legend_title = "Nível de instrução")
col1.plotly_chart(fig_total)

df_trimestre = df_filtro_r.groupby(["Trimestre", "Nível de instrução"])[["Pessoas de 14 anos ou mais de idade, desocupadas na semana de referência (Mil pessoas)"]].sum().reset_index()
fig_total_anos = px.line(df_trimestre, 
                        x = "Trimestre",
                        y = "Pessoas de 14 anos ou mais de idade, desocupadas na semana de referência (Mil pessoas)", 
                        color = "Nível de instrução",
                        title = f"Evolução do Desemprego por Nível de Instrução - {regiao}/{ano}")
fig_total_anos.update_layout(yaxis_title="Mil pessoas")
col2.plotly_chart(fig_total_anos)

def graf_linha(df, coluna, titulo):
    fig = px.line(df[df["Ano"] != 2020].groupby(["Ano", "Nível de instrução"])[[coluna]].sum().reset_index(), 
                x = "Ano",
                y = coluna, 
                color = "Nível de instrução",
                title = titulo)
    fig.update_layout(yaxis_title="Mil pessoas")
    fig.update_xaxes(type='category')
    return fig
fig_evolucao_anos = graf_linha(df_escolhido, coluna, titulo)
st.plotly_chart(fig_evolucao_anos)

st.markdown("""
A relação entre escolaridade e desemprego no Brasil apresenta um padrão não linear, onde as taxas de desocupação são maiores entre 
trabalhadores semi-qualificados. Nesse grupo, o mercado apresenta maior dificuldade de avaliar produtividade, o que aumenta a incerteza 
e, consequentemente, o desemprego. Já trabalhadores com escolaridade muito baixa ou muito alta tendem a apresentar taxas menores.
Estudos econométricos identificaram um ponto ótimo de escolaridade (4,15 anos): abaixo desse valor, mais anos de estudo aumentam a 
taxa de desemprego; acima dele, passam a reduzi-la. Regiões como Sul e Sudeste já superavam esse nível médio, enquanto outras regiões 
permaneciam aquém. Além disso, melhorias educacionais levam 3 a 4 anos para refletir na redução do desemprego estadual, destacando a 
defasagem natural entre investimento em capital humano e impacto econômico.
Outro fator determinante é a assimetria de informação. Empregadores enfrentam dificuldade em inferir produtividade em grupos muito 
amplos e heterogêneos, como jovens e trabalhadores semi-qualificados. Regiões e setores com maior homogeneidade salarial tendem a apresentar 
maior desemprego justamente devido à incerteza no processo de contratação.
O cenário recente amplia essa complexidade. Profissionais com ensino superior completo possuem a menor taxa de desocupação, mas o país enfrenta 
um fenômeno crescente de sobre-educação: há mais trabalhadores com ensino superior do que vagas que exigem esse nível. Entre 2010 e 2019, o 
número de sobre-educados passou de 36,95% para 43,41%. A qualidade da educação, a crise econômica e a redução de vagas qualificadas dificultam 
a inserção dos recém-formados.
""")

fig_evol_desem_anos = px.line(df_filtro_r4.groupby(["Ano"])[["Pessoas de 14 anos ou mais de idade (Mil pessoas)"]].sum().reset_index(), 
                x = "Ano",
                y = "Pessoas de 14 anos ou mais de idade (Mil pessoas)",
                title = f"Evolução do Desemprego - {regiao}")
fig_evol_desem_anos.update_layout(yaxis_title="Mil pessoas")
fig_evol_desem_anos.update_xaxes(type='category')
st.plotly_chart(fig_evol_desem_anos)

with open("grandes_regioes_json.geojson", "r", encoding = "utf-8") as f: geojson = json.load(f)
df_mapa = (df_filtro2[df_filtro2["Brasil e Grande Região"] != "Brasil"].groupby(["Brasil e Grande Região", "Ano"])["Pessoas de 14 anos ou mais de idade (Mil pessoas)"].sum().reset_index())
fig_mapa = px.choropleth(df_mapa,
                            geojson = geojson,
                            locations = "Brasil e Grande Região",
                            featureidkey = "properties.NOME1",
                            color = "Pessoas de 14 anos ou mais de idade (Mil pessoas)",
                            scope = "south america",
                            color_continuous_scale = "Viridis",
                            title = f"Mapa do Desemprego por Grande Região — {ano}")
fig_mapa.update_geos(fitbounds="locations", visible=True)
st.plotly_chart(fig_mapa)

st.markdown("""
A análise demonstra que a influência da escolaridade sobre o desemprego no Brasil é marcada por múltiplos fatores e não segue o 
comportamento linear observado em outros países. O formato não linear evidencia que o mercado de trabalho brasileiro enfrenta 
desafios particulares, como a assimetria de informação, a heterogeneidade da força de trabalho e a distribuição desigual da escolaridade entre as regiões.
Embora o ensino superior ofereça maior proteção contra o desemprego, a expansão desse nível educacional sem crescimento equivalente 
de empregos qualificados gera sobre-educação e frustração de expectativas profissionais.
Os dados reforçam que políticas educacionais precisam vir acompanhadas de estratégias integradas de desenvolvimento econômico, 
redução de desigualdades regionais, qualificação profissional alinhada ao mercado e combate às assimetrias de informação. 
Assim, investir em escolaridade continua sendo fundamental, mas deve ser planejado.
""")