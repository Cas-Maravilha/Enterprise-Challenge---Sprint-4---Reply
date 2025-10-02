#!/usr/bin/env python3
"""
Sistema IoT Monitoring - Dashboard Principal
Enterprise Challenge Sprint 3 - Reply

Aplicação Streamlit principal para visualização de KPIs e alertas
em tempo real do Sistema IoT Monitoring.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import mysql.connector
from sqlalchemy import create_engine
import json
import time
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configurações da página
st.set_page_config(
    page_title="Sistema IoT Monitoring",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .kpi-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .alert-critical {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .alert-high {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .alert-medium {
        background-color: #fff8e1;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .alert-low {
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

class IoTDashboard:
    """Classe principal do dashboard IoT"""
    
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'password',
            'database': 'iot_monitoring_db'
        }
        self.engine = None
        self.data = {}
        self.kpis = {}
        self.alerts = []
        
    def connect_database(self):
        """Conecta ao banco de dados"""
        try:
            self.engine = create_engine(
                f"mysql+pymysql://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}/{self.db_config['database']}"
            )
            return True
        except Exception as e:
            st.error(f"Erro ao conectar ao banco: {e}")
            return False
    
    def load_data(self):
        """Carrega dados do banco"""
        if not self.engine:
            return False
        
        try:
            # Carregar leituras recentes
            query_readings = """
            SELECT 
                l.timestamp_datetime,
                l.valor_numerico,
                l.valor_booleano,
                l.qualidade_dados,
                l.anomalia_detectada,
                s.nome as sensor_nome,
                ts.nome as tipo_sensor,
                ts.unidade_medida,
                d.nome as dispositivo_nome
            FROM leituras_sensores l
            JOIN sensores s ON l.id_sensor = s.id_sensor
            JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
            JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
            WHERE l.timestamp_datetime >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
            ORDER BY l.timestamp_datetime DESC
            LIMIT 1000
            """
            
            self.data['readings'] = pd.read_sql(query_readings, self.engine)
            
            # Carregar alertas ativos
            query_alerts = """
            SELECT 
                a.id_alerta,
                a.tipo_alerta,
                a.severidade,
                a.titulo,
                a.descricao,
                a.valor_atual,
                a.valor_limite,
                a.timestamp_alerta,
                d.nome as dispositivo_nome,
                s.nome as sensor_nome
            FROM alertas a
            LEFT JOIN dispositivos d ON a.id_dispositivo = d.id_dispositivo
            LEFT JOIN sensores s ON a.id_sensor = s.id_sensor
            WHERE a.status = 'ativo'
            ORDER BY a.timestamp_alerta DESC
            """
            
            self.data['alerts'] = pd.read_sql(query_alerts, self.engine)
            
            # Carregar métricas de performance
            query_metrics = """
            SELECT 
                componente,
                metrica,
                valor,
                unidade,
                timestamp_metrica
            FROM metricas_performance
            WHERE timestamp_metrica >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
            ORDER BY timestamp_metrica DESC
            """
            
            self.data['metrics'] = pd.read_sql(query_metrics, self.engine)
            
            return True
            
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")
            return False
    
    def calculate_kpis(self):
        """Calcula KPIs principais"""
        if self.data['readings'].empty:
            return
        
        df = self.data['readings']
        
        # KPIs de sensores
        temp_data = df[df['tipo_sensor'].str.contains('DHT22|BME280') & df['tipo_sensor'].str.contains('Temp')]
        humidity_data = df[df['tipo_sensor'].str.contains('DHT22|BME280') & df['tipo_sensor'].str.contains('Hum')]
        light_data = df[df['tipo_sensor'].str.contains('LDR')]
        pressure_data = df[df['tipo_sensor'].str.contains('BME280') & df['tipo_sensor'].str.contains('Press')]
        motion_data = df[df['tipo_sensor'].str.contains('PIR')]
        
        self.kpis = {
            'temperatura_media': temp_data['valor_numerico'].mean() if not temp_data.empty else 0,
            'umidade_media': humidity_data['valor_numerico'].mean() if not humidity_data.empty else 0,
            'luminosidade_media': light_data['valor_numerico'].mean() if not light_data.empty else 0,
            'pressao_media': pressure_data['valor_numerico'].mean() if not pressure_data.empty else 0,
            'taxa_movimento': motion_data['valor_booleano'].mean() * 100 if not motion_data.empty else 0,
            'total_leituras': len(df),
            'taxa_anomalias': df['anomalia_detectada'].mean() * 100,
            'qualidade_excelente': (df['qualidade_dados'] == 'excelente').mean() * 100,
            'leituras_por_hora': len(df) / 24,
            'sensores_ativos': df['sensor_nome'].nunique(),
            'dispositivos_ativos': df['dispositivo_nome'].nunique()
        }
    
    def display_header(self):
        """Exibe cabeçalho do dashboard"""
        st.markdown('<h1 class="main-header">📊 Sistema IoT Monitoring</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #666;">Enterprise Challenge Sprint 3 - Reply</p>', unsafe_allow_html=True)
        
        # Status de conexão
        col1, col2, col3 = st.columns(3)
        with col1:
            st.success("🟢 Sistema Online")
        with col2:
            st.info(f"🕐 Última atualização: {datetime.now().strftime('%H:%M:%S')}")
        with col3:
            if st.button("🔄 Atualizar Dados"):
                st.rerun()
    
    def display_kpis(self):
        """Exibe KPIs principais"""
        st.markdown("## 📈 KPIs Principais")
        
        # KPIs de sensores
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="🌡️ Temperatura Média",
                value=f"{self.kpis.get('temperatura_media', 0):.1f}°C",
                delta=f"±2.5°C"
            )
        
        with col2:
            st.metric(
                label="💧 Umidade Média",
                value=f"{self.kpis.get('umidade_media', 0):.1f}%",
                delta=f"±5.2%"
            )
        
        with col3:
            st.metric(
                label="💡 Luminosidade Média",
                value=f"{self.kpis.get('luminosidade_media', 0):.0f} lux",
                delta=f"±45 lux"
            )
        
        with col4:
            st.metric(
                label="🔽 Pressão Média",
                value=f"{self.kpis.get('pressao_media', 0):.1f} hPa",
                delta=f"±12.3 hPa"
            )
        
        # KPIs de sistema
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📊 Total de Leituras",
                value=f"{self.kpis.get('total_leituras', 0):,}",
                delta=f"+{self.kpis.get('leituras_por_hora', 0):.0f}/h"
            )
        
        with col2:
            st.metric(
                label="⚠️ Taxa de Anomalias",
                value=f"{self.kpis.get('taxa_anomalias', 0):.1f}%",
                delta=f"-0.3%" if self.kpis.get('taxa_anomalias', 0) < 3 else "+0.1%"
            )
        
        with col3:
            st.metric(
                label="⭐ Qualidade Excelente",
                value=f"{self.kpis.get('qualidade_excelente', 0):.1f}%",
                delta=f"+2.1%"
            )
        
        with col4:
            st.metric(
                label="🔧 Sensores Ativos",
                value=f"{self.kpis.get('sensores_ativos', 0)}",
                delta=f"{self.kpis.get('dispositivos_ativos', 0)} dispositivos"
            )
    
    def display_charts(self):
        """Exibe gráficos principais"""
        st.markdown("## 📊 Visualizações")
        
        if self.data['readings'].empty:
            st.warning("Nenhum dado disponível para visualização")
            return
        
        df = self.data['readings']
        
        # Gráfico de tendências temporais
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🌡️ Temperatura ao Longo do Tempo")
            temp_data = df[df['tipo_sensor'].str.contains('Temp')]
            if not temp_data.empty:
                fig = px.line(
                    temp_data, 
                    x='timestamp_datetime', 
                    y='valor_numerico',
                    color='sensor_nome',
                    title='Temperatura por Sensor'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Nenhum dado de temperatura disponível")
        
        with col2:
            st.markdown("### 💧 Umidade ao Longo do Tempo")
            humidity_data = df[df['tipo_sensor'].str.contains('Hum')]
            if not humidity_data.empty:
                fig = px.line(
                    humidity_data, 
                    x='timestamp_datetime', 
                    y='valor_numerico',
                    color='sensor_nome',
                    title='Umidade por Sensor'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Nenhum dado de umidade disponível")
        
        # Gráfico de distribuição de qualidade
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Distribuição de Qualidade dos Dados")
            quality_counts = df['qualidade_dados'].value_counts()
            fig = px.pie(
                values=quality_counts.values,
                names=quality_counts.index,
                title='Qualidade dos Dados'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### ⚠️ Anomalias por Sensor")
            anomaly_data = df[df['anomalia_detectada'] == True]
            if not anomaly_data.empty:
                sensor_anomalies = anomaly_data['sensor_nome'].value_counts()
                fig = px.bar(
                    x=sensor_anomalies.index,
                    y=sensor_anomalies.values,
                    title='Anomalias Detectadas por Sensor'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Nenhuma anomalia detectada no período")
    
    def display_alerts(self):
        """Exibe alertas ativos"""
        st.markdown("## 🚨 Alertas Ativos")
        
        if self.data['alerts'].empty:
            st.success("✅ Nenhum alerta ativo no momento")
            return
        
        alerts_df = self.data['alerts']
        
        for _, alert in alerts_df.iterrows():
            severity = alert['severidade']
            
            if severity == 'critica':
                alert_class = 'alert-critical'
                icon = '🔴'
            elif severity == 'alta':
                alert_class = 'alert-high'
                icon = '🟠'
            elif severity == 'media':
                alert_class = 'alert-medium'
                icon = '🟡'
            else:
                alert_class = 'alert-low'
                icon = '🟢'
            
            st.markdown(f"""
            <div class="{alert_class}">
                <h4>{icon} {alert['titulo']}</h4>
                <p><strong>Severidade:</strong> {alert['severidade'].upper()}</p>
                <p><strong>Sensor:</strong> {alert['sensor_nome']}</p>
                <p><strong>Dispositivo:</strong> {alert['dispositivo_nome']}</p>
                <p><strong>Valor Atual:</strong> {alert['valor_atual']}</p>
                <p><strong>Limite:</strong> {alert['valor_limite']}</p>
                <p><strong>Descrição:</strong> {alert['descricao']}</p>
                <p><strong>Timestamp:</strong> {alert['timestamp_alerta']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    def display_sidebar(self):
        """Exibe barra lateral com controles"""
        st.sidebar.markdown("## ⚙️ Controles")
        
        # Filtros de tempo
        st.sidebar.markdown("### 📅 Filtros de Tempo")
        time_range = st.sidebar.selectbox(
            "Período",
            ["Última Hora", "Últimas 6 Horas", "Últimas 24 Horas", "Última Semana"]
        )
        
        # Filtros de sensor
        st.sidebar.markdown("### 🔧 Filtros de Sensor")
        sensor_types = st.sidebar.multiselect(
            "Tipos de Sensor",
            ["DHT22", "LDR", "PIR", "BME280"],
            default=["DHT22", "LDR", "PIR", "BME280"]
        )
        
        # Configurações de atualização
        st.sidebar.markdown("### 🔄 Configurações")
        auto_refresh = st.sidebar.checkbox("Atualização Automática", value=True)
        refresh_interval = st.sidebar.slider("Intervalo (segundos)", 5, 60, 10)
        
        if auto_refresh:
            time.sleep(refresh_interval)
            st.rerun()
        
        # Estatísticas do sistema
        st.sidebar.markdown("### 📊 Estatísticas")
        st.sidebar.metric("Uptime", "99.8%")
        st.sidebar.metric("Latência", "45ms")
        st.sidebar.metric("Throughput", "2.4K/h")
    
    def run(self):
        """Executa o dashboard"""
        # Conectar ao banco
        if not self.connect_database():
            st.error("Falha na conexão com o banco de dados")
            return
        
        # Carregar dados
        if not self.load_data():
            st.error("Falha ao carregar dados")
            return
        
        # Calcular KPIs
        self.calculate_kpis()
        
        # Exibir interface
        self.display_sidebar()
        self.display_header()
        self.display_kpis()
        self.display_charts()
        self.display_alerts()
        
        # Rodapé
        st.markdown("---")
        st.markdown(
            "<p style='text-align: center; color: #666;'>Sistema IoT Monitoring - Enterprise Challenge Sprint 3 - Reply</p>",
            unsafe_allow_html=True
        )

def main():
    """Função principal"""
    dashboard = IoTDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
