#!/usr/bin/env python3
"""
Sistema de Relatórios Automáticos - Sistema IoT Monitoring Sprint 3
Gera relatórios automáticos com KPIs, alertas e análises

Autor: Enterprise Challenge - Sprint 3 - Reply
Data: 2024
"""

import os
import sys
import json
import time
import logging
import threading
import schedule
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from jinja2 import Template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import warnings
warnings.filterwarnings('ignore')

# Importar módulos do projeto
from persistencia_banco_relacional import (
    PersistenciaBancoRelacional, 
    ConfiguracaoBanco
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("RelatoriosAutomaticos")

@dataclass
class ConfiguracaoRelatorios:
    """Configuração do sistema de relatórios"""
    diretorio_relatorios: str = "relatorios/"
    formato_relatorio: str = "html"  # html, pdf, excel
    enviar_email: bool = False
    email_smtp: str = "smtp.gmail.com"
    email_port: int = 587
    email_user: str = ""
    email_password: str = ""
    email_destinatarios: List[str] = None
    frequencia_diario: str = "08:00"
    frequencia_semanal: str = "monday 09:00"
    frequencia_mensal: str = "1 10:00"
    
    def __post_init__(self):
        if self.email_destinatarios is None:
            self.email_destinatarios = []

class GeradorRelatorios:
    """
    Gerador de relatórios automáticos
    """
    
    def __init__(self, persistencia: PersistenciaBancoRelacional, config: ConfiguracaoRelatorios):
        self.persistencia = persistencia
        self.config = config
        
        # Cria diretório de relatórios
        os.makedirs(self.config.diretorio_relatorios, exist_ok=True)
        
        # Configura matplotlib
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def gerar_relatorio_diario(self) -> str:
        """Gera relatório diário"""
        try:
            logger.info("Gerando relatório diário")
            
            # Dados do dia anterior
            data_inicio = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
            data_fim = data_inicio + timedelta(days=1)
            
            # Coleta dados
            dados = self._coletar_dados_periodo(data_inicio, data_fim)
            
            # Gera gráficos
            graficos = self._gerar_graficos_diario(dados)
            
            # Cria relatório HTML
            relatorio_html = self._criar_template_relatorio_diario(dados, graficos)
            
            # Salva arquivo
            nome_arquivo = f"relatorio_diario_{data_inicio.strftime('%Y%m%d')}.html"
            caminho_arquivo = os.path.join(self.config.diretorio_relatorios, nome_arquivo)
            
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                f.write(relatorio_html)
            
            logger.info(f"Relatório diário salvo: {caminho_arquivo}")
            return caminho_arquivo
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório diário: {e}")
            return None
    
    def gerar_relatorio_semanal(self) -> str:
        """Gera relatório semanal"""
        try:
            logger.info("Gerando relatório semanal")
            
            # Dados da semana anterior
            hoje = datetime.now()
            inicio_semana = hoje - timedelta(days=hoje.weekday() + 7)
            fim_semana = inicio_semana + timedelta(days=7)
            
            # Coleta dados
            dados = self._coletar_dados_periodo(inicio_semana, fim_semana)
            
            # Gera gráficos
            graficos = self._gerar_graficos_semanal(dados)
            
            # Cria relatório HTML
            relatorio_html = self._criar_template_relatorio_semanal(dados, graficos)
            
            # Salva arquivo
            nome_arquivo = f"relatorio_semanal_{inicio_semana.strftime('%Y%m%d')}.html"
            caminho_arquivo = os.path.join(self.config.diretorio_relatorios, nome_arquivo)
            
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                f.write(relatorio_html)
            
            logger.info(f"Relatório semanal salvo: {caminho_arquivo}")
            return caminho_arquivo
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório semanal: {e}")
            return None
    
    def gerar_relatorio_mensal(self) -> str:
        """Gera relatório mensal"""
        try:
            logger.info("Gerando relatório mensal")
            
            # Dados do mês anterior
            hoje = datetime.now()
            inicio_mes = hoje.replace(day=1) - timedelta(days=1)
            inicio_mes = inicio_mes.replace(day=1)
            fim_mes = hoje.replace(day=1)
            
            # Coleta dados
            dados = self._coletar_dados_periodo(inicio_mes, fim_mes)
            
            # Gera gráficos
            graficos = self._gerar_graficos_mensal(dados)
            
            # Cria relatório HTML
            relatorio_html = self._criar_template_relatorio_mensal(dados, graficos)
            
            # Salva arquivo
            nome_arquivo = f"relatorio_mensal_{inicio_mes.strftime('%Y%m')}.html"
            caminho_arquivo = os.path.join(self.config.diretorio_relatorios, nome_arquivo)
            
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                f.write(relatorio_html)
            
            logger.info(f"Relatório mensal salvo: {caminho_arquivo}")
            return caminho_arquivo
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório mensal: {e}")
            return None
    
    def _coletar_dados_periodo(self, data_inicio: datetime, data_fim: datetime) -> Dict[str, Any]:
        """Coleta dados do período especificado"""
        try:
            with self.persistencia.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                # KPIs básicos
                cursor.execute("""
                    SELECT 
                        COUNT(DISTINCT d.id_dispositivo) as total_dispositivos,
                        COUNT(DISTINCT s.id_sensor) as total_sensores,
                        COUNT(ls.id_leitura) as total_leituras,
                        SUM(CASE WHEN ls.anomalia_detectada = 1 THEN 1 ELSE 0 END) as total_anomalias,
                        SUM(CASE WHEN a.status = 'ativo' THEN 1 ELSE 0 END) as total_alertas
                    FROM dispositivos d
                    LEFT JOIN sensores s ON d.id_dispositivo = s.id_dispositivo
                    LEFT JOIN leituras_sensores ls ON s.id_sensor = ls.id_sensor 
                        AND ls.timestamp_datetime BETWEEN %s AND %s
                    LEFT JOIN alertas a ON d.id_dispositivo = a.id_dispositivo 
                        AND a.timestamp_alerta BETWEEN %s AND %s
                    WHERE d.status = 'ativo'
                """, (data_inicio, data_fim, data_inicio, data_fim))
                
                kpis = dict(zip([desc[0] for desc in cursor.description], cursor.fetchone()))
                
                # Leituras por sensor
                cursor.execute("""
                    SELECT 
                        ts.nome as tipo_sensor,
                        COUNT(ls.id_leitura) as total_leituras,
                        AVG(ls.valor_numerico) as valor_medio,
                        MIN(ls.valor_numerico) as valor_minimo,
                        MAX(ls.valor_numerico) as valor_maximo,
                        STDDEV(ls.valor_numerico) as desvio_padrao
                    FROM leituras_sensores ls
                    JOIN sensores s ON ls.id_sensor = s.id_sensor
                    JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
                    WHERE ls.timestamp_datetime BETWEEN %s AND %s
                    AND ls.valor_numerico IS NOT NULL
                    GROUP BY ts.nome
                """, (data_inicio, data_fim))
                
                leituras_por_sensor = cursor.fetchall()
                
                # Alertas por severidade
                cursor.execute("""
                    SELECT 
                        severidade,
                        COUNT(*) as total
                    FROM alertas 
                    WHERE timestamp_alerta BETWEEN %s AND %s
                    GROUP BY severidade
                """, (data_inicio, data_fim))
                
                alertas_por_severidade = dict(cursor.fetchall())
                
                # Qualidade dos dados
                cursor.execute("""
                    SELECT 
                        qualidade_dados,
                        COUNT(*) as total
                    FROM leituras_sensores 
                    WHERE timestamp_datetime BETWEEN %s AND %s
                    GROUP BY qualidade_dados
                """, (data_inicio, data_fim))
                
                qualidade_dados = dict(cursor.fetchall())
                
                # Leituras por hora
                cursor.execute("""
                    SELECT 
                        HOUR(timestamp_datetime) as hora,
                        COUNT(*) as total_leituras
                    FROM leituras_sensores 
                    WHERE timestamp_datetime BETWEEN %s AND %s
                    GROUP BY HOUR(timestamp_datetime)
                    ORDER BY hora
                """, (data_inicio, data_fim))
                
                leituras_por_hora = cursor.fetchall()
                
                cursor.close()
                
                return {
                    'periodo': {
                        'inicio': data_inicio,
                        'fim': data_fim
                    },
                    'kpis': kpis,
                    'leituras_por_sensor': leituras_por_sensor,
                    'alertas_por_severidade': alertas_por_severidade,
                    'qualidade_dados': qualidade_dados,
                    'leituras_por_hora': leituras_por_hora
                }
                
        except Exception as e:
            logger.error(f"Erro ao coletar dados: {e}")
            return {}
    
    def _gerar_graficos_diario(self, dados: Dict[str, Any]) -> Dict[str, str]:
        """Gera gráficos para relatório diário"""
        graficos = {}
        
        try:
            # Gráfico de leituras por hora
            if dados.get('leituras_por_hora'):
                horas, totais = zip(*dados['leituras_por_hora'])
                
                plt.figure(figsize=(12, 6))
                plt.plot(horas, totais, marker='o', linewidth=2, markersize=6)
                plt.title('Leituras por Hora - Dia Anterior', fontsize=16, fontweight='bold')
                plt.xlabel('Hora do Dia')
                plt.ylabel('Número de Leituras')
                plt.grid(True, alpha=0.3)
                plt.xticks(range(0, 24, 2))
                
                grafico_path = os.path.join(self.config.diretorio_relatorios, 'leituras_por_hora_diario.png')
                plt.savefig(grafico_path, dpi=300, bbox_inches='tight')
                plt.close()
                graficos['leituras_por_hora'] = grafico_path
            
            # Gráfico de qualidade dos dados
            if dados.get('qualidade_dados'):
                qualidades = list(dados['qualidade_dados'].keys())
                totais = list(dados['qualidade_dados'].values())
                cores = ['#28a745', '#20c997', '#ffc107', '#dc3545']
                
                plt.figure(figsize=(10, 6))
                plt.pie(totais, labels=qualidades, autopct='%1.1f%%', colors=cores[:len(qualidades)])
                plt.title('Distribuição da Qualidade dos Dados', fontsize=16, fontweight='bold')
                
                grafico_path = os.path.join(self.config.diretorio_relatorios, 'qualidade_dados_diario.png')
                plt.savefig(grafico_path, dpi=300, bbox_inches='tight')
                plt.close()
                graficos['qualidade_dados'] = grafico_path
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráficos diários: {e}")
        
        return graficos
    
    def _gerar_graficos_semanal(self, dados: Dict[str, Any]) -> Dict[str, str]:
        """Gera gráficos para relatório semanal"""
        graficos = {}
        
        try:
            # Gráfico de tendência dos sensores
            if dados.get('leituras_por_sensor'):
                sensores = [row[0] for row in dados['leituras_por_sensor']]
                valores_medios = [row[2] for row in dados['leituras_por_sensor']]
                
                plt.figure(figsize=(12, 8))
                bars = plt.bar(sensores, valores_medios, color='skyblue', alpha=0.7)
                plt.title('Valores Médios por Tipo de Sensor - Semana', fontsize=16, fontweight='bold')
                plt.xlabel('Tipo de Sensor')
                plt.ylabel('Valor Médio')
                plt.xticks(rotation=45)
                plt.grid(True, alpha=0.3)
                
                # Adiciona valores nas barras
                for bar, valor in zip(bars, valores_medios):
                    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                            f'{valor:.2f}', ha='center', va='bottom')
                
                grafico_path = os.path.join(self.config.diretorio_relatorios, 'sensores_semanal.png')
                plt.savefig(grafico_path, dpi=300, bbox_inches='tight')
                plt.close()
                graficos['sensores'] = grafico_path
            
            # Gráfico de alertas por severidade
            if dados.get('alertas_por_severidade'):
                severidades = list(dados['alertas_por_severidade'].keys())
                totais = list(dados['alertas_por_severidade'].values())
                cores = ['#dc3545', '#fd7e14', '#ffc107', '#28a745']
                
                plt.figure(figsize=(10, 6))
                plt.bar(severidades, totais, color=cores[:len(severidades)], alpha=0.8)
                plt.title('Alertas por Severidade - Semana', fontsize=16, fontweight='bold')
                plt.xlabel('Severidade')
                plt.ylabel('Número de Alertas')
                plt.grid(True, alpha=0.3)
                
                grafico_path = os.path.join(self.config.diretorio_relatorios, 'alertas_semanal.png')
                plt.savefig(grafico_path, dpi=300, bbox_inches='tight')
                plt.close()
                graficos['alertas'] = grafico_path
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráficos semanais: {e}")
        
        return graficos
    
    def _gerar_graficos_mensal(self, dados: Dict[str, Any]) -> Dict[str, str]:
        """Gera gráficos para relatório mensal"""
        graficos = {}
        
        try:
            # Gráfico de evolução dos KPIs
            kpis = dados.get('kpis', {})
            metricas = ['total_leituras', 'total_anomalias', 'total_alertas']
            valores = [kpis.get(metrica, 0) for metrica in metricas]
            
            plt.figure(figsize=(12, 8))
            bars = plt.bar(metricas, valores, color=['#007bff', '#dc3545', '#ffc107'], alpha=0.8)
            plt.title('Resumo de Atividade - Mês', fontsize=16, fontweight='bold')
            plt.xlabel('Métricas')
            plt.ylabel('Quantidade')
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            
            # Adiciona valores nas barras
            for bar, valor in zip(bars, valores):
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(valores)*0.01,
                        f'{valor:,}', ha='center', va='bottom')
            
            grafico_path = os.path.join(self.config.diretorio_relatorios, 'kpis_mensal.png')
            plt.savefig(grafico_path, dpi=300, bbox_inches='tight')
            plt.close()
            graficos['kpis'] = grafico_path
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráficos mensais: {e}")
        
        return graficos
    
    def _criar_template_relatorio_diario(self, dados: Dict[str, Any], graficos: Dict[str, str]) -> str:
        """Cria template HTML para relatório diário"""
        template = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório Diário - IoT Monitoring</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; }
        .kpi-card { background: white; border-radius: 10px; padding: 20px; margin: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .kpi-value { font-size: 2rem; font-weight: bold; color: #667eea; }
        .grafico { text-align: center; margin: 20px 0; }
        .grafico img { max-width: 100%; height: auto; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <div class="header">
        <h1><i class="fas fa-chart-line"></i> Relatório Diário - IoT Monitoring</h1>
        <p>Período: {{ dados.periodo.inicio.strftime('%d/%m/%Y') }} - {{ dados.periodo.fim.strftime('%d/%m/%Y') }}</p>
        <p>Gerado em: {{ datetime.now().strftime('%d/%m/%Y %H:%M:%S') }}</p>
    </div>
    
    <div class="container-fluid mt-4">
        <!-- KPIs Principais -->
        <div class="row">
            <div class="col-md-3">
                <div class="kpi-card">
                    <h5>Dispositivos Ativos</h5>
                    <div class="kpi-value">{{ dados.kpis.total_dispositivos or 0 }}</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="kpi-card">
                    <h5>Total de Leituras</h5>
                    <div class="kpi-value">{{ dados.kpis.total_leituras or 0 }}</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="kpi-card">
                    <h5>Anomalias Detectadas</h5>
                    <div class="kpi-value">{{ dados.kpis.total_anomalias or 0 }}</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="kpi-card">
                    <h5>Alertas Ativos</h5>
                    <div class="kpi-value">{{ dados.kpis.total_alertas or 0 }}</div>
                </div>
            </div>
        </div>
        
        <!-- Gráficos -->
        {% if graficos.leituras_por_hora %}
        <div class="grafico">
            <h4>Leituras por Hora</h4>
            <img src="{{ graficos.leituras_por_hora }}" alt="Leituras por Hora">
        </div>
        {% endif %}
        
        {% if graficos.qualidade_dados %}
        <div class="grafico">
            <h4>Qualidade dos Dados</h4>
            <img src="{{ graficos.qualidade_dados }}" alt="Qualidade dos Dados">
        </div>
        {% endif %}
        
        <!-- Tabela de Sensores -->
        {% if dados.leituras_por_sensor %}
        <div class="row mt-4">
            <div class="col-md-12">
                <h4>Resumo por Tipo de Sensor</h4>
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th>Tipo de Sensor</th>
                            <th>Total de Leituras</th>
                            <th>Valor Médio</th>
                            <th>Valor Mínimo</th>
                            <th>Valor Máximo</th>
                            <th>Desvio Padrão</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for sensor in dados.leituras_por_sensor %}
                        <tr>
                            <td>{{ sensor[0] }}</td>
                            <td>{{ sensor[1] }}</td>
                            <td>{{ "%.2f"|format(sensor[2]) }}</td>
                            <td>{{ "%.2f"|format(sensor[3]) }}</td>
                            <td>{{ "%.2f"|format(sensor[4]) }}</td>
                            <td>{{ "%.2f"|format(sensor[5]) }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
        """
        
        from jinja2 import Template
        return Template(template).render(dados=dados, graficos=graficos, datetime=datetime)
    
    def _criar_template_relatorio_semanal(self, dados: Dict[str, Any], graficos: Dict[str, str]) -> str:
        """Cria template HTML para relatório semanal"""
        # Similar ao diário, mas com foco em tendências semanais
        return self._criar_template_relatorio_diario(dados, graficos)
    
    def _criar_template_relatorio_mensal(self, dados: Dict[str, Any], graficos: Dict[str, str]) -> str:
        """Cria template HTML para relatório mensal"""
        # Similar ao diário, mas com foco em análises mensais
        return self._criar_template_relatorio_diario(dados, graficos)
    
    def enviar_relatorio_email(self, caminho_arquivo: str, tipo_relatorio: str):
        """Envia relatório por email"""
        if not self.config.enviar_email or not self.config.email_destinatarios:
            return
        
        try:
            # Configura email
            msg = MIMEMultipart()
            msg['From'] = self.config.email_user
            msg['To'] = ', '.join(self.config.email_destinatarios)
            msg['Subject'] = f"Relatório {tipo_relatorio} - IoT Monitoring"
            
            # Corpo do email
            body = f"""
            Prezados,
            
            Segue em anexo o relatório {tipo_relatorio} do sistema IoT Monitoring.
            
            Período: {datetime.now().strftime('%d/%m/%Y')}
            
            Atenciosamente,
            Sistema IoT Monitoring
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Anexa arquivo
            with open(caminho_arquivo, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(caminho_arquivo)}')
                msg.attach(part)
            
            # Envia email
            server = smtplib.SMTP(self.config.email_smtp, self.config.email_port)
            server.starttls()
            server.login(self.config.email_user, self.config.email_password)
            text = msg.as_string()
            server.sendmail(self.config.email_user, self.config.email_destinatarios, text)
            server.quit()
            
            logger.info(f"Relatório {tipo_relatorio} enviado por email")
            
        except Exception as e:
            logger.error(f"Erro ao enviar email: {e}")

class SistemaRelatoriosAutomaticos:
    """
    Sistema de relatórios automáticos
    """
    
    def __init__(self, config_banco: ConfiguracaoBanco, config_relatorios: ConfiguracaoRelatorios):
        self.config_banco = config_banco
        self.config_relatorios = config_relatorios
        
        # Inicializa componentes
        self.persistencia = PersistenciaBancoRelacional(config_banco)
        self.gerador = GeradorRelatorios(self.persistencia, config_relatorios)
        
        # Estado do sistema
        self.executando = False
        self.thread_agendador = None
    
    def iniciar(self):
        """Inicia o sistema de relatórios automáticos"""
        try:
            logger.info("Iniciando sistema de relatórios automáticos")
            
            # Configura agendamentos
            self._configurar_agendamentos()
            
            # Inicia thread do agendador
            self.executando = True
            self.thread_agendador = threading.Thread(target=self._thread_agendador, daemon=True)
            self.thread_agendador.start()
            
            logger.info("Sistema de relatórios automáticos iniciado")
            
        except Exception as e:
            logger.error(f"Erro ao iniciar sistema de relatórios: {e}")
            raise
    
    def parar(self):
        """Para o sistema de relatórios automáticos"""
        try:
            logger.info("Parando sistema de relatórios automáticos")
            
            self.executando = False
            
            if self.thread_agendador and self.thread_agendador.is_alive():
                self.thread_agendador.join(timeout=5)
            
            logger.info("Sistema de relatórios automáticos parado")
            
        except Exception as e:
            logger.error(f"Erro ao parar sistema de relatórios: {e}")
    
    def _configurar_agendamentos(self):
        """Configura agendamentos dos relatórios"""
        try:
            # Relatório diário
            schedule.every().day.at(self.config_relatorios.frequencia_diario).do(
                self._executar_relatorio_diario
            )
            
            # Relatório semanal
            schedule.every().monday.at(self.config_relatorios.frequencia_semanal.split()[1]).do(
                self._executar_relatorio_semanal
            )
            
            # Relatório mensal
            schedule.every().month.do(
                self._executar_relatorio_mensal
            )
            
            logger.info("Agendamentos configurados")
            
        except Exception as e:
            logger.error(f"Erro ao configurar agendamentos: {e}")
    
    def _thread_agendador(self):
        """Thread do agendador de relatórios"""
        logger.info("Thread do agendador iniciada")
        
        while self.executando:
            try:
                schedule.run_pending()
                time.sleep(60)  # Verifica a cada minuto
                
            except Exception as e:
                logger.error(f"Erro no agendador: {e}")
                time.sleep(60)
        
        logger.info("Thread do agendador finalizada")
    
    def _executar_relatorio_diario(self):
        """Executa geração do relatório diário"""
        try:
            logger.info("Executando relatório diário agendado")
            
            caminho_arquivo = self.gerador.gerar_relatorio_diario()
            
            if caminho_arquivo and self.config_relatorios.enviar_email:
                self.gerador.enviar_relatorio_email(caminho_arquivo, "Diário")
            
        except Exception as e:
            logger.error(f"Erro no relatório diário: {e}")
    
    def _executar_relatorio_semanal(self):
        """Executa geração do relatório semanal"""
        try:
            logger.info("Executando relatório semanal agendado")
            
            caminho_arquivo = self.gerador.gerar_relatorio_semanal()
            
            if caminho_arquivo and self.config_relatorios.enviar_email:
                self.gerador.enviar_relatorio_email(caminho_arquivo, "Semanal")
            
        except Exception as e:
            logger.error(f"Erro no relatório semanal: {e}")
    
    def _executar_relatorio_mensal(self):
        """Executa geração do relatório mensal"""
        try:
            logger.info("Executando relatório mensal agendado")
            
            caminho_arquivo = self.gerador.gerar_relatorio_mensal()
            
            if caminho_arquivo and self.config_relatorios.enviar_email:
                self.gerador.enviar_relatorio_email(caminho_arquivo, "Mensal")
            
        except Exception as e:
            logger.error(f"Erro no relatório mensal: {e}")
    
    def gerar_relatorio_manual(self, tipo: str) -> str:
        """Gera relatório manual"""
        try:
            if tipo == 'diario':
                return self.gerador.gerar_relatorio_diario()
            elif tipo == 'semanal':
                return self.gerador.gerar_relatorio_semanal()
            elif tipo == 'mensal':
                return self.gerador.gerar_relatorio_mensal()
            else:
                raise ValueError(f"Tipo de relatório inválido: {tipo}")
                
        except Exception as e:
            logger.error(f"Erro ao gerar relatório manual: {e}")
            return None

# =====================================================
# EXEMPLO DE USO
# =====================================================

def exemplo_uso():
    """Exemplo de uso do sistema de relatórios"""
    
    # Configurações
    config_banco = ConfiguracaoBanco(
        host="localhost",
        port=3306,
        database="iot_monitoring_db",
        username="root",
        password="password"
    )
    
    config_relatorios = ConfiguracaoRelatorios(
        diretorio_relatorios="relatorios/",
        enviar_email=False,
        frequencia_diario="08:00",
        frequencia_semanal="monday 09:00"
    )
    
    # Inicializa sistema
    sistema_relatorios = SistemaRelatoriosAutomaticos(config_banco, config_relatorios)
    
    try:
        # Inicia sistema
        sistema_relatorios.iniciar()
        
        # Gera relatório manual de exemplo
        caminho_relatorio = sistema_relatorios.gerar_relatorio_manual('diario')
        if caminho_relatorio:
            print(f"Relatório gerado: {caminho_relatorio}")
        
        # Mantém execução
        while True:
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("Parando sistema...")
    finally:
        sistema_relatorios.parar()

if __name__ == "__main__":
    exemplo_uso()
