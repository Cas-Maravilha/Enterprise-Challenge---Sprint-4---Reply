#!/usr/bin/env python3
"""
Script para treinar o modelo ML usando datasets CSV
Sistema de Detecção de Anomalias IoT
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (classification_report, confusion_matrix, accuracy_score, 
                           precision_score, recall_score, f1_score, roc_auc_score, 
                           roc_curve, precision_recall_curve, average_precision_score)
import joblib
import warnings
warnings.filterwarnings('ignore')

def carregar_dataset_csv(arquivo_csv):
    """
    Carrega dataset CSV e prepara para treinamento
    """
    print(f"📂 Carregando dataset: {arquivo_csv}")
    
    try:
        df = pd.read_csv(arquivo_csv)
        print(f"   ✅ Dataset carregado: {len(df)} amostras")
        print(f"   • Colunas: {len(df.columns)}")
        print(f"   • Período: {df['timestamp'].min()} a {df['timestamp'].max()}")
        
        return df
    except FileNotFoundError:
        print(f"   ❌ Arquivo não encontrado: {arquivo_csv}")
        return None
    except Exception as e:
        print(f"   ❌ Erro ao carregar: {e}")
        return None

def preparar_dados_ml(df):
    """
    Prepara dados para treinamento de ML
    """
    print("🔧 Preparando dados para ML...")
    
    # Selecionar features numéricas
    feature_columns = [
        'temperature', 'humidity', 'pressure', 'vibration_mag',
        'level', 'luminosity', 'movement', 'co2', 'noise',
        'temp_humidity_ratio', 'pressure_vibration', 'level_luminosity',
        'temp_pressure_ratio', 'humidity_level_ratio', 'co2_noise_ratio'
    ]
    
    # Verificar se todas as features existem
    missing_features = set(feature_columns) - set(df.columns)
    if missing_features:
        print(f"   ⚠️ Features ausentes: {missing_features}")
        return None, None, None
    
    X = df[feature_columns].copy()
    y = df['anomaly'].copy()
    
    # Tratar valores infinitos e nulos
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(X.median())
    
    print(f"   • Features: {X.shape[1]}")
    print(f"   • Amostras: {X.shape[0]}")
    print(f"   • Distribuição: {y.value_counts().to_dict()}")
    
    return X, y, feature_columns

def treinar_modelo_csv(X, y, feature_columns):
    """
    Treina modelo usando dados CSV
    """
    print("🤖 Treinando modelo com dados CSV...")
    
    # Dividir dados
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Normalizar dados
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Treinar Random Forest
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight='balanced'
    )
    
    rf_model.fit(X_train_scaled, y_train)
    
    # Fazer predições
    y_pred = rf_model.predict(X_test_scaled)
    y_pred_proba = rf_model.predict_proba(X_test_scaled)[:, 1]
    
    # Calcular métricas
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_pred_proba)
    
    print(f"✅ Modelo treinado com sucesso!")
    print(f"   • Accuracy: {accuracy:.4f}")
    print(f"   • Precision: {precision:.4f}")
    print(f"   • Recall: {recall:.4f}")
    print(f"   • F1-Score: {f1:.4f}")
    print(f"   • AUC: {auc:.4f}")
    
    return rf_model, scaler, feature_columns, X_test, y_test, y_pred, y_pred_proba

def plotar_resultados_csv(X_test, y_test, y_pred, y_pred_proba, feature_columns, rf_model):
    """
    Plota resultados do modelo treinado com CSV
    """
    print("📊 Gerando visualizações...")
    
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('Resultados do Modelo ML - Dataset CSV', fontsize=16, fontweight='bold')
    
    # 1. Matriz de confusão
    ax1 = axes[0, 0]
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
               xticklabels=['Normal', 'Anomalia'],
               yticklabels=['Normal', 'Anomalia'], ax=ax1)
    ax1.set_title('Matriz de Confusão', fontweight='bold')
    ax1.set_xlabel('Predição')
    ax1.set_ylabel('Valor Real')
    
    # 2. Curva ROC
    ax2 = axes[0, 1]
    fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
    auc_score = roc_auc_score(y_test, y_pred_proba)
    ax2.plot(fpr, tpr, color='darkorange', lw=2, 
            label=f'ROC Curve (AUC = {auc_score:.4f})')
    ax2.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
    ax2.set_xlim([0.0, 1.0])
    ax2.set_ylim([0.0, 1.05])
    ax2.set_xlabel('Taxa de Falsos Positivos')
    ax2.set_ylabel('Taxa de Verdadeiros Positivos')
    ax2.set_title('Curva ROC', fontweight='bold')
    ax2.legend(loc="lower right")
    ax2.grid(True, alpha=0.3)
    
    # 3. Curva Precision-Recall
    ax3 = axes[0, 2]
    precision_curve, recall_curve, _ = precision_recall_curve(y_test, y_pred_proba)
    ap_score = average_precision_score(y_test, y_pred_proba)
    ax3.plot(recall_curve, precision_curve, color='darkorange', lw=2,
            label=f'PR Curve (AP = {ap_score:.4f})')
    ax3.set_xlim([0.0, 1.0])
    ax3.set_ylim([0.0, 1.05])
    ax3.set_xlabel('Recall')
    ax3.set_ylabel('Precision')
    ax3.set_title('Curva Precision-Recall', fontweight='bold')
    ax3.legend(loc="lower left")
    ax3.grid(True, alpha=0.3)
    
    # 4. Importância das features
    ax4 = axes[1, 0]
    feature_importance = rf_model.feature_importances_
    indices = np.argsort(feature_importance)[::-1]
    bars = ax4.bar(range(len(feature_importance)), feature_importance[indices])
    ax4.set_title('Importância das Features', fontweight='bold')
    ax4.set_xlabel('Features')
    ax4.set_ylabel('Importância')
    ax4.set_xticks(range(len(feature_columns)))
    ax4.set_xticklabels([feature_columns[i] for i in indices], rotation=45, ha='right')
    
    # Colorir barras
    colors = plt.cm.viridis(np.linspace(0, 1, len(bars)))
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    ax4.grid(True, alpha=0.3, axis='y')
    
    # 5. Distribuição das predições
    ax5 = axes[1, 1]
    ax5.hist(y_pred_proba[y_test == 0], bins=30, alpha=0.7, label='Normal', color='blue')
    ax5.hist(y_pred_proba[y_test == 1], bins=30, alpha=0.7, label='Anomalia', color='red')
    ax5.set_xlabel('Probabilidade de Anomalia')
    ax5.set_ylabel('Frequência')
    ax5.set_title('Distribuição das Predições', fontweight='bold')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # 6. Métricas de performance
    ax6 = axes[1, 2]
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC']
    values = [
        accuracy_score(y_test, y_pred),
        precision_score(y_test, y_pred),
        recall_score(y_test, y_pred),
        f1_score(y_test, y_pred),
        roc_auc_score(y_test, y_pred_proba)
    ]
    bars = ax6.bar(metrics, values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
    ax6.set_title('Métricas de Performance', fontweight='bold')
    ax6.set_ylabel('Score')
    ax6.set_xticklabels(metrics, rotation=45)
    
    # Adicionar valores nas barras
    for bar, value in zip(bars, values):
        ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{value:.3f}', ha='center', va='bottom')
    
    ax6.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('resultados_modelo_csv.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Visualizações salvas como: resultados_modelo_csv.png")

def salvar_modelo_csv(rf_model, scaler, feature_columns, filename='modelo_anomalia_csv.pkl'):
    """
    Salva o modelo treinado com dados CSV
    """
    print(f"💾 Salvando modelo: {filename}")
    
    model_data = {
        'model': rf_model,
        'scaler': scaler,
        'feature_columns': feature_columns,
        'trained_with_csv': True
    }
    
    joblib.dump(model_data, filename)
    print(f"✅ Modelo salvo: {filename}")

def main():
    """
    Função principal para treinar modelo com CSV
    """
    print("🚀 TREINAMENTO DE MODELO ML COM DATASET CSV")
    print("=" * 60)
    
    # Verificar se o dataset existe
    dataset_file = 'datasets/iot_sensor_data_completo.csv'
    
    if not os.path.exists(dataset_file):
        print(f"❌ Dataset não encontrado: {dataset_file}")
        print("   Execute primeiro: python gerar_dataset_csv_ml.py")
        return
    
    # Carregar dataset
    df = carregar_dataset_csv(dataset_file)
    if df is None:
        return
    
    # Preparar dados
    X, y, feature_columns = preparar_dados_ml(df)
    if X is None:
        return
    
    # Treinar modelo
    rf_model, scaler, feature_columns, X_test, y_test, y_pred, y_pred_proba = treinar_modelo_csv(X, y, feature_columns)
    
    # Plotar resultados
    plotar_resultados_csv(X_test, y_test, y_pred, y_pred_proba, feature_columns, rf_model)
    
    # Salvar modelo
    salvar_modelo_csv(rf_model, scaler, feature_columns)
    
    # Relatório final
    print(f"\n📋 RELATÓRIO FINAL - MODELO TREINADO COM CSV")
    print("=" * 60)
    print(f"📊 MÉTRICAS PRINCIPAIS:")
    print(f"   • Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"   • Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"   • Recall: {recall_score(y_test, y_pred):.4f}")
    print(f"   • F1-Score: {f1_score(y_test, y_pred):.4f}")
    print(f"   • AUC: {roc_auc_score(y_test, y_pred_proba):.4f}")
    
    print(f"\n📁 ARQUIVOS GERADOS:")
    print(f"   • resultados_modelo_csv.png - Visualizações")
    print(f"   • modelo_anomalia_csv.pkl - Modelo treinado")
    
    print(f"\n✅ MODELO TREINADO COM SUCESSO USANDO DATASET CSV!")
    print("   • Dataset carregado e processado")
    print("   • Modelo treinado e validado")
    print("   • Visualizações geradas")
    print("   • Modelo salvo para uso")

if __name__ == "__main__":
    import os
    main()