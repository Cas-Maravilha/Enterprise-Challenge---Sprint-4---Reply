#!/usr/bin/env python3
"""
Sistema IoT Monitoring - Sistema de Alertas
Enterprise Challenge Sprint 3 - Reply

Sistema de alertas em tempo real com notificações automáticas
e gerenciamento de alertas do Sistema IoT Monitoring.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import mysql.connector
from sqlalchemy import create_engine
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configurações da página
st.set_page_config(
    page_title="Alertas - Sistema IoT Monitoring",
    page_icon="🚨",
    layout="wide"
)

class SistemaAlertas:
    """Sistema de alertas do IoT Monitoring"""
    
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'password',
            'database': 'iot_monitoring_db'
        }
        self.engine = None
        self.alert_config = {
            'temperatura_alta': 35.0,
            'temperatura_baixa': 5.0,
            'umidade_alta': 90.0,
            'umidade_baixa': 20.0,
            'luminosidade_alta': 800.0,
            'luminosidade_baixa': 100.0,
            'pressao_alta': 1050.0,
            'pressao_baixa': 950.0
        }
        
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
    
    def load_alerts(self, status='ativo'):
        """Carrega alertas do banco"""
        if not self.engine:
            return pd.DataFrame()
        
        try:
            query = """
            SELECT 
                a.id_alerta,
                a.tipo_alerta,
                a.severidade,
                a.titulo,
                a.descricao,
                a.valor_atual,
                a.valor_limite,
                a.timestamp_alerta,
                a.status,
                a.resolved_at,
                d.nome as dispositivo_nome,
                s.nome as sensor_nome,
                ts.nome as tipo_sensor
            FROM alertas a
            LEFT JOIN dispositivos d ON a.id_dispositivo = d.id_dispositivo
            LEFT JOIN sensores s ON a.id_sensor = s.id_sensor
            LEFT JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
            WHERE a.status = %s
            ORDER BY a.timestamp_alerta DESC
            """
            
            return pd.read_sql(query, self.engine, params=[status])
            
        except Exception as e:
            st.error(f"Erro ao carregar alertas: {e}")
            return pd.DataFrame()
    
    def load_alert_history(self, days=7):
        """Carrega histórico de alertas"""
        if not self.engine:
            return pd.DataFrame()
        
        try:
            query = """
            SELECT 
                a.id_alerta,
                a.tipo_alerta,
                a.severidade,
                a.titulo,
                a.descricao,
                a.valor_atual,
                a.valor_limite,
                a.timestamp_alerta,
                a.status,
                a.resolved_at,
                d.nome as dispositivo_nome,
                s.nome as sensor_nome
            FROM alertas a
            LEFT JOIN dispositivos d ON a.id_dispositivo = d.id_dispositivo
            LEFT JOIN sensores s ON a.id_sensor = s.id_sensor
            WHERE a.timestamp_alerta >= DATE_SUB(NOW(), INTERVAL %s DAY)
            ORDER BY a.timestamp_alerta DESC
            """
            
            return pd.read_sql(query, self.engine, params=[days])
            
        except Exception as e:
            st.error(f"Erro ao carregar histórico: {e}")
            return pd.DataFrame()
    
    def check_thresholds(self, sensor_data):
        """Verifica se os dados ultrapassam os thresholds"""
        alerts = []
        
        for _, reading in sensor_data.iterrows():
            sensor_type = reading['tipo_sensor']
            value = reading['valor_numerico']
            
            if pd.isna(value):
                continue
            
            # Verificar temperatura
            if 'Temp' in sensor_type:
                if value > self.alert_config['temperatura_alta']:
                    alerts.append({
                        'tipo': 'temperatura_alta',
                        'severidade': 'critica' if value > 40 else 'alta',
                        'valor_atual': value,
                        'valor_limite': self.alert_config['temperatura_alta'],
                        'sensor': reading['sensor_nome'],
                        'dispositivo': reading['dispositivo_nome']
                    })
                elif value < self.alert_config['temperatura_baixa']:
                    alerts.append({
                        'tipo': 'temperatura_baixa',
                        'severidade': 'critica' if value < 0 else 'alta',
                        'valor_atual': value,
                        'valor_limite': self.alert_config['temperatura_baixa'],
                        'sensor': reading['sensor_nome'],
                        'dispositivo': reading['dispositivo_nome']
                    })
            
            # Verificar umidade
            elif 'Hum' in sensor_type:
                if value > self.alert_config['umidade_alta']:
                    alerts.append({
                        'tipo': 'umidade_alta',
                        'severidade': 'alta',
                        'valor_atual': value,
                        'valor_limite': self.alert_config['umidade_alta'],
                        'sensor': reading['sensor_nome'],
                        'dispositivo': reading['dispositivo_nome']
                    })
                elif value < self.alert_config['umidade_baixa']:
                    alerts.append({
                        'tipo': 'umidade_baixa',
                        'severidade': 'media',
                        'valor_atual': value,
                        'valor_limite': self.alert_config['umidade_baixa'],
                        'sensor': reading['sensor_nome'],
                        'dispositivo': reading['dispositivo_nome']
                    })
            
            # Verificar luminosidade
            elif 'LDR' in sensor_type:
                if value > self.alert_config['luminosidade_alta']:
                    alerts.append({
                        'tipo': 'luminosidade_alta',
                        'severidade': 'media',
                        'valor_atual': value,
                        'valor_limite': self.alert_config['luminosidade_alta'],
                        'sensor': reading['sensor_nome'],
                        'dispositivo': reading['dispositivo_nome']
                    })
                elif value < self.alert_config['luminosidade_baixa']:
                    alerts.append({
                        'tipo': 'luminosidade_baixa',
                        'severidade': 'baixa',
                        'valor_atual': value,
                        'valor_limite': self.alert_config['luminosidade_baixa'],
                        'sensor': reading['sensor_nome'],
                        'dispositivo': reading['dispositivo_nome']
                    })
            
            # Verificar pressão
            elif 'Press' in sensor_type:
                if value > self.alert_config['pressao_alta']:
                    alerts.append({
                        'tipo': 'pressao_alta',
                        'severidade': 'alta',
                        'valor_atual': value,
                        'valor_limite': self.alert_config['pressao_alta'],
                        'sensor': reading['sensor_nome'],
                        'dispositivo': reading['dispositivo_nome']
                    })
                elif value < self.alert_config['pressao_baixa']:
                    alerts.append({
                        'tipo': 'pressao_baixa',
                        'severidade': 'alta',
                        'valor_atual': value,
                        'valor_limite': self.alert_config['pressao_baixa'],
                        'sensor': reading['sensor_nome'],
                        'dispositivo': reading['dispositivo_nome']
                    })
        
        return alerts
    
    def display_active_alerts(self):
        """Exibe alertas ativos"""
        st.markdown("## 🚨 Alertas Ativos")
        
        alerts_df = self.load_alerts('ativo')
        
        if alerts_df.empty:
            st.success("✅ Nenhum alerta ativo no momento")
            return
        
        # Estatísticas dos alertas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Alertas", len(alerts_df))
        
        with col2:
            critical_count = len(alerts_df[alerts_df['severidade'] == 'critica'])
            st.metric("Críticos", critical_count, delta=f"+{critical_count}" if critical_count > 0 else None)
        
        with col3:
            high_count = len(alerts_df[alerts_df['severidade'] == 'alta'])
            st.metric("Alta Prioridade", high_count)
        
        with col4:
            medium_count = len(alerts_df[alerts_df['severidade'] == 'media'])
            st.metric("Média Prioridade", medium_count)
        
        # Lista de alertas
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
                <p><strong>Tipo:</strong> {alert['tipo_alerta']}</p>
                <p><strong>Sensor:</strong> {alert['sensor_nome']}</p>
                <p><strong>Dispositivo:</strong> {alert['dispositivo_nome']}</p>
                <p><strong>Valor Atual:</strong> {alert['valor_atual']}</p>
                <p><strong>Limite:</strong> {alert['valor_limite']}</p>
                <p><strong>Descrição:</strong> {alert['descricao']}</p>
                <p><strong>Timestamp:</strong> {alert['timestamp_alerta']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    def display_alert_history(self):
        """Exibe histórico de alertas"""
        st.markdown("## 📊 Histórico de Alertas")
        
        days = st.sidebar.slider("Período (dias)", 1, 30, 7)
        history_df = self.load_alert_history(days)
        
        if history_df.empty:
            st.info("Nenhum alerta no período selecionado")
            return
        
        # Gráfico de alertas por dia
        history_df['date'] = pd.to_datetime(history_df['timestamp_alerta']).dt.date
        daily_alerts = history_df.groupby(['date', 'severidade']).size().reset_index(name='count')
        
        fig = px.bar(
            daily_alerts, 
            x='date', 
            y='count', 
            color='severidade',
            title=f'Alertas por Dia (Últimos {days} dias)',
            color_discrete_map={
                'critica': '#f44336',
                'alta': '#ff9800',
                'media': '#ffc107',
                'baixa': '#4caf50'
            }
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela de alertas
        st.markdown("### 📋 Lista de Alertas")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            severity_filter = st.selectbox("Filtrar por Severidade", 
                                         ["Todas", "critica", "alta", "media", "baixa"])
        
        with col2:
            tipo_filter = st.selectbox("Filtrar por Tipo", 
                                     ["Todos"] + list(history_df['tipo_alerta'].unique()))
        
        with col3:
            status_filter = st.selectbox("Filtrar por Status", 
                                       ["Todos"] + list(history_df['status'].unique()))
        
        # Aplicar filtros
        filtered_df = history_df.copy()
        
        if severity_filter != "Todas":
            filtered_df = filtered_df[filtered_df['severidade'] == severity_filter]
        
        if tipo_filter != "Todos":
            filtered_df = filtered_df[filtered_df['tipo_alerta'] == tipo_filter]
        
        if status_filter != "Todos":
            filtered_df = filtered_df[filtered_df['status'] == status_filter]
        
        # Exibir tabela
        st.dataframe(
            filtered_df[['timestamp_alerta', 'tipo_alerta', 'severidade', 'status', 
                        'sensor_nome', 'dispositivo_nome', 'valor_atual', 'valor_limite']],
            use_container_width=True
        )
    
    def display_alert_statistics(self):
        """Exibe estatísticas de alertas"""
        st.markdown("## 📈 Estatísticas de Alertas")
        
        history_df = self.load_alert_history(30)
        
        if history_df.empty:
            st.info("Nenhum dado de histórico disponível")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Alertas por tipo
            tipo_counts = history_df['tipo_alerta'].value_counts()
            fig = px.pie(
                values=tipo_counts.values,
                names=tipo_counts.index,
                title="Distribuição por Tipo de Alerta"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Alertas por severidade
            severity_counts = history_df['severidade'].value_counts()
            fig = px.bar(
                x=severity_counts.index,
                y=severity_counts.values,
                title="Alertas por Severidade",
                color=severity_counts.index,
                color_discrete_map={
                    'critica': '#f44336',
                    'alta': '#ff9800',
                    'media': '#ffc107',
                    'baixa': '#4caf50'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Métricas de performance
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_alerts = len(history_df)
            st.metric("Total de Alertas (30d)", total_alerts)
        
        with col2:
            resolved_alerts = len(history_df[history_df['status'] == 'resolvido'])
            resolution_rate = (resolved_alerts / total_alerts * 100) if total_alerts > 0 else 0
            st.metric("Taxa de Resolução", f"{resolution_rate:.1f}%")
        
        with col3:
            avg_resolution_time = self.calculate_avg_resolution_time(history_df)
            st.metric("Tempo Médio de Resolução", f"{avg_resolution_time:.1f}h")
        
        with col4:
            critical_alerts = len(history_df[history_df['severidade'] == 'critica'])
            critical_rate = (critical_alerts / total_alerts * 100) if total_alerts > 0 else 0
            st.metric("Taxa de Alertas Críticos", f"{critical_rate:.1f}%")
    
    def calculate_avg_resolution_time(self, df):
        """Calcula tempo médio de resolução"""
        resolved_df = df[df['status'] == 'resolvido'].copy()
        
        if resolved_df.empty:
            return 0
        
        resolved_df['timestamp_alerta'] = pd.to_datetime(resolved_df['timestamp_alerta'])
        resolved_df['resolved_at'] = pd.to_datetime(resolved_df['resolved_at'])
        
        resolved_df['resolution_time'] = (resolved_df['resolved_at'] - resolved_df['timestamp_alerta']).dt.total_seconds() / 3600
        
        return resolved_df['resolution_time'].mean()
    
    def display_alert_configuration(self):
        """Exibe configuração de alertas"""
        st.markdown("## ⚙️ Configuração de Alertas")
        
        st.markdown("### 📊 Thresholds Atuais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🌡️ Temperatura")
            temp_high = st.number_input("Temperatura Alta (°C)", value=self.alert_config['temperatura_alta'], min_value=0.0, max_value=100.0)
            temp_low = st.number_input("Temperatura Baixa (°C)", value=self.alert_config['temperatura_baixa'], min_value=-50.0, max_value=50.0)
            
            st.markdown("#### 💧 Umidade")
            hum_high = st.number_input("Umidade Alta (%)", value=self.alert_config['umidade_alta'], min_value=0.0, max_value=100.0)
            hum_low = st.number_input("Umidade Baixa (%)", value=self.alert_config['umidade_baixa'], min_value=0.0, max_value=100.0)
        
        with col2:
            st.markdown("#### 💡 Luminosidade")
            light_high = st.number_input("Luminosidade Alta (lux)", value=self.alert_config['luminosidade_alta'], min_value=0.0, max_value=10000.0)
            light_low = st.number_input("Luminosidade Baixa (lux)", value=self.alert_config['luminosidade_baixa'], min_value=0.0, max_value=1000.0)
            
            st.markdown("#### 🔽 Pressão")
            press_high = st.number_input("Pressão Alta (hPa)", value=self.alert_config['pressao_alta'], min_value=800.0, max_value=1200.0)
            press_low = st.number_input("Pressão Baixa (hPa)", value=self.alert_config['pressao_baixa'], min_value=800.0, max_value=1200.0)
        
        if st.button("💾 Salvar Configurações"):
            self.alert_config.update({
                'temperatura_alta': temp_high,
                'temperatura_baixa': temp_low,
                'umidade_alta': hum_high,
                'umidade_baixa': hum_low,
                'luminosidade_alta': light_high,
                'luminosidade_baixa': light_low,
                'pressao_alta': press_high,
                'pressao_baixa': press_low
            })
            st.success("✅ Configurações salvas com sucesso!")
    
    def run(self):
        """Executa o sistema de alertas"""
        # Conectar ao banco
        if not self.connect_database():
            return
        
        # CSS personalizado
        st.markdown("""
        <style>
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
        
        # Interface principal
        st.title("🚨 Sistema de Alertas - IoT Monitoring")
        st.markdown("Enterprise Challenge Sprint 3 - Reply")
        
        # Sidebar
        st.sidebar.markdown("## 🎛️ Controles")
        
        page = st.sidebar.selectbox(
            "Página",
            ["Alertas Ativos", "Histórico", "Estatísticas", "Configuração"]
        )
        
        # Auto-refresh
        auto_refresh = st.sidebar.checkbox("Atualização Automática", value=True)
        refresh_interval = st.sidebar.slider("Intervalo (segundos)", 5, 60, 10)
        
        if auto_refresh:
            time.sleep(refresh_interval)
            st.rerun()
        
        # Exibir página selecionada
        if page == "Alertas Ativos":
            self.display_active_alerts()
        elif page == "Histórico":
            self.display_alert_history()
        elif page == "Estatísticas":
            self.display_alert_statistics()
        elif page == "Configuração":
            self.display_alert_configuration()

def main():
    """Função principal"""
    sistema = SistemaAlertas()
    sistema.run()

if __name__ == "__main__":
    main()
