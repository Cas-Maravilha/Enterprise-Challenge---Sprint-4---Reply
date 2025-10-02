#!/usr/bin/env python3
"""
Executador do Pipeline Completo - Sistema IoT Monitoring Sprint 3
Executa o pipeline integrado completo com coleta ESP32, processamento ML e dashboard

Autor: Enterprise Challenge - Sprint 3 - Reply
Data: 2024
"""

import os
import sys
import time
import subprocess
import threading
import signal
import logging
from datetime import datetime
from typing import List, Dict

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("Executador Pipeline")

class ExecutadorPipelineCompleto:
    """
    Executador do pipeline completo integrado
    """
    
    def __init__(self):
        self.processos = {}
        self.threads = {}
        self.executando = False
        
        # Configurações dos componentes
        self.componentes = {
            'coletor_wokwi': {
                'script': 'coletor_dados_wokwi.py',
                'descricao': 'Coletor de dados ESP32 (Wokwi)',
                'obrigatorio': True
            },
            'pipeline_integrado': {
                'script': 'pipeline_integrado_esp32.py',
                'descricao': 'Pipeline integrado principal',
                'obrigatorio': True
            },
            'dashboard': {
                'script': 'interactive_dashboard.py',
                'descricao': 'Dashboard interativo',
                'obrigatorio': False
            }
        }
        
        logger.info("Executador do pipeline completo inicializado")
    
    def verificar_dependencias(self) -> bool:
        """Verifica se todas as dependências estão instaladas"""
        logger.info("Verificando dependências...")
        
        dependencias = [
            'paho-mqtt',
            'pandas',
            'numpy',
            'scikit-learn',
            'matplotlib',
            'seaborn',
            'mysql-connector-python',
            'joblib',
            'python-dotenv'
        ]
        
        dependencias_faltando = []
        
        for dep in dependencias:
            try:
                __import__(dep.replace('-', '_'))
                logger.debug(f"✅ {dep}")
            except ImportError:
                dependencias_faltando.append(dep)
                logger.warning(f"❌ {dep}")
        
        if dependencias_faltando:
            logger.error(f"Dependências faltando: {', '.join(dependencias_faltando)}")
            logger.error("Execute: pip install -r requirements.txt")
            return False
        
        logger.info("✅ Todas as dependências estão instaladas")
        return True
    
    def verificar_arquivos(self) -> bool:
        """Verifica se todos os arquivos necessários existem"""
        logger.info("Verificando arquivos...")
        
        arquivos_necessarios = [
            'pipeline_integrado_esp32.py',
            'coletor_dados_wokwi.py',
            'config_pipeline.json',
            'modelos_ia.py',
            'kpis_negocio.py',
            'monitoramento_drift.py',
            'metricas_validacao_detalhadas.py'
        ]
        
        arquivos_faltando = []
        
        for arquivo in arquivos_necessarios:
            if os.path.exists(arquivo):
                logger.debug(f"✅ {arquivo}")
            else:
                arquivos_faltando.append(arquivo)
                logger.warning(f"❌ {arquivo}")
        
        if arquivos_faltando:
            logger.error(f"Arquivos faltando: {', '.join(arquivos_faltando)}")
            return False
        
        logger.info("✅ Todos os arquivos necessários existem")
        return True
    
    def verificar_banco_dados(self) -> bool:
        """Verifica se o banco de dados está configurado"""
        logger.info("Verificando banco de dados...")
        
        try:
            import mysql.connector
            from config_pipeline import config
            
            # Tentar conectar
            connection = mysql.connector.connect(
                host=config['database']['host'],
                port=config['database']['port'],
                database=config['database']['database'],
                user=config['database']['username'],
                password=config['database']['password']
            )
            
            if connection.is_connected():
                logger.info("✅ Banco de dados conectado")
                connection.close()
                return True
            else:
                logger.error("❌ Falha na conexão com banco de dados")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao verificar banco de dados: {e}")
            logger.error("Execute: python executar_criacao_banco.py")
            return False
    
    def verificar_modelo_ml(self) -> bool:
        """Verifica se o modelo ML está disponível"""
        logger.info("Verificando modelo ML...")
        
        modelo_path = "modelos/modelo_anomalia_iot_completo.pkl"
        
        if os.path.exists(modelo_path):
            logger.info("✅ Modelo ML encontrado")
            return True
        else:
            logger.warning("⚠️ Modelo ML não encontrado")
            logger.warning("Execute: python ml_anomaly_detection_completo.py")
            return False
    
    def executar_componente(self, nome: str) -> subprocess.Popen:
        """Executa um componente do pipeline"""
        componente = self.componentes[nome]
        script = componente['script']
        
        logger.info(f"🚀 Iniciando {componente['descricao']}...")
        
        try:
            processo = subprocess.Popen(
                [sys.executable, script],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processos[nome] = processo
            logger.info(f"✅ {componente['descricao']} iniciado (PID: {processo.pid})")
            return processo
            
        except Exception as e:
            logger.error(f"❌ Erro ao iniciar {componente['descricao']}: {e}")
            return None
    
    def monitorar_componente(self, nome: str):
        """Monitora um componente do pipeline"""
        processo = self.processos.get(nome)
        if not processo:
            return
        
        logger.info(f"👁️ Monitorando {nome}...")
        
        while self.executando and processo.poll() is None:
            time.sleep(1)
        
        if processo.poll() is not None:
            stdout, stderr = processo.communicate()
            if processo.returncode != 0:
                logger.error(f"❌ {nome} terminou com erro (código: {processo.returncode})")
                if stderr:
                    logger.error(f"Erro: {stderr}")
            else:
                logger.info(f"✅ {nome} terminou normalmente")
    
    def iniciar_pipeline(self):
        """Inicia o pipeline completo"""
        logger.info("🚀 INICIANDO PIPELINE COMPLETO")
        logger.info("=" * 50)
        
        # Verificações prévias
        if not self.verificar_dependencias():
            return False
        
        if not self.verificar_arquivos():
            return False
        
        if not self.verificar_banco_dados():
            logger.warning("⚠️ Continuando sem banco de dados...")
        
        if not self.verificar_modelo_ml():
            logger.warning("⚠️ Continuando sem modelo ML...")
        
        # Iniciar componentes
        self.executando = True
        
        # 1. Pipeline integrado principal
        if not self.executar_componente('pipeline_integrado'):
            logger.error("❌ Falha ao iniciar pipeline principal")
            return False
        
        # Aguardar pipeline principal inicializar
        time.sleep(5)
        
        # 2. Coletor de dados Wokwi
        if not self.executar_componente('coletor_wokwi'):
            logger.error("❌ Falha ao iniciar coletor de dados")
            return False
        
        # 3. Dashboard (opcional)
        if os.path.exists('interactive_dashboard.py'):
            self.executar_componente('dashboard')
        
        # Iniciar monitoramento
        for nome in self.processos.keys():
            thread = threading.Thread(target=self.monitorar_componente, args=(nome,))
            thread.daemon = True
            thread.start()
            self.threads[nome] = thread
        
        logger.info("✅ Pipeline completo iniciado!")
        logger.info("📊 Componentes ativos:")
        for nome, processo in self.processos.items():
            if processo and processo.poll() is None:
                logger.info(f"   - {self.componentes[nome]['descricao']} (PID: {processo.pid})")
        
        return True
    
    def parar_pipeline(self):
        """Para o pipeline completo"""
        logger.info("🛑 PARANDO PIPELINE COMPLETO")
        logger.info("=" * 50)
        
        self.executando = False
        
        # Parar processos
        for nome, processo in self.processos.items():
            if processo and processo.poll() is None:
                logger.info(f"🛑 Parando {self.componentes[nome]['descricao']}...")
                processo.terminate()
                
                # Aguardar término
                try:
                    processo.wait(timeout=10)
                    logger.info(f"✅ {self.componentes[nome]['descricao']} parado")
                except subprocess.TimeoutExpired:
                    logger.warning(f"⚠️ Forçando parada de {self.componentes[nome]['descricao']}...")
                    processo.kill()
                    processo.wait()
                    logger.info(f"✅ {self.componentes[nome]['descricao']} forçado a parar")
        
        # Aguardar threads de monitoramento
        for thread in self.threads.values():
            thread.join(timeout=5)
        
        logger.info("✅ Pipeline completo parado!")
    
    def status_pipeline(self) -> Dict:
        """Retorna status do pipeline"""
        status = {
            'executando': self.executando,
            'componentes': {},
            'timestamp': datetime.now().isoformat()
        }
        
        for nome, processo in self.processos.items():
            if processo:
                status['componentes'][nome] = {
                    'pid': processo.pid,
                    'ativo': processo.poll() is None,
                    'codigo_saida': processo.returncode if processo.poll() is not None else None
                }
            else:
                status['componentes'][nome] = {
                    'pid': None,
                    'ativo': False,
                    'codigo_saida': None
                }
        
        return status
    
    def executar_dashboard_status(self):
        """Executa dashboard de status do pipeline"""
        try:
            import dash
            from dash import dcc, html, Input, Output
            import plotly.graph_objs as go
            
            app = dash.Dash(__name__)
            
            app.layout = html.Div([
                html.H1("Status do Pipeline IoT Monitoring"),
                html.Div(id='status-componentes'),
                html.Div(id='logs-pipeline'),
                dcc.Interval(
                    id='interval-component',
                    interval=5000,  # Atualizar a cada 5 segundos
                    n_intervals=0
                )
            ])
            
            @app.callback(Output('status-componentes', 'children'),
                         Input('interval-component', 'n_intervals'))
            def atualizar_status(n):
                status = self.status_pipeline()
                
                componentes_html = []
                for nome, info in status['componentes'].items():
                    cor = 'green' if info['ativo'] else 'red'
                    status_text = 'Ativo' if info['ativo'] else 'Inativo'
                    
                    componentes_html.append(
                        html.Div([
                            html.H3(f"{self.componentes[nome]['descricao']}"),
                            html.P(f"Status: {status_text}", style={'color': cor}),
                            html.P(f"PID: {info['pid'] or 'N/A'}"),
                            html.Hr()
                        ])
                    )
                
                return componentes_html
            
            @app.callback(Output('logs-pipeline', 'children'),
                         Input('interval-component', 'n_intervals'))
            def atualizar_logs(n):
                # Aqui você implementaria leitura de logs
                return html.Div([
                    html.H3("Logs do Pipeline"),
                    html.P("Logs serão implementados aqui...")
                ])
            
            app.run_server(debug=False, host='0.0.0.0', port=8051)
            
        except ImportError:
            logger.warning("Dash não instalado. Dashboard de status não disponível.")
        except Exception as e:
            logger.error(f"Erro ao executar dashboard de status: {e}")


def signal_handler(signum, frame):
    """Handler para sinais do sistema"""
    print("\n🛑 Recebido sinal de parada...")
    global executador
    if executador:
        executador.parar_pipeline()
    sys.exit(0)


def main():
    """Função principal"""
    global executador
    
    print("🚀 EXECUTADOR DO PIPELINE COMPLETO")
    print("Sistema IoT Monitoring - Sprint 3")
    print("=" * 50)
    
    # Configurar handlers de sinal
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Criar executador
    executador = ExecutadorPipelineCompleto()
    
    try:
        # Iniciar pipeline
        if executador.iniciar_pipeline():
            print("\n✅ Pipeline iniciado com sucesso!")
            print("📊 Monitorando componentes...")
            print("🔍 Verificando status...")
            print("\nPressione Ctrl+C para parar...")
            
            # Loop principal
            while True:
                time.sleep(10)
                
                # Mostrar status
                status = executador.status_pipeline()
                componentes_ativos = sum(1 for c in status['componentes'].values() if c['ativo'])
                print(f"\n📊 Status: {componentes_ativos} componentes ativos")
        
        else:
            print("❌ Falha ao iniciar pipeline")
            return 1
    
    except KeyboardInterrupt:
        print("\n🛑 Parando pipeline...")
        executador.parar_pipeline()
        print("✅ Pipeline parado com sucesso!")
        return 0
    
    except Exception as e:
        print(f"❌ Erro no pipeline: {e}")
        executador.parar_pipeline()
        return 1


if __name__ == "__main__":
    executador = None
    sys.exit(main())
