import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# --------------------------
# CONFIGURAÇÃO DA PÁGINA
# --------------------------
st.set_page_config(
    page_title="Análise de Distância das Escolas",
    layout="wide",
    page_icon="📍"
)

# --------------------------
# FUNÇÕES AUXILIARES
# --------------------------
@st.cache_data
def carregar_dados():
    return pd.read_excel("ESCOLAS - 062025_Finalizado 1.xlsx")

def exibir_tela_inicial():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("assets/ASSINATURA-MCOM-2.png", width=400)


    st.markdown("# Cálculo de distância de infraestrutura Escolas")
    st.markdown("""
        **Bem-vindo(a) ao painel interativo para análise geoespacial da infraestrutura educacional e de telecomunicações.**

        **Navegue pelo menu lateral** para:
        - **Explorar mapas interativos por região e distância**
        - **Ver indicadores gerais sobre a distribuição das escolas e antenas**

        ---
    """)


def exibir_mapa(df):
    # KPIs
    st.subheader("📊 Indicadores Gerais")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("**Total na Base**", len(df))
    col2.metric("**Total ≥ 10km**", df["Acima 10km"].sum())
    col3.metric("**Nordeste**", (df["REGIAO"] == "Nordeste").sum())
    col4.metric("**Norte**", (df["REGIAO"] == "Norte").sum())

    # Filtros na barra lateral
    with st.sidebar:
        st.header("🎚️ Filtros de Visualização")
        with st.expander("Filtrar por Região", expanded=True):
            regioes_disponiveis = sorted(df["REGIAO"].dropna().unique())
            filtro_regioes = st.multiselect("Regiões:", regioes_disponiveis, default=regioes_disponiveis)

        with st.expander("Faixa de Distância", expanded=True):
            opcoes_distancia = [
                "Menor que 500m", "Entre 500m e 1km", "Entre 1km e 2km",
                "Entre 2km e 5km", "Entre 5km e 10km", "Acima 10km"
            ]
            filtro_distancia = st.radio("Selecione uma faixa:", opcoes_distancia)

    # Exibir mapa
    st.subheader("🗺️ Mapa Interativo")
    st.markdown("O mapa abaixo mostra as escolas e antenas agrupadas por região e faixa de distância.")

    caminho_html = "ESCOLAS 062025 com Faixas-Regiões (1).html"
    with open(caminho_html, "r", encoding="utf-8") as f:
        mapa_html = f.read()
    components.html(mapa_html, height=800, width=1100, scrolling=False)

# --------------------------
# EXECUÇÃO
# --------------------------
df = carregar_dados()

# Menu de navegação
st.sidebar.title("📁 Navegação")
pagina = st.sidebar.radio("Ir para:", ["🏠 Início", "🗺️ Mapa Interativo"])

if pagina == "🏠 Início":
    exibir_tela_inicial()
elif pagina == "🗺️ Mapa Interativo":
    exibir_mapa(df)
