#!/usr/bin/env python3
"""
Dashboard interativo para visualização e análise de dados de sensores industriais.
Implementado com Dash e Plotly.
"""
import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy import stats
import os
import argparse
from datetime import datetime
import dash_auth
import smtplib
from email.mime.text import MIMEText

# Inicializa o app Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Autenticação básica
VALID_USERNAME_PASSWORD_PAIRS = {
    'admin': 'senha123'
}
auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

# Layout do dashboard
app.layout = html.Div([
    html.H1("Dashboard de Análise de Sensores Industriais", style={'textAlign': 'center'}),
    
    html.Div([
        html.Div([
            html.H3("Configurações", style={'textAlign': 'center'}),
            
            html.Label("Selecione o arquivo de dados:"),
            dcc.Dropdown(id='file-dropdown', style={'marginBottom': '10px'}),
            
            html.Label("Selecione o sensor:"),
            dcc.Dropdown(id='sensor-dropdown', style={'marginBottom': '10px'}),
            
            html.Label("Tipo de gráfico:"),
            dcc.Dropdown(
                id='chart-type-dropdown',
                options=[
                    {'label': 'Série Temporal', 'value': 'time_series'},
                    {'label': 'Histograma', 'value': 'histogram'},
                    {'label': 'Box Plot', 'value': 'box_plot'},
                    {'label': 'Dispersão', 'value': 'scatter'},
                    {'label': 'Mapa de Calor', 'value': 'heatmap'}
                ],
                value='time_series',
                style={'marginBottom': '10px'}
            ),
            
            html.Div(id='scatter-options', style={'display': 'none'}, children=[
                html.Label("Selecione o segundo sensor (para dispersão):"),
                dcc.Dropdown(id='sensor2-dropdown', style={'marginBottom': '10px'})
            ]),
            
            html.Label("Detecção de Anomalias:"),
            dcc.Dropdown(
                id='anomaly-method-dropdown',
                options=[
                    {'label': 'Nenhum', 'value': 'none'},
                    {'label': 'Z-Score', 'value': 'zscore'},
                    {'label': 'IQR', 'value': 'iqr'},
                    {'label': 'Isolation Forest', 'value': 'isolation_forest'}
                ],
                value='none',
                style={'marginBottom': '10px'}
            ),
            
            html.Div(id='zscore-options', style={'display': 'none'}, children=[
                html.Label("Limiar Z-Score:"),
                dcc.Slider(
                    id='zscore-threshold-slider',
                    min=1,
                    max=5,
                    step=0.1,
                    value=3,
                    marks={i: str(i) for i in range(1, 6)},
                    tooltip={"placement": "bottom", "always_visible": True}
                )
            ]),
            
            html.Button('Atualizar Gráfico', id='update-button', n_clicks=0, 
                       style={'marginTop': '20px', 'width': '100%'})
        ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),
        
        html.Div([
            html.H3("Visualização", style={'textAlign': 'center'}),
            dcc.Graph(id='main-graph', style={'height': '60vh'})
        ], style={'width': '75%', 'display': 'inline-block', 'padding': '20px'})
    ]),
    
    html.Div([
        html.H3("Estatísticas", style={'textAlign': 'center'}),
        html.Div(id='stats-container', style={'padding': '20px'})
    ])
])

# Callback para atualizar as opções de arquivo
@app.callback(
    Output('file-dropdown', 'options'),
    Input('file-dropdown', 'id')  # Dummy input para inicializar
)
def update_file_options(dummy):
    # Lista os arquivos CSV no diretório de dados
    data_dir = os.path.join(os.getcwd(), 'data')
    if not os.path.exists(data_dir):
        return [{'label': 'Nenhum arquivo encontrado', 'value': 'none'}]
    
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    if not csv_files:
        return [{'label': 'Nenhum arquivo encontrado', 'value': 'none'}]
    
    return [{'label': f, 'value': os.path.join(data_dir, f)} for f in csv_files]

# Callback para atualizar as opções de sensor
@app.callback(
    [Output('sensor-dropdown', 'options'),
     Output('sensor-dropdown', 'value'),
     Output('sensor2-dropdown', 'options')],
    [Input('file-dropdown', 'value')]
)
def update_sensor_options(file_path):
    if not file_path or file_path == 'none':
        return [], None, []
    
    try:
        # Carrega o arquivo
        df = pd.read_csv(file_path)
        
        # Identifica as colunas de sensores
        non_sensor_cols = ['timestamp', 'datetime', 'mode', 'status', 'anomaly']
        sensor_cols = [col for col in df.columns if col not in non_sensor_cols]
        
        options = [{'label': col, 'value': col} for col in sensor_cols]
        default_value = sensor_cols[0] if sensor_cols else None
        
        return options, default_value, options
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return [], None, []

# Callback para mostrar/esconder opções específicas
@app.callback(
    [Output('scatter-options', 'style'),
     Output('zscore-options', 'style')],
    [Input('chart-type-dropdown', 'value'),
     Input('anomaly-method-dropdown', 'value')]
)
def toggle_options(chart_type, anomaly_method):
    scatter_style = {'display': 'block'} if chart_type == 'scatter' else {'display': 'none'}
    zscore_style = {'display': 'block'} if anomaly_method == 'zscore' else {'display': 'none'}
    
    return scatter_style, zscore_style

# Função para detectar anomalias
def detect_anomalies(df, sensor_col, method, threshold=3.0):
    if method == 'none':
        return df, []
    
    # Cria uma cópia do DataFrame
    result_df = df.copy()
    
    if method == 'zscore':
        # Calcula o Z-Score
        z_scores = np.abs(stats.zscore(result_df[sensor_col].dropna()))
        anomaly_indices = np.where(z_scores > threshold)[0]
    
    elif method == 'iqr':
        # Calcula Q1, Q3 e IQR
        q1 = result_df[sensor_col].quantile(0.25)
        q3 = result_df[sensor_col].quantile(0.75)
        iqr = q3 - q1
        
        # Define os limites
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        # Identifica anomalias
        anomaly_indices = result_df[
            (result_df[sensor_col] < lower_bound) | 
            (result_df[sensor_col] > upper_bound)
        ].index.tolist()
    
    elif method == 'isolation_forest':
        from sklearn.ensemble import IsolationForest
        
        # Prepara os dados
        X = result_df[sensor_col].values.reshape(-1, 1)
        
        # Aplica o algoritmo
        model = IsolationForest(contamination=0.05, random_state=42)
        preds = model.fit_predict(X)
        
        # Identifica anomalias
        anomaly_indices = np.where(preds == -1)[0]
    
    else:
        return df, []
    
    return result_df, anomaly_indices

# Callback para atualizar o gráfico principal
@app.callback(
    Output('main-graph', 'figure'),
    [Input('update-button', 'n_clicks')],
    [State('file-dropdown', 'value'),
     State('sensor-dropdown', 'value'),
     State('sensor2-dropdown', 'value'),
     State('chart-type-dropdown', 'value'),
     State('anomaly-method-dropdown', 'value'),
     State('zscore-threshold-slider', 'value')]
)
def update_graph(n_clicks, file_path, sensor_col, sensor2_col, chart_type, anomaly_method, zscore_threshold):
    if not file_path or file_path == 'none' or not sensor_col:
        return go.Figure()
    
    try:
        # Carrega o arquivo
        df = pd.read_csv(file_path)
        
        # Converte timestamp para datetime se existir
        if 'timestamp' in df.columns and 'datetime' not in df.columns:
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
        
        # Detecta anomalias
        df, anomaly_indices = detect_anomalies(df, sensor_col, anomaly_method, zscore_threshold)
        
        # Cria o gráfico de acordo com o tipo selecionado
        if chart_type == 'time_series':
            fig = create_time_series(df, sensor_col, anomaly_indices)
        elif chart_type == 'histogram':
            fig = create_histogram(df, sensor_col, anomaly_indices)
        elif chart_type == 'box_plot':
            fig = create_box_plot(df, sensor_col, anomaly_indices)
        elif chart_type == 'scatter':
            fig = create_scatter(df, sensor_col, sensor2_col, anomaly_indices)
        elif chart_type == 'heatmap':
            fig = create_heatmap(df)
        else:
            fig = go.Figure()
        
        return fig
    
    except Exception as e:
        print(f"Erro ao criar o gráfico: {e}")
        return go.Figure()

def create_time_series(df, sensor_col, anomaly_indices):
    """Cria um gráfico de série temporal"""
    fig = go.Figure()
    
    # Adiciona a série temporal
    fig.add_trace(go.Scatter(
        x=df['datetime'] if 'datetime' in df.columns else df.index,
        y=df[sensor_col],
        mode='lines+markers',
        name=sensor_col,
        marker=dict(size=6)
    ))
    
    # Adiciona anomalias se existirem
    if len(anomaly_indices) > 0:
        anomaly_df = df.iloc[anomaly_indices]
        fig.add_trace(go.Scatter(
            x=anomaly_df['datetime'] if 'datetime' in df.columns else anomaly_df.index,
            y=anomaly_df[sensor_col],
            mode='markers',
            name='Anomalias',
            marker=dict(color='red', size=10, symbol='x')
        ))
    
    # Configura o layout
    fig.update_layout(
        title=f'Série Temporal - {sensor_col}',
        xaxis_title='Tempo' if 'datetime' in df.columns else 'Índice',
        yaxis_title=sensor_col,
        template='plotly_white'
    )
    
    return fig

def create_histogram(df, sensor_col, anomaly_indices):
    """Cria um histograma"""
    # Dados normais
    normal_data = df[sensor_col]
    if len(anomaly_indices) > 0:
        normal_data = df.drop(anomaly_indices)[sensor_col]
    
    fig = go.Figure()
    
    # Adiciona histograma para dados normais
    fig.add_trace(go.Histogram(
        x=normal_data,
        name='Normal',
        opacity=0.7,
        nbinsx=30
    ))
    
    # Adiciona histograma para anomalias se existirem
    if len(anomaly_indices) > 0:
        anomaly_data = df.iloc[anomaly_indices][sensor_col]
        fig.add_trace(go.Histogram(
            x=anomaly_data,
            name='Anomalias',
            opacity=0.7,
            nbinsx=30
        ))
    
    # Configura o layout
    fig.update_layout(
        title=f'Histograma - {sensor_col}',
        xaxis_title=sensor_col,
        yaxis_title='Frequência',
        barmode='overlay',
        template='plotly_white'
    )
    
    return fig

def create_box_plot(df, sensor_col, anomaly_indices):
    """Cria um box plot"""
    fig = go.Figure()
    
    # Adiciona box plot
    fig.add_trace(go.Box(
        y=df[sensor_col],
        name=sensor_col,
        boxpoints='outliers',
        jitter=0.3,
        pointpos=-1.8,
        boxmean=True
    ))
    
    # Configura o layout
    fig.update_layout(
        title=f'Box Plot - {sensor_col}',
        yaxis_title=sensor_col,
        template='plotly_white'
    )
    
    return fig

def create_scatter(df, sensor_col, sensor2_col, anomaly_indices):
    """Cria um gráfico de dispersão"""
    if not sensor2_col:
        return go.Figure()
    
    fig = go.Figure()
    
    # Dados normais
    normal_df = df
    if len(anomaly_indices) > 0:
        normal_df = df.drop(anomaly_indices)
    
    # Adiciona pontos normais
    fig.add_trace(go.Scatter(
        x=normal_df[sensor_col],
        y=normal_df[sensor2_col],
        mode='markers',
        name='Normal',
        marker=dict(size=8)
    ))
    
    # Adiciona anomalias se existirem
    if len(anomaly_indices) > 0:
        anomaly_df = df.iloc[anomaly_indices]
        fig.add_trace(go.Scatter(
            x=anomaly_df[sensor_col],
            y=anomaly_df[sensor2_col],
            mode='markers',
            name='Anomalias',
            marker=dict(color='red', size=10, symbol='x')
        ))
    
    # Adiciona linha de tendência
    x = df[sensor_col]
    y = df[sensor2_col]
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    
    fig.add_trace(go.Scatter(
        x=x,
        y=p(x),
        mode='lines',
        name='Tendência',
        line=dict(color='black', dash='dash')
    ))
    
    # Configura o layout
    fig.update_layout(
        title=f'Dispersão - {sensor_col} vs {sensor2_col}',
        xaxis_title=sensor_col,
        yaxis_title=sensor2_col,
        template='plotly_white'
    )
    
    return fig

def create_heatmap(df):
    """Cria um mapa de calor de correlação"""
    # Identifica as colunas de sensores
    non_sensor_cols = ['timestamp', 'datetime', 'mode', 'status', 'anomaly']
    sensor_cols = [col for col in df.columns if col not in non_sensor_cols]
    
    # Calcula a matriz de correlação
    corr_matrix = df[sensor_cols].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu_r',
        zmin=-1,
        zmax=1,
        colorbar=dict(title='Correlação'),
        text=np.round(corr_matrix.values, 2),
        texttemplate='%{text:.2f}'
    ))
    
    # Configura o layout
    fig.update_layout(
        title='Matriz de Correlação entre Sensores',
        template='plotly_white'
    )
    
    return fig

# Callback para atualizar as estatísticas
@app.callback(
    Output('stats-container', 'children'),
    [Input('update-button', 'n_clicks')],
    [State('file-dropdown', 'value'),
     State('sensor-dropdown', 'value'),
     State('anomaly-method-dropdown', 'value'),
     State('zscore-threshold-slider', 'value')]
)
def update_stats(n_clicks, file_path, sensor_col, anomaly_method, zscore_threshold):
    if not file_path or file_path == 'none' or not sensor_col:
        return html.Div("Selecione um arquivo e um sensor para ver as estatísticas.")
    
    try:
        # Carrega o arquivo
        df = pd.read_csv(file_path)
        
        # Detecta anomalias
        df, anomaly_indices = detect_anomalies(df, sensor_col, anomaly_method, zscore_threshold)
        
        # Calcula estatísticas básicas
        stats = {
            'Média': df[sensor_col].mean(),
            'Mediana': df[sensor_col].median(),
            'Desvio Padrão': df[sensor_col].std(),
            'Mínimo': df[sensor_col].min(),
            'Máximo': df[sensor_col].max(),
            'Q1 (25%)': df[sensor_col].quantile(0.25),
            'Q3 (75%)': df[sensor_col].quantile(0.75),
            'IQR': df[sensor_col].quantile(0.75) - df[sensor_col].quantile(0.25),
            'Assimetria': stats.skew(df[sensor_col].dropna()),
            'Curtose': stats.kurtosis(df[sensor_col].dropna()),
            'Total de Registros': len(df),
            'Valores Nulos': df[sensor_col].isna().sum()
        }
        
        # Adiciona estatísticas de anomalias
        if anomaly_method != 'none':
            stats['Anomalias Detectadas'] = len(anomaly_indices)
            stats['Percentual de Anomalias'] = len(anomaly_indices) / len(df) * 100
        
        # Cria a tabela de estatísticas
        stats_table = html.Table([
            html.Thead(html.Tr([html.Th("Estatística"), html.Th("Valor")])),
            html.Tbody([
                html.Tr([html.Td(k), html.Td(f"{v:.4f}" if isinstance(v, float) else str(v))])
                for k, v in stats.items()
            ])
        ], style={'width': '100%', 'border': '1px solid #ddd', 'borderCollapse': 'collapse'})
        
        return stats_table
    
    except Exception as e:
        print(f"Erro ao calcular estatísticas: {e}")
        return html.Div(f"Erro ao calcular estatísticas: {str(e)}")

def send_email_notification(subject, body, to_email):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'monitor@empresa.com'
    msg['To'] = to_email
    with smtplib.SMTP('smtp.seuprovedor.com', 587) as server:
        server.starttls()
        server.login('monitor@empresa.com', 'SENHA_DO_EMAIL')
        server.sendmail('monitor@empresa.com', [to_email], msg.as_string())

def main():
    parser = argparse.ArgumentParser(description='Dashboard interativo para análise de sensores industriais')
    parser.add_argument('--port', type=int, default=8050, help='Porta para o servidor web')
    parser.add_argument('--debug', action='store_true', help='Executar em modo debug')
    
    args = parser.parse_args()
    
    print(f"Iniciando dashboard na porta {args.port}...")
    print(f"Acesse http://localhost:{args.port} no seu navegador")
    
    app.run_server(debug=args.debug, port=args.port)

if __name__ == '__main__':
    main()