#!/usr/bin/env python3
"""
Analisador de Dataset ML - Sistema IoT Monitoring
Enterprise Challenge Sprint 3 - Reply

Este script analisa o dataset utilizado no ML e gera
relatórios detalhados sobre os dados.
"""

import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import logging
from typing import Dict, List, Any
import warnings
warnings.filterwarnings('ignore')

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dataset_ml_analisador.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DatasetMLAnalisador:
    """Analisador de dataset para ML"""
    
    def __init__(self, host='localhost', user='root', password='', database='iot_monitoring_db'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self.df_completo = None
        
        logger.info("=== Analisador de Dataset ML ===")
        logger.info("Enterprise Challenge Sprint 3 - Reply")
        logger.info("=================================")
    
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
    
    def carregar_dataset_completo(self):
        """Carrega dataset completo para análise"""
        logger.info("📊 Carregando dataset completo...")
        
        query = """
        SELECT 
            l.id_leitura,
            l.id_sensor,
            l.timestamp_datetime,
            l.timestamp_unix,
            l.valor_numerico,
            l.valor_booleano,
            l.valor_string,
            l.qualidade_dados,
            l.anomalia_detectada,
            l.data_coleta,
            s.nome as sensor_nome,
            s.id_tipo_sensor,
            s.pino_analogico,
            s.pino_digital,
            s.calibracao_min,
            s.calibracao_max,
            s.status as sensor_status,
            s.data_instalacao,
            s.ultima_calibracao,
            d.id_dispositivo,
            d.nome as dispositivo_nome,
            d.mac_address,
            d.ip_address,
            d.localizacao,
            d.status as dispositivo_status,
            d.data_cadastro,
            d.ultima_conexao,
            d.versao_firmware,
            ts.nome as tipo_sensor_nome,
            ts.descricao as tipo_sensor_descricao,
            ts.unidade_medida,
            ts.faixa_min,
            ts.faixa_max,
            ts.precisao
        FROM leituras_sensores l
        JOIN sensores s ON l.id_sensor = s.id_sensor
        JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
        JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
        ORDER BY l.timestamp_datetime DESC
        """
        
        self.df_completo = self.executar_consulta(query)
        
        if self.df_completo.empty:
            logger.error("Nenhum dado encontrado no banco")
            return False
        
        logger.info(f"Dataset carregado: {len(self.df_completo)} registros")
        return True
    
    def analisar_estrutura_dataset(self):
        """Analisa a estrutura do dataset"""
        logger.info("🔍 Analisando estrutura do dataset...")
        
        estrutura = {
            'dimensoes': {
                'linhas': len(self.df_completo),
                'colunas': len(self.df_completo.columns)
            },
            'tipos_dados': self.df_completo.dtypes.to_dict(),
            'valores_nulos': self.df_completo.isnull().sum().to_dict(),
            'valores_unicos': self.df_completo.nunique().to_dict(),
            'memoria_uso': self.df_completo.memory_usage(deep=True).sum()
        }
        
        logger.info("📋 Estrutura do Dataset:")
        logger.info(f"  - Dimensões: {estrutura['dimensoes']['linhas']} linhas x {estrutura['dimensoes']['colunas']} colunas")
        logger.info(f"  - Uso de memória: {estrutura['memoria_uso'] / 1024 / 1024:.2f} MB")
        logger.info(f"  - Colunas com valores nulos: {sum(1 for v in estrutura['valores_nulos'].values() if v > 0)}")
        
        return estrutura
    
    def analisar_distribuicao_temporal(self):
        """Analisa distribuição temporal dos dados"""
        logger.info("⏰ Analisando distribuição temporal...")
        
        # Converter timestamp
        self.df_completo['timestamp_datetime'] = pd.to_datetime(self.df_completo['timestamp_datetime'])
        
        # Análise temporal
        temporal = {
            'periodo_total': {
                'inicio': self.df_completo['timestamp_datetime'].min(),
                'fim': self.df_completo['timestamp_datetime'].max(),
                'duracao_dias': (self.df_completo['timestamp_datetime'].max() - 
                               self.df_completo['timestamp_datetime'].min()).days
            },
            'leituras_por_dia': self.df_completo.groupby(
                self.df_completo['timestamp_datetime'].dt.date
            ).size().to_dict(),
            'leituras_por_hora': self.df_completo.groupby(
                self.df_completo['timestamp_datetime'].dt.hour
            ).size().to_dict(),
            'leituras_por_dia_semana': self.df_completo.groupby(
                self.df_completo['timestamp_datetime'].dt.day_name()
            ).size().to_dict()
        }
        
        logger.info("📅 Distribuição Temporal:")
        logger.info(f"  - Período: {temporal['periodo_total']['inicio']} a {temporal['periodo_total']['fim']}")
        logger.info(f"  - Duração: {temporal['periodo_total']['duracao_dias']} dias")
        logger.info(f"  - Média de leituras por dia: {len(self.df_completo) / temporal['periodo_total']['duracao_dias']:.1f}")
        
        return temporal
    
    def analisar_distribuicao_sensores(self):
        """Analisa distribuição por sensores"""
        logger.info("📡 Analisando distribuição por sensores...")
        
        sensores = {
            'total_sensores': self.df_completo['id_sensor'].nunique(),
            'leituras_por_sensor': self.df_completo.groupby('id_sensor').size().to_dict(),
            'leituras_por_tipo_sensor': self.df_completo.groupby('tipo_sensor_nome').size().to_dict(),
            'leituras_por_dispositivo': self.df_completo.groupby('dispositivo_nome').size().to_dict(),
            'leituras_por_localizacao': self.df_completo.groupby('localizacao').size().to_dict()
        }
        
        logger.info("📊 Distribuição por Sensores:")
        logger.info(f"  - Total de sensores: {sensores['total_sensores']}")
        logger.info(f"  - Tipos de sensor: {list(sensores['leituras_por_tipo_sensor'].keys())}")
        logger.info(f"  - Dispositivos: {list(sensores['leituras_por_dispositivo'].keys())}")
        
        return sensores
    
    def analisar_qualidade_dados(self):
        """Analisa qualidade dos dados"""
        logger.info("🔍 Analisando qualidade dos dados...")
        
        qualidade = {
            'distribuicao_qualidade': self.df_completo['qualidade_dados'].value_counts().to_dict(),
            'anomalias_detectadas': {
                'total': self.df_completo['anomalia_detectada'].sum(),
                'percentual': (self.df_completo['anomalia_detectada'].sum() / len(self.df_completo)) * 100
            },
            'valores_nulos_por_coluna': self.df_completo.isnull().sum().to_dict(),
            'valores_duplicados': self.df_completo.duplicated().sum()
        }
        
        logger.info("✅ Qualidade dos Dados:")
        logger.info(f"  - Anomalias detectadas: {qualidade['anomalias_detectadas']['total']} ({qualidade['anomalias_detectadas']['percentual']:.1f}%)")
        logger.info(f"  - Valores duplicados: {qualidade['valores_duplicados']}")
        logger.info(f"  - Distribuição de qualidade: {qualidade['distribuicao_qualidade']}")
        
        return qualidade
    
    def analisar_valores_numericos(self):
        """Analisa valores numéricos"""
        logger.info("🔢 Analisando valores numéricos...")
        
        # Filtrar apenas valores numéricos válidos
        df_numerico = self.df_completo[self.df_completo['valor_numerico'].notna()].copy()
        
        if df_numerico.empty:
            logger.warning("Nenhum valor numérico encontrado")
            return {}
        
        valores = {
            'estatisticas_gerais': {
                'media': df_numerico['valor_numerico'].mean(),
                'mediana': df_numerico['valor_numerico'].median(),
                'desvio_padrao': df_numerico['valor_numerico'].std(),
                'minimo': df_numerico['valor_numerico'].min(),
                'maximo': df_numerico['valor_numerico'].max(),
                'quartil_25': df_numerico['valor_numerico'].quantile(0.25),
                'quartil_75': df_numerico['valor_numerico'].quantile(0.75)
            },
            'estatisticas_por_tipo_sensor': {},
            'estatisticas_por_dispositivo': {}
        }
        
        # Estatísticas por tipo de sensor
        for tipo in df_numerico['tipo_sensor_nome'].unique():
            df_tipo = df_numerico[df_numerico['tipo_sensor_nome'] == tipo]
            valores['estatisticas_por_tipo_sensor'][tipo] = {
                'media': df_tipo['valor_numerico'].mean(),
                'desvio_padrao': df_tipo['valor_numerico'].std(),
                'minimo': df_tipo['valor_numerico'].min(),
                'maximo': df_tipo['valor_numerico'].max(),
                'count': len(df_tipo)
            }
        
        # Estatísticas por dispositivo
        for dispositivo in df_numerico['dispositivo_nome'].unique():
            df_disp = df_numerico[df_numerico['dispositivo_nome'] == dispositivo]
            valores['estatisticas_por_dispositivo'][dispositivo] = {
                'media': df_disp['valor_numerico'].mean(),
                'desvio_padrao': df_disp['valor_numerico'].std(),
                'minimo': df_disp['valor_numerico'].min(),
                'maximo': df_disp['valor_numerico'].max(),
                'count': len(df_disp)
            }
        
        logger.info("📈 Valores Numéricos:")
        logger.info(f"  - Média geral: {valores['estatisticas_gerais']['media']:.2f}")
        logger.info(f"  - Desvio padrão: {valores['estatisticas_gerais']['desvio_padrao']:.2f}")
        logger.info(f"  - Faixa: {valores['estatisticas_gerais']['minimo']:.2f} a {valores['estatisticas_gerais']['maximo']:.2f}")
        
        return valores
    
    def gerar_visualizacoes_dataset(self):
        """Gera visualizações do dataset"""
        logger.info("📊 Gerando visualizações do dataset...")
        
        # Configurar estilo
        plt.style.use('seaborn-v0_8')
        
        # Criar figura com subplots
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Análise do Dataset ML - Sistema IoT Monitoring', fontsize=16, fontweight='bold')
        
        # 1. Distribuição temporal
        df_diario = self.df_completo.groupby(
            self.df_completo['timestamp_datetime'].dt.date
        ).size()
        
        axes[0, 0].plot(df_diario.index, df_diario.values, marker='o', linewidth=2)
        axes[0, 0].set_title('Leituras por Dia')
        axes[0, 0].set_xlabel('Data')
        axes[0, 0].set_ylabel('Número de Leituras')
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # 2. Distribuição por tipo de sensor
        tipo_counts = self.df_completo['tipo_sensor_nome'].value_counts()
        axes[0, 1].pie(tipo_counts.values, labels=tipo_counts.index, autopct='%1.1f%%')
        axes[0, 1].set_title('Distribuição por Tipo de Sensor')
        
        # 3. Distribuição por dispositivo
        disp_counts = self.df_completo['dispositivo_nome'].value_counts()
        axes[0, 2].bar(range(len(disp_counts)), disp_counts.values)
        axes[0, 2].set_title('Leituras por Dispositivo')
        axes[0, 2].set_xlabel('Dispositivo')
        axes[0, 2].set_ylabel('Número de Leituras')
        axes[0, 2].set_xticks(range(len(disp_counts)))
        axes[0, 2].set_xticklabels(disp_counts.index, rotation=45)
        
        # 4. Distribuição de qualidade
        qualidade_counts = self.df_completo['qualidade_dados'].value_counts()
        axes[1, 0].bar(qualidade_counts.index, qualidade_counts.values, color=['green', 'blue', 'orange', 'red'])
        axes[1, 0].set_title('Distribuição de Qualidade dos Dados')
        axes[1, 0].set_xlabel('Qualidade')
        axes[1, 0].set_ylabel('Número de Leituras')
        
        # 5. Histograma de valores numéricos
        df_numerico = self.df_completo[self.df_completo['valor_numerico'].notna()]
        if not df_numerico.empty:
            axes[1, 1].hist(df_numerico['valor_numerico'], bins=50, alpha=0.7, color='skyblue')
            axes[1, 1].set_title('Distribuição de Valores Numéricos')
            axes[1, 1].set_xlabel('Valor')
            axes[1, 1].set_ylabel('Frequência')
        
        # 6. Anomalias por dispositivo
        anomalias_por_disp = self.df_completo.groupby('dispositivo_nome')['anomalia_detectada'].sum()
        axes[1, 2].bar(range(len(anomalias_por_disp)), anomalias_por_disp.values, color='red', alpha=0.7)
        axes[1, 2].set_title('Anomalias por Dispositivo')
        axes[1, 2].set_xlabel('Dispositivo')
        axes[1, 2].set_ylabel('Número de Anomalias')
        axes[1, 2].set_xticks(range(len(anomalias_por_disp)))
        axes[1, 2].set_xticklabels(anomalias_por_disp.index, rotation=45)
        
        plt.tight_layout()
        plt.savefig('analise_dataset_ml.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        logger.info("📊 Visualizações salvas em: analise_dataset_ml.png")
    
    def gerar_relatorio_completo(self):
        """Gera relatório completo do dataset"""
        logger.info("📋 Gerando relatório completo...")
        
        # Executar todas as análises
        estrutura = self.analisar_estrutura_dataset()
        temporal = self.analisar_distribuicao_temporal()
        sensores = self.analisar_distribuicao_sensores()
        qualidade = self.analisar_qualidade_dados()
        valores = self.analisar_valores_numericos()
        
        # Compilar relatório
        relatorio = {
            'timestamp': datetime.now().isoformat(),
            'estrutura': estrutura,
            'temporal': temporal,
            'sensores': sensores,
            'qualidade': qualidade,
            'valores': valores
        }
        
        # Salvar relatório
        with open('relatorio_dataset_ml.json', 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False, default=str)
        
        # Imprimir resumo
        logger.info("=" * 60)
        logger.info("📊 RELATÓRIO COMPLETO DO DATASET ML")
        logger.info("=" * 60)
        
        logger.info("📋 ESTRUTURA:")
        logger.info(f"  - Dimensões: {estrutura['dimensoes']['linhas']} linhas x {estrutura['dimensoes']['colunas']} colunas")
        logger.info(f"  - Uso de memória: {estrutura['memoria_uso'] / 1024 / 1024:.2f} MB")
        
        logger.info("⏰ TEMPORAL:")
        logger.info(f"  - Período: {temporal['periodo_total']['inicio']} a {temporal['periodo_total']['fim']}")
        logger.info(f"  - Duração: {temporal['periodo_total']['duracao_dias']} dias")
        
        logger.info("📡 SENSORES:")
        logger.info(f"  - Total de sensores: {sensores['total_sensores']}")
        logger.info(f"  - Tipos de sensor: {len(sensores['leituras_por_tipo_sensor'])}")
        logger.info(f"  - Dispositivos: {len(sensores['leituras_por_dispositivo'])}")
        
        logger.info("✅ QUALIDADE:")
        logger.info(f"  - Anomalias: {qualidade['anomalias_detectadas']['total']} ({qualidade['anomalias_detectadas']['percentual']:.1f}%)")
        logger.info(f"  - Duplicatas: {qualidade['valores_duplicados']}")
        
        if valores:
            logger.info("🔢 VALORES NUMÉRICOS:")
            logger.info(f"  - Média: {valores['estatisticas_gerais']['media']:.2f}")
            logger.info(f"  - Desvio padrão: {valores['estatisticas_gerais']['desvio_padrao']:.2f}")
            logger.info(f"  - Faixa: {valores['estatisticas_gerais']['minimo']:.2f} a {valores['estatisticas_gerais']['maximo']:.2f}")
        
        logger.info("")
        logger.info("📁 Relatório salvo em: relatorio_dataset_ml.json")
        
        return relatorio
    
    def executar_analise_completa(self):
        """Executa análise completa do dataset"""
        if not self.conectar_banco():
            return False
        
        try:
            # Carregar dataset
            if not self.carregar_dataset_completo():
                return False
            
            # Gerar análises
            self.gerar_relatorio_completo()
            self.gerar_visualizacoes_dataset()
            
            logger.info("🎉 Análise completa do dataset executada com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"Erro na análise: {e}")
            return False
        
        finally:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()


def main():
    """Função principal"""
    print("=== Analisador de Dataset ML ===")
    print("Enterprise Challenge Sprint 3 - Reply")
    print("=================================")
    
    # Configurar parâmetros de conexão
    host = input("Host do banco (padrão: localhost): ").strip() or 'localhost'
    user = input("Usuário do banco (padrão: root): ").strip() or 'root'
    password = input("Senha do banco: ").strip()
    database = input("Nome do banco (padrão: iot_monitoring_db): ").strip() or 'iot_monitoring_db'
    
    # Criar analisador
    analisador = DatasetMLAnalisador(host, user, password, database)
    
    # Executar análise
    sucesso = analisador.executar_analise_completa()
    
    if sucesso:
        print("\n✅ Análise executada com sucesso!")
        print("📊 Verifique os arquivos gerados:")
        print("  - analise_dataset_ml.png")
        print("  - relatorio_dataset_ml.json")
        print("  - dataset_ml_analisador.log")
    else:
        print("\n❌ Erro na execução da análise.")


if __name__ == "__main__":
    main()
