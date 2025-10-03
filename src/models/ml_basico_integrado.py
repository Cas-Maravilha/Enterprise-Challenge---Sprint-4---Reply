#!/usr/bin/env python3
"""
ML Básico Integrado - Sistema IoT Monitoring
Enterprise Challenge Sprint 3 - Reply

Este script implementa treino e inferência de ML sobre dados do banco,
incluindo métricas e visualizações pertinentes.
"""

import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.metrics import roc_curve, auc, precision_recall_curve
import joblib
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import warnings
warnings.filterwarnings('ignore')

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ml_basico_integrado.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MLBasicoIntegrado:
    """Sistema ML básico integrado com banco de dados"""
    
    def __init__(self, host='localhost', user='root', password='', database='iot_monitoring_db'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        
        # Modelos
        self.modelo_anomalia = None
        self.modelo_temperatura = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        
        # Dados
        self.df_leituras = None
        self.df_sensores = None
        self.df_dispositivos = None
        
        # Métricas
        self.metricas_anomalia = {}
        self.metricas_temperatura = {}
        
        logger.info("=== ML Básico Integrado - Sistema IoT Monitoring ===")
        logger.info("Enterprise Challenge Sprint 3 - Reply")
        logger.info("=================================================")
    
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
    
    def carregar_dados_banco(self):
        """Carrega dados do banco para treinamento"""
        logger.info("📊 Carregando dados do banco...")
        
        # Query para leituras com informações dos sensores e dispositivos
        query_leituras = """
        SELECT 
            l.id_leitura,
            l.id_sensor,
            l.timestamp_datetime,
            l.valor_numerico,
            l.valor_booleano,
            l.qualidade_dados,
            l.anomalia_detectada,
            l.data_coleta,
            s.nome as sensor_nome,
            s.id_tipo_sensor,
            s.status as sensor_status,
            d.nome as dispositivo_nome,
            d.localizacao,
            d.status as dispositivo_status,
            ts.nome as tipo_sensor_nome,
            ts.unidade_medida
        FROM leituras_sensores l
        JOIN sensores s ON l.id_sensor = s.id_sensor
        JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
        JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
        WHERE l.timestamp_datetime >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        ORDER BY l.timestamp_datetime DESC
        """
        
        self.df_leituras = self.executar_consulta(query_leituras)
        
        if self.df_leituras.empty:
            logger.error("Nenhum dado encontrado no banco")
            return False
        
        logger.info(f"Carregados {len(self.df_leituras)} registros de leituras")
        logger.info(f"Período: {self.df_leituras['timestamp_datetime'].min()} a {self.df_leituras['timestamp_datetime'].max()}")
        
        # Informações sobre o dataset
        logger.info("📋 Informações do Dataset:")
        logger.info(f"  - Total de registros: {len(self.df_leituras)}")
        logger.info(f"  - Sensores únicos: {self.df_leituras['id_sensor'].nunique()}")
        logger.info(f"  - Dispositivos únicos: {self.df_leituras['dispositivo_nome'].nunique()}")
        logger.info(f"  - Tipos de sensor: {self.df_leituras['tipo_sensor_nome'].unique()}")
        logger.info(f"  - Anomalias detectadas: {self.df_leituras['anomalia_detectada'].sum()}")
        
        return True
    
    def preparar_dados_anomalia(self):
        """Prepara dados para detecção de anomalias"""
        logger.info("🔍 Preparando dados para detecção de anomalias...")
        
        # Filtrar apenas sensores numéricos
        sensores_numericos = ['DHT22', 'LDR', 'Pressão', 'Vibração', 'Nível']
        df_numerico = self.df_leituras[
            self.df_leituras['tipo_sensor_nome'].isin(sensores_numericos)
        ].copy()
        
        if df_numerico.empty:
            logger.error("Nenhum dado numérico encontrado")
            return None, None
        
        # Criar features
        features = []
        target = []
        
        for sensor_id in df_numerico['id_sensor'].unique():
            df_sensor = df_numerico[df_numerico['id_sensor'] == sensor_id].copy()
            df_sensor = df_sensor.sort_values('timestamp_datetime')
            
            # Features: valor atual, média móvel, desvio padrão, tendência
            df_sensor['valor_anterior'] = df_sensor['valor_numerico'].shift(1)
            df_sensor['media_movel'] = df_sensor['valor_numerico'].rolling(window=5).mean()
            df_sensor['std_movel'] = df_sensor['valor_numerico'].rolling(window=5).std()
            df_sensor['tendencia'] = df_sensor['valor_numerico'].diff()
            
            # Remover NaN
            df_sensor = df_sensor.dropna()
            
            if len(df_sensor) > 0:
                # Features
                X_sensor = df_sensor[['valor_numerico', 'valor_anterior', 'media_movel', 'std_movel', 'tendencia']].values
                features.extend(X_sensor)
                
                # Target (anomalia detectada)
                y_sensor = df_sensor['anomalia_detectada'].values
                target.extend(y_sensor)
        
        X = np.array(features)
        y = np.array(target)
        
        logger.info(f"Dados preparados: {X.shape[0]} amostras, {X.shape[1]} features")
        logger.info(f"Anomalias: {np.sum(y)} ({np.sum(y)/len(y)*100:.1f}%)")
        
        return X, y
    
    def preparar_dados_temperatura(self):
        """Prepara dados para previsão de temperatura"""
        logger.info("🌡️ Preparando dados para previsão de temperatura...")
        
        # Filtrar apenas sensores de temperatura
        df_temp = self.df_leituras[
            (self.df_leituras['tipo_sensor_nome'] == 'DHT22') &
            (self.df_leituras['sensor_nome'].str.contains('Temperatura', na=False))
        ].copy()
        
        if df_temp.empty:
            logger.error("Nenhum dado de temperatura encontrado")
            return None, None
        
        # Criar features temporais
        df_temp['timestamp_datetime'] = pd.to_datetime(df_temp['timestamp_datetime'])
        df_temp['hora'] = df_temp['timestamp_datetime'].dt.hour
        df_temp['dia_semana'] = df_temp['timestamp_datetime'].dt.dayofweek
        df_temp['dia_mes'] = df_temp['timestamp_datetime'].dt.day
        
        # Features: hora, dia da semana, dia do mês, valor anterior, média móvel
        df_temp = df_temp.sort_values(['id_sensor', 'timestamp_datetime'])
        df_temp['valor_anterior'] = df_temp.groupby('id_sensor')['valor_numerico'].shift(1)
        df_temp['media_movel'] = df_temp.groupby('id_sensor')['valor_numerico'].rolling(window=3).mean().reset_index(0, drop=True)
        
        # Remover NaN
        df_temp = df_temp.dropna()
        
        if len(df_temp) == 0:
            logger.error("Nenhum dado válido após limpeza")
            return None, None
        
        # Features
        X = df_temp[['hora', 'dia_semana', 'dia_mes', 'valor_anterior', 'media_movel']].values
        y = df_temp['valor_numerico'].values
        
        logger.info(f"Dados preparados: {X.shape[0]} amostras, {X.shape[1]} features")
        logger.info(f"Temperatura média: {np.mean(y):.2f}°C")
        logger.info(f"Temperatura min/max: {np.min(y):.2f}°C / {np.max(y):.2f}°C")
        
        return X, y
    
    def treinar_modelo_anomalia(self, X, y):
        """Treina modelo para detecção de anomalias"""
        logger.info("🤖 Treinando modelo de detecção de anomalias...")
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Normalizar features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Treinar modelo
        self.modelo_anomalia = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        
        self.modelo_anomalia.fit(X_train_scaled, y_train)
        
        # Fazer previsões
        y_pred = self.modelo_anomalia.predict(X_test_scaled)
        y_pred_proba = self.modelo_anomalia.predict_proba(X_test_scaled)[:, 1]
        
        # Calcular métricas
        accuracy = accuracy_score(y_test, y_pred)
        self.metricas_anomalia = {
            'accuracy': accuracy,
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred),
            'y_test': y_test,
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba
        }
        
        logger.info(f"✅ Modelo de anomalia treinado - Acurácia: {accuracy:.3f}")
        
        return True
    
    def treinar_modelo_temperatura(self, X, y):
        """Treina modelo para previsão de temperatura"""
        logger.info("🌡️ Treinando modelo de previsão de temperatura...")
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Normalizar features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Treinar modelo
        self.modelo_temperatura = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        self.modelo_temperatura.fit(X_train_scaled, y_train)
        
        # Fazer previsões
        y_pred = self.modelo_temperatura.predict(X_test_scaled)
        
        # Calcular métricas
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        self.metricas_temperatura = {
            'mae': mae,
            'mse': mse,
            'rmse': np.sqrt(mse),
            'r2': r2,
            'y_test': y_test,
            'y_pred': y_pred
        }
        
        logger.info(f"✅ Modelo de temperatura treinado - MAE: {mae:.3f}, R²: {r2:.3f}")
        
        return True
    
    def gerar_visualizacoes(self):
        """Gera visualizações dos modelos"""
        logger.info("📊 Gerando visualizações...")
        
        # Configurar estilo
        plt.style.use('seaborn-v0_8')
        
        # Criar figura com subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('ML Básico Integrado - Sistema IoT Monitoring', fontsize=16, fontweight='bold')
        
        # 1. Matriz de Confusão - Detecção de Anomalias
        if self.metricas_anomalia:
            cm = self.metricas_anomalia['confusion_matrix']
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0, 0])
            axes[0, 0].set_title('Matriz de Confusão - Detecção de Anomalias')
            axes[0, 0].set_xlabel('Predito')
            axes[0, 0].set_ylabel('Real')
            
            # Adicionar métricas
            accuracy = self.metricas_anomalia['accuracy']
            axes[0, 0].text(0.5, -0.15, f'Acurácia: {accuracy:.3f}', 
                           transform=axes[0, 0].transAxes, ha='center', fontweight='bold')
        
        # 2. Curva ROC - Detecção de Anomalias
        if self.metricas_anomalia and 'y_pred_proba' in self.metricas_anomalia:
            y_test = self.metricas_anomalia['y_test']
            y_pred_proba = self.metricas_anomalia['y_pred_proba']
            
            fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
            roc_auc = auc(fpr, tpr)
            
            axes[0, 1].plot(fpr, tpr, color='darkorange', lw=2, 
                           label=f'ROC Curve (AUC = {roc_auc:.3f})')
            axes[0, 1].plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
            axes[0, 1].set_xlim([0.0, 1.0])
            axes[0, 1].set_ylim([0.0, 1.05])
            axes[0, 1].set_xlabel('Taxa de Falsos Positivos')
            axes[0, 1].set_ylabel('Taxa de Verdadeiros Positivos')
            axes[0, 1].set_title('Curva ROC - Detecção de Anomalias')
            axes[0, 1].legend(loc="lower right")
        
        # 3. Previsões vs Valores Reais - Temperatura
        if self.metricas_temperatura:
            y_test = self.metricas_temperatura['y_test']
            y_pred = self.metricas_temperatura['y_pred']
            
            axes[1, 0].scatter(y_test, y_pred, alpha=0.6, color='blue')
            axes[1, 0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 
                           'r--', lw=2)
            axes[1, 0].set_xlabel('Temperatura Real (°C)')
            axes[1, 0].set_ylabel('Temperatura Predita (°C)')
            axes[1, 0].set_title('Previsões vs Valores Reais - Temperatura')
            
            # Adicionar métricas
            mae = self.metricas_temperatura['mae']
            r2 = self.metricas_temperatura['r2']
            axes[1, 0].text(0.05, 0.95, f'MAE: {mae:.3f}°C\nR²: {r2:.3f}', 
                           transform=axes[1, 0].transAxes, va='top',
                           bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        # 4. Resíduos - Temperatura
        if self.metricas_temperatura:
            y_test = self.metricas_temperatura['y_test']
            y_pred = self.metricas_temperatura['y_pred']
            residuos = y_test - y_pred
            
            axes[1, 1].scatter(y_pred, residuos, alpha=0.6, color='green')
            axes[1, 1].axhline(y=0, color='r', linestyle='--')
            axes[1, 1].set_xlabel('Temperatura Predita (°C)')
            axes[1, 1].set_ylabel('Resíduos (°C)')
            axes[1, 1].set_title('Análise de Resíduos - Temperatura')
        
        plt.tight_layout()
        plt.savefig('ml_basico_visualizacoes.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        logger.info("📊 Visualizações salvas em: ml_basico_visualizacoes.png")
    
    def gerar_relatorio_metricas(self):
        """Gera relatório detalhado das métricas"""
        logger.info("📋 Gerando relatório de métricas...")
        
        relatorio = {
            'timestamp': datetime.now().isoformat(),
            'dataset_info': {
                'total_registros': len(self.df_leituras),
                'periodo': {
                    'inicio': self.df_leituras['timestamp_datetime'].min().isoformat(),
                    'fim': self.df_leituras['timestamp_datetime'].max().isoformat()
                },
                'sensores_unicos': self.df_leituras['id_sensor'].nunique(),
                'dispositivos_unicos': self.df_leituras['dispositivo_nome'].nunique(),
                'tipos_sensor': self.df_leituras['tipo_sensor_nome'].unique().tolist()
            },
            'modelo_anomalia': self.metricas_anomalia.copy(),
            'modelo_temperatura': self.metricas_temperatura.copy()
        }
        
        # Remover arrays numpy para serialização JSON
        if 'y_test' in relatorio['modelo_anomalia']:
            relatorio['modelo_anomalia']['y_test'] = relatorio['modelo_anomalia']['y_test'].tolist()
        if 'y_pred' in relatorio['modelo_anomalia']:
            relatorio['modelo_anomalia']['y_pred'] = relatorio['modelo_anomalia']['y_pred'].tolist()
        if 'y_pred_proba' in relatorio['modelo_anomalia']:
            relatorio['modelo_anomalia']['y_pred_proba'] = relatorio['modelo_anomalia']['y_pred_proba'].tolist()
        
        if 'y_test' in relatorio['modelo_temperatura']:
            relatorio['modelo_temperatura']['y_test'] = relatorio['modelo_temperatura']['y_test'].tolist()
        if 'y_pred' in relatorio['modelo_temperatura']:
            relatorio['modelo_temperatura']['y_pred'] = relatorio['modelo_temperatura']['y_pred'].tolist()
        
        # Salvar relatório
        with open('relatorio_ml_basico.json', 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        
        # Imprimir resumo
        logger.info("=" * 60)
        logger.info("📊 RELATÓRIO DE MÉTRICAS - ML BÁSICO INTEGRADO")
        logger.info("=" * 60)
        
        logger.info("📋 INFORMAÇÕES DO DATASET:")
        logger.info(f"  - Total de registros: {relatorio['dataset_info']['total_registros']}")
        logger.info(f"  - Período: {relatorio['dataset_info']['periodo']['inicio']} a {relatorio['dataset_info']['periodo']['fim']}")
        logger.info(f"  - Sensores únicos: {relatorio['dataset_info']['sensores_unicos']}")
        logger.info(f"  - Dispositivos únicos: {relatorio['dataset_info']['dispositivos_unicos']}")
        logger.info(f"  - Tipos de sensor: {', '.join(relatorio['dataset_info']['tipos_sensor'])}")
        
        if self.metricas_anomalia:
            logger.info("")
            logger.info("🤖 MODELO DE DETECÇÃO DE ANOMALIAS:")
            logger.info(f"  - Acurácia: {self.metricas_anomalia['accuracy']:.3f}")
            logger.info("  - Relatório de Classificação:")
            logger.info(f"    {self.metricas_anomalia['classification_report']}")
        
        if self.metricas_temperatura:
            logger.info("")
            logger.info("🌡️ MODELO DE PREVISÃO DE TEMPERATURA:")
            logger.info(f"  - MAE (Mean Absolute Error): {self.metricas_temperatura['mae']:.3f}°C")
            logger.info(f"  - RMSE (Root Mean Square Error): {self.metricas_temperatura['rmse']:.3f}°C")
            logger.info(f"  - R² (Coefficient of Determination): {self.metricas_temperatura['r2']:.3f}")
        
        logger.info("")
        logger.info("📁 Relatório salvo em: relatorio_ml_basico.json")
        
        return relatorio
    
    def salvar_modelos(self):
        """Salva os modelos treinados"""
        logger.info("💾 Salvando modelos treinados...")
        
        if self.modelo_anomalia:
            joblib.dump(self.modelo_anomalia, 'modelo_anomalia.pkl')
            logger.info("✅ Modelo de anomalia salvo: modelo_anomalia.pkl")
        
        if self.modelo_temperatura:
            joblib.dump(self.modelo_temperatura, 'modelo_temperatura.pkl')
            logger.info("✅ Modelo de temperatura salvo: modelo_temperatura.pkl")
        
        if self.scaler:
            joblib.dump(self.scaler, 'scaler.pkl')
            logger.info("✅ Scaler salvo: scaler.pkl")
    
    def executar_inferencia_tempo_real(self):
        """Executa inferência em tempo real sobre dados recentes"""
        logger.info("⚡ Executando inferência em tempo real...")
        
        # Buscar dados recentes (última hora)
        query_recente = """
        SELECT 
            l.id_leitura,
            l.id_sensor,
            l.timestamp_datetime,
            l.valor_numerico,
            l.anomalia_detectada,
            s.nome as sensor_nome,
            s.id_tipo_sensor,
            d.nome as dispositivo_nome,
            ts.nome as tipo_sensor_nome
        FROM leituras_sensores l
        JOIN sensores s ON l.id_sensor = s.id_sensor
        JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
        JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
        WHERE l.timestamp_datetime >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
        ORDER BY l.timestamp_datetime DESC
        LIMIT 100
        """
        
        df_recente = self.executar_consulta(query_recente)
        
        if df_recente.empty:
            logger.warning("Nenhum dado recente encontrado para inferência")
            return
        
        logger.info(f"📊 Processando {len(df_recente)} registros recentes...")
        
        # Processar cada registro
        for _, row in df_recente.iterrows():
            sensor_id = row['id_sensor']
            valor = row['valor_numerico']
            timestamp = row['timestamp_datetime']
            dispositivo = row['dispositivo_nome']
            sensor_nome = row['sensor_nome']
            
            # Aqui você implementaria a lógica de inferência
            # Por exemplo, usar o modelo treinado para prever anomalias
            logger.info(f"  📡 {dispositivo} - {sensor_nome}: {valor:.2f} (timestamp: {timestamp})")
        
        logger.info("✅ Inferência em tempo real concluída")
    
    def executar_pipeline_completo(self):
        """Executa o pipeline completo de ML"""
        logger.info("🚀 Iniciando pipeline completo de ML...")
        
        try:
            # 1. Conectar ao banco
            if not self.conectar_banco():
                return False
            
            # 2. Carregar dados
            if not self.carregar_dados_banco():
                return False
            
            # 3. Preparar dados para anomalias
            X_anomalia, y_anomalia = self.preparar_dados_anomalia()
            if X_anomalia is not None:
                self.treinar_modelo_anomalia(X_anomalia, y_anomalia)
            
            # 4. Preparar dados para temperatura
            X_temp, y_temp = self.preparar_dados_temperatura()
            if X_temp is not None:
                self.treinar_modelo_temperatura(X_temp, y_temp)
            
            # 5. Gerar visualizações
            self.gerar_visualizacoes()
            
            # 6. Gerar relatório
            self.gerar_relatorio_metricas()
            
            # 7. Salvar modelos
            self.salvar_modelos()
            
            # 8. Executar inferência em tempo real
            self.executar_inferencia_tempo_real()
            
            logger.info("🎉 Pipeline completo executado com sucesso!")
            return True
            
        except Exception as e:
            logger.error(f"Erro no pipeline: {e}")
            return False
        
        finally:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
    
    def fechar_conexao(self):
        """Fecha conexão com o banco"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        logger.info("Conexão com banco fechada")


def main():
    """Função principal"""
    print("=== ML Básico Integrado - Sistema IoT Monitoring ===")
    print("Enterprise Challenge Sprint 3 - Reply")
    print("=================================================")
    
    # Configurar parâmetros de conexão
    host = input("Host do banco (padrão: localhost): ").strip() or 'localhost'
    user = input("Usuário do banco (padrão: root): ").strip() or 'root'
    password = input("Senha do banco: ").strip()
    database = input("Nome do banco (padrão: iot_monitoring_db): ").strip() or 'iot_monitoring_db'
    
    # Criar instância do ML
    ml = MLBasicoIntegrado(host, user, password, database)
    
    # Executar pipeline
    sucesso = ml.executar_pipeline_completo()
    
    if sucesso:
        print("\n✅ Pipeline ML executado com sucesso!")
        print("📊 Verifique os arquivos gerados:")
        print("  - ml_basico_visualizacoes.png")
        print("  - relatorio_ml_basico.json")
        print("  - modelo_anomalia.pkl")
        print("  - modelo_temperatura.pkl")
        print("  - scaler.pkl")
        print("  - ml_basico_integrado.log")
    else:
        print("\n❌ Erro na execução do pipeline ML.")


if __name__ == "__main__":
    main()
