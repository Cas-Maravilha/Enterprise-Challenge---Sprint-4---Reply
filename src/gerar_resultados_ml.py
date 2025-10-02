#!/usr/bin/env python3
"""
Script para gerar gráficos e resultados do modelo de Machine Learning
Sistema de Detecção de Anomalias IoT
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score, roc_curve
import warnings
warnings.filterwarnings('ignore')

# Configuração para gráficos
plt.style.use('default')
sns.set_palette("husl")

def gerar_dados_sinteticos(n_samples=2000):
    """Gera dados sintéticos para demonstração"""
    print("🔄 Gerando dados sintéticos...")
    
    np.random.seed(42)
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
        
        # Adicionar anomalias ocasionais
        if np.random.random() < 0.05:  # 5% de anomalia extrema
            temperature += np.random.normal(0, 10)
            humidity += np.random.normal(0, 20)
            pressure += np.random.normal(0, 2)
            vibration += np.random.normal(0, 1)
            level += np.random.normal(0, 30)
            luminosity += np.random.normal(0, 300)
            mode = 2
        
        vibration_mag = np.sqrt(vibration**2 + np.random.normal(0, 0.1)**2 + np.random.normal(0, 0.1)**2)
        
        data.append({
            'temperature': max(-40, min(80, temperature)),
            'humidity': max(0, min(100, humidity)),
            'pressure': max(0, min(10, pressure)),
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
    
    print(f"✅ Dados gerados: {len(df)} amostras")
    return df

def treinar_modelo(df):
    """Treina modelo de detecção de anomalias"""
    print("🔄 Treinando modelo...")
    
    # Selecionar features
    feature_columns = ['temperature', 'humidity', 'pressure', 'vibration_mag', 
                      'level', 'luminosity', 'movement', 'temp_humidity_ratio', 
                      'pressure_vibration', 'level_luminosity']
    
    X = df[feature_columns]
    y = df['anomaly']
    
    # Dividir dados
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Normalizar
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Treinar modelo
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42, class_weight='balanced')
    model.fit(X_train_scaled, y_train)
    
    # Predições
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    print("✅ Modelo treinado!")
    return model, scaler, X_test_scaled, y_test, y_pred, y_pred_proba, feature_columns

def plotar_distribuicao_dados(df):
    """Plota distribuição dos dados"""
    print("📊 Gerando gráfico de distribuição...")
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Distribuição dos Dados IoT por Modo de Operação', fontsize=16, fontweight='bold')
    
    features = ['temperature', 'humidity', 'pressure', 'vibration_mag', 'level', 'luminosity']
    
    for i, feature in enumerate(features):
        row = i // 3
        col = i % 3
        ax = axes[row, col]
        
        # Plotar por anomalia
        normal_data = df[df['anomaly'] == 0][feature]
        anomaly_data = df[df['anomaly'] == 1][feature]
        
        ax.hist(normal_data, alpha=0.7, label='Normal', bins=30, color='green')
        ax.hist(anomaly_data, alpha=0.7, label='Anomalia', bins=30, color='red')
        
        ax.set_title(f'Distribuição de {feature.title()}')
        ax.set_xlabel(feature.title())
        ax.set_ylabel('Frequência')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('distribuicao_dados_iot.png', dpi=300, bbox_inches='tight')
    plt.show()

def plotar_matriz_confusao(y_test, y_pred):
    """Plota matriz de confusão"""
    print("📊 Gerando matriz de confusão...")
    
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
               xticklabels=['Normal', 'Anomalia'],
               yticklabels=['Normal', 'Anomalia'])
    plt.title('Matriz de Confusão - Detecção de Anomalias IoT', fontsize=14, fontweight='bold')
    plt.xlabel('Predição')
    plt.ylabel('Valor Real')
    plt.tight_layout()
    plt.savefig('matriz_confusao_iot.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return cm

def plotar_curva_roc(y_test, y_pred_proba):
    """Plota curva ROC"""
    print("📊 Gerando curva ROC...")
    
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    auc_score = roc_auc_score(y_test, y_pred_proba)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, 
            label=f'ROC Curve (AUC = {auc_score:.4f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Classificador Aleatório')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Taxa de Falsos Positivos')
    plt.ylabel('Taxa de Verdadeiros Positivos')
    plt.title('Curva ROC - Detecção de Anomalias IoT', fontsize=14, fontweight='bold')
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('curva_roc_iot.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return auc_score

def plotar_importancia_features(model, feature_columns):
    """Plota importância das features"""
    print("📊 Gerando gráfico de importância das features...")
    
    feature_importance = model.feature_importances_
    indices = np.argsort(feature_importance)[::-1]
    
    plt.figure(figsize=(10, 8))
    bars = plt.bar(range(len(feature_importance)), feature_importance[indices])
    plt.title('Importância das Features - Random Forest', fontsize=14, fontweight='bold')
    plt.xlabel('Features')
    plt.ylabel('Importância')
    plt.xticks(range(len(feature_columns)), [feature_columns[i] for i in indices], rotation=45)
    
    # Colorir barras
    colors = plt.cm.viridis(np.linspace(0, 1, len(bars)))
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('importancia_features_iot.png', dpi=300, bbox_inches='tight')
    plt.show()

def plotar_metricas_performance(y_test, y_pred, y_pred_proba):
    """Plota métricas de performance"""
    print("📊 Gerando gráfico de métricas...")
    
    # Calcular métricas
    accuracy = accuracy_score(y_test, y_pred)
    auc_score = roc_auc_score(y_test, y_pred_proba)
    
    # Matriz de confusão para métricas
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    
    # Gráfico de métricas
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'Specificity', 'AUC']
    values = [accuracy, precision, recall, f1_score, specificity, auc_score]
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(metrics, values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'])
    plt.title('Métricas de Performance do Modelo', fontsize=14, fontweight='bold')
    plt.ylabel('Valor')
    plt.ylim(0, 1)
    
    # Adicionar valores nas barras
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
                f'{value:.3f}', ha='center', va='bottom', fontweight='bold')
    
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('metricas_performance_iot.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'specificity': specificity,
        'auc_score': auc_score
    }

def plotar_distribuicao_probabilidades(y_test, y_pred_proba):
    """Plota distribuição das probabilidades"""
    print("📊 Gerando gráfico de distribuição de probabilidades...")
    
    plt.figure(figsize=(12, 5))
    
    # Subplot 1: Distribuição geral
    plt.subplot(1, 2, 1)
    normal_probs = y_pred_proba[y_test == 0]
    anomaly_probs = y_pred_proba[y_test == 1]
    
    plt.hist(normal_probs, alpha=0.7, label='Normal', bins=30, color='green')
    plt.hist(anomaly_probs, alpha=0.7, label='Anomalia', bins=30, color='red')
    plt.xlabel('Probabilidade de Anomalia')
    plt.ylabel('Frequência')
    plt.title('Distribuição das Probabilidades')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Subplot 2: Boxplot
    plt.subplot(1, 2, 2)
    data_to_plot = [normal_probs, anomaly_probs]
    labels = ['Normal', 'Anomalia']
    
    plt.boxplot(data_to_plot, labels=labels)
    plt.ylabel('Probabilidade de Anomalia')
    plt.title('Boxplot das Probabilidades')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('distribuicao_probabilidades_iot.png', dpi=300, bbox_inches='tight')
    plt.show()

def gerar_relatorio_final(metrics):
    """Gera relatório final em texto"""
    print("\n" + "="*60)
    print("🎯 RELATÓRIO FINAL - DETECÇÃO DE ANOMALIAS IoT")
    print("="*60)
    print(f"📊 PROBLEMA: Classificação de anomalias em dados de sensores ESP32")
    print(f"🤖 MODELO: Random Forest Classifier")
    print(f"📈 DATASET: 2.000 amostras sintéticas baseadas em dados reais")
    print(f"🔧 FEATURES: 10 variáveis (temperatura, umidade, pressão, etc.)")
    print("\n📈 MÉTRICAS DE PERFORMANCE:")
    print(f"   • Accuracy: {metrics['accuracy']:.4f}")
    print(f"   • Precision: {metrics['precision']:.4f}")
    print(f"   • Recall: {metrics['recall']:.4f}")
    print(f"   • F1-Score: {metrics['f1_score']:.4f}")
    print(f"   • Specificity: {metrics['specificity']:.4f}")
    print(f"   • AUC Score: {metrics['auc_score']:.4f}")
    
    print(f"\n✅ APLICAÇÕES PRÁTICAS:")
    print(f"   • Sistema de alertas automáticos para sensores ESP32")
    print(f"   • Detecção precoce de falhas em equipamentos IoT")
    print(f"   • Otimização de manutenção preventiva")
    print(f"   • Redução de falsos positivos em monitoramento")
    
    print(f"\n📁 GRÁFICOS GERADOS:")
    print(f"   • distribuicao_dados_iot.png")
    print(f"   • matriz_confusao_iot.png")
    print(f"   • curva_roc_iot.png")
    print(f"   • importancia_features_iot.png")
    print(f"   • metricas_performance_iot.png")
    print(f"   • distribuicao_probabilidades_iot.png")
    
    print("="*60)

def main():
    """Função principal"""
    print("🚀 SISTEMA DE DETECÇÃO DE ANOMALIAS IoT")
    print("="*50)
    
    # 1. Gerar dados
    df = gerar_dados_sinteticos(2000)
    
    # 2. Treinar modelo
    model, scaler, X_test, y_test, y_pred, y_pred_proba, feature_columns = treinar_modelo(df)
    
    # 3. Gerar visualizações
    plotar_distribuicao_dados(df)
    cm = plotar_matriz_confusao(y_test, y_pred)
    auc_score = plotar_curva_roc(y_test, y_pred_proba)
    plotar_importancia_features(model, feature_columns)
    metrics = plotar_metricas_performance(y_test, y_pred, y_pred_proba)
    plotar_distribuicao_probabilidades(y_test, y_pred_proba)
    
    # 4. Relatório final
    gerar_relatorio_final(metrics)
    
    print("\n✅ Processo concluído com sucesso!")
    print("📊 Todos os gráficos foram salvos no diretório atual")

if __name__ == "__main__":
    main()
