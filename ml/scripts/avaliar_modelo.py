#!/usr/bin/env python3
"""
Sistema IoT Monitoring - Avaliação de Modelo ML
Enterprise Challenge Sprint 3 - Reply

Este script avalia modelos de Machine Learning treinados e gera
métricas detalhadas e visualizações de performance.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import json
import os
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve,
    precision_recall_curve, average_precision_score
)
from sklearn.model_selection import cross_val_score, validation_curve
import mysql.connector
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings('ignore')

class IoTModelEvaluator:
    """Classe para avaliação de modelos ML IoT"""
    
    def __init__(self, db_config, model_path='../modelos/'):
        self.db_config = db_config
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.label_encoders = {}
        self.test_data = None
        self.predictions = None
        self.metrics = {}
        
        # Configurar visualizações
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        plt.rcParams['figure.figsize'] = (12, 8)
        
        print("=== Sistema IoT Monitoring - Avaliação de Modelo ===")
        print("Enterprise Challenge Sprint 3 - Reply")
        print("=================================================")
    
    def load_model(self):
        """Carrega modelo treinado"""
        try:
            print("🔄 Carregando modelo...")
            
            # Carregar modelo
            self.model = joblib.load(f'{self.model_path}random_forest.pkl')
            self.scaler = joblib.load(f'{self.model_path}scaler.pkl')
            self.label_encoders['sensor'] = joblib.load(f'{self.model_path}label_encoder_sensor.pkl')
            self.label_encoders['qualidade'] = joblib.load(f'{self.model_path}label_encoder_qualidade.pkl')
            
            print("✅ Modelo carregado com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar modelo: {e}")
            return False
    
    def load_test_data(self, limit=5000):
        """Carrega dados de teste do banco"""
        try:
            print("🔄 Carregando dados de teste...")
            
            engine = create_engine(
                f"mysql+pymysql://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}/{self.db_config['database']}"
            )
            
            query = """
            SELECT 
                l.id_leitura,
                l.timestamp_datetime,
                l.valor_numerico,
                l.valor_booleano,
                l.qualidade_dados,
                l.anomalia_detectada,
                s.nome as sensor_nome,
                ts.nome as tipo_sensor,
                ts.unidade_medida,
                d.nome as dispositivo_nome
            FROM leituras_sensores l
            JOIN sensores s ON l.id_sensor = s.id_sensor
            JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
            JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
            WHERE l.timestamp_datetime >= DATE_SUB(NOW(), INTERVAL 3 DAY)
            ORDER BY l.timestamp_datetime
            LIMIT %s
            """ % limit
            
            df = pd.read_sql(query, engine)
            
            if df.empty:
                print("❌ Nenhum dado de teste encontrado")
                return False
            
            print(f"✅ Dados de teste carregados: {len(df)} registros")
            self.test_data = df
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar dados de teste: {e}")
            return False
    
    def prepare_test_features(self):
        """Prepara features dos dados de teste"""
        print("🔧 Preparando features de teste...")
        
        df = self.test_data.copy()
        
        # Converter timestamp
        df['timestamp_datetime'] = pd.to_datetime(df['timestamp_datetime'])
        df['hour'] = df['timestamp_datetime'].dt.hour
        df['day_of_week'] = df['timestamp_datetime'].dt.dayofweek
        df['day_of_month'] = df['timestamp_datetime'].dt.day
        
        # Codificar variáveis categóricas
        df['sensor_encoded'] = self.label_encoders['sensor'].transform(df['tipo_sensor'])
        df['qualidade_encoded'] = self.label_encoders['qualidade'].transform(df['qualidade_dados'])
        
        # Selecionar features
        features = ['valor_numerico', 'valor_booleano', 'hour', 'day_of_week', 'day_of_month', 
                   'sensor_encoded', 'qualidade_encoded']
        
        X = df[features].fillna(0)
        y = df['anomalia_detectada']
        
        # Normalizar
        X_scaled = self.scaler.transform(X)
        
        print(f"✅ Features preparadas: {X_scaled.shape}")
        return X_scaled, y
    
    def make_predictions(self, X_test, y_test):
        """Faz predições no conjunto de teste"""
        print("🔮 Fazendo predições...")
        
        # Predições
        y_pred = self.model.predict(X_test)
        
        # Probabilidades (se disponível)
        y_proba = None
        if hasattr(self.model, 'predict_proba'):
            y_proba = self.model.predict_proba(X_test)[:, 1]
        
        self.predictions = {
            'y_true': y_test,
            'y_pred': y_pred,
            'y_proba': y_proba
        }
        
        print(f"✅ Predições concluídas: {len(y_pred)} amostras")
        return y_pred, y_proba
    
    def calculate_metrics(self):
        """Calcula métricas de avaliação"""
        print("📊 Calculando métricas...")
        
        y_true = self.predictions['y_true']
        y_pred = self.predictions['y_pred']
        y_proba = self.predictions['y_proba']
        
        # Métricas básicas
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        
        # Matriz de confusão
        cm = confusion_matrix(y_true, y_pred)
        tn, fp, fn, tp = cm.ravel()
        
        # Métricas adicionais
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
        
        # ROC AUC (se probabilidades disponíveis)
        roc_auc = None
        if y_proba is not None:
            roc_auc = roc_auc_score(y_true, y_proba)
        
        # Precision-Recall AUC
        pr_auc = None
        if y_proba is not None:
            pr_auc = average_precision_score(y_true, y_proba)
        
        self.metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'specificity': specificity,
            'sensitivity': sensitivity,
            'roc_auc': roc_auc,
            'pr_auc': pr_auc,
            'confusion_matrix': cm.tolist(),
            'classification_report': classification_report(y_true, y_pred, output_dict=True)
        }
        
        print(f"✅ Métricas calculadas:")
        print(f"  Accuracy: {accuracy:.3f}")
        print(f"  Precision: {precision:.3f}")
        print(f"  Recall: {recall:.3f}")
        print(f"  F1-Score: {f1:.3f}")
        if roc_auc:
            print(f"  ROC AUC: {roc_auc:.3f}")
        if pr_auc:
            print(f"  PR AUC: {pr_auc:.3f}")
    
    def generate_visualizations(self):
        """Gera visualizações de avaliação"""
        print("📈 Gerando visualizações...")
        
        # Criar diretório
        os.makedirs('../visualizacoes', exist_ok=True)
        
        y_true = self.predictions['y_true']
        y_pred = self.predictions['y_pred']
        y_proba = self.predictions['y_proba']
        
        # 1. Matriz de Confusão
        plt.figure(figsize=(8, 6))
        cm = confusion_matrix(y_true, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Normal', 'Anomalia'],
                   yticklabels=['Normal', 'Anomalia'])
        plt.title('Matriz de Confusão')
        plt.xlabel('Predito')
        plt.ylabel('Real')
        plt.tight_layout()
        plt.savefig('../visualizacoes/confusion_matrix_evaluation.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Curva ROC (se probabilidades disponíveis)
        if y_proba is not None:
            plt.figure(figsize=(8, 6))
            fpr, tpr, _ = roc_curve(y_true, y_proba)
            roc_auc = roc_auc_score(y_true, y_proba)
            
            plt.plot(fpr, tpr, color='darkorange', lw=2, 
                    label=f'ROC Curve (AUC = {roc_auc:.3f})')
            plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('Taxa de Falsos Positivos')
            plt.ylabel('Taxa de Verdadeiros Positivos')
            plt.title('Curva ROC')
            plt.legend(loc="lower right")
            plt.tight_layout()
            plt.savefig('../visualizacoes/roc_curve.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        # 3. Curva Precision-Recall
        if y_proba is not None:
            plt.figure(figsize=(8, 6))
            precision_vals, recall_vals, _ = precision_recall_curve(y_true, y_proba)
            pr_auc = average_precision_score(y_true, y_proba)
            
            plt.plot(recall_vals, precision_vals, color='darkorange', lw=2,
                    label=f'PR Curve (AUC = {pr_auc:.3f})')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('Recall')
            plt.ylabel('Precision')
            plt.title('Curva Precision-Recall')
            plt.legend(loc="lower left")
            plt.tight_layout()
            plt.savefig('../visualizacoes/precision_recall_curve.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        # 4. Distribuição de Probabilidades
        if y_proba is not None:
            plt.figure(figsize=(10, 6))
            
            # Separar por classe real
            normal_proba = y_proba[y_true == 0]
            anomaly_proba = y_proba[y_true == 1]
            
            plt.hist(normal_proba, bins=50, alpha=0.7, label='Normal', color='skyblue')
            plt.hist(anomaly_proba, bins=50, alpha=0.7, label='Anomalia', color='orange')
            plt.xlabel('Probabilidade de Anomalia')
            plt.ylabel('Frequência')
            plt.title('Distribuição de Probabilidades por Classe')
            plt.legend()
            plt.tight_layout()
            plt.savefig('../visualizacoes/probability_distribution.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        # 5. Métricas por Sensor
        sensor_metrics = self.calculate_sensor_metrics()
        if sensor_metrics:
            plt.figure(figsize=(12, 8))
            
            sensors = list(sensor_metrics.keys())
            f1_scores = [sensor_metrics[s]['f1_score'] for s in sensors]
            
            plt.bar(range(len(sensors)), f1_scores, color='lightgreen')
            plt.xlabel('Sensor')
            plt.ylabel('F1-Score')
            plt.title('F1-Score por Sensor')
            plt.xticks(range(len(sensors)), sensors, rotation=45)
            
            # Adicionar valores nas barras
            for i, v in enumerate(f1_scores):
                plt.text(i, v + 0.01, f'{v:.3f}', ha='center', va='bottom')
            
            plt.tight_layout()
            plt.savefig('../visualizacoes/f1_score_by_sensor.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        print("✅ Visualizações salvas em ../visualizacoes/")
    
    def calculate_sensor_metrics(self):
        """Calcula métricas por sensor"""
        sensor_metrics = {}
        
        for sensor in self.test_data['sensor_nome'].unique():
            mask = self.test_data['sensor_nome'] == sensor
            y_true_sensor = self.predictions['y_true'][mask]
            y_pred_sensor = self.predictions['y_pred'][mask]
            
            if len(y_true_sensor) > 0:
                accuracy = accuracy_score(y_true_sensor, y_pred_sensor)
                precision = precision_score(y_true_sensor, y_pred_sensor, zero_division=0)
                recall = recall_score(y_true_sensor, y_pred_sensor, zero_division=0)
                f1 = f1_score(y_true_sensor, y_pred_sensor, zero_division=0)
                
                sensor_metrics[sensor] = {
                    'accuracy': accuracy,
                    'precision': precision,
                    'recall': recall,
                    'f1_score': f1,
                    'samples': len(y_true_sensor)
                }
        
        return sensor_metrics
    
    def save_metrics(self):
        """Salva métricas em arquivos JSON"""
        print("💾 Salvando métricas...")
        
        # Criar diretório
        os.makedirs('../metricas', exist_ok=True)
        
        # Salvar métricas principais
        with open('../metricas/evaluation_metrics.json', 'w') as f:
            json.dump(self.metrics, f, indent=2)
        
        # Salvar métricas por sensor
        sensor_metrics = self.calculate_sensor_metrics()
        with open('../metricas/sensor_metrics.json', 'w') as f:
            json.dump(sensor_metrics, f, indent=2)
        
        print("✅ Métricas salvas em ../metricas/")
    
    def run_evaluation(self, limit=5000):
        """Executa avaliação completa do modelo"""
        print("🚀 Iniciando avaliação do modelo...")
        
        # 1. Carregar modelo
        if not self.load_model():
            return False
        
        # 2. Carregar dados de teste
        if not self.load_test_data(limit):
            return False
        
        # 3. Preparar features
        X_test, y_test = self.prepare_test_features()
        
        # 4. Fazer predições
        y_pred, y_proba = self.make_predictions(X_test, y_test)
        
        # 5. Calcular métricas
        self.calculate_metrics()
        
        # 6. Gerar visualizações
        self.generate_visualizations()
        
        # 7. Salvar métricas
        self.save_metrics()
        
        print("\n🎉 Avaliação concluída com sucesso!")
        return True

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Avaliação de Modelo - Sistema IoT Monitoring')
    parser.add_argument('--limit', type=int, default=5000,
                       help='Limite de leituras para avaliação')
    
    args = parser.parse_args()
    
    # Configurações do banco
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'password',
        'database': 'iot_monitoring_db'
    }
    
    # Criar avaliador
    evaluator = IoTModelEvaluator(db_config)
    
    # Executar avaliação
    success = evaluator.run_evaluation(limit=args.limit)
    
    if success:
        print("\n✅ Avaliação concluída com sucesso!")
        print("📁 Arquivos gerados:")
        print("  - ../metricas/evaluation_metrics.json - Métricas principais")
        print("  - ../metricas/sensor_metrics.json - Métricas por sensor")
        print("  - ../visualizacoes/ - Gráficos de avaliação")
    else:
        print("\n❌ Falha na avaliação.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
