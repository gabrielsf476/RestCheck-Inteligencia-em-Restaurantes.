import streamlit as st
import pandas as pd
import os

import ingestao
import modelo
import pre_processamento
import visualizacoes
import exportacao


st.set_page_config(page_title="restcheck_core", layout="wide")
st.title("📊 Painel de Inteligência de Pedidos")
st.sidebar.info("❓ Precisa de ajuda? Visite restcheck.com.br/ajuda")

arquivo = st.sidebar.file_uploader("📁 Envie o arquivo pedidos.csv", type=["csv"])

if arquivo:
    df = ingestao.carregar_csv(arquivo)
    if not ingestao.validar_colunas(df):
        st.error("❌ Arquivo inválido: faltando colunas obrigatórias como data, prato e quantidade.")
    else:
        df = pre_processamento.tratar_dados(df)

        st.sidebar.markdown("### 🔁 Treinar modelo")
        if st.sidebar.button("📚 Treinar"):
            _, rmse, r2 = modelo.treinar(df)
            st.sidebar.success(f"✅ Modelo treinado! RMSE: {rmse:.2f} | R²: {r2:.2f}")

        if os.path.exists("modelo.pkl"):
            y_pred = modelo.prever(df)
            df_previsto = df.copy()
            df_previsto["quantidade_prevista"] = y_pred
        else:
            st.warning("⚠️ Modelo não encontrado. Treine primeiro.")
            df_previsto = df.copy()
            df_previsto["quantidade_prevista"] = None

        aba = st.sidebar.radio("📌 Navegar", [
            "📋 Dados Reais",
            "📈 Previsão",
            "📊 Estatísticas",
            "📎 Gráficos",
            "📥 Exportar"
        ])
        if aba == "📋 Dados Reais":
            st.subheader("📋 Tabela dos dados reais")
            cols = ['data_formatada', 'dia_semana', 'prato', 'quantidade', 'valor_total']
            cols = [c for c in cols if c in df.columns]
            st.dataframe(df[cols])
            st.plotly_chart(visualizacoes.grafico_total_por_dia(df), use_container_width=True)
            st.subheader("📅 Tabela por prato e data")
            st.dataframe(visualizacoes.gerar_tabela_por_prato(df))

        elif aba == "📈 Previsão":
            st.subheader("📈 Tabela de previsão")
            st.dataframe(df_previsto[['data_formatada', 'prato', 'quantidade_prevista']])
            st.plotly_chart(visualizacoes.grafico_total_por_dia(df_previsto, coluna='quantidade_prevista', titulo="Total previsto por dia"), use_container_width=True)

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

        elif aba == "📎 Gráficos":
            prato = st.selectbox("🍽️ Escolha um prato para evolução", df_previsto['prato'].unique())
            df_filtro = df_previsto[df_previsto['prato'] == prato]
            fig = visualizacoes.grafico_total_por_dia(df_filtro, coluna='quantidade_prevista', titulo=f"Evolução prevista - {prato}")
            st.plotly_chart(fig, use_container_width=True)

        elif aba == "📥 Exportar":
            st.subheader("📥 Baixar dados")
            buffer = exportacao.gerar_excel(df)
            st.download_button("📄 Baixar dados reais em Excel", data=buffer, file_name="pedidos_reais.xlsx")
            buffer_prev = exportacao.gerar_excel(df_previsto, nome_aba="Previsao")
            st.download_button("📄 Baixar previsões em Excel", data=buffer_prev, file_name="previsao_pedidos.xlsx")
