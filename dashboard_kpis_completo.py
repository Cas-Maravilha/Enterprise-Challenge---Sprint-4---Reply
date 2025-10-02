#!/usr/bin/env python3
"""
Dashboard Completo com KPIs e Alertas - Sistema IoT Monitoring Sprint 3
Sistema de dashboard em tempo real com KPIs, alertas e visualizações

Autor: Enterprise Challenge - Sprint 3 - Reply
Data: 2024
"""

import os
import sys
import json
import time
import logging
import threading
import queue
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, render_template, jsonify, request
import plotly.graph_objs as go
import plotly.utils
from plotly.offline import plot
import warnings
warnings.filterwarnings('ignore')

# Importar módulos do projeto
from persistencia_banco_relacional import (
    PersistenciaBancoRelacional, 
    ConfiguracaoBanco
)
from sistema_ml_completo import (
    SistemaMLCompleto,
    ConfiguracaoML
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("DashboardKPIs")

@dataclass
class ConfiguracaoDashboard:
    """Configuração do dashboard"""
    host: str = "0.0.0.0"
    port: int = 5000
    debug: bool = False
    update_interval: int = 30  # segundos
    max_alertas_exibidos: int = 50
    graficos_por_pagina: int = 6

class SistemaAlertas:
    """
    Sistema de alertas com thresholds e regras simples
    """
    
    def __init__(self, persistencia: PersistenciaBancoRelacional):
        self.persistencia = persistencia
        self.regras_alertas = self._carregar_regras_padrao()
        self.alertas_ativos = {}
        self.historico_alertas = []
    
    def _carregar_regras_padrao(self) -> Dict[str, Any]:
        """Carrega regras padrão de alertas"""
        return {
            'temperatura': {
                'minimo': 10.0,
                'maximo': 35.0,
                'critico_min': 5.0,
                'critico_max': 40.0,
                'severidade_baixa': 'media',
                'severidade_critica': 'critica'
            },
            'umidade': {
                'minimo': 30.0,
                'maximo': 80.0,
                'critico_min': 20.0,
                'critico_max': 90.0,
                'severidade_baixa': 'media',
                'severidade_critica': 'critica'
            },
            'pressao': {
                'minimo': 0.98,
                'maximo': 1.05,
                'critico_min': 0.95,
                'critico_max': 1.08,
                'severidade_baixa': 'media',
                'severidade_critica': 'critica'
            },
            'vibracao': {
                'maximo': 0.5,
                'critico_max': 1.0,
                'severidade_baixa': 'media',
                'severidade_critica': 'critica'
            },
            'nivel': {
                'minimo': 20.0,
                'maximo': 180.0,
                'critico_min': 10.0,
                'critico_max': 190.0,
                'severidade_baixa': 'media',
                'severidade_critica': 'critica'
            },
            'luminosidade': {
                'minimo': 100.0,
                'maximo': 800.0,
                'critico_min': 50.0,
                'critico_max': 1000.0,
                'severidade_baixa': 'media',
                'severidade_critica': 'critica'
            }
        }
    
    def verificar_alertas(self, dados_sensor: Dict[str, Any], sensor_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Verifica alertas baseados em thresholds"""
        alertas = []
        
        try:
            valor = float(dados_sensor.get('valor', 0))
            tipo_sensor = self._determinar_tipo_sensor(sensor_info['nome'])
            
            if tipo_sensor not in self.regras_alertas:
                return alertas
            
            regras = self.regras_alertas[tipo_sensor]
            
            # Verifica limites mínimos
            if 'minimo' in regras and valor < regras['minimo']:
                severidade = 'baixa'
                if 'critico_min' in regras and valor < regras['critico_min']:
                    severidade = 'critica'
                
                alerta = self._criar_alerta(
                    sensor_info, dados_sensor, tipo_sensor, 
                    'minimo', valor, regras['minimo'], severidade
                )
                alertas.append(alerta)
            
            # Verifica limites máximos
            if 'maximo' in regras and valor > regras['maximo']:
                severidade = 'baixa'
                if 'critico_max' in regras and valor > regras['critico_max']:
                    severidade = 'critica'
                
                alerta = self._criar_alerta(
                    sensor_info, dados_sensor, tipo_sensor,
                    'maximo', valor, regras['maximo'], severidade
                )
                alertas.append(alerta)
            
            return alertas
            
        except Exception as e:
            logger.error(f"Erro ao verificar alertas: {e}")
            return []
    
    def _determinar_tipo_sensor(self, nome_sensor: str) -> str:
        """Determina tipo do sensor baseado no nome"""
        nome_lower = nome_sensor.lower()
        
        if 'temperatura' in nome_lower or 'temperature' in nome_lower:
            return 'temperatura'
        elif 'umidade' in nome_lower or 'humidity' in nome_lower:
            return 'umidade'
        elif 'pressao' in nome_lower or 'pressure' in nome_lower:
            return 'pressao'
        elif 'vibracao' in nome_lower or 'vibration' in nome_lower:
            return 'vibracao'
        elif 'nivel' in nome_lower or 'level' in nome_lower:
            return 'nivel'
        elif 'luminosidade' in nome_lower or 'luminosity' in nome_lower:
            return 'luminosidade'
        else:
            return 'geral'
    
    def _criar_alerta(self, sensor_info: Dict[str, Any], dados_sensor: Dict[str, Any],
                     tipo_sensor: str, tipo_limite: str, valor_atual: float,
                     valor_limite: float, severidade: str) -> Dict[str, Any]:
        """Cria estrutura de alerta"""
        return {
            'id_dispositivo': sensor_info['id_dispositivo'],
            'id_sensor': sensor_info['id_sensor'],
            'id_modo': 2 if severidade == 'critica' else 1,
            'tipo_alerta': tipo_sensor,
            'severidade': severidade,
            'titulo': f'Limite {tipo_limite} excedido: {sensor_info["nome"]}',
            'descricao': f'Valor atual: {valor_atual:.2f} | Limite: {valor_limite:.2f}',
            'valor_atual': valor_atual,
            'valor_limite': valor_limite,
            'timestamp': datetime.now().isoformat()
        }

class CalculadoraKPIs:
    """
    Calculadora de KPIs do sistema
    """
    
    def __init__(self, persistencia: PersistenciaBancoRelacional):
        self.persistencia = persistencia
    
    def calcular_kpis_sistema(self) -> Dict[str, Any]:
        """Calcula KPIs principais do sistema"""
        try:
            # KPIs básicos do banco
            kpis_banco = self.persistencia.obter_kpis_sistema()
            
            # KPIs adicionais
            kpis_adicionais = self._calcular_kpis_adicionais()
            
            # Combina KPIs
            kpis_completos = {
                **kpis_banco,
                **kpis_adicionais,
                'timestamp': datetime.now().isoformat()
            }
            
            return kpis_completos
            
        except Exception as e:
            logger.error(f"Erro ao calcular KPIs: {e}")
            return {}
    
    def _calcular_kpis_adicionais(self) -> Dict[str, Any]:
        """Calcula KPIs adicionais"""
        try:
            with self.persistencia.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                # Taxa de disponibilidade dos dispositivos
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total,
                        SUM(CASE WHEN ultima_conexao > DATE_SUB(NOW(), INTERVAL 5 MINUTE) THEN 1 ELSE 0 END) as online
                    FROM dispositivos 
                    WHERE status = 'ativo'
                """)
                resultado = cursor.fetchone()
                disponibilidade = (resultado[1] / resultado[0] * 100) if resultado[0] > 0 else 0
                
                # Qualidade média dos dados
                cursor.execute("""
                    SELECT 
                        AVG(CASE 
                            WHEN qualidade_dados = 'excelente' THEN 4
                            WHEN qualidade_dados = 'bom' THEN 3
                            WHEN qualidade_dados = 'regular' THEN 2
                            WHEN qualidade_dados = 'ruim' THEN 1
                            ELSE 0
                        END) as qualidade_media
                    FROM leituras_sensores 
                    WHERE timestamp_datetime > DATE_SUB(NOW(), INTERVAL 1 HOUR)
                """)
                resultado = cursor.fetchone()
                qualidade_media = resultado[0] if resultado[0] else 0
                
                # Taxa de anomalias
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total,
                        SUM(CASE WHEN anomalia_detectada = 1 THEN 1 ELSE 0 END) as anomalias
                    FROM leituras_sensores 
                    WHERE timestamp_datetime > DATE_SUB(NOW(), INTERVAL 1 HOUR)
                """)
                resultado = cursor.fetchone()
                taxa_anomalias = (resultado[1] / resultado[0] * 100) if resultado[0] > 0 else 0
                
                # Alertas por severidade
                cursor.execute("""
                    SELECT 
                        severidade,
                        COUNT(*) as total
                    FROM alertas 
                    WHERE status = 'ativo' 
                    AND timestamp_alerta > DATE_SUB(NOW(), INTERVAL 24 HOUR)
                    GROUP BY severidade
                """)
                alertas_por_severidade = dict(cursor.fetchall())
                
                cursor.close()
                
                return {
                    'disponibilidade_dispositivos': round(disponibilidade, 2),
                    'qualidade_dados_media': round(qualidade_media, 2),
                    'taxa_anomalias_1h': round(taxa_anomalias, 2),
                    'alertas_baixa': alertas_por_severidade.get('baixa', 0),
                    'alertas_media': alertas_por_severidade.get('media', 0),
                    'alertas_alta': alertas_por_severidade.get('alta', 0),
                    'alertas_critica': alertas_por_severidade.get('critica', 0)
                }
                
        except Exception as e:
            logger.error(f"Erro ao calcular KPIs adicionais: {e}")
            return {}

class GeradorGraficos:
    """
    Gerador de gráficos para o dashboard
    """
    
    def __init__(self, persistencia: PersistenciaBancoRelacional):
        self.persistencia = persistencia
    
    def gerar_grafico_tendencia_sensores(self, horas: int = 24) -> str:
        """Gera gráfico de tendência dos sensores"""
        try:
            with self.persistencia.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                query = """
                SELECT 
                    ls.timestamp_datetime,
                    ts.nome as tipo_sensor,
                    AVG(ls.valor_numerico) as valor_medio
                FROM leituras_sensores ls
                JOIN sensores s ON ls.id_sensor = s.id_sensor
                JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
                WHERE ls.timestamp_datetime > DATE_SUB(NOW(), INTERVAL %s HOUR)
                AND ls.valor_numerico IS NOT NULL
                GROUP BY ls.timestamp_datetime, ts.nome
                ORDER BY ls.timestamp_datetime
                """
                
                cursor.execute(query, (horas,))
                dados = cursor.fetchall()
                cursor.close()
                
                if not dados:
                    return self._grafico_vazio("Nenhum dado disponível")
                
                # Converte para DataFrame
                df = pd.DataFrame(dados, columns=['timestamp', 'tipo_sensor', 'valor_medio'])
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                # Cria gráfico
                fig = go.Figure()
                
                for tipo in df['tipo_sensor'].unique():
                    dados_tipo = df[df['tipo_sensor'] == tipo]
                    fig.add_trace(go.Scatter(
                        x=dados_tipo['timestamp'],
                        y=dados_tipo['valor_medio'],
                        mode='lines+markers',
                        name=tipo,
                        line=dict(width=2)
                    ))
                
                fig.update_layout(
                    title=f'Tendência dos Sensores - Últimas {horas}h',
                    xaxis_title='Tempo',
                    yaxis_title='Valor Médio',
                    hovermode='x unified',
                    template='plotly_white'
                )
                
                return plot(fig, output_type='div', include_plotlyjs=False)
                
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de tendência: {e}")
            return self._grafico_vazio("Erro ao gerar gráfico")
    
    def gerar_grafico_distribuicao_alertas(self) -> str:
        """Gera gráfico de distribuição de alertas"""
        try:
            with self.persistencia.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                query = """
                SELECT 
                    severidade,
                    COUNT(*) as total
                FROM alertas 
                WHERE timestamp_alerta > DATE_SUB(NOW(), INTERVAL 24 HOUR)
                GROUP BY severidade
                ORDER BY 
                    CASE severidade 
                        WHEN 'critica' THEN 4
                        WHEN 'alta' THEN 3
                        WHEN 'media' THEN 2
                        WHEN 'baixa' THEN 1
                    END
                """
                
                cursor.execute(query)
                dados = cursor.fetchall()
                cursor.close()
                
                if not dados:
                    return self._grafico_vazio("Nenhum alerta nos últimos 24h")
                
                severidades, totais = zip(*dados)
                cores = ['#dc3545', '#fd7e14', '#ffc107', '#28a745']
                
                fig = go.Figure(data=[go.Bar(
                    x=list(severidades),
                    y=list(totais),
                    marker_color=cores[:len(severidades)]
                )])
                
                fig.update_layout(
                    title='Distribuição de Alertas por Severidade - 24h',
                    xaxis_title='Severidade',
                    yaxis_title='Quantidade',
                    template='plotly_white'
                )
                
                return plot(fig, output_type='div', include_plotlyjs=False)
                
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de alertas: {e}")
            return self._grafico_vazio("Erro ao gerar gráfico")
    
    def gerar_grafico_qualidade_dados(self) -> str:
        """Gera gráfico de qualidade dos dados"""
        try:
            with self.persistencia.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                query = """
                SELECT 
                    DATE(timestamp_datetime) as data,
                    qualidade_dados,
                    COUNT(*) as total
                FROM leituras_sensores 
                WHERE timestamp_datetime > DATE_SUB(NOW(), INTERVAL 7 DAY)
                GROUP BY DATE(timestamp_datetime), qualidade_dados
                ORDER BY data
                """
                
                cursor.execute(query)
                dados = cursor.fetchall()
                cursor.close()
                
                if not dados:
                    return self._grafico_vazio("Nenhum dado disponível")
                
                # Converte para DataFrame
                df = pd.DataFrame(dados, columns=['data', 'qualidade', 'total'])
                df['data'] = pd.to_datetime(df['data'])
                
                # Cria gráfico de barras empilhadas
                fig = go.Figure()
                
                qualidades = ['excelente', 'bom', 'regular', 'ruim']
                cores = ['#28a745', '#20c997', '#ffc107', '#dc3545']
                
                for qualidade, cor in zip(qualidades, cores):
                    dados_qualidade = df[df['qualidade'] == qualidade]
                    if not dados_qualidade.empty:
                        fig.add_trace(go.Bar(
                            x=dados_qualidade['data'],
                            y=dados_qualidade['total'],
                            name=qualidade.title(),
                            marker_color=cor
                        ))
                
                fig.update_layout(
                    title='Qualidade dos Dados - Últimos 7 Dias',
                    xaxis_title='Data',
                    yaxis_title='Quantidade de Leituras',
                    barmode='stack',
                    template='plotly_white'
                )
                
                return plot(fig, output_type='div', include_plotlyjs=False)
                
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de qualidade: {e}")
            return self._grafico_vazio("Erro ao gerar gráfico")
    
    def _grafico_vazio(self, mensagem: str) -> str:
        """Gera gráfico vazio com mensagem"""
        fig = go.Figure()
        fig.add_annotation(
            text=mensagem,
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=False, showticklabels=False),
            plot_bgcolor='white'
        )
        return plot(fig, output_type='div', include_plotlyjs=False)

class DashboardKPIsCompleto:
    """
    Dashboard completo com KPIs e alertas
    """
    
    def __init__(self, config_banco: ConfiguracaoBanco, config_dashboard: ConfiguracaoDashboard):
        self.config_banco = config_banco
        self.config_dashboard = config_dashboard
        
        # Inicializa componentes
        self.persistencia = PersistenciaBancoRelacional(config_banco)
        self.sistema_alertas = SistemaAlertas(self.persistencia)
        self.calculadora_kpis = CalculadoraKPIs(self.persistencia)
        self.gerador_graficos = GeradorGraficos(self.persistencia)
        
        # Flask app
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'iot_monitoring_sprint3'
        
        # Estado do dashboard
        self.executando = False
        self.thread_atualizacao = None
        self.cache_dados = {}
        
        # Configura rotas
        self._configurar_rotas()
    
    def _configurar_rotas(self):
        """Configura rotas do Flask"""
        
        @self.app.route('/')
        def index():
            return render_template('dashboard.html', 
                                 titulo="Dashboard IoT Monitoring",
                                 kpis=self.cache_dados.get('kpis', {}),
                                 alertas=self.cache_dados.get('alertas', []),
                                 graficos=self.cache_dados.get('graficos', {}))
        
        @self.app.route('/api/kpis')
        def api_kpis():
            kpis = self.calculadora_kpis.calcular_kpis_sistema()
            return jsonify(kpis)
        
        @self.app.route('/api/alertas')
        def api_alertas():
            alertas = self.persistencia.obter_alertas_ativos()
            return jsonify(alertas)
        
        @self.app.route('/api/graficos/tendencia')
        def api_grafico_tendencia():
            horas = request.args.get('horas', 24, type=int)
            grafico = self.gerador_graficos.gerar_grafico_tendencia_sensores(horas)
            return jsonify({'grafico': grafico})
        
        @self.app.route('/api/graficos/alertas')
        def api_grafico_alertas():
            grafico = self.gerador_graficos.gerar_grafico_distribuicao_alertas()
            return jsonify({'grafico': grafico})
        
        @self.app.route('/api/graficos/qualidade')
        def api_grafico_qualidade():
            grafico = self.gerador_graficos.gerar_grafico_qualidade_dados()
            return jsonify({'grafico': grafico})
        
        @self.app.route('/api/status')
        def api_status():
            return jsonify({
                'status': 'online' if self.executando else 'offline',
                'timestamp': datetime.now().isoformat(),
                'ultima_atualizacao': self.cache_dados.get('ultima_atualizacao', 'Nunca')
            })
    
    def iniciar(self):
        """Inicia o dashboard"""
        try:
            logger.info("Iniciando dashboard de KPIs")
            
            # Inicia thread de atualização
            self.executando = True
            self.thread_atualizacao = threading.Thread(target=self._thread_atualizacao, daemon=True)
            self.thread_atualizacao.start()
            
            # Inicia Flask
            logger.info(f"Dashboard disponível em: http://{self.config_dashboard.host}:{self.config_dashboard.port}")
            self.app.run(
                host=self.config_dashboard.host,
                port=self.config_dashboard.port,
                debug=self.config_dashboard.debug,
                threaded=True
            )
            
        except Exception as e:
            logger.error(f"Erro ao iniciar dashboard: {e}")
            raise
    
    def parar(self):
        """Para o dashboard"""
        try:
            logger.info("Parando dashboard")
            self.executando = False
            
            if self.thread_atualizacao and self.thread_atualizacao.is_alive():
                self.thread_atualizacao.join(timeout=5)
            
            logger.info("Dashboard parado")
            
        except Exception as e:
            logger.error(f"Erro ao parar dashboard: {e}")
    
    def _thread_atualizacao(self):
        """Thread de atualização dos dados"""
        logger.info("Thread de atualização iniciada")
        
        while self.executando:
            try:
                # Atualiza KPIs
                kpis = self.calculadora_kpis.calcular_kpis_sistema()
                
                # Atualiza alertas
                alertas = self.persistencia.obter_alertas_ativos()
                
                # Atualiza gráficos
                graficos = {
                    'tendencia': self.gerador_graficos.gerar_grafico_tendencia_sensores(24),
                    'alertas': self.gerador_graficos.gerar_grafico_distribuicao_alertas(),
                    'qualidade': self.gerador_graficos.gerar_grafico_qualidade_dados()
                }
                
                # Atualiza cache
                self.cache_dados = {
                    'kpis': kpis,
                    'alertas': alertas[:self.config_dashboard.max_alertas_exibidos],
                    'graficos': graficos,
                    'ultima_atualizacao': datetime.now().isoformat()
                }
                
                logger.debug("Dados do dashboard atualizados")
                
                # Aguarda próximo ciclo
                time.sleep(self.config_dashboard.update_interval)
                
            except Exception as e:
                logger.error(f"Erro na atualização: {e}")
                time.sleep(10)
        
        logger.info("Thread de atualização finalizada")

# =====================================================
# TEMPLATE HTML DO DASHBOARD
# =====================================================

def criar_template_dashboard():
    """Cria template HTML do dashboard"""
    template_html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ titulo }}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .kpi-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .kpi-value {
            font-size: 2.5rem;
            font-weight: bold;
        }
        .kpi-label {
            font-size: 1rem;
            opacity: 0.9;
        }
        .alert-card {
            border-left: 4px solid #dc3545;
            margin-bottom: 10px;
        }
        .alert-critica { border-left-color: #dc3545; }
        .alert-alta { border-left-color: #fd7e14; }
        .alert-media { border-left-color: #ffc107; }
        .alert-baixa { border-left-color: #28a745; }
        .status-online { color: #28a745; }
        .status-offline { color: #dc3545; }
        .grafico-container {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body class="bg-light">
    <nav class="navbar navbar-dark bg-dark">
        <div class="container-fluid">
            <span class="navbar-brand mb-0 h1">
                <i class="fas fa-chart-line"></i> {{ titulo }}
            </span>
            <span class="navbar-text">
                <i class="fas fa-circle status-online" id="status-indicator"></i>
                <span id="status-text">Online</span>
            </span>
        </div>
    </nav>

    <div class="container-fluid mt-4">
        <!-- KPIs Principais -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="kpi-card">
                    <div class="kpi-value" id="total-dispositivos">{{ kpis.total_dispositivos or 0 }}</div>
                    <div class="kpi-label">Dispositivos Ativos</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="kpi-card">
                    <div class="kpi-value" id="leituras-24h">{{ kpis.leituras_24h or 0 }}</div>
                    <div class="kpi-label">Leituras (24h)</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="kpi-card">
                    <div class="kpi-value" id="alertas-ativos">{{ kpis.alertas_ativos or 0 }}</div>
                    <div class="kpi-label">Alertas Ativos</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="kpi-card">
                    <div class="kpi-value" id="disponibilidade">{{ kpis.disponibilidade_dispositivos or 0 }}%</div>
                    <div class="kpi-label">Disponibilidade</div>
                </div>
            </div>
        </div>

        <!-- Gráficos -->
        <div class="row mb-4">
            <div class="col-md-8">
                <div class="grafico-container">
                    <h5><i class="fas fa-chart-line"></i> Tendência dos Sensores</h5>
                    <div id="grafico-tendencia">{{ graficos.tendencia | safe }}</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="grafico-container">
                    <h5><i class="fas fa-exclamation-triangle"></i> Alertas por Severidade</h5>
                    <div id="grafico-alertas">{{ graficos.alertas | safe }}</div>
                </div>
            </div>
        </div>

        <div class="row mb-4">
            <div class="col-md-12">
                <div class="grafico-container">
                    <h5><i class="fas fa-chart-bar"></i> Qualidade dos Dados</h5>
                    <div id="grafico-qualidade">{{ graficos.qualidade | safe }}</div>
                </div>
            </div>
        </div>

        <!-- Alertas Recentes -->
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-bell"></i> Alertas Recentes</h5>
                    </div>
                    <div class="card-body">
                        <div id="alertas-container">
                            {% for alerta in alertas %}
                            <div class="alert alert-{{ alerta.severidade }} alert-dismissible fade show alert-card">
                                <strong>{{ alerta.titulo }}</strong><br>
                                <small>{{ alerta.descricao }}</small><br>
                                <small class="text-muted">{{ alerta.timestamp_alerta }}</small>
                            </div>
                            {% endfor %}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Atualização automática dos dados
        function atualizarDados() {
            fetch('/api/kpis')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('total-dispositivos').textContent = data.total_dispositivos || 0;
                    document.getElementById('leituras-24h').textContent = data.leituras_24h || 0;
                    document.getElementById('alertas-ativos').textContent = data.alertas_ativos || 0;
                    document.getElementById('disponibilidade').textContent = (data.disponibilidade_dispositivos || 0) + '%';
                })
                .catch(error => console.error('Erro ao atualizar KPIs:', error));
        }

        // Verifica status do sistema
        function verificarStatus() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    const indicator = document.getElementById('status-indicator');
                    const text = document.getElementById('status-text');
                    
                    if (data.status === 'online') {
                        indicator.className = 'fas fa-circle status-online';
                        text.textContent = 'Online';
                    } else {
                        indicator.className = 'fas fa-circle status-offline';
                        text.textContent = 'Offline';
                    }
                })
                .catch(error => {
                    const indicator = document.getElementById('status-indicator');
                    const text = document.getElementById('status-text');
                    indicator.className = 'fas fa-circle status-offline';
                    text.textContent = 'Erro';
                });
        }

        // Atualiza dados a cada 30 segundos
        setInterval(atualizarDados, 30000);
        setInterval(verificarStatus, 10000);

        // Atualização inicial
        atualizarDados();
        verificarStatus();
    </script>
</body>
</html>
    """
    
    # Cria diretório de templates se não existir
    os.makedirs('templates', exist_ok=True)
    
    # Salva template
    with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(template_html)
    
    logger.info("Template HTML do dashboard criado")

# =====================================================
# EXEMPLO DE USO
# =====================================================

def exemplo_uso():
    """Exemplo de uso do dashboard"""
    
    # Configurações
    config_banco = ConfiguracaoBanco(
        host="localhost",
        port=3306,
        database="iot_monitoring_db",
        username="root",
        password="password"
    )
    
    config_dashboard = ConfiguracaoDashboard(
        host="0.0.0.0",
        port=5000,
        debug=False,
        update_interval=30
    )
    
    # Cria template HTML
    criar_template_dashboard()
    
    # Inicializa dashboard
    dashboard = DashboardKPIsCompleto(config_banco, config_dashboard)
    
    try:
        # Inicia dashboard
        dashboard.iniciar()
        
    except KeyboardInterrupt:
        print("Parando dashboard...")
    finally:
        dashboard.parar()

if __name__ == "__main__":
    exemplo_uso()
