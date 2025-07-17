import plotly.express as px

def grafico_total_por_dia(df, coluna='quantidade', titulo="Total por dia"):
    totais = df.groupby('data_formatada')[coluna].sum().reset_index()
    media = totais[coluna].mean()
    totais['acima_media'] = totais[coluna] > media
    fig = px.bar(totais, x='data_formatada', y=coluna, color='acima_media',
                 color_discrete_map={True: 'crimson', False: 'steelblue'},
                 title=titulo)
    return fig

def gerar_tabela_por_prato(df):
    tabela = df.groupby(['prato', 'data_formatada'])['quantidade'].sum().reset_index()
    return tabela.pivot_table(index='prato', columns='data_formatada', values='quantidade', fill_value=0)
