import streamlit as st
import pandas as pd
import os

from restcheck_core import (
    ingestao,
    pre_processamento,
    modelo,
    visualizacoes,
    exportacao
)

st.set_page_config(page_title="RestCheck · Inteligência em Pedidos", layout="wide")
st.title("🍽️ RestCheck — Inteligência para Restaurantes")

# 🎨 Sidebar personalizada
st.sidebar.title("🧠 RestCheck")
st.sidebar.caption("Inteligência para Restaurantes")

arquivo = st.sidebar.file_uploader("📁 Envie seu arquivo de pedidos (.csv)", type=["csv"])

st.sidebar.markdown("### 🔮 Previsão")
treinar = st.sidebar.button("📚 Gerar Previsões")

aba = st.sidebar.radio("📍 Navegar pelo painel", [
    "📅 Histórico de Vendas",
    "🔮 Previsão por Prato",
    "📊 Estatísticas",
    "📈 Gráficos",
    "📥 Exportar Relatórios",
    "📍 Sobre o RestCheck"
])

st.sidebar.info("❓ Precisa de ajuda? Visite [restcheck.com.br/ajuda](https://restcheck.com.br/ajuda)")
st.sidebar.markdown("📬 Fale com o criador: [@gabrielsf476](https://github.com/gabrielsf476)")
st.sidebar.caption("🧠 Powered by RestCheck · IA para Restaurantes")

# 🧩 Corpo principal
if arquivo:
    df = ingestao.carregar_csv(arquivo)
    if not ingestao.validar_colunas(df):
        st.error("❌ Arquivo inválido: certifique-se de incluir as colunas 'data', 'prato' e 'quantidade'.")
    else:
        df = pre_processamento.tratar_dados(df)

        if treinar:
            _, rmse, r2 = modelo.treinar(df)
            st.sidebar.success(f"✅ Previsão gerada! RMSE: {rmse:.2f} · R²: {r2:.2f}")

        if os.path.exists("modelo.pkl"):
            y_pred = modelo.prever(df)
            df_previsto = df.copy()
            df_previsto["quantidade_prevista"] = y_pred
        else:
            st.warning("⚠️ O modelo ainda não foi treinado. Clique em '📚 Gerar Previsões' na lateral.")
            df_previsto = df.copy()
            df_previsto["quantidade_prevista"] = None

        # 📍 Navegação entre abas
        if aba == "📅 Histórico de Vendas":
            st.subheader("📅 Tabela de Pedidos Reais")
            cols = ['data_formatada', 'dia_semana', 'prato', 'quantidade', 'valor_total']
            cols = [c for c in cols if c in df.columns]
            st.dataframe(df[cols], use_container_width=True)
            st.plotly_chart(visualizacoes.grafico_total_por_dia(df), use_container_width=True)

        elif aba == "🔮 Previsão por Prato":
            st.subheader("🔮 Tabela Previsiva")
            st.dataframe(df_previsto[['data_formatada', 'prato', 'quantidade_prevista']], use_container_width=True)
            st.plotly_chart(visualizacoes.grafico_total_por_dia(
                df_previsto, coluna='quantidade_prevista', titulo="Previsão Total por Dia"
            ), use_container_width=True)

        elif aba == "📊 Estatísticas":
            st.subheader("📊 Estatísticas de Previsão por Prato")
            stats = df_previsto.groupby('prato')['quantidade_prevista'].agg([
                ('Total Previsto', 'sum'),
                ('Média Diária', 'mean'),
                ('Desvio Padrão', 'std'),
                ('Máximo', 'max'),
                ('Mínimo', 'min')
            ]).sort_values('Total Previsto', ascending=False)
            st.dataframe(stats.style.format("{:.2f}"))

        elif aba == "📈 Gráficos":
            prato = st.selectbox("🍽️ Escolha um prato para visualizar a evolução:", df_previsto['prato'].unique())
            df_filtro = df_previsto[df_previsto['prato'] == prato]
            fig = visualizacoes.grafico_total_por_dia(
                df_filtro, coluna='quantidade_prevista', titulo=f"📈 Evolução Prevista — {prato}"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif aba == "📥 Exportar Relatórios":
            st.subheader("📥 Exportação de Dados")
            buffer_reais = exportacao.gerar_excel(df)
            st.download_button("📄 Baixar Relatório Real (.xlsx)", data=buffer_reais, file_name="pedidos_reais.xlsx")
            buffer_previsto = exportacao.gerar_excel(df_previsto, nome_aba="Previsao")
            st.download_button("📄 Baixar Relatório Previsto (.xlsx)", data=buffer_previsto, file_name="previsao_pedidos.xlsx")

        elif aba == "📍 Sobre o RestCheck":
            st.subheader("📍 Sobre o RestCheck")
            st.markdown("""
            O **RestCheck** é um painel de inteligência artificial desenvolvido para otimizar os pedidos de restaurantes.

            - Crie previsões precisas por prato
            - Reduza desperdício e antecipe decisões
            - Acesse relatórios inteligentes de forma simples

            🔗 Desenvolvido por [Gabriel S.](https://github.com/gabrielsf476) · Powered by Streamlit  
            📬 Dúvidas ou melhorias? [restcheck.com.br/contato](https://restcheck.com.br/contato)
            """)
else:
    st.info("👈 Envie seu arquivo `.csv` na lateral para começar. O modelo precisa de dados históricos com colunas 'data', 'prato' e 'quantidade'.")
