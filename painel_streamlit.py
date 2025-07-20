import streamlit as st
import pandas as pd
import os
import io

import ingestao
import pre_processamento
import modelo
import visualizacoes
import exportacao


# 🔧 Configuração visual
st.set_page_config(page_title="RestCheck · IA para Restaurantes", page_icon="🍽️", layout="wide")
st.markdown('<style>.block-container {padding-top: 2rem;}</style>', unsafe_allow_html=True)

if os.path.exists("logo-restcheck.png"):
    st.image("logo-restcheck.png", width=120)
else:
    st.caption("🍽️ RestCheck — Inteligência para Restaurantes")

st.title("🍽️ RestCheck — Inteligência para Restaurantes")

# 🎨 Barra lateral
st.sidebar.title("🧠 RestCheck")
st.sidebar.caption("Previsão de pedidos com IA")

# ✅ Modo de demonstração
st.sidebar.markdown("### 🧪 Modo de teste")
usar_demo = st.sidebar.checkbox("🔍 Usar dados de demonstração")

df = None

if usar_demo:
    st.sidebar.success("✅ Modo demonstração ativado!")
    dados_demo = {
        'data': ['2024-07-01','2024-07-01','2024-07-01',
                 '2024-07-02','2024-07-02','2024-07-02',
                 '2024-07-03','2024-07-03','2024-07-03'],
        'prato': ['Feijoada','Strogonoff','Frango Grelhado'] * 3,
        'quantidade': [32,18,24,29,21,30,34,17,27]
    }
    df = pd.DataFrame(dados_demo)
    st.info("🔍 Visualizando dados fictícios para demonstração.")
else:
    st.sidebar.markdown("### 🔍 Validador de CSV")
    arquivo = st.sidebar.file_uploader("📁 Envie seu arquivo (.csv)", type=["csv"], key="upload_validar")

    if arquivo:
        try:
            conteudo = arquivo.read().decode("utf-8")
            df_raw = pd.read_csv(io.StringIO(conteudo))
            colunas_obrigatorias = {'data', 'prato', 'quantidade'}
            colunas_encontradas = set(df_raw.columns.str.lower().str.strip())
            faltando = colunas_obrigatorias - colunas_encontradas

            if faltando:
                st.error(f"❌ Arquivo inválido. Faltam as colunas: {', '.join(faltando)}")
                st.stop()
            else:
                st.sidebar.success("✅ Estrutura válida!")
                df = df_raw.copy()
        except Exception as e:
            st.error(f"❌ Erro ao validar CSV: {e}")
            st.stop()

# 🔮 Controles adicionais
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

# 🧠 Ajuda e crédito
st.sidebar.info("❓ Ajuda: [restcheck.com.br/ajuda](https://restcheck.com.br/ajuda)")
st.sidebar.markdown("📬 [@gabrielsf476](https://github.com/gabrielsf476)")
st.sidebar.caption("🧠 Powered by RestCheck")

# 🔄 Execução do painel
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
        O **RestCheck** é um painel de inteligência artificial para restaurantes.  
        Ele analisa pedidos anteriores e entrega previsões precisas com relatórios interativos.

        - 🔮 Previsão por prato
        - 📊 Gráficos visuais
        - 📥 Exportação em Excel

        Desenvolvido por [Gabriel S. de Freitas](https://github.com/gabrielsf476) com apoio do Copilot  
        [restcheck.com.br/teste](#) · [Instagram @restcheckapp](https://instagram.com/restcheckapp)
        """)
else:
    st.info("👈 Envie um arquivo válido ou ative o modo de demonstração para iniciar.")
