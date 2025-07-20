import streamlit as st
import pandas as pd
import os

import
import ingestao
import pre_processamento
import modelo
import visualizacoes
import exportacao

# 🔧 Configuração de página com identidade visual
st.set_page_config(page_title="RestCheck · IA para Restaurantes", page_icon="🍽️", layout="wide")
st.markdown("""
    <style>
    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.image("logo-restcheck.png", width=120)
st.title("🍽️ RestCheck — Inteligência para Restaurantes")

# 🎨 Barra lateral refinada
st.sidebar.title("🧠 RestCheck")
st.sidebar.caption("Previsão de pedidos com IA")

# ✅ Modo de teste
st.sidebar.markdown("### 🧪 Modo de teste")
usar_demo = st.sidebar.checkbox("🔍 Usar dados de demonstração")

df = None
arquivo = None

if usar_demo:
    st.sidebar.success("✅ Modo demonstração ativado!")
    demo_dados = {
        'data': ['2024-07-01','2024-07-01','2024-07-01',
                 '2024-07-02','2024-07-02','2024-07-02',
                 '2024-07-03','2024-07-03','2024-07-03'],
        'prato': ['Feijoada','Strogonoff','Frango Grelhado'] * 3,
        'quantidade': [32,18,24,29,21,30,34,17,27]
    }
    df = pd.DataFrame(demo_dados)
    st.info("🔍 Você está visualizando dados fictícios para fins de demonstração.")
else:
    arquivo = st.sidebar.file_uploader("📁 Envie seu arquivo de pedidos (.csv)", type=["csv"], key="upload_real")
    if arquivo:
        try:
            df = pd.read_csv(arquivo)
            colunas_obrigatorias = {'data', 'prato', 'quantidade'}
            if not colunas_obrigatorias.issubset(df.columns):
                st.error("❌ Arquivo inválido: certifique-se de incluir as colunas 'data', 'prato' e 'quantidade'.")
                df = None
        except Exception as e:
            st.error(f"❌ Erro ao ler o arquivo: {e}")
            df = None

st.sidebar.markdown("### 🔮 Previsão")
treinar = st.sidebar.button("📚 Gerar Previsões")

aba = st.sidebar.radio("📍 Navegar pelo painel", [
    "📅 Histórico",
    "🔮 Previsões",
    "📊 Estatísticas",
    "📈 Gráficos",
    "📥 Exportar",
    "📍 Sobre o RestCheck"
])

st.sidebar.info("❓ Ajuda: [restcheck.com.br/ajuda](https://restcheck.com.br/ajuda)")
st.sidebar.markdown("📬 [@gabrielsf476](https://github.com/gabrielsf476)")
st.sidebar.caption("🧠 Powered by RestCheck")

# 🔄 Corpo principal
if df is not None:
    df = pre_processamento.tratar_dados(df)

    if treinar:
        _, rmse, r2 = modelo.treinar(df)
        st.sidebar.success(f"✅ Previsão gerada! RMSE: {rmse:.2f} · R²: {r2:.2f}")

    if os.path.exists("modelo.pkl"):
        y_pred = modelo.prever(df)
        df_previsto = df.copy()
        df_previsto["quantidade_prevista"] = y_pred
    else:
        st.warning("⚠️ O modelo ainda não foi treinado.")
        df_previsto = df.copy()
        df_previsto["quantidade_prevista"] = None

    if aba == "📅 Histórico":
        st.subheader("📅 Pedidos reais")
        st.dataframe(df[['data_formatada','prato','quantidade']], use_container_width=True)
        st.plotly_chart(visualizacoes.grafico_total_por_dia(df), use_container_width=True)

    elif aba == "🔮 Previsões":
        st.subheader("🔮 Previsão por prato")
        st.dataframe(df_previsto[['data_formatada','prato','quantidade_prevista']], use_container_width=True)
        st.plotly_chart(visualizacoes.grafico_total_por_dia(
            df_previsto, coluna="quantidade_prevista", titulo="📈 Demanda Prevista"
        ), use_container_width=True)

    elif aba == "📊 Estatísticas":
        st.subheader("📊 Estatísticas por prato")
        stats = df_previsto.groupby('prato')['quantidade_prevista'].agg([
            ('Total Previsto', 'sum'),
            ('Média Diária', 'mean'),
            ('Desvio Padrão', 'std'),
            ('Máximo', 'max'),
            ('Mínimo', 'min')
        ]).sort_values('Total Previsto', ascending=False)
        st.dataframe(stats.style.format("{:.2f}"))

    elif aba == "📈 Gráficos":
        prato = st.selectbox("🍽️ Escolha um prato:", df_previsto['prato'].unique())
        df_filtro = df_previsto[df_previsto['prato'] == prato]
        fig = visualizacoes.grafico_total_por_dia(
            df_filtro, coluna="quantidade_prevista", titulo=f"📈 Previsão — {prato}"
        )
        st.plotly_chart(fig, use_container_width=True)

    elif aba == "📥 Exportar":
        st.subheader("📥 Relatórios")
        buffer_reais = exportacao.gerar_excel(df)
        nome_real = "pedidos_reais.xlsx" if not usar_demo else "DEMO_pedidos_reais.xlsx"
        st.download_button("📄 Baixar Reais", data=buffer_reais, file_name=nome_real)

        buffer_previsto = exportacao.gerar_excel(df_previsto, nome_aba="Previsao")
        nome_prev = "previsao_pedidos.xlsx" if not usar_demo else "DEMO_previsao_pedidos.xlsx"
        st.download_button("📄 Baixar Previsões", data=buffer_previsto, file_name=nome_prev)

    elif aba == "📍 Sobre o RestCheck":
        st.subheader("📍 Sobre")
        st.markdown("""
        O **RestCheck** é um painel de inteligência artificial desenvolvido para restaurantes.  
        Ele gera previsões com base em pedidos anteriores e entrega relatórios completos e interativos.

        - 🔮 Previsão por prato
        - 📊 Gráficos visuais e estatísticas
        - 📥 Exportação de dados

        Desenvolvido por [Gabriel S. de Freitas](https://github.com/gabrielsf476) com apoio do Copilot · Powered by Streamlit  
        [restcheck.com.br/teste](#) | [Instagram @restcheckapp](https://instagram.com/restcheckapp)
        """)
else:
    st.info("👈 Envie seu `.csv` ou ative o modo de demonstração na barra lateral para iniciar.")
