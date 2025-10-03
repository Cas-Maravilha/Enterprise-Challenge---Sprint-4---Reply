#!/usr/bin/env python3
"""
Simulador de Dados ESP32 - Sistema IoT Monitoring
Enterprise Challenge Sprint 3 - Reply

Este script simula dados do ESP32 quando o hardware não está disponível,
gerando dados realísticos para testes e demonstração.
"""

import json
import time
import random
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Any
import warnings
warnings.filterwarnings('ignore')

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('simulador_dados.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SimuladorDadosESP32:
    """Simulador de dados do ESP32"""
    
    def __init__(self):
        self.dados_simulados = []
        self.timestamp_inicio = datetime.now()
        
        # Configurações da simulação
        self.num_leituras = 100
        self.intervalo_leituras = 1.0  # segundos
        self.device_id = "ESP32_001"
        
        # Parâmetros para simulação realística
        self.parametros = {
            'temperatura': {'base': 23.0, 'variacao': 5.0, 'tendencia': 0.1},
            'umidade': {'base': 60.0, 'variacao': 15.0, 'tendencia': -0.05},
            'luminosidade': {'base': 500, 'variacao': 300, 'tendencia': 2.0},
            'pressao': {'base': 1013.25, 'variacao': 10.0, 'tendencia': 0.0},
            'vibracao_x': {'base': 0.0, 'variacao': 1.0, 'tendencia': 0.0},
            'vibracao_y': {'base': 0.0, 'variacao': 1.0, 'tendencia': 0.0},
            'vibracao_z': {'base': 0.0, 'variacao': 1.0, 'tendencia': 0.0}
        }
        
        logger.info("=== Simulador de Dados ESP32 ===")
        logger.info("Enterprise Challenge Sprint 3 - Reply")
        logger.info("=================================")
    
    def gerar_dados_sensor(self, leitura_id: int) -> Dict[str, Any]:
        """Gera dados simulados para um sensor"""
        timestamp = datetime.now()
        
        # Gerar dados baseados nos parâmetros
        dados = {
            'id': leitura_id,
            'device_id': self.device_id,
            'timestamp': timestamp.isoformat(),
            'timestamp_unix': int(timestamp.timestamp())
        }
        
        # Simular cada sensor
        for sensor, params in self.parametros.items():
            # Calcular valor base com tendência temporal
            valor_base = params['base'] + (leitura_id * params['tendencia'])
            
            # Adicionar variação aleatória
            variacao = random.gauss(0, params['variacao'] * 0.1)
            
            # Adicionar ruído cíclico (simular variações do ambiente)
            ciclo = np.sin(leitura_id * 0.1) * params['variacao'] * 0.2
            
            # Calcular valor final
            valor = valor_base + variacao + ciclo
            
            # Aplicar limites realísticos
            if sensor == 'temperatura':
                valor = max(15.0, min(35.0, valor))
            elif sensor == 'umidade':
                valor = max(20.0, min(90.0, valor))
            elif sensor == 'luminosidade':
                valor = max(0, min(1000, int(valor)))
            elif sensor == 'pressao':
                valor = max(990.0, min(1030.0, valor))
            elif sensor.startswith('vibracao'):
                valor = max(-2.0, min(2.0, valor))
            
            dados[sensor] = round(valor, 2) if sensor != 'luminosidade' else int(valor)
        
        # Simular movimento (PIR)
        dados['movimento'] = random.random() < 0.1  # 10% de chance de movimento
        
        # Simular bateria
        dados['bateria'] = max(20.0, 100.0 - (leitura_id * 0.1) + random.gauss(0, 5))
        
        # Simular qualidade do sinal
        dados['rssi'] = -30 - random.randint(0, 70)
        
        # Simular qualidade da leitura
        dados['qualidade'] = random.uniform(0.8, 1.0)
        
        return dados
    
    def simular_coleta(self):
        """Simula coleta de dados do ESP32"""
        logger.info(f"Iniciando simulação de {self.num_leituras} leituras...")
        logger.info(f"Intervalo entre leituras: {self.intervalo_leituras}s")
        logger.info("")
        
        # Cabeçalho do Monitor Serial
        self.imprimir_cabecalho()
        
        for i in range(1, self.num_leituras + 1):
            # Gerar dados
            dados = self.gerar_dados_sensor(i)
            self.dados_simulados.append(dados)
            
            # Imprimir no formato do Monitor Serial
            self.imprimir_dados_serial(dados)
            
            # Log detalhado a cada 10 leituras
            if i % 10 == 0:
                self.imprimir_log_detalhado(dados)
            
            # Simular intervalo entre leituras
            time.sleep(self.intervalo_leituras)
        
        logger.info("")
        logger.info("Simulação concluída!")
        logger.info(f"Total de leituras: {len(self.dados_simulados)}")
    
    def imprimir_cabecalho(self):
        """Imprime cabeçalho do Monitor Serial"""
        print("==========================================")
        print("| ID | Temp | Umid | Luz | Mov | Press |")
        print("|----|------|------|-----|-----|-------|")
    
    def imprimir_dados_serial(self, dados: Dict[str, Any]):
        """Imprime dados no formato do Monitor Serial"""
        print(f"|{dados['id']:3d} |{dados['temperatura']:5.1f} |{dados['umidade']:5.1f} |"
              f"{dados['luminosidade']:4d} |{('SIM' if dados['movimento'] else 'NÃO'):3s} |"
              f"{dados['pressao']:6.1f} |")
    
    def imprimir_log_detalhado(self, dados: Dict[str, Any]):
        """Imprime log detalhado"""
        print("------------------------------------------")
        print(f"Leitura #{dados['id']} - Timestamp: {dados['timestamp']}")
        print(f"Temperatura: {dados['temperatura']:.1f}°C")
        print(f"Umidade: {dados['umidade']:.1f}%")
        print(f"Luminosidade: {dados['luminosidade']} lux")
        print(f"Movimento: {'Detectado' if dados['movimento'] else 'Não detectado'}")
        print(f"Pressão: {dados['pressao']:.1f} hPa")
        print(f"Vibração X: {dados['vibracao_x']:.2f}, Y: {dados['vibracao_y']:.2f}, Z: {dados['vibracao_z']:.2f}")
        print(f"Bateria: {dados['bateria']:.0f}%")
        print(f"RSSI: {dados['rssi']} dBm")
        print(f"Qualidade: {dados['qualidade']:.2f}")
        print("==========================================")
    
    def salvar_dados_csv(self, arquivo='dados_simulados.csv'):
        """Salva dados simulados em CSV"""
        try:
            df = pd.DataFrame(self.dados_simulados)
            df.to_csv(arquivo, index=False)
            logger.info(f"Dados salvos em {arquivo}")
            logger.info(f"Total de registros: {len(df)}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar CSV: {e}")
            return False
    
    def salvar_dados_json(self, arquivo='dados_simulados.json'):
        """Salva dados simulados em JSON"""
        try:
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.dados_simulados, f, indent=2, ensure_ascii=False)
            logger.info(f"Dados salvos em {arquivo}")
            return True
        except Exception as e:
            logger.error(f"Erro ao salvar JSON: {e}")
            return False
    
    def gerar_graficos_series(self):
        """Gera gráficos das séries de dados simulados"""
        if not self.dados_simulados:
            logger.warning("Nenhum dado para gerar gráficos")
            return False
        
        try:
            df = pd.DataFrame(self.dados_simulados)
            
            # Configurar estilo
            plt.style.use('seaborn-v0_8')
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle('Séries de Dados Simulados - ESP32', fontsize=16, fontweight='bold')
            
            # Gráfico 1: Temperatura
            axes[0, 0].plot(df['id'], df['temperatura'], 'r-', linewidth=2, marker='o', markersize=4)
            axes[0, 0].set_title('Temperatura Simulada')
            axes[0, 0].set_xlabel('Leitura ID')
            axes[0, 0].set_ylabel('Temperatura (°C)')
            axes[0, 0].grid(True, alpha=0.3)
            
            # Gráfico 2: Umidade
            axes[0, 1].plot(df['id'], df['umidade'], 'b-', linewidth=2, marker='s', markersize=4)
            axes[0, 1].set_title('Umidade Simulada')
            axes[0, 1].set_xlabel('Leitura ID')
            axes[0, 1].set_ylabel('Umidade (%)')
            axes[0, 1].grid(True, alpha=0.3)
            
            # Gráfico 3: Luminosidade (Barras)
            axes[1, 0].bar(df['id'], df['luminosidade'], color='orange', alpha=0.7)
            axes[1, 0].set_title('Luminosidade Simulada')
            axes[1, 0].set_xlabel('Leitura ID')
            axes[1, 0].set_ylabel('Luminosidade (lux)')
            axes[1, 0].grid(True, alpha=0.3)
            
            # Gráfico 4: Pressão
            axes[1, 1].plot(df['id'], df['pressao'], 'g-', linewidth=2, marker='^', markersize=4)
            axes[1, 1].set_title('Pressão Simulada')
            axes[1, 1].set_xlabel('Leitura ID')
            axes[1, 1].set_ylabel('Pressão (hPa)')
            axes[1, 1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('graficos_dados_simulados.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            logger.info("Gráficos gerados: graficos_dados_simulados.png")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráficos: {e}")
            return False
    
    def gerar_grafico_vibracao(self):
        """Gera gráfico 3D da vibração simulada"""
        if not self.dados_simulados:
            logger.warning("Nenhum dado para gerar gráfico de vibração")
            return False
        
        try:
            df = pd.DataFrame(self.dados_simulados)
            
            # Criar gráfico 3D
            fig = plt.figure(figsize=(12, 8))
            ax = fig.add_subplot(111, projection='3d')
            
            # Plotar vibração em 3D
            ax.scatter(df['vibracao_x'], df['vibracao_y'], df['vibracao_z'], 
                      c=df['id'], cmap='viridis', s=50, alpha=0.7)
            
            ax.set_xlabel('Vibração X')
            ax.set_ylabel('Vibração Y')
            ax.set_zlabel('Vibração Z')
            ax.set_title('Simulação de Vibração Triaxial')
            
            # Adicionar barra de cores
            cbar = plt.colorbar(ax.scatter(df['vibracao_x'], df['vibracao_y'], df['vibracao_z'], 
                                          c=df['id'], cmap='viridis', s=50, alpha=0.7))
            cbar.set_label('Leitura ID')
            
            plt.savefig('vibracao_3d_simulada.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            logger.info("Gráfico 3D de vibração gerado: vibracao_3d_simulada.png")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de vibração: {e}")
            return False
    
    def gerar_grafico_correlacao(self):
        """Gera gráfico de correlação entre variáveis"""
        if not self.dados_simulados:
            logger.warning("Nenhum dado para gerar gráfico de correlação")
            return False
        
        try:
            df = pd.DataFrame(self.dados_simulados)
            
            # Selecionar variáveis numéricas
            variaveis = ['temperatura', 'umidade', 'luminosidade', 'pressao', 
                        'vibracao_x', 'vibracao_y', 'vibracao_z']
            df_numeric = df[variaveis]
            
            # Calcular correlação
            correlacao = df_numeric.corr()
            
            # Criar heatmap
            plt.figure(figsize=(10, 8))
            plt.imshow(correlacao, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
            plt.colorbar(label='Correlação')
            
            # Configurar labels
            plt.xticks(range(len(variaveis)), variaveis, rotation=45)
            plt.yticks(range(len(variaveis)), variaveis)
            
            # Adicionar valores de correlação
            for i in range(len(variaveis)):
                for j in range(len(variaveis)):
                    plt.text(j, i, f'{correlacao.iloc[i, j]:.2f}',
                           ha='center', va='center', fontweight='bold')
            
            plt.title('Matriz de Correlação - Dados Simulados', fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.savefig('correlacao_dados_simulados.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            logger.info("Gráfico de correlação gerado: correlacao_dados_simulados.png")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de correlação: {e}")
            return False
    
    def gerar_relatorio(self):
        """Gera relatório das estatísticas dos dados simulados"""
        if not self.dados_simulados:
            logger.warning("Nenhum dado para gerar relatório")
            return False
        
        try:
            df = pd.DataFrame(self.dados_simulados)
            
            logger.info("=== RELATÓRIO DE DADOS SIMULADOS ===")
            logger.info(f"Total de leituras: {len(df)}")
            logger.info(f"Período de simulação: {self.timestamp_inicio.strftime('%H:%M:%S')} - {datetime.now().strftime('%H:%M:%S')}")
            logger.info(f"Duração: {(datetime.now() - self.timestamp_inicio).total_seconds():.1f} segundos")
            logger.info("")
            
            # Estatísticas por variável
            variaveis = ['temperatura', 'umidade', 'luminosidade', 'pressao', 
                        'vibracao_x', 'vibracao_y', 'vibracao_z']
            
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
            
            # Estatísticas de bateria
            if 'bateria' in df.columns:
                logger.info(f"--- BATERIA ---")
                logger.info(f"Média: {df['bateria'].mean():.1f}%")
                logger.info(f"Mínimo: {df['bateria'].min():.1f}%")
                logger.info(f"Máximo: {df['bateria'].max():.1f}%")
                logger.info("")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório: {e}")
            return False
    
    def executar_simulacao_completa(self):
        """Executa simulação completa de dados"""
        try:
            # Simular coleta
            self.simular_coleta()
            
            # Salvar dados
            self.salvar_dados_csv()
            self.salvar_dados_json()
            
            # Gerar visualizações
            self.gerar_graficos_series()
            self.gerar_grafico_vibracao()
            self.gerar_grafico_correlacao()
            
            # Gerar relatório
            self.gerar_relatorio()
            
            logger.info("Simulação completa executada com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"Erro na simulação completa: {e}")
            return False


def main():
    """Função principal"""
    print("=== Simulador de Dados ESP32 ===")
    print("Enterprise Challenge Sprint 3 - Reply")
    print("===================================")
    
    # Configurar parâmetros da simulação
    num_leituras = input("Número de leituras (padrão: 100): ").strip()
    if num_leituras:
        try:
            num_leituras = int(num_leituras)
        except ValueError:
            num_leituras = 100
    else:
        num_leituras = 100
    
    # Criar simulador
    simulador = SimuladorDadosESP32()
    simulador.num_leituras = num_leituras
    
    # Executar simulação
    sucesso = simulador.executar_simulacao_completa()
    
    if sucesso:
        print("\n✅ Simulação executada com sucesso!")
        print("📊 Verifique os arquivos gerados:")
        print("  - dados_simulados.csv")
        print("  - dados_simulados.json")
        print("  - graficos_dados_simulados.png")
        print("  - vibracao_3d_simulada.png")
        print("  - correlacao_dados_simulados.png")
        print("  - simulador_dados.log")
    else:
        print("\n❌ Erro na execução da simulação.")


if __name__ == "__main__":
    main()
