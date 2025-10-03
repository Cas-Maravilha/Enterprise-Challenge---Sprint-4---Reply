#!/usr/bin/env python3
"""
Sistema de Alertas Avançado - Sistema IoT Monitoring
Enterprise Challenge Sprint 3 - Reply

Este script implementa um sistema completo de alertas com
thresholds configuráveis, notificações e logs.
"""

import mysql.connector
import pandas as pd
import numpy as np
import smtplib
import json
import logging
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Any, Tuple
import warnings
warnings.filterwarnings('ignore')

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sistema_alertas.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SistemaAlertasAvancado:
    """Sistema avançado de alertas IoT"""
    
    def __init__(self, host='localhost', user='root', password='', database='iot_monitoring_db'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        
        # Configurações de alertas
        self.thresholds = {
            'temperatura': {'max': 30.0, 'min': 15.0, 'critico_max': 35.0, 'critico_min': 10.0},
            'umidade': {'max': 80.0, 'min': 30.0, 'critico_max': 90.0, 'critico_min': 20.0},
            'luminosidade': {'max': 800.0, 'min': 50.0, 'critico_max': 1000.0, 'critico_min': 10.0},
            'pressao': {'max': 1050.0, 'min': 950.0, 'critico_max': 1100.0, 'critico_min': 900.0},
            'vibracao': {'max': 1.5, 'min': -1.5, 'critico_max': 2.0, 'critico_min': -2.0}
        }
        
        # Configurações de notificação
        self.config_email = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'email_remetente': 'iot.monitoring@empresa.com',
            'senha_remetente': 'senha_segura',
            'emails_destinatarios': ['admin@empresa.com', 'operador@empresa.com']
        }
        
        # Histórico de alertas
        self.historico_alertas = []
        
        logger.info("=== Sistema de Alertas Avançado ===")
        logger.info("Enterprise Challenge Sprint 3 - Reply")
        logger.info("===================================")
    
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
            logger.info("Conectado ao banco de dados com sucesso")
            return True
        except mysql.connector.Error as e:
            logger.error(f"Erro ao conectar ao banco: {e}")
            return False
    
    def executar_consulta(self, query: str, params: Tuple = None) -> pd.DataFrame:
        """Executa uma consulta SQL e retorna DataFrame"""
        try:
            self.cursor.execute(query, params)
            resultado = self.cursor.fetchall()
            return pd.DataFrame(resultado)
        except mysql.connector.Error as e:
            logger.error(f"Erro na consulta: {e}")
            return pd.DataFrame()
    
    def carregar_dados_recentes(self):
        """Carrega dados recentes para verificação de alertas"""
        query = """
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
            d.ip_address,
            ts.nome as tipo_sensor_nome,
            ts.unidade_medida
        FROM leituras_sensores l
        JOIN sensores s ON l.id_sensor = s.id_sensor
        JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
        JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
        WHERE l.timestamp_datetime >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
        AND l.valor_numerico IS NOT NULL
        ORDER BY l.timestamp_datetime DESC
        """
        
        return self.executar_consulta(query)
    
    def verificar_thresholds(self, df_dados):
        """Verifica thresholds e gera alertas"""
        alertas_gerados = []
        
        for _, row in df_dados.iterrows():
            sensor_tipo = row['tipo_sensor_nome'].lower()
            valor = row['valor_numerico']
            
            if sensor_tipo not in self.thresholds:
                continue
            
            threshold = self.thresholds[sensor_tipo]
            alerta = None
            
            # Verificar limites críticos
            if valor > threshold['critico_max']:
                alerta = {
                    'tipo': 'CRÍTICO ALTO',
                    'sensor': row['sensor_nome'],
                    'dispositivo': row['dispositivo_nome'],
                    'localizacao': row['localizacao'],
                    'valor': valor,
                    'limite': threshold['critico_max'],
                    'timestamp': row['timestamp_datetime'],
                    'severidade': 'CRÍTICA',
                    'unidade': row['unidade_medida']
                }
            elif valor < threshold['critico_min']:
                alerta = {
                    'tipo': 'CRÍTICO BAIXO',
                    'sensor': row['sensor_nome'],
                    'dispositivo': row['dispositivo_nome'],
                    'localizacao': row['localizacao'],
                    'valor': valor,
                    'limite': threshold['critico_min'],
                    'timestamp': row['timestamp_datetime'],
                    'severidade': 'CRÍTICA',
                    'unidade': row['unidade_medida']
                }
            # Verificar limites normais
            elif valor > threshold['max']:
                alerta = {
                    'tipo': 'ALERTA ALTO',
                    'sensor': row['sensor_nome'],
                    'dispositivo': row['dispositivo_nome'],
                    'localizacao': row['localizacao'],
                    'valor': valor,
                    'limite': threshold['max'],
                    'timestamp': row['timestamp_datetime'],
                    'severidade': 'ALTA',
                    'unidade': row['unidade_medida']
                }
            elif valor < threshold['min']:
                alerta = {
                    'tipo': 'ALERTA BAIXO',
                    'sensor': row['sensor_nome'],
                    'dispositivo': row['dispositivo_nome'],
                    'localizacao': row['localizacao'],
                    'valor': valor,
                    'limite': threshold['min'],
                    'timestamp': row['timestamp_datetime'],
                    'severidade': 'ALTA',
                    'unidade': row['unidade_medida']
                }
            
            if alerta:
                alertas_gerados.append(alerta)
        
        return alertas_gerados
    
    def gerar_banner_alerta(self, alerta):
        """Gera banner visual para alerta"""
        timestamp = alerta['timestamp'].strftime('%H:%M:%S')
        
        if alerta['severidade'] == 'CRÍTICA':
            banner = f"""
            ╔══════════════════════════════════════════════════════════════════════════════════╗
            ║                                    🚨 ALERTA CRÍTICO 🚨                          ║
            ╠══════════════════════════════════════════════════════════════════════════════════╣
            ║ Tipo: {alerta['tipo']:<20} Severidade: {alerta['severidade']:<10} Timestamp: {timestamp} ║
            ║ Dispositivo: {alerta['dispositivo']:<30} Local: {alerta['localizacao']:<20} ║
            ║ Sensor: {alerta['sensor']:<35} Valor: {alerta['valor']:.2f} {alerta['unidade']:<10} ║
            ║ Limite: {alerta['limite']:.2f} {alerta['unidade']:<35} Diferença: {abs(alerta['valor'] - alerta['limite']):.2f} ║
            ╚══════════════════════════════════════════════════════════════════════════════════╝
            """
        else:
            banner = f"""
            ╔══════════════════════════════════════════════════════════════════════════════════╗
            ║                                    ⚠️  ALERTA  ⚠️                               ║
            ╠══════════════════════════════════════════════════════════════════════════════════╣
            ║ Tipo: {alerta['tipo']:<20} Severidade: {alerta['severidade']:<10} Timestamp: {timestamp} ║
            ║ Dispositivo: {alerta['dispositivo']:<30} Local: {alerta['localizacao']:<20} ║
            ║ Sensor: {alerta['sensor']:<35} Valor: {alerta['valor']:.2f} {alerta['unidade']:<10} ║
            ║ Limite: {alerta['limite']:.2f} {alerta['unidade']:<35} Diferença: {abs(alerta['valor'] - alerta['limite']):.2f} ║
            ╚══════════════════════════════════════════════════════════════════════════════════╝
            """
        
        return banner
    
    def gerar_log_alerta(self, alerta):
        """Gera log estruturado do alerta"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'tipo_alerta': alerta['tipo'],
            'severidade': alerta['severidade'],
            'dispositivo': alerta['dispositivo'],
            'sensor': alerta['sensor'],
            'localizacao': alerta['localizacao'],
            'valor_atual': alerta['valor'],
            'valor_limite': alerta['limite'],
            'diferenca': abs(alerta['valor'] - alerta['limite']),
            'unidade': alerta['unidade'],
            'timestamp_leitura': alerta['timestamp'].isoformat()
        }
        
        return log_entry
    
    def gerar_email_alerta(self, alerta):
        """Gera email de notificação do alerta"""
        timestamp = alerta['timestamp'].strftime('%d/%m/%Y %H:%M:%S')
        
        subject = f"🚨 {alerta['severidade']} - {alerta['tipo']} - {alerta['dispositivo']}"
        
        body = f"""
        <html>
        <body>
        <h2>🚨 Alerta do Sistema IoT Monitoring</h2>
        
        <table border="1" cellpadding="5" cellspacing="0">
        <tr><td><strong>Tipo de Alerta:</strong></td><td>{alerta['tipo']}</td></tr>
        <tr><td><strong>Severidade:</strong></td><td>{alerta['severidade']}</td></tr>
        <tr><td><strong>Dispositivo:</strong></td><td>{alerta['dispositivo']}</td></tr>
        <tr><td><strong>Sensor:</strong></td><td>{alerta['sensor']}</td></tr>
        <tr><td><strong>Localização:</strong></td><td>{alerta['localizacao']}</td></tr>
        <tr><td><strong>Valor Atual:</strong></td><td>{alerta['valor']:.2f} {alerta['unidade']}</td></tr>
        <tr><td><strong>Valor Limite:</strong></td><td>{alerta['limite']:.2f} {alerta['unidade']}</td></tr>
        <tr><td><strong>Diferença:</strong></td><td>{abs(alerta['valor'] - alerta['limite']):.2f} {alerta['unidade']}</td></tr>
        <tr><td><strong>Timestamp:</strong></td><td>{timestamp}</td></tr>
        </table>
        
        <p><strong>Ação Recomendada:</strong></p>
        <ul>
        <li>Verificar o dispositivo {alerta['dispositivo']}</li>
        <li>Analisar o sensor {alerta['sensor']}</li>
        <li>Verificar condições ambientais em {alerta['localizacao']}</li>
        <li>Considerar calibração do sensor se necessário</li>
        </ul>
        
        <p><em>Este é um alerta automático do Sistema IoT Monitoring.</em></p>
        </body>
        </html>
        """
        
        return subject, body
    
    def enviar_email(self, subject, body):
        """Envia email de notificação"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.config_email['email_remetente']
            msg['To'] = ', '.join(self.config_email['emails_destinatarios'])
            
            html_part = MIMEText(body, 'html')
            msg.attach(html_part)
            
            server = smtplib.SMTP(self.config_email['smtp_server'], self.config_email['smtp_port'])
            server.starttls()
            server.login(self.config_email['email_remetente'], self.config_email['senha_remetente'])
            
            text = msg.as_string()
            server.sendmail(
                self.config_email['email_remetente'],
                self.config_email['emails_destinatarios'],
                text
            )
            server.quit()
            
            logger.info("Email enviado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao enviar email: {e}")
            return False
    
    def salvar_alerta_banco(self, alerta):
        """Salva alerta no banco de dados"""
        try:
            # Buscar ID do dispositivo
            query_disp = "SELECT id_dispositivo FROM dispositivos WHERE nome = %s"
            self.cursor.execute(query_disp, (alerta['dispositivo'],))
            resultado_disp = self.cursor.fetchone()
            
            if not resultado_disp:
                logger.error(f"Dispositivo {alerta['dispositivo']} não encontrado")
                return False
            
            id_dispositivo = resultado_disp['id_dispositivo']
            
            # Buscar ID do sensor
            query_sensor = """
            SELECT s.id_sensor 
            FROM sensores s 
            JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo 
            WHERE s.nome = %s AND d.nome = %s
            """
            self.cursor.execute(query_sensor, (alerta['sensor'], alerta['dispositivo']))
            resultado_sensor = self.cursor.fetchone()
            
            id_sensor = resultado_sensor['id_sensor'] if resultado_sensor else None
            
            # Buscar ID do modo de operação
            modo_map = {
                'CRÍTICA': 'Falha',
                'ALTA': 'Alerta',
                'MÉDIA': 'Normal'
            }
            modo = modo_map.get(alerta['severidade'], 'Alerta')
            
            query_modo = "SELECT id_modo FROM modos_operacao WHERE nome = %s"
            self.cursor.execute(query_modo, (modo,))
            resultado_modo = self.cursor.fetchone()
            id_modo = resultado_modo['id_modo'] if resultado_modo else 2  # Default: Alerta
            
            # Inserir alerta
            query_insert = """
            INSERT INTO alertas (
                id_dispositivo, id_sensor, id_modo, tipo_alerta, severidade,
                titulo, descricao, valor_atual, valor_limite, timestamp_alerta, status
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            titulo = f"{alerta['tipo']} - {alerta['dispositivo']} - {alerta['sensor']}"
            descricao = f"Valor: {alerta['valor']:.2f} {alerta['unidade']}, Limite: {alerta['limite']:.2f} {alerta['unidade']}"
            
            valores = (
                id_dispositivo, id_sensor, id_modo, alerta['tipo'].lower(),
                alerta['severidade'].lower(), titulo, descricao,
                alerta['valor'], alerta['limite'], alerta['timestamp'], 'ativo'
            )
            
            self.cursor.execute(query_insert, valores)
            self.connection.commit()
            
            logger.info(f"Alerta salvo no banco: {titulo}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar alerta no banco: {e}")
            return False
    
    def processar_alertas(self, alertas):
        """Processa lista de alertas"""
        for alerta in alertas:
            # Gerar banner
            banner = self.gerar_banner_alerta(alerta)
            print(banner)
            
            # Gerar log
            log_entry = self.gerar_log_alerta(alerta)
            self.historico_alertas.append(log_entry)
            logger.info(f"Alerta processado: {alerta['tipo']} - {alerta['dispositivo']}")
            
            # Salvar no banco
            self.salvar_alerta_banco(alerta)
            
            # Enviar email (simulado)
            if alerta['severidade'] == 'CRÍTICA':
                subject, body = self.gerar_email_alerta(alerta)
                logger.info(f"Email gerado: {subject}")
                # self.enviar_email(subject, body)  # Descomente para enviar emails reais
    
    def executar_verificacao_alertas(self):
        """Executa verificação completa de alertas"""
        logger.info("🔍 Iniciando verificação de alertas...")
        
        # Conectar ao banco
        if not self.conectar_banco():
            return False
        
        try:
            # Carregar dados recentes
            df_dados = self.carregar_dados_recentes()
            
            if df_dados.empty:
                logger.warning("Nenhum dado recente encontrado")
                return True
            
            logger.info(f"Processando {len(df_dados)} leituras recentes")
            
            # Verificar thresholds
            alertas = self.verificar_thresholds(df_dados)
            
            if alertas:
                logger.info(f"🚨 {len(alertas)} alerta(s) detectado(s)")
                self.processar_alertas(alertas)
            else:
                logger.info("✅ Nenhum alerta detectado")
            
            # Salvar histórico
            self.salvar_historico_alertas()
            
            return True
            
        except Exception as e:
            logger.error(f"Erro na verificação de alertas: {e}")
            return False
        
        finally:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
    
    def salvar_historico_alertas(self):
        """Salva histórico de alertas em arquivo"""
        try:
            with open('historico_alertas.json', 'w', encoding='utf-8') as f:
                json.dump(self.historico_alertas, f, indent=2, ensure_ascii=False, default=str)
            logger.info("Histórico de alertas salvo")
        except Exception as e:
            logger.error(f"Erro ao salvar histórico: {e}")
    
    def configurar_thresholds(self, novos_thresholds):
        """Configura novos thresholds"""
        self.thresholds.update(novos_thresholds)
        logger.info("Thresholds atualizados")
    
    def obter_estatisticas_alertas(self):
        """Obtém estatísticas dos alertas"""
        if not self.historico_alertas:
            return {}
        
        df_alertas = pd.DataFrame(self.historico_alertas)
        
        stats = {
            'total_alertas': len(df_alertas),
            'alertas_por_severidade': df_alertas['severidade'].value_counts().to_dict(),
            'alertas_por_dispositivo': df_alertas['dispositivo'].value_counts().to_dict(),
            'alertas_por_tipo': df_alertas['tipo_alerta'].value_counts().to_dict(),
            'ultimo_alerta': df_alertas['timestamp'].max() if not df_alertas.empty else None
        }
        
        return stats


def main():
    """Função principal"""
    print("=== Sistema de Alertas Avançado ===")
    print("Enterprise Challenge Sprint 3 - Reply")
    print("===================================")
    
    # Configurar parâmetros de conexão
    host = input("Host do banco (padrão: localhost): ").strip() or 'localhost'
    user = input("Usuário do banco (padrão: root): ").strip() or 'root'
    password = input("Senha do banco: ").strip()
    database = input("Nome do banco (padrão: iot_monitoring_db): ").strip() or 'iot_monitoring_db'
    
    # Criar sistema de alertas
    sistema = SistemaAlertasAvancado(host, user, password, database)
    
    # Executar verificação
    sucesso = sistema.executar_verificacao_alertas()
    
    if sucesso:
        print("\n✅ Verificação de alertas executada com sucesso!")
        print("📊 Verifique os arquivos gerados:")
        print("  - historico_alertas.json")
        print("  - sistema_alertas.log")
    else:
        print("\n❌ Erro na execução da verificação de alertas.")


if __name__ == "__main__":
    main()
