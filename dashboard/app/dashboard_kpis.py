#!/usr/bin/env python3
"""
Sistema IoT Monitoring - Dashboard de KPIs
Enterprise Challenge Sprint 3 - Reply

Dashboard especializado em KPIs e métricas de performance
do Sistema IoT Monitoring.
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
    page_title="KPIs - Sistema IoT Monitoring",
    page_icon="📊",
    layout="wide"
)

class KPIDashboard:
    """Dashboard especializado em KPIs"""
    
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'password',
            'database': 'iot_monitoring_db'
        }
        self.engine = None
        self.kpis = {}
        self.trends = {}
        
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
    
    def load_kpi_data(self, hours=24):
        """Carrega dados para cálculo de KPIs"""
        if not self.engine:
            return False
        
        try:
            # Carregar leituras do período
            query = """
            SELECT 
                l.timestamp_datetime,
                l.valor_numerico,
                l.valor_booleano,
                l.qualidade_dados,
                l.anomalia_detectada,
                s.nome as sensor_nome,
                ts.nome as tipo_sensor,
                ts.unidade_medida,
                d.nome as dispositivo_nome,
                d.localizacao
            FROM leituras_sensores l
            JOIN sensores s ON l.id_sensor = s.id_sensor
            JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
            JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
            WHERE l.timestamp_datetime >= DATE_SUB(NOW(), INTERVAL %s HOUR)
            ORDER BY l.timestamp_datetime
            """ % hours
            
            self.data = pd.read_sql(query, self.engine)
            return True
            
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")
            return False
    
    def calculate_sensor_kpis(self):
        """Calcula KPIs de sensores"""
        if self.data.empty:
            return
        
        df = self.data
        
        # Separar dados por tipo de sensor
        temp_data = df[df['tipo_sensor'].str.contains('Temp', na=False)]
        humidity_data = df[df['tipo_sensor'].str.contains('Hum', na=False)]
        light_data = df[df['tipo_sensor'].str.contains('LDR', na=False)]
        pressure_data = df[df['tipo_sensor'].str.contains('Press', na=False)]
        motion_data = df[df['tipo_sensor'].str.contains('PIR', na=False)]
        
        self.kpis['sensors'] = {
            'temperatura': {
                'media': temp_data['valor_numerico'].mean() if not temp_data.empty else 0,
                'min': temp_data['valor_numerico'].min() if not temp_data.empty else 0,
                'max': temp_data['valor_numerico'].max() if not temp_data.empty else 0,
                'std': temp_data['valor_numerico'].std() if not temp_data.empty else 0,
                'leituras': len(temp_data)
            },
            'umidade': {
                'media': humidity_data['valor_numerico'].mean() if not humidity_data.empty else 0,
                'min': humidity_data['valor_numerico'].min() if not humidity_data.empty else 0,
                'max': humidity_data['valor_numerico'].max() if not humidity_data.empty else 0,
                'std': humidity_data['valor_numerico'].std() if not humidity_data.empty else 0,
                'leituras': len(humidity_data)
            },
            'luminosidade': {
                'media': light_data['valor_numerico'].mean() if not light_data.empty else 0,
                'min': light_data['valor_numerico'].min() if not light_data.empty else 0,
                'max': light_data['valor_numerico'].max() if not light_data.empty else 0,
                'std': light_data['valor_numerico'].std() if not light_data.empty else 0,
                'leituras': len(light_data)
            },
            'pressao': {
                'media': pressure_data['valor_numerico'].mean() if not pressure_data.empty else 0,
                'min': pressure_data['valor_numerico'].min() if not pressure_data.empty else 0,
                'max': pressure_data['valor_numerico'].max() if not pressure_data.empty else 0,
                'std': pressure_data['valor_numerico'].std() if not pressure_data.empty else 0,
                'leituras': len(pressure_data)
            },
            'movimento': {
                'taxa': motion_data['valor_booleano'].mean() * 100 if not motion_data.empty else 0,
                'total_deteccoes': motion_data['valor_booleano'].sum() if not motion_data.empty else 0,
                'leituras': len(motion_data)
            }
        }
    
    def calculate_system_kpis(self):
        """Calcula KPIs do sistema"""
        if self.data.empty:
            return
        
        df = self.data
        
        # KPIs de sistema
        total_readings = len(df)
        unique_sensors = df['sensor_nome'].nunique()
        unique_devices = df['dispositivo_nome'].nunique()
        
        # Qualidade dos dados
        quality_counts = df['qualidade_dados'].value_counts()
        total_quality = quality_counts.sum()
        
        quality_percentages = {
            'excelente': (quality_counts.get('excelente', 0) / total_quality * 100) if total_quality > 0 else 0,
            'boa': (quality_counts.get('boa', 0) / total_quality * 100) if total_quality > 0 else 0,
            'regular': (quality_counts.get('regular', 0) / total_quality * 100) if total_quality > 0 else 0,
            'ruim': (quality_counts.get('ruim', 0) / total_quality * 100) if total_quality > 0 else 0
        }
        
        # Anomalias
        anomaly_rate = df['anomalia_detectada'].mean() * 100
        total_anomalies = df['anomalia_detectada'].sum()
        
        # Throughput
        time_span_hours = (df['timestamp_datetime'].max() - df['timestamp_datetime'].min()).total_seconds() / 3600
        throughput = total_readings / time_span_hours if time_span_hours > 0 else 0
        
        self.kpis['system'] = {
            'total_readings': total_readings,
            'unique_sensors': unique_sensors,
            'unique_devices': unique_devices,
            'quality_percentages': quality_percentages,
            'anomaly_rate': anomaly_rate,
            'total_anomalies': total_anomalies,
            'throughput': throughput,
            'time_span_hours': time_span_hours
        }
    
    def calculate_performance_kpis(self):
        """Calcula KPIs de performance"""
        if self.data.empty:
            return
        
        df = self.data
        
        # Latência (simulada)
        avg_latency = np.random.normal(45, 10)  # 45ms ± 10ms
        
        # Uptime (simulada)
        uptime = 99.8 + np.random.normal(0, 0.1)
        
        # Disponibilidade por sensor
        sensor_availability = {}
        for sensor in df['sensor_nome'].unique():
            sensor_data = df[df['sensor_nome'] == sensor]
            expected_readings = 24 * 60  # 1 leitura por minuto
            actual_readings = len(sensor_data)
            availability = min(100, (actual_readings / expected_readings) * 100)
            sensor_availability[sensor] = availability
        
        self.kpis['performance'] = {
            'avg_latency': avg_latency,
            'uptime': uptime,
            'sensor_availability': sensor_availability
        }
    
    def display_sensor_kpis(self):
        """Exibe KPIs de sensores"""
        st.markdown("## 🌡️ KPIs de Sensores")
        
        if 'sensors' not in self.kpis:
            st.warning("Nenhum dado de sensor disponível")
            return
        
        sensors_kpis = self.kpis['sensors']
        
        # Temperatura
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🌡️ Temperatura Média",
                f"{sensors_kpis['temperatura']['media']:.1f}°C",
                f"±{sensors_kpis['temperatura']['std']:.1f}°C"
            )
        
        with col2:
            st.metric(
                "💧 Umidade Média",
                f"{sensors_kpis['umidade']['media']:.1f}%",
                f"±{sensors_kpis['umidade']['std']:.1f}%"
            )
        
        with col3:
            st.metric(
                "💡 Luminosidade Média",
                f"{sensors_kpis['luminosidade']['media']:.0f} lux",
                f"±{sensors_kpis['luminosidade']['std']:.0f} lux"
            )
        
        with col4:
            st.metric(
                "🔽 Pressão Média",
                f"{sensors_kpis['pressao']['media']:.1f} hPa",
                f"±{sensors_kpis['pressao']['std']:.1f} hPa"
            )
        
        # Ranges
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🌡️ Range Temperatura",
                f"{sensors_kpis['temperatura']['min']:.1f}°C - {sensors_kpis['temperatura']['max']:.1f}°C"
            )
        
        with col2:
            st.metric(
                "💧 Range Umidade",
                f"{sensors_kpis['umidade']['min']:.1f}% - {sensors_kpis['umidade']['max']:.1f}%"
            )
        
        with col3:
            st.metric(
                "💡 Range Luminosidade",
                f"{sensors_kpis['luminosidade']['min']:.0f} - {sensors_kpis['luminosidade']['max']:.0f} lux"
            )
        
        with col4:
            st.metric(
                "🔽 Range Pressão",
                f"{sensors_kpis['pressao']['min']:.1f} - {sensors_kpis['pressao']['max']:.1f} hPa"
            )
    
    def display_system_kpis(self):
        """Exibe KPIs do sistema"""
        st.markdown("## ⚙️ KPIs do Sistema")
        
        if 'system' not in self.kpis:
            st.warning("Nenhum dado de sistema disponível")
            return
        
        system_kpis = self.kpis['system']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "📊 Total de Leituras",
                f"{system_kpis['total_readings']:,}",
                f"{system_kpis['throughput']:.1f}/h"
            )
        
        with col2:
            st.metric(
                "🔧 Sensores Ativos",
                f"{system_kpis['unique_sensors']}",
                f"{system_kpis['unique_devices']} dispositivos"
            )
        
        with col3:
            st.metric(
                "⚠️ Taxa de Anomalias",
                f"{system_kpis['anomaly_rate']:.1f}%",
                f"{system_kpis['total_anomalies']} anomalias"
            )
        
        with col4:
            st.metric(
                "⭐ Qualidade Excelente",
                f"{system_kpis['quality_percentages']['excelente']:.1f}%",
                f"Boa: {system_kpis['quality_percentages']['boa']:.1f}%"
            )
    
    def display_performance_kpis(self):
        """Exibe KPIs de performance"""
        st.markdown("## 🚀 KPIs de Performance")
        
        if 'performance' not in self.kpis:
            st.warning("Nenhum dado de performance disponível")
            return
        
        perf_kpis = self.kpis['performance']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "⚡ Latência Média",
                f"{perf_kpis['avg_latency']:.1f}ms",
                "±10ms"
            )
        
        with col2:
            st.metric(
                "🟢 Uptime",
                f"{perf_kpis['uptime']:.1f}%",
                "99.9%"
            )
        
        with col3:
            avg_availability = np.mean(list(perf_kpis['sensor_availability'].values()))
            st.metric(
                "📡 Disponibilidade Média",
                f"{avg_availability:.1f}%",
                f"{len(perf_kpis['sensor_availability'])} sensores"
            )
    
    def display_quality_chart(self):
        """Exibe gráfico de qualidade dos dados"""
        st.markdown("## 📊 Qualidade dos Dados")
        
        if 'system' not in self.kpis:
            return
        
        quality_data = self.kpis['system']['quality_percentages']
        
        fig = px.pie(
            values=list(quality_data.values()),
            names=list(quality_data.keys()),
            title="Distribuição da Qualidade dos Dados",
            color_discrete_map={
                'excelente': '#2E8B57',
                'boa': '#32CD32',
                'regular': '#FFD700',
                'ruim': '#FF6347'
            }
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    def display_availability_chart(self):
        """Exibe gráfico de disponibilidade por sensor"""
        st.markdown("## 📡 Disponibilidade por Sensor")
        
        if 'performance' not in self.kpis:
            return
        
        availability_data = self.kpis['performance']['sensor_availability']
        
        sensors = list(availability_data.keys())
        availabilities = list(availability_data.values())
        
        fig = px.bar(
            x=sensors,
            y=availabilities,
            title="Disponibilidade por Sensor",
            labels={'x': 'Sensor', 'y': 'Disponibilidade (%)'}
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            yaxis_range=[0, 100]
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def display_trends(self):
        """Exibe tendências temporais"""
        st.markdown("## 📈 Tendências Temporais")
        
        if self.data.empty:
            return
        
        # Agrupar por hora
        df_hourly = self.data.copy()
        df_hourly['hour'] = pd.to_datetime(df_hourly['timestamp_datetime']).dt.floor('H')
        
        # Calcular métricas por hora
        hourly_metrics = df_hourly.groupby('hour').agg({
            'valor_numerico': ['mean', 'std', 'count'],
            'anomalia_detectada': 'mean',
            'qualidade_dados': lambda x: (x == 'excelente').mean()
        }).reset_index()
        
        hourly_metrics.columns = ['hour', 'avg_value', 'std_value', 'count', 'anomaly_rate', 'quality_rate']
        
        # Gráfico de tendências
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Valor Médio', 'Taxa de Anomalias', 'Qualidade dos Dados', 'Número de Leituras'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Valor médio
        fig.add_trace(
            go.Scatter(x=hourly_metrics['hour'], y=hourly_metrics['avg_value'], 
                      name='Valor Médio', line=dict(color='blue')),
            row=1, col=1
        )
        
        # Taxa de anomalias
        fig.add_trace(
            go.Scatter(x=hourly_metrics['hour'], y=hourly_metrics['anomaly_rate'] * 100, 
                      name='Taxa de Anomalias (%)', line=dict(color='red')),
            row=1, col=2
        )
        
        # Qualidade dos dados
        fig.add_trace(
            go.Scatter(x=hourly_metrics['hour'], y=hourly_metrics['quality_rate'] * 100, 
                      name='Qualidade Excelente (%)', line=dict(color='green')),
            row=2, col=1
        )
        
        # Número de leituras
        fig.add_trace(
            go.Bar(x=hourly_metrics['hour'], y=hourly_metrics['count'], 
                   name='Leituras por Hora', marker_color='orange'),
            row=2, col=2
        )
        
        fig.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    def run(self):
        """Executa o dashboard de KPIs"""
        # Conectar ao banco
        if not self.connect_database():
            return
        
        # Carregar dados
        hours = st.sidebar.slider("Período (horas)", 1, 168, 24)
        if not self.load_kpi_data(hours):
            return
        
        # Calcular KPIs
        self.calculate_sensor_kpis()
        self.calculate_system_kpis()
        self.calculate_performance_kpis()
        
        # Exibir interface
        st.title("📊 Dashboard de KPIs - Sistema IoT Monitoring")
        st.markdown("Enterprise Challenge Sprint 3 - Reply")
        
        self.display_sensor_kpis()
        self.display_system_kpis()
        self.display_performance_kpis()
        
        col1, col2 = st.columns(2)
        with col1:
            self.display_quality_chart()
        with col2:
            self.display_availability_chart()
        
        self.display_trends()

def main():
    """Função principal"""
    dashboard = KPIDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
