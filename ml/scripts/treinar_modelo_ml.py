#!/usr/bin/env python3
"""
Sistema IoT Monitoring - Treinamento de Modelo ML
Enterprise Challenge Sprint 3 - Reply

Este script treina modelos de Machine Learning para detecção de anomalias
em dados IoT e salva os modelos treinados.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)
import joblib
import mysql.connector
from sqlalchemy import create_engine
import json
import os
import warnings
warnings.filterwarnings('ignore')

class IoTMLTrainer:
    """Classe para treinamento de modelos ML para IoT"""
    
    def __init__(self, db_config):
        self.db_config = db_config
        self.models = {}
        self.results = {}
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
        # Configurar visualizações
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        plt.rcParams['figure.figsize'] = (12, 8)
        
        print("=== Sistema IoT Monitoring - Treinamento ML ===")
        print("Enterprise Challenge Sprint 3 - Reply")
        print("=============================================")
    
    def connect_database(self):
        """Conecta ao banco de dados MySQL"""
        try:
            engine = create_engine(
                f"mysql+pymysql://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}/{self.db_config['database']}"
            )
            print("✅ Conexão com banco de dados estabelecida")
            return engine
        except Exception as e:
            print(f"❌ Erro ao conectar ao banco: {e}")
            return None
    
    def load_data(self, engine, limit=10000):
        """Carrega dados do banco de dados"""
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
        WHERE l.timestamp_datetime >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        ORDER BY l.timestamp_datetime
        LIMIT %s
        """ % limit
        
        try:
            df = pd.read_sql(query, engine)
            print(f"✅ Dados carregados: {len(df)} registros")
            print(f"📊 Colunas: {list(df.columns)}")
            return df
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
            return None
    
    def prepare_features(self, df):
        """Prepara features para treinamento do modelo"""
        print("\n🔧 Preparando features...")
        
        # Criar cópia do dataframe
        df_ml = df.copy()
        
        # Converter timestamp para features temporais
        df_ml['timestamp_datetime'] = pd.to_datetime(df_ml['timestamp_datetime'])
        df_ml['hour'] = df_ml['timestamp_datetime'].dt.hour
        df_ml['day_of_week'] = df_ml['timestamp_datetime'].dt.dayofweek
        df_ml['day_of_month'] = df_ml['timestamp_datetime'].dt.day
        
        # Codificar variáveis categóricas
        le_sensor = LabelEncoder()
        le_qualidade = LabelEncoder()
        
        df_ml['sensor_encoded'] = le_sensor.fit_transform(df_ml['tipo_sensor'])
        df_ml['qualidade_encoded'] = le_qualidade.fit_transform(df_ml['qualidade_dados'])
        
        # Armazenar encoders
        self.label_encoders['sensor'] = le_sensor
        self.label_encoders['qualidade'] = le_qualidade
        
        # Selecionar features numéricas
        features = ['valor_numerico', 'valor_booleano', 'hour', 'day_of_week', 'day_of_month', 
                   'sensor_encoded', 'qualidade_encoded']
        
        X = df_ml[features].fillna(0)
        y = df_ml['anomalia_detectada']
        
        print(f"✅ Features preparadas: {X.shape}")
        print(f"📊 Features: {list(X.columns)}")
        print(f"🎯 Target: {y.value_counts().to_dict()}")
        
        return X, y
    
    def train_models(self, X, y):
        """Treina múltiplos modelos de ML"""
        print("\n🤖 Treinando modelos...")
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Normalizar features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Definir modelos
        models_config = {
            'Random Forest': {
                'model': RandomForestClassifier(
                    n_estimators=100,
                    max_depth=10,
                    min_samples_split=5,
                    min_samples_leaf=2,
                    random_state=42
                ),
                'supervised': True
            },
            'Isolation Forest': {
                'model': IsolationForest(
                    contamination=0.1,
                    n_estimators=100,
                    random_state=42
                ),
                'supervised': False
            },
            'One-Class SVM': {
                'model': OneClassSVM(
                    nu=0.1,
                    kernel='rbf'
                ),
                'supervised': False
            },
            'Local Outlier Factor': {
                'model': LocalOutlierFactor(
                    n_neighbors=20,
                    contamination=0.1
                ),
                'supervised': False
            }
        }
        
        # Treinar modelos
        for name, config in models_config.items():
            print(f"\n🔄 Treinando {name}...")
            
            model = config['model']
            
            if config['supervised']:
                # Modelos supervisionados
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
            else:
                # Modelos não supervisionados
                model.fit(X_train_scaled)
                
                if name == 'Local Outlier Factor':
                    y_pred = model.fit_predict(X_test_scaled)
                    y_pred = (y_pred == -1).astype(int)
                else:
                    y_pred = model.predict(X_test_scaled)
                    y_pred = (y_pred == -1).astype(int)
            
            # Calcular métricas
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, zero_division=0)
            recall = recall_score(y_test, y_pred, zero_division=0)
            f1 = f1_score(y_test, y_pred, zero_division=0)
            
            self.models[name] = model
            self.results[name] = {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'y_pred': y_pred,
                'y_test': y_test
            }
            
            print(f"✅ {name} - Accuracy: {accuracy:.3f}, F1: {f1:.3f}")
        
        return X_test_scaled, y_test
    
    def evaluate_models(self):
        """Avalia e compara modelos"""
        print("\n📊 Avaliando modelos...")
        
        # Criar DataFrame com resultados
        results_df = pd.DataFrame({
            name: {
                'Accuracy': results['accuracy'],
                'Precision': results['precision'],
                'Recall': results['recall'],
                'F1-Score': results['f1_score']
            }
            for name, results in self.results.items()
        }).T
        
        print("\n=== COMPARAÇÃO DE MODELOS ===")
        print(results_df.round(3))
        
        # Encontrar melhor modelo
        best_model = results_df['F1-Score'].idxmax()
        print(f"\n🏆 Melhor modelo: {best_model}")
        print(f"📊 F1-Score: {results_df.loc[best_model, 'F1-Score']:.3f}")
        
        return results_df, best_model
    
    def generate_visualizations(self, X_test, y_test, best_model):
        """Gera visualizações dos resultados"""
        print("\n📈 Gerando visualizações...")
        
        # Criar diretório para visualizações
        os.makedirs('../visualizacoes', exist_ok=True)
        
        # 1. Comparação de modelos
        results_df = pd.DataFrame({
            name: {
                'Accuracy': results['accuracy'],
                'Precision': results['precision'],
                'Recall': results['recall'],
                'F1-Score': results['f1_score']
            }
            for name, results in self.results.items()
        }).T
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Comparação de Performance dos Modelos', fontsize=16, fontweight='bold')
        
        metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
        colors = ['skyblue', 'lightgreen', 'orange', 'pink']
        
        for i, metric in enumerate(metrics):
            ax = axes[i//2, i%2]
            results_df[metric].plot(kind='bar', ax=ax, color=colors[i])
            ax.set_title(f'{metric} por Modelo')
            ax.set_xlabel('Modelo')
            ax.set_ylabel(metric)
            ax.tick_params(axis='x', rotation=45)
            
            # Adicionar valores nas barras
            for j, v in enumerate(results_df[metric]):
                ax.text(j, v + 0.01, f'{v:.3f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('../visualizacoes/comparacao_modelos.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 2. Matriz de confusão do melhor modelo
        y_pred = self.results[best_model]['y_pred']
        cm = confusion_matrix(y_test, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title(f'Matriz de Confusão - {best_model}')
        plt.xlabel('Predito')
        plt.ylabel('Real')
        plt.tight_layout()
        plt.savefig('../visualizacoes/confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Importância das features (Random Forest)
        if best_model == 'Random Forest':
            feature_importance = self.models['Random Forest'].feature_importances_
            feature_names = ['valor_numerico', 'valor_booleano', 'hour', 'day_of_week', 
                           'day_of_month', 'sensor_encoded', 'qualidade_encoded']
            
            importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': feature_importance
            }).sort_values('importance', ascending=False)
            
            plt.figure(figsize=(10, 6))
            sns.barplot(data=importance_df, x='importance', y='feature', palette='viridis')
            plt.title('Importância das Features - Random Forest')
            plt.xlabel('Importância')
            plt.ylabel('Feature')
            plt.tight_layout()
            plt.savefig('../visualizacoes/feature_importance.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        print("✅ Visualizações salvas em ../visualizacoes/")
    
    def save_models(self, best_model):
        """Salva modelos treinados"""
        print(f"\n💾 Salvando modelos...")
        
        # Criar diretório para modelos
        os.makedirs('../modelos', exist_ok=True)
        
        # Salvar melhor modelo
        best_model_obj = self.models[best_model]
        joblib.dump(best_model_obj, f'../modelos/{best_model.lower().replace(" ", "_")}.pkl')
        joblib.dump(self.scaler, '../modelos/scaler.pkl')
        joblib.dump(self.label_encoders['sensor'], '../modelos/label_encoder_sensor.pkl')
        joblib.dump(self.label_encoders['qualidade'], '../modelos/label_encoder_qualidade.pkl')
        
        print(f"✅ Modelo {best_model} salvo: ../modelos/{best_model.lower().replace(' ', '_')}.pkl")
        print(f"✅ Scaler salvo: ../modelos/scaler.pkl")
        print(f"✅ Label encoders salvos: ../modelos/label_encoder_*.pkl")
    
    def save_metrics(self, results_df, best_model):
        """Salva métricas de avaliação"""
        print(f"\n📊 Salvando métricas...")
        
        # Criar diretório para métricas
        os.makedirs('../metricas', exist_ok=True)
        
        # Salvar métricas em JSON
        metrics_data = {
            'best_model': best_model,
            'best_f1_score': float(results_df.loc[best_model, 'F1-Score']),
            'best_accuracy': float(results_df.loc[best_model, 'Accuracy']),
            'all_models': results_df.to_dict()
        }
        
        with open('../metricas/model_metrics.json', 'w') as f:
            json.dump(metrics_data, f, indent=2)
        
        # Salvar matriz de confusão
        cm = confusion_matrix(
            self.results[best_model]['y_test'], 
            self.results[best_model]['y_pred']
        )
        
        confusion_data = {
            'confusion_matrix': cm.tolist(),
            'classification_report': classification_report(
                self.results[best_model]['y_test'], 
                self.results[best_model]['y_pred'],
                output_dict=True
            )
        }
        
        with open('../metricas/confusion_matrix.json', 'w') as f:
            json.dump(confusion_data, f, indent=2)
        
        print("✅ Métricas salvas em ../metricas/")
    
    def run_training(self, limit=10000):
        """Executa o pipeline completo de treinamento"""
        print("🚀 Iniciando pipeline de treinamento...")
        
        # 1. Conectar ao banco
        engine = self.connect_database()
        if engine is None:
            return False
        
        # 2. Carregar dados
        df = self.load_data(engine, limit)
        if df is None:
            return False
        
        # 3. Preparar features
        X, y = self.prepare_features(df)
        
        # 4. Treinar modelos
        X_test, y_test = self.train_models(X, y)
        
        # 5. Avaliar modelos
        results_df, best_model = self.evaluate_models()
        
        # 6. Gerar visualizações
        self.generate_visualizations(X_test, y_test, best_model)
        
        # 7. Salvar modelos
        self.save_models(best_model)
        
        # 8. Salvar métricas
        self.save_metrics(results_df, best_model)
        
        print("\n🎉 Pipeline de treinamento concluído com sucesso!")
        return True

def main():
    """Função principal"""
    # Configurações do banco
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'password',
        'database': 'iot_monitoring_db'
    }
    
    # Criar trainer
    trainer = IoTMLTrainer(db_config)
    
    # Executar treinamento
    success = trainer.run_training(limit=10000)
    
    if success:
        print("\n✅ Treinamento concluído com sucesso!")
        print("📁 Arquivos gerados:")
        print("  - ../modelos/ - Modelos treinados")
        print("  - ../metricas/ - Métricas de avaliação")
        print("  - ../visualizacoes/ - Gráficos e visualizações")
    else:
        print("\n❌ Falha no treinamento.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
