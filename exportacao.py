import pandas as pd
import io

def gerar_excel(df, nome_aba="Pedidos_Reais"):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=nome_aba)
    return buffer.getvalue()
