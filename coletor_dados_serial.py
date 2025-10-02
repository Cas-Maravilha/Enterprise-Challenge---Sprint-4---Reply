#!/usr/bin/env python3
"""
Coletor de Dados Serial - Sistema IoT Monitoring
Enterprise Challenge Sprint 3 - Reply

Este script coleta dados do ESP32 via Serial/USB,
processa e armazena para posterior carga no banco.
"""

import serial
import json
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import re
import logging
from typing import Dict, List, Any
import warnings
warnings.filterwarnings('ignore')

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('coleta_serial.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ColetorDadosSerial:
    """Coletor de dados do ESP32 via Serial"""
    
    def __init__(self, porta='COM3', baudrate=115200):
        self.porta = porta
        self.baudrate = baudrate
        self.serial_conn = None
        self.dados_coletados = []
        self.timestamp_inicio = datetime.now()
        
        # Configurações
        self.num_leituras = 100  # Número de leituras para coleta
        self.intervalo_log = 10  # Intervalo para logs detalhados
        
        logger.info("=== Coletor de Dados Serial ESP32 ===")
        logger.info("Enterprise Challenge Sprint 3 - Reply")
        logger.info("=====================================")
    
    def conectar_serial(self):
        """Conecta ao ESP32 via Serial"""
        try:
            self.serial_conn = serial.Serial(
                port=self.porta,
                baudrate=self.baudrate,
                timeout=1,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
            
            # Aguardar inicialização
            time.sleep(2)
            
            logger.info(f"Conectado ao ESP32 na porta {self.porta}")
            logger.info(f"Baudrate: {self.baudrate}")
            logger.info("Aguardando dados...")
            
            return True
            
        except serial.SerialException as e:
            logger.error(f"Erro ao conectar serial: {e}")
            return False
    
    def ler_dados_serial(self):
        """Lê dados do ESP32 via Serial"""
        if not self.serial_conn or not self.serial_conn.is_open:
            logger.error("Conexão serial não estabelecida")
            return None
        
        try:
            # Ler linha do serial
            linha = self.serial_conn.readline().decode('utf-8').strip()
            
            if linha:
                logger.debug(f"Dados recebidos: {linha}")
                return linha
            
        except Exception as e:
            logger.error(f"Erro ao ler serial: {e}")
        
        return None
    
    def parsear_dados_serial(self, linha: str) -> Dict[str, Any]:
        """Parseia dados do formato do Monitor Serial"""
        try:
            # Padrão para linha de dados: | ID | Temp | Umid | Luz | Mov | Press |
            padrao = r'\|\s*(\d+)\s*\|\s*([\d.]+)\s*\|\s*([\d.]+)\s*\|\s*(\d+)\s*\|\s*(\w+)\s*\|\s*([\d.]+)\s*\|'
            match = re.match(padrao, linha)
            
            if match:
                return {
                    'id': int(match.group(1)),
                    'temperatura': float(match.group(2)),
                    'umidade': float(match.group(3)),
                    'luminosidade': int(match.group(4)),
                    'movimento': match.group(5) == 'SIM',
                    'pressao': float(match.group(6)),
                    'timestamp': datetime.now().isoformat()
                }
            
            # Tentar parsear JSON se disponível
            if linha.startswith('{'):
                dados_json = json.loads(linha)
                return {
                    'id': dados_json.get('reading_id', 0),
                    'temperatura': dados_json.get('sensores', {}).get('temperatura', 0.0),
                    'umidade': dados_json.get('sensores', {}).get('umidade', 0.0),
                    'luminosidade': dados_json.get('sensores', {}).get('luminosidade', 0),
                    'movimento': dados_json.get('sensores', {}).get('movimento', False),
                    'pressao': dados_json.get('sensores', {}).get('pressao', 0.0),
                    'timestamp': datetime.now().isoformat()
                }
            
        except Exception as e:
            logger.debug(f"Erro ao parsear dados: {e}")
        
        return None
    
    def coletar_dados(self):
        """Coleta dados do ESP32"""
        logger.info(f"Iniciando coleta de {self.num_leituras} leituras...")
        
        leituras_coletadas = 0
        leituras_validas = 0
        
        while leituras_coletadas < self.num_leituras:
            # Ler dados do serial
            linha = self.ler_dados_serial()
            
            if linha:
                leituras_coletadas += 1
                
                # Parsear dados
                dados = self.parsear_dados_serial(linha)
                
                if dados:
                    self.dados_coletados.append(dados)
                    leituras_validas += 1
                    
                    # Log detalhado a cada intervalo
                    if leituras_validas % self.intervalo_log == 0:
                        logger.info(f"Leitura #{leituras_validas}: "
                                  f"Temp={dados['temperatura']:.1f}°C, "
                                  f"Umid={dados['umidade']:.1f}%, "
                                  f"Luz={dados['luminosidade']}lux")
                
                # Log de progresso
                if leituras_coletadas % 20 == 0:
                    logger.info(f"Progresso: {leituras_coletadas}/{self.num_leituras} leituras")
            
            time.sleep(0.1)  # Pequena pausa
        
        logger.info(f"Coleta concluída: {leituras_validas}/{self.num_leituras} leituras válidas")
        return leituras_validas > 0
    
    def salvar_dados_csv(self, arquivo='dados_coletados.csv'):
        """Salva dados coletados em CSV"""
        if not self.dados_coletados:
            logger.warning("Nenhum dado para salvar")
            return False
        
        try:
            df = pd.DataFrame(self.dados_coletados)
            df.to_csv(arquivo, index=False)
            logger.info(f"Dados salvos em {arquivo}")
            logger.info(f"Total de registros: {len(df)}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar CSV: {e}")
            return False
    
    def salvar_dados_json(self, arquivo='dados_coletados.json'):
        """Salva dados coletados em JSON"""
        if not self.dados_coletados:
            logger.warning("Nenhum dado para salvar")
            return False
        
        try:
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.dados_coletados, f, indent=2, ensure_ascii=False)
            logger.info(f"Dados salvos em {arquivo}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar JSON: {e}")
            return False
    
    def gerar_graficos(self):
        """Gera gráficos das séries de dados coletados"""
        if not self.dados_coletados:
            logger.warning("Nenhum dado para gerar gráficos")
            return False
        
        try:
            df = pd.DataFrame(self.dados_coletados)
            
            # Configurar estilo
            plt.style.use('seaborn-v0_8')
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle('Séries de Dados Coletados - ESP32', fontsize=16, fontweight='bold')
            
            # Gráfico 1: Temperatura
            axes[0, 0].plot(df['id'], df['temperatura'], 'r-', linewidth=2, marker='o', markersize=4)
            axes[0, 0].set_title('Temperatura ao Longo do Tempo')
            axes[0, 0].set_xlabel('Leitura ID')
            axes[0, 0].set_ylabel('Temperatura (°C)')
            axes[0, 0].grid(True, alpha=0.3)
            
            # Gráfico 2: Umidade
            axes[0, 1].plot(df['id'], df['umidade'], 'b-', linewidth=2, marker='s', markersize=4)
            axes[0, 1].set_title('Umidade ao Longo do Tempo')
            axes[0, 1].set_xlabel('Leitura ID')
            axes[0, 1].set_ylabel('Umidade (%)')
            axes[0, 1].grid(True, alpha=0.3)
            
            # Gráfico 3: Luminosidade (Barras)
            axes[1, 0].bar(df['id'], df['luminosidade'], color='orange', alpha=0.7)
            axes[1, 0].set_title('Luminosidade por Leitura')
            axes[1, 0].set_xlabel('Leitura ID')
            axes[1, 0].set_ylabel('Luminosidade (lux)')
            axes[1, 0].grid(True, alpha=0.3)
            
            # Gráfico 4: Pressão
            axes[1, 1].plot(df['id'], df['pressao'], 'g-', linewidth=2, marker='^', markersize=4)
            axes[1, 1].set_title('Pressão ao Longo do Tempo')
            axes[1, 1].set_xlabel('Leitura ID')
            axes[1, 1].set_ylabel('Pressão (hPa)')
            axes[1, 1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('graficos_dados_coletados.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            logger.info("Gráficos gerados: graficos_dados_coletados.png")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráficos: {e}")
            return False
    
    def gerar_grafico_correlacao(self):
        """Gera gráfico de correlação entre variáveis"""
        if not self.dados_coletados:
            logger.warning("Nenhum dado para gerar gráfico de correlação")
            return False
        
        try:
            df = pd.DataFrame(self.dados_coletados)
            
            # Selecionar variáveis numéricas
            variaveis = ['temperatura', 'umidade', 'luminosidade', 'pressao']
            df_numeric = df[variaveis]
            
            # Calcular correlação
            correlacao = df_numeric.corr()
            
            # Criar heatmap
            plt.figure(figsize=(10, 8))
            plt.imshow(correlacao, cmap='coolwarm', aspect='auto')
            plt.colorbar(label='Correlação')
            
            # Configurar labels
            plt.xticks(range(len(variaveis)), variaveis, rotation=45)
            plt.yticks(range(len(variaveis)), variaveis)
            
            # Adicionar valores de correlação
            for i in range(len(variaveis)):
                for j in range(len(variaveis)):
                    plt.text(j, i, f'{correlacao.iloc[i, j]:.2f}',
                           ha='center', va='center', fontweight='bold')
            
            plt.title('Matriz de Correlação - Variáveis dos Sensores', fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.savefig('correlacao_sensores.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            logger.info("Gráfico de correlação gerado: correlacao_sensores.png")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de correlação: {e}")
            return False
    
    def gerar_relatorio(self):
        """Gera relatório das estatísticas dos dados"""
        if not self.dados_coletados:
            logger.warning("Nenhum dado para gerar relatório")
            return False
        
        try:
            df = pd.DataFrame(self.dados_coletados)
            
            logger.info("=== RELATÓRIO DE DADOS COLETADOS ===")
            logger.info(f"Total de leituras: {len(df)}")
            logger.info(f"Período de coleta: {self.timestamp_inicio.strftime('%H:%M:%S')} - {datetime.now().strftime('%H:%M:%S')}")
            logger.info(f"Duração: {(datetime.now() - self.timestamp_inicio).total_seconds():.1f} segundos")
            logger.info("")
            
            # Estatísticas por variável
            variaveis = ['temperatura', 'umidade', 'luminosidade', 'pressao']
            
            for var in variaveis:
                if var in df.columns:
                    logger.info(f"--- {var.upper()} ---")
                    logger.info(f"Média: {df[var].mean():.2f}")
                    logger.info(f"Desvio Padrão: {df[var].std():.2f}")
                    logger.info(f"Mínimo: {df[var].min():.2f}")
                    logger.info(f"Máximo: {df[var].max():.2f}")
                    logger.info("")
            
            # Contagem de movimentos
            if 'movimento' in df.columns:
                movimentos = df['movimento'].sum()
                logger.info(f"--- MOVIMENTO ---")
                logger.info(f"Detecções: {movimentos}")
                logger.info(f"Taxa: {movimentos/len(df)*100:.1f}%")
                logger.info("")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório: {e}")
            return False
    
    def fechar_conexao(self):
        """Fecha conexão serial"""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            logger.info("Conexão serial fechada")
    
    def executar_coleta_completa(self):
        """Executa coleta completa de dados"""
        try:
            # Conectar ao ESP32
            if not self.conectar_serial():
                return False
            
            # Coletar dados
            if not self.coletar_dados():
                return False
            
            # Salvar dados
            self.salvar_dados_csv()
            self.salvar_dados_json()
            
            # Gerar visualizações
            self.gerar_graficos()
            self.gerar_grafico_correlacao()
            
            # Gerar relatório
            self.gerar_relatorio()
            
            logger.info("Coleta completa executada com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"Erro na coleta completa: {e}")
            return False
        
        finally:
            self.fechar_conexao()


def main():
    """Função principal"""
    print("=== Coletor de Dados Serial ESP32 ===")
    print("Enterprise Challenge Sprint 3 - Reply")
    print("=====================================")
    
    # Configurar porta serial (ajustar conforme necessário)
    porta = input("Digite a porta serial (ex: COM3, /dev/ttyUSB0): ").strip()
    if not porta:
        porta = 'COM3'  # Porta padrão Windows
    
    # Criar coletor
    coletor = ColetorDadosSerial(porta=porta)
    
    # Executar coleta
    sucesso = coletor.executar_coleta_completa()
    
    if sucesso:
        print("\n✅ Coleta executada com sucesso!")
        print("📊 Verifique os arquivos gerados:")
        print("  - dados_coletados.csv")
        print("  - dados_coletados.json")
        print("  - graficos_dados_coletados.png")
        print("  - correlacao_sensores.png")
        print("  - coleta_serial.log")
    else:
        print("\n❌ Erro na execução da coleta.")


if __name__ == "__main__":
    main()
