#!/usr/bin/env python3
"""
Executador do Dashboard Completo - Sistema IoT Monitoring Sprint 3
Executa o sistema completo de dashboard, KPIs e relatórios

Autor: Enterprise Challenge - Sprint 3 - Reply
Data: 2024
"""

import os
import sys
import json
import time
import logging
import argparse
import signal
import threading
from datetime import datetime
from typing import Dict, Any

# Importar módulos do projeto
from persistencia_banco_relacional import (
    PersistenciaBancoRelacional, 
    ConfiguracaoBanco
)
from dashboard_kpis_completo import (
    DashboardKPIsCompleto,
    ConfiguracaoDashboard
)
from sistema_relatorios_automaticos import (
    SistemaRelatoriosAutomaticos,
    ConfiguracaoRelatorios
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("ExecutadorDashboard")

class ExecutadorDashboardCompleto:
    """
    Executador do sistema completo de dashboard
    """
    
    def __init__(self, config_arquivo: str = "config_pipeline.json"):
        self.config_arquivo = config_arquivo
        self.config = self._carregar_configuracao()
        self.executando = False
        self.sistemas = {}
        
        # Configurar sinais para parada graceful
        signal.signal(signal.SIGINT, self._handler_sinal)
        signal.signal(signal.SIGTERM, self._handler_sinal)
    
    def _carregar_configuracao(self) -> Dict[str, Any]:
        """Carrega configuração do arquivo JSON"""
        try:
            if os.path.exists(self.config_arquivo):
                with open(self.config_arquivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning(f"Arquivo de configuração não encontrado: {self.config_arquivo}")
                return self._configuracao_padrao()
        except Exception as e:
            logger.error(f"Erro ao carregar configuração: {e}")
            return self._configuracao_padrao()
    
    def _configuracao_padrao(self) -> Dict[str, Any]:
        """Configuração padrão do sistema"""
        return {
            "database": {
                "host": "localhost",
                "port": 3306,
                "database": "iot_monitoring_db",
                "username": "root",
                "password": "password"
            },
            "dashboard": {
                "host": "0.0.0.0",
                "port": 5000,
                "debug": False,
                "update_interval": 30,
                "max_alertas_exibidos": 50
            },
            "relatorios": {
                "diretorio_relatorios": "relatorios/",
                "enviar_email": False,
                "frequencia_diario": "08:00",
                "frequencia_semanal": "monday 09:00",
                "frequencia_mensal": "1 10:00"
            }
        }
    
    def _handler_sinal(self, signum, frame):
        """Handler para sinais de parada"""
        logger.info(f"Sinal recebido: {signum}")
        self.parar()
    
    def inicializar_sistemas(self):
        """Inicializa todos os sistemas"""
        try:
            logger.info("Inicializando sistemas de dashboard")
            
            # Configuração do banco
            config_banco = ConfiguracaoBanco(
                host=self.config['database']['host'],
                port=self.config['database']['port'],
                database=self.config['database']['database'],
                username=self.config['database']['username'],
                password=self.config['database']['password']
            )
            
            # Configuração do dashboard
            config_dashboard = ConfiguracaoDashboard(
                host=self.config['dashboard']['host'],
                port=self.config['dashboard']['port'],
                debug=self.config['dashboard']['debug'],
                update_interval=self.config['dashboard']['update_interval'],
                max_alertas_exibidos=self.config['dashboard']['max_alertas_exibidos']
            )
            
            # Configuração dos relatórios
            config_relatorios = ConfiguracaoRelatorios(
                diretorio_relatorios=self.config['relatorios']['diretorio_relatorios'],
                enviar_email=self.config['relatorios']['enviar_email'],
                frequencia_diario=self.config['relatorios']['frequencia_diario'],
                frequencia_semanal=self.config['relatorios']['frequencia_semanal'],
                frequencia_mensal=self.config['relatorios']['frequencia_mensal']
            )
            
            # Sistema de persistência
            self.sistemas['persistencia'] = PersistenciaBancoRelacional(config_banco)
            
            # Sistema de dashboard
            self.sistemas['dashboard'] = DashboardKPIsCompleto(config_banco, config_dashboard)
            
            # Sistema de relatórios
            self.sistemas['relatorios'] = SistemaRelatoriosAutomaticos(config_banco, config_relatorios)
            
            logger.info("Sistemas inicializados com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar sistemas: {e}")
            raise
    
    def iniciar(self, modo: str = "completo"):
        """Inicia o sistema de dashboard"""
        try:
            logger.info(f"Iniciando sistema de dashboard em modo: {modo}")
            
            # Inicializa sistemas
            self.inicializar_sistemas()
            
            if modo == "completo":
                # Inicia dashboard e relatórios
                self.sistemas['relatorios'].iniciar()
                self.sistemas['dashboard'].iniciar()
                
            elif modo == "dashboard_apenas":
                # Inicia apenas dashboard
                self.sistemas['dashboard'].iniciar()
                
            elif modo == "relatorios_apenas":
                # Inicia apenas relatórios
                self.sistemas['relatorios'].iniciar()
                self.executando = True
                self._iniciar_monitoramento()
                
            elif modo == "teste":
                # Executa apenas testes
                self._executar_testes()
                
            else:
                raise ValueError(f"Modo inválido: {modo}")
            
            logger.info("Sistema de dashboard iniciado")
            
        except Exception as e:
            logger.error(f"Erro ao iniciar sistema de dashboard: {e}")
            raise
    
    def parar(self):
        """Para o sistema de dashboard"""
        try:
            logger.info("Parando sistema de dashboard")
            
            self.executando = False
            
            # Para sistemas
            if 'dashboard' in self.sistemas:
                self.sistemas['dashboard'].parar()
            
            if 'relatorios' in self.sistemas:
                self.sistemas['relatorios'].parar()
            
            logger.info("Sistema de dashboard parado")
            
        except Exception as e:
            logger.error(f"Erro ao parar sistema de dashboard: {e}")
    
    def _iniciar_monitoramento(self):
        """Inicia thread de monitoramento"""
        thread_monitoramento = threading.Thread(target=self._monitorar_sistema, daemon=True)
        thread_monitoramento.start()
    
    def _monitorar_sistema(self):
        """Thread de monitoramento do sistema"""
        logger.info("Thread de monitoramento iniciada")
        
        while self.executando:
            try:
                # Mostra estatísticas
                self._mostrar_estatisticas()
                
                # Aguarda próximo ciclo
                time.sleep(60)
                
            except Exception as e:
                logger.error(f"Erro no monitoramento: {e}")
                time.sleep(10)
        
        logger.info("Thread de monitoramento finalizada")
    
    def _mostrar_estatisticas(self):
        """Mostra estatísticas do sistema"""
        try:
            if 'persistencia' in self.sistemas:
                kpis = self.sistemas['persistencia'].obter_kpis_sistema()
                
                logger.info("=== ESTATÍSTICAS DO SISTEMA ===")
                logger.info(f"Dispositivos ativos: {kpis.get('total_dispositivos', 0)}")
                logger.info(f"Sensores ativos: {kpis.get('total_sensores', 0)}")
                logger.info(f"Leituras (24h): {kpis.get('leituras_24h', 0)}")
                logger.info(f"Alertas ativos: {kpis.get('alertas_ativos', 0)}")
                logger.info(f"Dispositivos offline: {kpis.get('dispositivos_offline', 0)}")
                logger.info("=" * 40)
                
        except Exception as e:
            logger.error(f"Erro ao mostrar estatísticas: {e}")
    
    def _executar_testes(self):
        """Executa testes do sistema"""
        try:
            logger.info("Executando testes do sistema de dashboard")
            
            # Teste 1: Verificar banco de dados
            if 'persistencia' in self.sistemas:
                kpis = self.sistemas['persistencia'].obter_kpis_sistema()
                if kpis:
                    logger.info("✅ Teste do banco de dados: SUCESSO")
                else:
                    logger.error("❌ Teste do banco de dados: FALHA")
                    return False
            
            # Teste 2: Gerar relatório de teste
            if 'relatorios' in self.sistemas:
                caminho_relatorio = self.sistemas['relatorios'].gerar_relatorio_manual('diario')
                if caminho_relatorio and os.path.exists(caminho_relatorio):
                    logger.info(f"✅ Teste de relatórios: SUCESSO - {caminho_relatorio}")
                else:
                    logger.error("❌ Teste de relatórios: FALHA")
                    return False
            
            # Teste 3: Verificar template do dashboard
            template_path = "templates/dashboard.html"
            if os.path.exists(template_path):
                logger.info("✅ Teste do template: SUCESSO")
            else:
                logger.warning("⚠️ Template do dashboard não encontrado")
            
            logger.info("✅ Todos os testes executados com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro nos testes: {e}")
            return False
    
    def gerar_relatorio_manual(self, tipo: str) -> str:
        """Gera relatório manual"""
        try:
            if 'relatorios' not in self.sistemas:
                self.inicializar_sistemas()
            
            return self.sistemas['relatorios'].gerar_relatorio_manual(tipo)
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório manual: {e}")
            return None
    
    def mostrar_status_sistema(self):
        """Mostra status do sistema"""
        try:
            logger.info("=== STATUS DO SISTEMA ===")
            
            # Status do banco
            if 'persistencia' in self.sistemas:
                if self.sistemas['persistencia'].gerenciador.testar_conexao():
                    logger.info("✅ Banco de dados: ONLINE")
                else:
                    logger.error("❌ Banco de dados: OFFLINE")
            
            # Status do dashboard
            if 'dashboard' in self.sistemas:
                logger.info("✅ Dashboard: INICIADO")
            else:
                logger.info("❌ Dashboard: NÃO INICIADO")
            
            # Status dos relatórios
            if 'relatorios' in self.sistemas:
                logger.info("✅ Relatórios: INICIADO")
            else:
                logger.info("❌ Relatórios: NÃO INICIADO")
            
            # Diretórios
            diretorios = ['templates', 'relatorios', 'modelos']
            for diretorio in diretorios:
                if os.path.exists(diretorio):
                    logger.info(f"✅ Diretório {diretorio}: EXISTE")
                else:
                    logger.warning(f"⚠️ Diretório {diretorio}: NÃO EXISTE")
            
            logger.info("=" * 30)
            
        except Exception as e:
            logger.error(f"Erro ao mostrar status: {e}")

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Executador do Dashboard Completo')
    parser.add_argument('--config', default='config_pipeline.json', help='Arquivo de configuração')
    parser.add_argument('--modo', choices=['completo', 'dashboard_apenas', 'relatorios_apenas', 'teste', 'status'], 
                       default='completo', help='Modo de execução')
    parser.add_argument('--tipo-relatorio', choices=['diario', 'semanal', 'mensal'], 
                       help='Tipo de relatório para geração manual')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                       default='INFO', help='Nível de log')
    
    args = parser.parse_args()
    
    # Configura nível de log
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    # Inicializa executador
    executador = ExecutadorDashboardCompleto(args.config)
    
    try:
        if args.modo == 'teste':
            # Executa apenas testes
            sucesso = executador._executar_testes()
            sys.exit(0 if sucesso else 1)
            
        elif args.modo == 'status':
            # Mostra status do sistema
            executador.mostrar_status_sistema()
            
        elif args.tipo_relatorio:
            # Gera relatório manual
            caminho = executador.gerar_relatorio_manual(args.tipo_relatorio)
            if caminho:
                print(f"Relatório gerado: {caminho}")
            else:
                print("Erro ao gerar relatório")
                sys.exit(1)
            
        else:
            # Executa sistema completo
            executador.iniciar(args.modo)
            
            # Mantém execução
            while True:
                time.sleep(1)
    
    except KeyboardInterrupt:
        logger.info("Interrupção pelo usuário")
    except Exception as e:
        logger.error(f"Erro na execução: {e}")
        sys.exit(1)
    finally:
        executador.parar()

if __name__ == "__main__":
    main()
