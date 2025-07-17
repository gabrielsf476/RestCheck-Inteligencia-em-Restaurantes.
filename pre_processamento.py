import pandas as pd

def tratar_dados(df):
    # Converter a coluna de datas
    df['data'] = pd.to_datetime(df['data'], errors='coerce')
    df['data_formatada'] = df['data'].dt.strftime('%d/%m/%Y')

    # Dicionário para dias da semana em português
    dias_pt = {
        'Monday': 'segunda-feira',
        'Tuesday': 'terça-feira',
        'Wednesday': 'quarta-feira',
        'Thursday': 'quinta-feira',
        'Friday': 'sexta-feira',
        'Saturday': 'sábado',
        'Sunday': 'domingo'
    }

    # Dicionário para meses em português
    meses_pt = {
        'January': 'janeiro',
        'February': 'fevereiro',
        'March': 'março',
        'April': 'abril',
        'May': 'maio',
        'June': 'junho',
        'July': 'julho',
        'August': 'agosto',
        'September': 'setembro',
        'October': 'outubro',
        'November': 'novembro',
        'December': 'dezembro'
    }

    # Aplicar os nomes localizados
    df['dia_semana'] = df['data'].dt.day_name().map(dias_pt)
    df['mes'] = df['data'].dt.month_name().map(meses_pt)

    # Extras para agrupamentos
    df['semana'] = df['data'].dt.isocalendar().week
    df['ano'] = df['data'].dt.year

    return df
