#!/usr/bin/env python3
"""
Sistema de Machine Learning para Detecção de Anomalias em Dados IoT
Problema: Classificação de anomalias em leituras de sensores
Dataset: Dados simulados de sensores ESP32
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score, roc_curve
from sklearn.cluster import DBSCAN
import warnings
warnings.filterwarnings('ignore')

# Configuração para gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class IoTAnomalyDetector:
    """
    Classe para detecção de anomalias em dados IoT
    """
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = None
        self.label_encoder = LabelEncoder()
        self.feature_columns = []
        self.is_trained = False
        
    def generate_synthetic_data(self, n_samples=5000):
        """
        Gera dataset sintético baseado nos dados reais do projeto IoT
        """
        print("🔄 Gerando dataset sintético...")
        
        np.random.seed(42)
        
        # Parâmetros baseados nos dados reais analisados
        data = []
        
        for i in range(n_samples):
            # Simular diferentes modos de operação
            mode = np.random.choice([0, 1, 2], p=[0.7, 0.2, 0.1])  # Normal, Alerta, Falha
            
            if mode == 0:  # Normal
                temperature = np.random.normal(25.0, 2.0)
                humidity = np.random.normal(60.0, 5.0)
                pressure = np.random.normal(5.0, 0.5)
                vibration = np.random.normal(0.0, 0.3)
                level = np.random.normal(100.0, 10.0)
                luminosity = np.random.normal(500.0, 100.0)
                movement = np.random.choice([0, 1], p=[0.9, 0.1])
                
            elif mode == 1:  # Alerta
                temperature = np.random.normal(28.0, 3.0)
                humidity = np.random.normal(70.0, 8.0)
                pressure = np.random.normal(6.5, 0.8)
                vibration = np.random.normal(0.5, 0.4)
                level = np.random.normal(120.0, 15.0)
                luminosity = np.random.normal(600.0, 150.0)
                movement = np.random.choice([0, 1], p=[0.7, 0.3])
                
            else:  # Falha
                temperature = np.random.normal(35.0, 5.0)
                humidity = np.random.normal(85.0, 10.0)
                pressure = np.random.normal(8.0, 1.5)
                vibration = np.random.normal(1.5, 0.8)
                level = np.random.normal(150.0, 25.0)
                luminosity = np.random.normal(800.0, 200.0)
                movement = np.random.choice([0, 1], p=[0.5, 0.5])
            
            # Adicionar ruído e anomalias ocasionais
            if np.random.random() < 0.05:  # 5% de chance de anomalia extrema
                temperature += np.random.normal(0, 10)
                humidity += np.random.normal(0, 20)
                pressure += np.random.normal(0, 2)
                vibration += np.random.normal(0, 1)
                level += np.random.normal(0, 30)
                luminosity += np.random.normal(0, 300)
                mode = 2  # Marcar como falha
            
            # Calcular magnitude da vibração
            vibration_mag = np.sqrt(vibration**2 + np.random.normal(0, 0.1)**2 + np.random.normal(0, 0.1)**2)
            
            # Calcular correlações entre variáveis
            if temperature > 30:
                humidity = min(100, humidity + (temperature - 30) * 2)
            
            data.append({
                'timestamp': i,
                'mode': mode,
                'temperature': max(-40, min(80, temperature)),
                'humidity': max(0, min(100, humidity)),
                'pressure': max(0, min(10, pressure)),
                'vibration_x': vibration,
                'vibration_y': np.random.normal(0, 0.1),
                'vibration_z': np.random.normal(0, 0.1),
                'vibration_mag': vibration_mag,
                'level': max(0, min(200, level)),
                'luminosity': max(0, min(1023, luminosity)),
                'movement': movement,
                'anomaly': 1 if mode == 2 else 0
            })
        
        df = pd.DataFrame(data)
        
        # Adicionar features derivadas
        df['temp_humidity_ratio'] = df['temperature'] / (df['humidity'] + 1)
        df['pressure_vibration'] = df['pressure'] * df['vibration_mag']
        df['level_luminosity'] = df['level'] * df['luminosity'] / 1000
        df['movement_frequency'] = df['movement'].rolling(window=10, min_periods=1).sum()
        
        print(f"✅ Dataset gerado: {len(df)} amostras, {len(df.columns)} features")
        return df
    
    def prepare_features(self, df):
        """
        Prepara features para treinamento
        """
        print("🔄 Preparando features...")
        
        # Selecionar features numéricas
        feature_columns = [
            'temperature', 'humidity', 'pressure', 'vibration_mag', 
            'level', 'luminosity', 'movement',
            'temp_humidity_ratio', 'pressure_vibration', 'level_luminosity'
        ]
        
        self.feature_columns = feature_columns
        
        # Separar features e target
        X = df[feature_columns].copy()
        y = df['anomaly'].copy()
        
        # Tratar valores infinitos e NaN
        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.fillna(X.median())
        
        print(f"✅ Features preparadas: {X.shape[1]} features, {X.shape[0]} amostras")
        return X, y
    
    def train_model(self, X, y):
        """
        Treina modelo de detecção de anomalias
        """
        print("🔄 Treinando modelo...")
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Normalizar features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Treinar Random Forest para classificação
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            class_weight='balanced'
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Fazer predições
        y_pred = self.model.predict(X_test_scaled)
        y_pred_proba = self.model.predict_proba(X_test_scaled)[:, 1]
        
        # Calcular métricas
        accuracy = accuracy_score(y_test, y_pred)
        auc_score = roc_auc_score(y_test, y_pred_proba)
        
        print(f"✅ Modelo treinado!")
        print(f"   Accuracy: {accuracy:.4f}")
        print(f"   AUC Score: {auc_score:.4f}")
        
        self.is_trained = True
        
        return X_test_scaled, y_test, y_pred, y_pred_proba
    
    def evaluate_model(self, X_test, y_test, y_pred, y_pred_proba):
        """
        Avalia performance do modelo
        """
        print("🔄 Avaliando modelo...")
        
        # Métricas de classificação
        print("\n📊 RELATÓRIO DE CLASSIFICAÇÃO:")
        print(classification_report(y_test, y_pred, target_names=['Normal', 'Anomalia']))
        
        # Matriz de confusão
        cm = confusion_matrix(y_test, y_pred)
        
        # Gráficos de avaliação
        self.plot_confusion_matrix(cm)
        self.plot_roc_curve(y_test, y_pred_proba)
        self.plot_feature_importance()
        
        return {
            'accuracy': accuracy_score(y_test, y_pred),
            'auc_score': roc_auc_score(y_test, y_pred_proba),
            'confusion_matrix': cm,
            'classification_report': classification_report(y_test, y_pred, output_dict=True)
        }
    
    def plot_confusion_matrix(self, cm):
        """
        Plota matriz de confusão
        """
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Normal', 'Anomalia'],
                   yticklabels=['Normal', 'Anomalia'])
        plt.title('Matriz de Confusão - Detecção de Anomalias', fontsize=14, fontweight='bold')
        plt.xlabel('Predição', fontsize=12)
        plt.ylabel('Valor Real', fontsize=12)
        plt.tight_layout()
        plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_roc_curve(self, y_test, y_pred_proba):
        """
        Plota curva ROC
        """
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        auc_score = roc_auc_score(y_test, y_pred_proba)
        
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, 
                label=f'ROC Curve (AUC = {auc_score:.4f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Taxa de Falsos Positivos', fontsize=12)
        plt.ylabel('Taxa de Verdadeiros Positivos', fontsize=12)
        plt.title('Curva ROC - Detecção de Anomalias', fontsize=14, fontweight='bold')
        plt.legend(loc="lower right")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('roc_curve.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_feature_importance(self):
        """
        Plota importância das features
        """
        if not self.is_trained:
            print("❌ Modelo não foi treinado ainda!")
            return
        
        feature_importance = self.model.feature_importances_
        feature_names = self.feature_columns
        
        # Ordenar por importância
        indices = np.argsort(feature_importance)[::-1]
        
        plt.figure(figsize=(10, 8))
        bars = plt.bar(range(len(feature_importance)), feature_importance[indices])
        plt.title('Importância das Features - Random Forest', fontsize=14, fontweight='bold')
        plt.xlabel('Features', fontsize=12)
        plt.ylabel('Importância', fontsize=12)
        plt.xticks(range(len(feature_names)), [feature_names[i] for i in indices], rotation=45)
        
        # Colorir barras
        colors = plt.cm.viridis(np.linspace(0, 1, len(bars)))
        for bar, color in zip(bars, colors):
            bar.set_color(color)
        
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_data_distribution(self, df):
        """
        Plota distribuição dos dados
        """
        print("🔄 Gerando visualizações dos dados...")
        
        # Configurar subplots
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Distribuição dos Dados IoT por Modo de Operação', fontsize=16, fontweight='bold')
        
        # Features principais
        features = ['temperature', 'humidity', 'pressure', 'vibration_mag', 'level', 'luminosity']
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
        
        for i, feature in enumerate(features):
            row = i // 3
            col = i % 3
            ax = axes[row, col]
            
            # Plotar distribuição por modo
            for mode, mode_name, color in [(0, 'Normal', '#2ECC71'), (1, 'Alerta', '#F39C12'), (2, 'Falha', '#E74C3C')]:
                data_mode = df[df['mode'] == mode][feature]
                ax.hist(data_mode, alpha=0.6, label=mode_name, color=color, bins=30)
            
            ax.set_title(f'Distribuição de {feature.title()}', fontweight='bold')
            ax.set_xlabel(feature.title())
            ax.set_ylabel('Frequência')
            ax.legend()
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('data_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_correlation_matrix(self, df):
        """
        Plota matriz de correlação
        """
        # Selecionar features numéricas
        numeric_features = df.select_dtypes(include=[np.number]).columns
        correlation_matrix = df[numeric_features].corr()
        
        plt.figure(figsize=(12, 10))
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
        sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
        plt.title('Matriz de Correlação - Features IoT', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('correlation_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def cross_validate_model(self, X, y, cv=5):
        """
        Validação cruzada do modelo
        """
        print(f"🔄 Executando validação cruzada ({cv} folds)...")
        
        X_scaled = self.scaler.fit_transform(X)
        
        # Validação cruzada
        cv_scores = cross_val_score(self.model, X_scaled, y, cv=cv, scoring='roc_auc')
        
        print(f"✅ Validação cruzada concluída!")
        print(f"   AUC Score médio: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        print(f"   Scores individuais: {cv_scores}")
        
        # Plotar resultados da validação cruzada
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, cv+1), cv_scores, 'o-', linewidth=2, markersize=8)
        plt.axhline(y=cv_scores.mean(), color='r', linestyle='--', 
                   label=f'Média: {cv_scores.mean():.4f}')
        plt.fill_between(range(1, cv+1), 
                        cv_scores.mean() - cv_scores.std(),
                        cv_scores.mean() + cv_scores.std(),
                        alpha=0.2, label=f'±1 std: {cv_scores.std():.4f}')
        plt.title('Validação Cruzada - AUC Score por Fold', fontsize=14, fontweight='bold')
        plt.xlabel('Fold', fontsize=12)
        plt.ylabel('AUC Score', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('cross_validation.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return cv_scores

def main():
    """
    Função principal para executar o pipeline completo
    """
    print("🚀 INICIANDO SISTEMA DE DETECÇÃO DE ANOMALIAS IoT")
    print("=" * 60)
    
    # Criar detector
    detector = IoTAnomalyDetector()
    
    # 1. Gerar dados sintéticos
    print("\n📊 FASE 1: GERAÇÃO DE DADOS")
    df = detector.generate_synthetic_data(n_samples=5000)
    
    # Visualizar distribuição dos dados
    detector.plot_data_distribution(df)
    detector.plot_correlation_matrix(df)
    
    # 2. Preparar features
    print("\n🔧 FASE 2: PREPARAÇÃO DE FEATURES")
    X, y = detector.prepare_features(df)
    
    # 3. Treinar modelo
    print("\n🤖 FASE 3: TREINAMENTO DO MODELO")
    X_test, y_test, y_pred, y_pred_proba = detector.train_model(X, y)
    
    # 4. Avaliar modelo
    print("\n📈 FASE 4: AVALIAÇÃO DO MODELO")
    metrics = detector.evaluate_model(X_test, y_test, y_pred, y_pred_proba)
    
    # 5. Validação cruzada
    print("\n🔄 FASE 5: VALIDAÇÃO CRUZADA")
    cv_scores = detector.cross_validate_model(X, y)
    
    # 6. Resumo final
    print("\n" + "=" * 60)
    print("📋 RESUMO FINAL")
    print("=" * 60)
    print(f"✅ Dataset: {len(df)} amostras, {len(df.columns)} features")
    print(f"✅ Accuracy: {metrics['accuracy']:.4f}")
    print(f"✅ AUC Score: {metrics['auc_score']:.4f}")
    print(f"✅ Validação Cruzada: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    print(f"✅ Gráficos salvos: confusion_matrix.png, roc_curve.png, feature_importance.png")
    print(f"✅ Visualizações: data_distribution.png, correlation_matrix.png, cross_validation.png")
    
    print("\n🎯 PROBLEMA RESOLVIDO:")
    print("   • Classificação de anomalias em dados IoT")
    print("   • Detecção de falhas em sensores ESP32")
    print("   • Sistema de alertas baseado em ML")
    print("   • Features: temperatura, umidade, pressão, vibração, nível, luminosidade")
    
    print("\n📊 DATASET UTILIZADO:")
    print("   • Dados sintéticos baseados em parâmetros reais")
    print("   • 3 modos de operação: Normal (70%), Alerta (20%), Falha (10%)")
    print("   • 5% de anomalias extremas adicionais")
    print("   • Features derivadas para melhor performance")
    
    return detector, df, metrics

if __name__ == "__main__":
    detector, df, metrics = main()
