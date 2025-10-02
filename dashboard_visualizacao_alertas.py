#!/usr/bin/env python3
"""
Dashboard de Visualização e Alertas - Sistema IoT Monitoring
Enterprise Challenge Sprint 3 - Reply

Este script implementa um dashboard interativo com Streamlit
exibindo KPIs do processo e sistema de alertas com thresholds.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import mysql.connector
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Any, Tuple
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="IoT Monitoring Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DashboardIoTMonitoring:
    """Dashboard de visualização e alertas IoT"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.df_leituras = None
        self.df_alertas = None
        self.kpis = {}
        self.alertas_ativos = []
        
        # Configurações de conexão
        self.host = 'localhost'
        self.user = 'root'
        self.password = ''
        self.database = 'iot_monitoring_db'
    
    def conectar_banco(self):
        """Conecta ao banco de dados"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4'
            )
            self.cursor = self.connection.cursor(dictionary=True)
            return True
        except mysql.connector.Error as e:
            st.error(f"Erro ao conectar ao banco: {e}")
            return False
    
    def executar_consulta(self, query: str, params: Tuple = None) -> pd.DataFrame:
        """Executa uma consulta SQL e retorna DataFrame"""
        try:
            self.cursor.execute(query, params)
            resultado = self.cursor.fetchall()
            return pd.DataFrame(resultado)
        except mysql.connector.Error as e:
            st.error(f"Erro na consulta: {e}")
            return pd.DataFrame()
    
    def carregar_dados_dashboard(self):
        """Carrega dados para o dashboard"""
        # Query para leituras recentes
        query_leituras = """
        SELECT 
            l.id_leitura,
            l.id_sensor,
            l.timestamp_datetime,
            l.valor_numerico,
            l.valor_booleano,
            l.qualidade_dados,
            l.anomalia_detectada,
            s.nome as sensor_nome,
            s.id_tipo_sensor,
            d.nome as dispositivo_nome,
            d.localizacao,
            ts.nome as tipo_sensor_nome,
            ts.unidade_medida
        FROM leituras_sensores l
        JOIN sensores s ON l.id_sensor = s.id_sensor
        JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
        JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
        WHERE l.timestamp_datetime >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
        ORDER BY l.timestamp_datetime DESC
        """
        
        self.df_leituras = self.executar_consulta(query_leituras)
        
        # Query para alertas
        query_alertas = """
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
            d.nome as dispositivo_nome,
            s.nome as sensor_nome
        FROM alertas a
        JOIN dispositivos d ON a.id_dispositivo = d.id_dispositivo
        LEFT JOIN sensores s ON a.id_sensor = s.id_sensor
        WHERE a.timestamp_alerta >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
        ORDER BY a.timestamp_alerta DESC
        """
        
        self.df_alertas = self.executar_consulta(query_alertas)
        
        return not self.df_leituras.empty
    
    def calcular_kpis(self):
        """Calcula KPIs do processo"""
        if self.df_leituras.empty:
            return
        
        # Converter timestamp
        self.df_leituras['timestamp_datetime'] = pd.to_datetime(self.df_leituras['timestamp_datetime'])
        
        # KPIs gerais
        self.kpis = {
            'total_leituras': len(self.df_leituras),
            'sensores_ativos': self.df_leituras['id_sensor'].nunique(),
            'dispositivos_ativos': self.df_leituras['dispositivo_nome'].nunique(),
            'anomalias_detectadas': self.df_leituras['anomalia_detectada'].sum(),
            'taxa_anomalias': (self.df_leituras['anomalia_detectada'].sum() / len(self.df_leituras)) * 100,
            'alertas_ativos': len(self.df_alertas[self.df_alertas['status'] == 'ativo']) if not self.df_alertas.empty else 0
        }
        
        # KPIs por tipo de sensor
        if not self.df_leituras.empty:
            df_numerico = self.df_leituras[self.df_leituras['valor_numerico'].notna()]
            if not df_numerico.empty:
                self.kpis['media_geral'] = df_numerico['valor_numerico'].mean()
                self.kpis['desvio_padrao_geral'] = df_numerico['valor_numerico'].std()
                self.kpis['minimo_geral'] = df_numerico['valor_numerico'].min()
                self.kpis['maximo_geral'] = df_numerico['valor_numerico'].max()
    
    def verificar_alertas_threshold(self):
        """Verifica alertas baseados em thresholds simples"""
        if self.df_leituras.empty:
            return
        
        # Thresholds configuráveis
        thresholds = {
            'temperatura': {'max': 30.0, 'min': 15.0},
            'umidade': {'max': 80.0, 'min': 30.0},
            'luminosidade': {'max': 800.0, 'min': 50.0},
            'pressao': {'max': 1050.0, 'min': 950.0}
        }
        
        self.alertas_ativos = []
        
        for _, row in self.df_leituras.iterrows():
            if pd.isna(row['valor_numerico']):
                continue
            
            sensor_tipo = row['tipo_sensor_nome'].lower()
            valor = row['valor_numerico']
            dispositivo = row['dispositivo_nome']
            sensor_nome = row['sensor_nome']
            timestamp = row['timestamp_datetime']
            
            # Verificar thresholds
            if sensor_tipo in thresholds:
                threshold = thresholds[sensor_tipo]
                
                if valor > threshold['max']:
                    self.alertas_ativos.append({
                        'tipo': 'ALERTA ALTO',
                        'sensor': sensor_nome,
                        'dispositivo': dispositivo,
                        'valor': valor,
                        'limite': threshold['max'],
                        'timestamp': timestamp,
                        'severidade': 'ALTA' if valor > threshold['max'] * 1.2 else 'MÉDIA'
                    })
                
                elif valor < threshold['min']:
                    self.alertas_ativos.append({
                        'tipo': 'ALERTA BAIXO',
                        'sensor': sensor_nome,
                        'dispositivo': dispositivo,
                        'valor': valor,
                        'limite': threshold['min'],
                        'timestamp': timestamp,
                        'severidade': 'ALTA' if valor < threshold['min'] * 0.8 else 'MÉDIA'
                    })
    
    def renderizar_sidebar(self):
        """Renderiza sidebar com controles"""
        st.sidebar.title("🎛️ Controles")
        
        # Filtros de tempo
        st.sidebar.subheader("⏰ Período")
        periodo = st.sidebar.selectbox(
            "Selecione o período",
            ["Última hora", "Últimas 6 horas", "Últimas 24 horas", "Últimos 7 dias"]
        )
        
        # Filtros de dispositivo
        if not self.df_leituras.empty:
            dispositivos = ['Todos'] + list(self.df_leituras['dispositivo_nome'].unique())
            dispositivo_selecionado = st.sidebar.selectbox("🏠 Dispositivo", dispositivos)
        else:
            dispositivo_selecionado = 'Todos'
        
        # Filtros de tipo de sensor
        if not self.df_leituras.empty:
            tipos_sensor = ['Todos'] + list(self.df_leituras['tipo_sensor_nome'].unique())
            tipo_selecionado = st.sidebar.selectbox("📡 Tipo de Sensor", tipos_sensor)
        else:
            tipo_selecionado = 'Todos'
        
        # Configurações de alertas
        st.sidebar.subheader("🚨 Configurações de Alertas")
        temp_max = st.sidebar.slider("Temperatura Máxima (°C)", 20.0, 40.0, 30.0)
        umid_max = st.sidebar.slider("Umidade Máxima (%)", 60.0, 100.0, 80.0)
        luz_max = st.sidebar.slider("Luminosidade Máxima (lux)", 500.0, 1000.0, 800.0)
        
        return {
            'periodo': periodo,
            'dispositivo': dispositivo_selecionado,
            'tipo_sensor': tipo_selecionado,
            'temp_max': temp_max,
            'umid_max': umid_max,
            'luz_max': luz_max
        }
    
    def renderizar_kpis(self):
        """Renderiza KPIs principais"""
        st.subheader("📊 KPIs Principais")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                label="📡 Total de Leituras",
                value=f"{self.kpis.get('total_leituras', 0):,}",
                delta=None
            )
        
        with col2:
            st.metric(
                label="🏠 Dispositivos Ativos",
                value=self.kpis.get('dispositivos_ativos', 0),
                delta=None
            )
        
        with col3:
            st.metric(
                label="⚠️ Anomalias Detectadas",
                value=self.kpis.get('anomalias_detectadas', 0),
                delta=f"{self.kpis.get('taxa_anomalias', 0):.1f}%"
            )
        
        with col4:
            st.metric(
                label="🚨 Alertas Ativos",
                value=self.kpis.get('alertas_ativos', 0),
                delta=None
            )
        
        with col5:
            if 'media_geral' in self.kpis:
                st.metric(
                    label="📈 Média Geral",
                    value=f"{self.kpis['media_geral']:.2f}",
                    delta=None
                )
    
    def renderizar_alertas(self):
        """Renderiza seção de alertas"""
        st.subheader("🚨 Alertas Ativos")
        
        if not self.alertas_ativos:
            st.success("✅ Nenhum alerta ativo no momento")
            return
        
        # Agrupar alertas por severidade
        alertas_alta = [a for a in self.alertas_ativos if a['severidade'] == 'ALTA']
        alertas_media = [a for a in self.alertas_ativos if a['severidade'] == 'MÉDIA']
        
        # Alertas de alta severidade
        if alertas_alta:
            st.error("🔴 **ALERTAS DE ALTA SEVERIDADE**")
            for alerta in alertas_alta:
                st.error(f"""
                **{alerta['tipo']}** - {alerta['dispositivo']} - {alerta['sensor']}
                - Valor: {alerta['valor']:.2f} | Limite: {alerta['limite']:.2f}
                - Timestamp: {alerta['timestamp'].strftime('%H:%M:%S')}
                """)
        
        # Alertas de média severidade
        if alertas_media:
            st.warning("🟡 **ALERTAS DE MÉDIA SEVERIDADE**")
            for alerta in alertas_media:
                st.warning(f"""
                **{alerta['tipo']}** - {alerta['dispositivo']} - {alerta['sensor']}
                - Valor: {alerta['valor']:.2f} | Limite: {alerta['limite']:.2f}
                - Timestamp: {alerta['timestamp'].strftime('%H:%M:%S')}
                """)
    
    def renderizar_graficos_tempo_real(self):
        """Renderiza gráficos de tempo real"""
        st.subheader("📈 Gráficos de Tempo Real")
        
        if self.df_leituras.empty:
            st.warning("Nenhum dado disponível para visualização")
            return
        
        # Filtrar dados por tipo de sensor
        tipos_graficos = ['DHT22', 'LDR', 'Pressão']
        
        for tipo in tipos_graficos:
            df_tipo = self.df_leituras[
                (self.df_leituras['tipo_sensor_nome'] == tipo) &
                (self.df_leituras['valor_numerico'].notna())
            ]
            
            if df_tipo.empty:
                continue
            
            # Criar gráfico de linha
            fig = px.line(
                df_tipo,
                x='timestamp_datetime',
                y='valor_numerico',
                color='dispositivo_nome',
                title=f'{tipo} - Valores ao Longo do Tempo',
                labels={'valor_numerico': f'{tipo} ({df_tipo["unidade_medida"].iloc[0] if not df_tipo.empty else ""})'}
            )
            
            fig.update_layout(
                xaxis_title="Tempo",
                yaxis_title=f"{tipo} ({df_tipo['unidade_medida'].iloc[0] if not df_tipo.empty else ''})",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def renderizar_graficos_distribuicao(self):
        """Renderiza gráficos de distribuição"""
        st.subheader("📊 Distribuição dos Dados")
        
        if self.df_leituras.empty:
            st.warning("Nenhum dado disponível para visualização")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de barras - Leituras por dispositivo
            disp_counts = self.df_leituras['dispositivo_nome'].value_counts()
            fig1 = px.bar(
                x=disp_counts.index,
                y=disp_counts.values,
                title="Leituras por Dispositivo",
                labels={'x': 'Dispositivo', 'y': 'Número de Leituras'}
            )
            fig1.update_xaxis(tickangle=45)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Gráfico de pizza - Distribuição de qualidade
            qualidade_counts = self.df_leituras['qualidade_dados'].value_counts()
            fig2 = px.pie(
                values=qualidade_counts.values,
                names=qualidade_counts.index,
                title="Distribuição de Qualidade dos Dados"
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    def renderizar_metricas_detalhadas(self):
        """Renderiza métricas detalhadas por sensor"""
        st.subheader("📋 Métricas Detalhadas por Sensor")
        
        if self.df_leituras.empty:
            st.warning("Nenhum dado disponível")
            return
        
        # Calcular métricas por sensor
        df_numerico = self.df_leituras[self.df_leituras['valor_numerico'].notna()]
        
        if df_numerico.empty:
            st.warning("Nenhum valor numérico disponível")
            return
        
        metricas_por_sensor = df_numerico.groupby(['dispositivo_nome', 'sensor_nome', 'tipo_sensor_nome']).agg({
            'valor_numerico': ['count', 'mean', 'std', 'min', 'max'],
            'anomalia_detectada': 'sum'
        }).round(2)
        
        # Flatten column names
        metricas_por_sensor.columns = ['_'.join(col).strip() for col in metricas_por_sensor.columns]
        metricas_por_sensor = metricas_por_sensor.reset_index()
        
        # Renomear colunas para exibição
        metricas_por_sensor.columns = [
            'Dispositivo', 'Sensor', 'Tipo', 'Leituras', 'Média', 
            'Desvio Padrão', 'Mínimo', 'Máximo', 'Anomalias'
        ]
        
        st.dataframe(metricas_por_sensor, use_container_width=True)
    
    def renderizar_dashboard(self):
        """Renderiza o dashboard completo"""
        # Título principal
        st.title("📊 Dashboard IoT Monitoring")
        st.markdown("**Enterprise Challenge Sprint 3 - Reply**")
        
        # Conectar ao banco
        if not self.conectar_banco():
            st.error("❌ Não foi possível conectar ao banco de dados")
            return
        
        # Carregar dados
        if not self.carregar_dados_dashboard():
            st.error("❌ Não foi possível carregar dados do banco")
            return
        
        # Calcular KPIs
        self.calcular_kpis()
        
        # Verificar alertas
        self.verificar_alertas_threshold()
        
        # Renderizar controles
        controles = self.renderizar_sidebar()
        
        # Renderizar seções
        self.renderizar_kpis()
        st.divider()
        
        self.renderizar_alertas()
        st.divider()
        
        self.renderizar_graficos_tempo_real()
        st.divider()
        
        self.renderizar_graficos_distribuicao()
        st.divider()
        
        self.renderizar_metricas_detalhadas()
        
        # Footer
        st.divider()
        st.markdown("---")
        st.markdown("**Dashboard IoT Monitoring** - Atualizado em: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))


def main():
    """Função principal"""
    dashboard = DashboardIoTMonitoring()
    dashboard.renderizar_dashboard()


if __name__ == "__main__":
    main()
