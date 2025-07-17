import pandas as pd

def tratar_dados(df):
    df['data'] = pd.to_datetime(df['data'], errors='coerce')
    df['data_formatada'] = df['data'].dt.strftime('%d/%m/%Y')
    df['dia_semana'] = df['data'].dt.day_name(locale='pt_BR')
    df['mes'] = df['data'].dt.month_name(locale='pt_BR')
    df['semana'] = df['data'].dt.isocalendar().week
    df['ano'] = df['data'].dt.year
    return df
