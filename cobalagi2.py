import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# df = pd.read_csv('D:\Task\Dataset\Tidak Berjudul 1.csv')

# app = dash.Dash()

app.layout = html.Div(
    children=[
        html.H1(children='Indeks Kebahagiaan Dunia', style={'textAlign': 'center'}),
        html.Hr(style={'width':'100%'}),

        html.Div(
            [
                html.H2(children='Skor Indikator Kebahagiaan'),
                html.Div(
                    [

                        html.Div(
                            [
                                html.P('Pilih Tahun :'),
                                dcc.Dropdown(
                                    id='tahun_dropdown',
                                    options=[
                                        {'label': '2018', 'value': '1'},
                                        {'label': '2019', 'value': '2'},
                                    ],
                                    value='2',
                                    clearable=False,
                                ),
                                html.P('Pilih Indikator :'),
                                dcc.Dropdown(
                                    id='demo_dropdown',
                                    options=[
                                        {'label': 'Score', 'value': '1'},
                                        {'label': 'GDP', 'value': '2'},
                                        {'label': 'Dukungan Sosial', 'value': '3'},
                                        {'label': 'Hidup Sehat', 'value': '4'},
                                        {'label': 'Kebebasan', 'value': '5'},
                                        {'label': 'Dermawan', 'value': '6'},
                                        {'label': 'Korupsi', 'value': '7'},
                                    ],
                                    value=''
                                ),
                            ],
                            className='col-sm-2 offset-sm-1'
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id='grafik'
                                )
                            ],
                            className='col-sm-8'
                        ),
                    ],
                    className='row justify-content-center',
                ),
                html.Hr(),
                html.H2(children='Perbandingan Indikator Kebahagiaan Indonesia dengan 10 Negara Terbaik Tahun 2019'),
                html.Div(
                    [
                        html.Div(
                            [

                                html.P('Pilih Indikator :'),
                                dcc.Dropdown(
                                    id='indikator',
                                    options=[
                                        {'label': 'Score', 'value': '1','disabled':True},
                                        {'label': 'GDP', 'value': '2'},
                                        {'label': 'Dukungan Sosial', 'value': '3'},
                                        {'label': 'Hidup Sehat', 'value': '4'},
                                        {'label': 'Kebebasan', 'value': '5'},
                                        {'label': 'Dermawan', 'value': '6'},
                                        {'label': 'Korupsi', 'value': '7'},
                                    ],
                                    value='',
                                    multi=True,
                                ),
                            ],
                            className='col-sm-2 offset-sm-1'
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id='grafik_2'
                                )
                            ],
                            className='col-sm-8'
                        ),
                    ],
                    className='row justify-content-center',
                    style={'margin-top': '10'}
                ),
            ],
            # className='row'
            style={'textAlign': 'center'}
        ),
    ]
)


@app.callback(
    dash.dependencies.Output('grafik', 'figure'),
    [dash.dependencies.Input('demo_dropdown', 'value'),
     dash.dependencies.Input('tahun_dropdown', 'value')])
def update_graph(demo_dropdown, tahun_dropdown):
    df = []
    data = []
    warna = 'Blues'
    judul = 'Judul'
    balik = False

    if '1' in tahun_dropdown:
        df = pd.read_csv('D:\Task\Dataset\Tidak Berjudul 2.csv')
    if '2' in tahun_dropdown:
        df = pd.read_csv('D:\Task\Dataset\Tidak Berjudul 1.csv')

    if '1' in demo_dropdown:
        data = df['Score']
        judul = 'Skor'
    if '2' in demo_dropdown:
        data = df['GDP per capita']
        judul = 'GDP'
    if '3' in demo_dropdown:
        data = df['Social support']
        judul = 'Sosial'
    if '4' in demo_dropdown:
        data = df['Healthy life expectancy']
        judul = 'Hidup Sehat'
        warna = 'Greens'
    if '5' in demo_dropdown:
        data = df['Freedom to make life choices']
        judul = 'Kebebasan'
    if '6' in demo_dropdown:
        data = df['Generosity']
        judul = 'Dermawan'
        warna = 'Greens'
    if '7' in demo_dropdown:
        data = df['Perceptions of corruption']
        judul = 'Korupsi'
        warna = 'Reds'
        balik = True

    fig = go.Figure(
        data=go.Choropleth(
            locations=df['CODE'],
            z=data,
            text=df['Country or region'],
            colorscale=warna,
            autocolorscale=False,
            reversescale=balik,
            marker_line_color='gray',
            marker_line_width=0.5,
            colorbar_tickprefix='',
            colorbar_title='Nilai',
        )
    )

    fig.update_layout(
        title_text=judul,
        geo=dict(
            showframe=True,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        annotations=[dict(
            x=0.55,
            y=0.1,
            xref='paper',
            yref='paper',
            text='Source: <a href="https://www.kaggle.com/unsdsn/world-happiness">\
                Kaggle</a>',
            showarrow=False
        )]
    )
    return fig

@app.callback(
    dash.dependencies.Output('grafik_2', 'figure'),
    [dash.dependencies.Input('indikator', 'value')])
def update_graph(indikator):
    Skor = go.Bar()
    GDP = go.Bar()
    Sosial = go.Bar()
    Kesehatan = go.Bar()
    Kebebasan = go.Bar()
    Dermawan = go.Bar()
    Korupsi = go.Bar()

    df_sementara = pd.read_csv('https://query.data.world/s/c55vrlpwbm2p3ixwrctg73uq2tftbq')
    df_sementara = df_sementara.sort_values(by='Ladder',ascending=True)
    df2 = df_sementara[:10]
    tambah = df_sementara.loc[df_sementara['Country (region)'] == 'Indonesia']
    df2 = df2.append(tambah)

    # if '1' in indikator:
    #     Skor = go.Bar(
    #         x=df2['Country or region'],
    #         y=df2['Score'],
    #         name='Skor'
    #     )
    if '2' in indikator:
        GDP = go.Bar(
            x=df2['Country (region)'],
            y=155 - df2['Log of GDP\nper capita'],
            name='GDP'
        )
    if '3' in indikator:
        Sosial = go.Bar(
            x=df2['Country (region)'],
            y=155 - df2['Social support'],
            name='Dukungan Sosial'
        )
    if '4' in indikator:
        Kesehatan = go.Bar(
            x=df2['Country (region)'],
            y=155 - df2['Healthy life\nexpectancy'],
            name='Hidup Sehat'
        )
    if '5' in indikator:
        Kebebasan = go.Bar(
            x=df2['Country (region)'],
            y=155 - df2['Freedom'],
            name='Kebebasan'
        )
    if '6' in indikator:
        Dermawan = go.Bar(
            x=df2['Country (region)'],
            y=155 - df2['Generosity'],
            name='Dermawan'
        )
    if '7' in indikator:
        Korupsi = go.Bar(
            x=df2['Country (region)'],
            y=155 - df2['Corruption'],
            name='Korupsi'
        )

    data_trace = [Skor, GDP, Sosial, Kesehatan, Kebebasan, Dermawan, Korupsi]

    fig = go.Figure(data=data_trace)

    fig.update_layout(
                      plot_bgcolor='rgb(230, 230,230)',
                      showlegend=True)
    return (fig)

if __name__ == '__main__':
    app.run_server(debug=True)