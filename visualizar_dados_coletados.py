#!/usr/bin/env python3
"""
Visualizador de Dados Coletados - Sistema IoT Monitoring
Enterprise Challenge Sprint 3 - Reply

Este script visualiza dados coletados do ESP32,
gerando gráficos e análises das séries de dados.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import os
from datetime import datetime
import logging
from typing import Dict, List, Any
import warnings
warnings.filterwarnings('ignore')

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VisualizadorDadosColetados:
    """Visualizador de dados coletados do ESP32"""
    
    def __init__(self):
        self.dados = None
        self.arquivo_dados = None
        
        logger.info("=== Visualizador de Dados Coletados ===")
        logger.info("Enterprise Challenge Sprint 3 - Reply")
        logger.info("=====================================")
    
    def carregar_dados_csv(self, arquivo: str):
        """Carrega dados de arquivo CSV"""
        try:
            self.dados = pd.read_csv(arquivo)
            self.arquivo_dados = arquivo
            logger.info(f"Dados carregados de {arquivo}")
            logger.info(f"Total de registros: {len(self.dados)}")
            return True
        except Exception as e:
            logger.error(f"Erro ao carregar CSV: {e}")
            return False
    
    def carregar_dados_json(self, arquivo: str):
        """Carrega dados de arquivo JSON"""
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                dados_json = json.load(f)
            
            self.dados = pd.DataFrame(dados_json)
            self.arquivo_dados = arquivo
            logger.info(f"Dados carregados de {arquivo}")
            logger.info(f"Total de registros: {len(self.dados)}")
            return True
        except Exception as e:
            logger.error(f"Erro ao carregar JSON: {e}")
            return False
    
    def detectar_arquivo_dados(self):
        """Detecta automaticamente arquivo de dados"""
        arquivos_possiveis = [
            'dados_coletados.csv',
            'dados_simulados.csv',
            'dados_coletados.json',
            'dados_simulados.json'
        ]
        
        for arquivo in arquivos_possiveis:
            if os.path.exists(arquivo):
                logger.info(f"Arquivo detectado: {arquivo}")
                if arquivo.endswith('.csv'):
                    return self.carregar_dados_csv(arquivo)
                else:
                    return self.carregar_dados_json(arquivo)
        
        logger.warning("Nenhum arquivo de dados encontrado")
        return False
    
    def gerar_graficos_principais(self):
        """Gera gráficos principais das séries de dados"""
        if self.dados is None:
            logger.error("Nenhum dado carregado")
            return False
        
        try:
            # Configurar estilo
            plt.style.use('seaborn-v0_8')
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle('Análise de Dados Coletados - ESP32', fontsize=16, fontweight='bold')
            
            # Gráfico 1: Temperatura
            if 'temperatura' in self.dados.columns:
                axes[0, 0].plot(self.dados['id'], self.dados['temperatura'], 'r-', linewidth=2, marker='o', markersize=3)
                axes[0, 0].set_title('Temperatura ao Longo do Tempo')
                axes[0, 0].set_xlabel('Leitura ID')
                axes[0, 0].set_ylabel('Temperatura (°C)')
                axes[0, 0].grid(True, alpha=0.3)
                
                # Adicionar linha de tendência
                z = np.polyfit(self.dados['id'], self.dados['temperatura'], 1)
                p = np.poly1d(z)
                axes[0, 0].plot(self.dados['id'], p(self.dados['id']), "r--", alpha=0.8, linewidth=1)
            
            # Gráfico 2: Umidade
            if 'umidade' in self.dados.columns:
                axes[0, 1].plot(self.dados['id'], self.dados['umidade'], 'b-', linewidth=2, marker='s', markersize=3)
                axes[0, 1].set_title('Umidade ao Longo do Tempo')
                axes[0, 1].set_xlabel('Leitura ID')
                axes[0, 1].set_ylabel('Umidade (%)')
                axes[0, 1].grid(True, alpha=0.3)
                
                # Adicionar linha de tendência
                z = np.polyfit(self.dados['id'], self.dados['umidade'], 1)
                p = np.poly1d(z)
                axes[0, 1].plot(self.dados['id'], p(self.dados['id']), "b--", alpha=0.8, linewidth=1)
            
            # Gráfico 3: Luminosidade (Barras)
            if 'luminosidade' in self.dados.columns:
                axes[1, 0].bar(self.dados['id'], self.dados['luminosidade'], color='orange', alpha=0.7, width=0.8)
                axes[1, 0].set_title('Luminosidade por Leitura')
                axes[1, 0].set_xlabel('Leitura ID')
                axes[1, 0].set_ylabel('Luminosidade (lux)')
                axes[1, 0].grid(True, alpha=0.3)
            
            # Gráfico 4: Pressão
            if 'pressao' in self.dados.columns:
                axes[1, 1].plot(self.dados['id'], self.dados['pressao'], 'g-', linewidth=2, marker='^', markersize=3)
                axes[1, 1].set_title('Pressão ao Longo do Tempo')
                axes[1, 1].set_xlabel('Leitura ID')
                axes[1, 1].set_ylabel('Pressão (hPa)')
                axes[1, 1].grid(True, alpha=0.3)
                
                # Adicionar linha de tendência
                z = np.polyfit(self.dados['id'], self.dados['pressao'], 1)
                p = np.poly1d(z)
                axes[1, 1].plot(self.dados['id'], p(self.dados['id']), "g--", alpha=0.8, linewidth=1)
            
            plt.tight_layout()
            plt.savefig('analise_dados_coletados.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            logger.info("Gráficos principais gerados: analise_dados_coletados.png")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráficos principais: {e}")
            return False
    
    def gerar_grafico_distribuicao(self):
        """Gera gráficos de distribuição das variáveis"""
        if self.dados is None:
            logger.error("Nenhum dado carregado")
            return False
        
        try:
            # Selecionar variáveis numéricas
            variaveis_numericas = ['temperatura', 'umidade', 'luminosidade', 'pressao']
            variaveis_existentes = [var for var in variaveis_numericas if var in self.dados.columns]
            
            if not variaveis_existentes:
                logger.warning("Nenhuma variável numérica encontrada")
                return False
            
            # Configurar subplots
            n_vars = len(variaveis_existentes)
            n_cols = 2
            n_rows = (n_vars + 1) // 2
            
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 4 * n_rows))
            if n_rows == 1:
                axes = axes.reshape(1, -1)
            
            fig.suptitle('Distribuição das Variáveis Coletadas', fontsize=16, fontweight='bold')
            
            for i, var in enumerate(variaveis_existentes):
                row = i // n_cols
                col = i % n_cols
                
                # Histograma
                axes[row, col].hist(self.dados[var], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
                axes[row, col].set_title(f'Distribuição de {var.title()}')
                axes[row, col].set_xlabel(var.title())
                axes[row, col].set_ylabel('Frequência')
                axes[row, col].grid(True, alpha=0.3)
                
                # Adicionar estatísticas
                media = self.dados[var].mean()
                std = self.dados[var].std()
                axes[row, col].axvline(media, color='red', linestyle='--', linewidth=2, label=f'Média: {media:.2f}')
                axes[row, col].axvline(media + std, color='orange', linestyle='--', alpha=0.7, label=f'+1σ: {media + std:.2f}')
                axes[row, col].axvline(media - std, color='orange', linestyle='--', alpha=0.7, label=f'-1σ: {media - std:.2f}')
                axes[row, col].legend()
            
            # Ocultar subplots vazios
            for i in range(n_vars, n_rows * n_cols):
                row = i // n_cols
                col = i % n_cols
                axes[row, col].set_visible(False)
            
            plt.tight_layout()
            plt.savefig('distribuicao_dados_coletados.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            logger.info("Gráficos de distribuição gerados: distribuicao_dados_coletados.png")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráficos de distribuição: {e}")
            return False
    
    def gerar_grafico_correlacao(self):
        """Gera gráfico de correlação entre variáveis"""
        if self.dados is None:
            logger.error("Nenhum dado carregado")
            return False
        
        try:
            # Selecionar variáveis numéricas
            variaveis_numericas = ['temperatura', 'umidade', 'luminosidade', 'pressao', 
                                 'vibracao_x', 'vibracao_y', 'vibracao_z']
            variaveis_existentes = [var for var in variaveis_numericas if var in self.dados.columns]
            
            if len(variaveis_existentes) < 2:
                logger.warning("Poucas variáveis numéricas para correlação")
                return False
            
            # Calcular correlação
            df_numeric = self.dados[variaveis_existentes]
            correlacao = df_numeric.corr()
            
            # Criar heatmap
            plt.figure(figsize=(10, 8))
            plt.imshow(correlacao, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
            plt.colorbar(label='Correlação')
            
            # Configurar labels
            plt.xticks(range(len(variaveis_existentes)), variaveis_existentes, rotation=45)
            plt.yticks(range(len(variaveis_existentes)), variaveis_existentes)
            
            # Adicionar valores de correlação
            for i in range(len(variaveis_existentes)):
                for j in range(len(variaveis_existentes)):
                    plt.text(j, i, f'{correlacao.iloc[i, j]:.2f}',
                           ha='center', va='center', fontweight='bold')
            
            plt.title('Matriz de Correlação - Dados Coletados', fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.savefig('correlacao_dados_coletados.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            logger.info("Gráfico de correlação gerado: correlacao_dados_coletados.png")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de correlação: {e}")
            return False
    
    def gerar_grafico_tempo_real(self):
        """Gera gráfico simulando tempo real"""
        if self.dados is None:
            logger.error("Nenhum dado carregado")
            return False
        
        try:
            # Configurar animação
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle('Simulação de Dados em Tempo Real', fontsize=16, fontweight='bold')
            
            # Preparar dados
            n_dados = len(self.dados)
            x = np.arange(n_dados)
            
            # Gráfico 1: Temperatura
            if 'temperatura' in self.dados.columns:
                axes[0, 0].plot(x, self.dados['temperatura'], 'r-', linewidth=2)
                axes[0, 0].set_title('Temperatura')
                axes[0, 0].set_ylabel('°C')
                axes[0, 0].grid(True, alpha=0.3)
                
                # Adicionar linha de média móvel
                window = min(10, n_dados // 4)
                if window > 1:
                    temp_ma = self.dados['temperatura'].rolling(window=window).mean()
                    axes[0, 0].plot(x, temp_ma, 'r--', alpha=0.7, linewidth=1, label=f'Média Móvel ({window})')
                    axes[0, 0].legend()
            
            # Gráfico 2: Umidade
            if 'umidade' in self.dados.columns:
                axes[0, 1].plot(x, self.dados['umidade'], 'b-', linewidth=2)
                axes[0, 1].set_title('Umidade')
                axes[0, 1].set_ylabel('%')
                axes[0, 1].grid(True, alpha=0.3)
            
            # Gráfico 3: Luminosidade
            if 'luminosidade' in self.dados.columns:
                axes[1, 0].plot(x, self.dados['luminosidade'], 'orange', linewidth=2)
                axes[1, 0].set_title('Luminosidade')
                axes[1, 0].set_ylabel('lux')
                axes[1, 0].grid(True, alpha=0.3)
            
            # Gráfico 4: Pressão
            if 'pressao' in self.dados.columns:
                axes[1, 1].plot(x, self.dados['pressao'], 'g-', linewidth=2)
                axes[1, 1].set_title('Pressão')
                axes[1, 1].set_ylabel('hPa')
                axes[1, 1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('tempo_real_dados_coletados.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            logger.info("Gráfico de tempo real gerado: tempo_real_dados_coletados.png")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao gerar gráfico de tempo real: {e}")
            return False
    
    def gerar_relatorio_estatistico(self):
        """Gera relatório estatístico dos dados"""
        if self.dados is None:
            logger.error("Nenhum dado carregado")
            return False
        
        try:
            logger.info("=== RELATÓRIO ESTATÍSTICO ===")
            logger.info(f"Arquivo: {self.arquivo_dados}")
            logger.info(f"Total de registros: {len(self.dados)}")
            logger.info("")
            
            # Estatísticas gerais
            logger.info("--- ESTATÍSTICAS GERAIS ---")
            logger.info(f"Período de coleta: {len(self.dados)} leituras")
            if 'timestamp' in self.dados.columns:
                timestamps = pd.to_datetime(self.dados['timestamp'])
                duracao = (timestamps.max() - timestamps.min()).total_seconds()
                logger.info(f"Duração: {duracao:.1f} segundos")
                logger.info(f"Frequência média: {len(self.dados) / duracao:.2f} Hz")
            logger.info("")
            
            # Estatísticas por variável
            variaveis_numericas = ['temperatura', 'umidade', 'luminosidade', 'pressao', 
                                 'vibracao_x', 'vibracao_y', 'vibracao_z', 'bateria']
            
            for var in variaveis_numericas:
                if var in self.dados.columns:
                    logger.info(f"--- {var.upper()} ---")
                    logger.info(f"Média: {self.dados[var].mean():.2f}")
                    logger.info(f"Mediana: {self.dados[var].median():.2f}")
                    logger.info(f"Desvio Padrão: {self.dados[var].std():.2f}")
                    logger.info(f"Mínimo: {self.dados[var].min():.2f}")
                    logger.info(f"Máximo: {self.dados[var].max():.2f}")
                    logger.info(f"Amplitude: {self.dados[var].max() - self.dados[var].min():.2f}")
                    logger.info("")
            
            # Análise de movimento
            if 'movimento' in self.dados.columns:
                movimentos = self.dados['movimento'].sum()
                logger.info("--- MOVIMENTO ---")
                logger.info(f"Detecções: {movimentos}")
                logger.info(f"Taxa: {movimentos/len(self.dados)*100:.1f}%")
                logger.info("")
            
            # Análise de qualidade
            if 'qualidade' in self.dados.columns:
                logger.info("--- QUALIDADE ---")
                logger.info(f"Média: {self.dados['qualidade'].mean():.3f}")
                logger.info(f"Mínima: {self.dados['qualidade'].min():.3f}")
                logger.info(f"Máxima: {self.dados['qualidade'].max():.3f}")
                logger.info("")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório estatístico: {e}")
            return False
    
    def executar_visualizacao_completa(self):
        """Executa visualização completa dos dados"""
        try:
            # Carregar dados
            if not self.detectar_arquivo_dados():
                logger.error("Não foi possível carregar dados")
                return False
            
            # Gerar visualizações
            self.gerar_graficos_principais()
            self.gerar_grafico_distribuicao()
            self.gerar_grafico_correlacao()
            self.gerar_grafico_tempo_real()
            
            # Gerar relatório
            self.gerar_relatorio_estatistico()
            
            logger.info("Visualização completa executada com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"Erro na visualização completa: {e}")
            return False


def main():
    """Função principal"""
    print("=== Visualizador de Dados Coletados ===")
    print("Enterprise Challenge Sprint 3 - Reply")
    print("======================================")
    
    # Criar visualizador
    visualizador = VisualizadorDadosColetados()
    
    # Executar visualização
    sucesso = visualizador.executar_visualizacao_completa()
    
    if sucesso:
        print("\n✅ Visualização executada com sucesso!")
        print("📊 Verifique os arquivos gerados:")
        print("  - analise_dados_coletados.png")
        print("  - distribuicao_dados_coletados.png")
        print("  - correlacao_dados_coletados.png")
        print("  - tempo_real_dados_coletados.png")
    else:
        print("\n❌ Erro na execução da visualização.")


if __name__ == "__main__":
    main()
