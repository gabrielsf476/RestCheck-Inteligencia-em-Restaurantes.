import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Validador CSV · RestCheck", layout="centered")
st.title("📄 Validador de Arquivo CSV · RestCheck")
st.caption("Verifique se seu arquivo está pronto para previsão de pedidos com IA")

# 🎨 Requisitos do RestCheck
colunas_obrigatorias = {'data', 'prato', 'quantidade'}

# 📁 Upload
arquivo = st.file_uploader("🔍 Envie seu arquivo de pedidos (.csv)", type=["csv"])

if arquivo:
    try:
        conteudo = arquivo.read().decode("utf-8")
        df = pd.read_csv(io.StringIO(conteudo))
        st.success("✅ Arquivo lido com sucesso!")

        # 🧪 Verificação de colunas
        colunas_atuais = set(df.columns.str.lower().str.strip())
        faltando = colunas_obrigatorias - colunas_atuais

        if not faltando:
            st.success("✅ Estrutura válida: todas as colunas obrigatórias estão presentes.")
            st.write("📋 Prévia dos dados:")
            st.dataframe(df.head(5), use_container_width=True)
            st.markdown("✅ Pronto para ser usado no RestCheck!")

        else:
            st.error("❌ Colunas obrigatórias ausentes:")
            for col in faltando:
                st.markdown(f"- `{col}`")
            st.warning("Corrija o nome das colunas e salve novamente como `.csv` UTF-8")

        # 📊 Extras úteis
        st.markdown("### 📊 Análise rápida")
        st.write("Número de linhas:", len(df))
        st.write("Colunas detectadas:", list(df.columns))

    except Exception as e:
        st.error(f"❌ Erro ao processar arquivo: {e}")
else:
    st.info("👈 Envie um arquivo `.csv` com as colunas obrigatórias: `data`, `prato`, `quantidade`.")
