import pandas as pd

def carregar_csv(caminho_arquivo):
    """
    Lê um arquivo CSV e normaliza os nomes das colunas.
    Remove espaços, acentos e converte para minúsculas.
    """
    df = pd.read_csv(caminho_arquivo)

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("ã", "a")
        .str.replace("ç", "c")
        .str.replace("á", "a")
        .str.replace("é", "e")
        .str.replace("í", "i")
        .str.replace("ó", "o")
        .str.replace("ú", "u")
    )

    return df

def validar_colunas(df, obrigatorias=('data', 'prato', 'quantidade')):
    """
    Verifica se o DataFrame possui todas as colunas obrigatórias.
    Retorna False se estiver vazio ou se alguma coluna estiver faltando.
    """
    if df is None or df.empty:
        return False

    colunas_normalizadas = set(df.columns)
    return set(obrigatorias).issubset(colunas_normalizadas)
