#!/usr/bin/env python3
"""
Visualizador de Dados - Sistema IoT Monitoring
Enterprise Challenge Sprint 3 - Reply

Este script gera gráficos simples dos dados coletados
ou simulados para demonstração do sistema.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import numpy as np
from datetime import datetime
import argparse
import sys
import os

class VisualizadorDados:
    """Visualizador de dados IoT"""
    
    def __init__(self):
        # Configurar estilo dos gráficos
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Configurações de figura
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12
        
        print("=== Visualizador de Dados IoT ===")
        print("Enterprise Challenge Sprint 3 - Reply")
        print("==================================")
    
    def carregar_dados_csv(self, arquivo: str) -> pd.DataFrame:
        """Carrega dados de arquivo CSV"""
        try:
            df = pd.read_csv(arquivo)
            print(f"✓ Dados carregados de: {arquivo}")
            print(f"  Total de registros: {len(df)}")
            return df
        except Exception as e:
            print(f"✗ Erro ao carregar CSV: {e}")
            return None
    
    def carregar_dados_json(self, arquivo: str) -> pd.DataFrame:
        """Carrega dados de arquivo JSON"""
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            # Converter para DataFrame
            df_data = []
            for item in dados:
                row = {
                    'timestamp': item.get('timestamp', ''),
                    'device': item.get('device', ''),
                    'quality': item.get('quality', ''),
                    'read_count': item.get('read_count', 0),
                    'processed_at': item.get('processed_at', '')
                }
                
                # Extrair dados dos sensores
                sensores = item.get('sensors', {})
                if 'DHT22' in sensores:
                    row['temperature'] = sensores['DHT22'].get('temperature', np.nan)
                    row['humidity'] = sensores['DHT22'].get('humidity', np.nan)
                if 'LDR' in sensores:
                    row['light'] = sensores['LDR'].get('light', np.nan)
                if 'PIR' in sensores:
                    row['motion'] = sensores['PIR'].get('motion', np.nan)
                if 'BME280' in sensores:
                    row['pressure'] = sensores['BME280'].get('pressure', np.nan)
                
                df_data.append(row)
            
            df = pd.DataFrame(df_data)
            print(f"✓ Dados carregados de: {arquivo}")
            print(f"  Total de registros: {len(df)}")
            return df
        except Exception as e:
            print(f"✗ Erro ao carregar JSON: {e}")
            return None
    
    def preparar_dados_temporais(self, df: pd.DataFrame) -> pd.DataFrame:
        """Prepara dados para visualização temporal"""
        if df.empty:
            return df
        
        # Converter timestamp para datetime
        if 'timestamp' in df.columns:
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms', errors='coerce')
        elif 'processed_at' in df.columns:
            df['datetime'] = pd.to_datetime(df['processed_at'], errors='coerce')
        else:
            df['datetime'] = pd.date_range(start='2024-01-11', periods=len(df), freq='1S')
        
        # Criar índice temporal
        df = df.set_index('datetime')
        
        # Remover valores NaN para gráficos
        df_clean = df.dropna(subset=['temperature', 'humidity', 'light', 'pressure'])
        
        return df_clean
    
    def gerar_grafico_temperatura(self, df: pd.DataFrame, arquivo_saida: str = 'ingest/graficos/temperatura_tempo.png'):
        """Gera gráfico de temperatura ao longo do tempo"""
        if df.empty or 'temperature' not in df.columns:
            print("✗ Dados de temperatura não disponíveis")
            return False
        
        plt.figure(figsize=(14, 6))
        
        # Gráfico de linha
        plt.subplot(1, 2, 1)
        plt.plot(df.index, df['temperature'], 'b-', linewidth=2, alpha=0.7)
        plt.title('Temperatura ao Longo do Tempo', fontsize=16, fontweight='bold')
        plt.xlabel('Tempo')
        plt.ylabel('Temperatura (°C)')
        plt.grid(True, alpha=0.3)
        
        # Adicionar linha de média
        media_temp = df['temperature'].mean()
        plt.axhline(y=media_temp, color='r', linestyle='--', alpha=0.7, 
                   label=f'Média: {media_temp:.1f}°C')
        plt.legend()
        
        # Histograma
        plt.subplot(1, 2, 2)
        plt.hist(df['temperature'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        plt.title('Distribuição da Temperatura', fontsize=16, fontweight='bold')
        plt.xlabel('Temperatura (°C)')
        plt.ylabel('Frequência')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(arquivo_saida, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Gráfico de temperatura salvo: {arquivo_saida}")
        return True
    
    def gerar_grafico_umidade(self, df: pd.DataFrame, arquivo_saida: str = 'ingest/graficos/umidade_tempo.png'):
        """Gera gráfico de umidade ao longo do tempo"""
        if df.empty or 'humidity' not in df.columns:
            print("✗ Dados de umidade não disponíveis")
            return False
        
        plt.figure(figsize=(14, 6))
        
        # Gráfico de linha
        plt.subplot(1, 2, 1)
        plt.plot(df.index, df['humidity'], 'g-', linewidth=2, alpha=0.7)
        plt.title('Umidade ao Longo do Tempo', fontsize=16, fontweight='bold')
        plt.xlabel('Tempo')
        plt.ylabel('Umidade (%)')
        plt.grid(True, alpha=0.3)
        
        # Adicionar linha de média
        media_umid = df['humidity'].mean()
        plt.axhline(y=media_umid, color='r', linestyle='--', alpha=0.7, 
                   label=f'Média: {media_umid:.1f}%')
        plt.legend()
        
        # Histograma
        plt.subplot(1, 2, 2)
        plt.hist(df['humidity'], bins=20, alpha=0.7, color='lightgreen', edgecolor='black')
        plt.title('Distribuição da Umidade', fontsize=16, fontweight='bold')
        plt.xlabel('Umidade (%)')
        plt.ylabel('Frequência')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(arquivo_saida, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Gráfico de umidade salvo: {arquivo_saida}")
        return True
    
    def gerar_grafico_luminosidade(self, df: pd.DataFrame, arquivo_saida: str = 'ingest/graficos/luminosidade_tempo.png'):
        """Gera gráfico de luminosidade ao longo do tempo"""
        if df.empty or 'light' not in df.columns:
            print("✗ Dados de luminosidade não disponíveis")
            return False
        
        plt.figure(figsize=(14, 6))
        
        # Gráfico de linha
        plt.subplot(1, 2, 1)
        plt.plot(df.index, df['light'], 'orange', linewidth=2, alpha=0.7)
        plt.title('Luminosidade ao Longo do Tempo', fontsize=16, fontweight='bold')
        plt.xlabel('Tempo')
        plt.ylabel('Luminosidade (lux)')
        plt.grid(True, alpha=0.3)
        
        # Adicionar linha de média
        media_luz = df['light'].mean()
        plt.axhline(y=media_luz, color='r', linestyle='--', alpha=0.7, 
                   label=f'Média: {media_luz:.0f} lux')
        plt.legend()
        
        # Histograma
        plt.subplot(1, 2, 2)
        plt.hist(df['light'], bins=20, alpha=0.7, color='gold', edgecolor='black')
        plt.title('Distribuição da Luminosidade', fontsize=16, fontweight='bold')
        plt.xlabel('Luminosidade (lux)')
        plt.ylabel('Frequência')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(arquivo_saida, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Gráfico de luminosidade salvo: {arquivo_saida}")
        return True
    
    def gerar_grafico_correlacao(self, df: pd.DataFrame, arquivo_saida: str = 'ingest/graficos/correlacao_sensores.png'):
        """Gera gráfico de correlação entre sensores"""
        if df.empty:
            print("✗ Dados não disponíveis para correlação")
            return False
        
        # Selecionar colunas numéricas
        colunas_numericas = ['temperature', 'humidity', 'light', 'pressure']
        df_corr = df[colunas_numericas].dropna()
        
        if df_corr.empty:
            print("✗ Dados numéricos insuficientes para correlação")
            return False
        
        plt.figure(figsize=(12, 8))
        
        # Matriz de correlação
        corr_matrix = df_corr.corr()
        
        # Heatmap
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                   square=True, fmt='.2f', cbar_kws={'shrink': 0.8})
        plt.title('Correlação entre Sensores', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        plt.savefig(arquivo_saida, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Gráfico de correlação salvo: {arquivo_saida}")
        return True
    
    def gerar_grafico_combinado(self, df: pd.DataFrame, arquivo_saida: str = 'ingest/graficos/dados_combinados.png'):
        """Gera gráfico combinado com todos os sensores"""
        if df.empty:
            print("✗ Dados não disponíveis")
            return False
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Dados dos Sensores IoT - Sistema de Monitoramento', fontsize=18, fontweight='bold')
        
        # Temperatura
        if 'temperature' in df.columns:
            axes[0, 0].plot(df.index, df['temperature'], 'b-', linewidth=2, alpha=0.7)
            axes[0, 0].set_title('Temperatura', fontsize=14, fontweight='bold')
            axes[0, 0].set_ylabel('Temperatura (°C)')
            axes[0, 0].grid(True, alpha=0.3)
            axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Umidade
        if 'humidity' in df.columns:
            axes[0, 1].plot(df.index, df['humidity'], 'g-', linewidth=2, alpha=0.7)
            axes[0, 1].set_title('Umidade', fontsize=14, fontweight='bold')
            axes[0, 1].set_ylabel('Umidade (%)')
            axes[0, 1].grid(True, alpha=0.3)
            axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Luminosidade
        if 'light' in df.columns:
            axes[1, 0].plot(df.index, df['light'], 'orange', linewidth=2, alpha=0.7)
            axes[1, 0].set_title('Luminosidade', fontsize=14, fontweight='bold')
            axes[1, 0].set_ylabel('Luminosidade (lux)')
            axes[1, 0].grid(True, alpha=0.3)
            axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Pressão
        if 'pressure' in df.columns:
            axes[1, 1].plot(df.index, df['pressure'], 'purple', linewidth=2, alpha=0.7)
            axes[1, 1].set_title('Pressão Atmosférica', fontsize=14, fontweight='bold')
            axes[1, 1].set_ylabel('Pressão (hPa)')
            axes[1, 1].grid(True, alpha=0.3)
            axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(arquivo_saida, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✓ Gráfico combinado salvo: {arquivo_saida}")
        return True
    
    def gerar_todos_graficos(self, df: pd.DataFrame):
        """Gera todos os gráficos disponíveis"""
        print("\n🎨 Gerando gráficos...")
        
        # Criar diretório de gráficos se não existir
        os.makedirs('ingest/graficos', exist_ok=True)
        
        graficos_gerados = 0
        
        # Gráficos individuais
        if self.gerar_grafico_temperatura(df):
            graficos_gerados += 1
        
        if self.gerar_grafico_umidade(df):
            graficos_gerados += 1
        
        if self.gerar_grafico_luminosidade(df):
            graficos_gerados += 1
        
        if self.gerar_grafico_correlacao(df):
            graficos_gerados += 1
        
        if self.gerar_grafico_combinado(df):
            graficos_gerados += 1
        
        print(f"\n✅ Total de gráficos gerados: {graficos_gerados}")
        return graficos_gerados > 0

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Visualizador de Dados IoT - Sistema IoT Monitoring')
    parser.add_argument('--arquivo', default='ingest/dados/dados_simulados.csv', 
                       help='Arquivo de dados (CSV ou JSON)')
    parser.add_argument('--formato', choices=['csv', 'json'], default='csv',
                       help='Formato do arquivo de dados')
    
    args = parser.parse_args()
    
    # Criar visualizador
    visualizador = VisualizadorDados()
    
    # Carregar dados
    if args.formato == 'csv':
        df = visualizador.carregar_dados_csv(args.arquivo)
    else:
        df = visualizador.carregar_dados_json(args.arquivo)
    
    if df is None or df.empty:
        print("❌ Não foi possível carregar os dados.")
        sys.exit(1)
    
    # Preparar dados temporais
    df_temporal = visualizador.preparar_dados_temporais(df)
    
    # Gerar gráficos
    sucesso = visualizador.gerar_todos_graficos(df_temporal)
    
    if sucesso:
        print("\n🎉 Visualização de dados concluída com sucesso!")
        print("📁 Gráficos salvos em: ingest/graficos/")
        print("  - temperatura_tempo.png")
        print("  - umidade_tempo.png")
        print("  - luminosidade_tempo.png")
        print("  - correlacao_sensores.png")
        print("  - dados_combinados.png")
    else:
        print("\n❌ Falha na geração de gráficos.")
        sys.exit(1)

if __name__ == "__main__":
    main()
