#!/usr/bin/env python3
"""
Processo Completo de Treino do Modelo de Machine Learning
Sistema de Detecção de Anomalias IoT
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score, roc_curve
import warnings
warnings.filterwarnings('ignore')

# Configuração para gráficos
plt.style.use('default')
sns.set_palette("husl")

def gerar_dados_sinteticos(n_samples=2000):
    """
    Gera dataset sintético baseado nos dados reais do projeto IoT
    """
    print("🔄 FASE 1: GERAÇÃO DO DATASET")
    print("=" * 50)
    
    np.random.seed(42)
    data = []
    
    print(f"Gerando {n_samples} amostras sintéticas...")
    
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
        
        # Adicionar anomalias ocasionais (5% de chance)
        if np.random.random() < 0.05:
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
    
    print(f"✅ Dataset gerado com sucesso!")
    print(f"   • Total de amostras: {len(df)}")
    print(f"   • Total de features: {len(df.columns)}")
    print(f"   • Distribuição de anomalias: {df['anomaly'].value_counts().to_dict()}")
    print(f"   • Proporção de anomalias: {df['anomaly'].mean():.2%}")
    
    return df

def analisar_dados(df):
    """
    Análise exploratória dos dados
    """
    print("\n🔍 FASE 2: ANÁLISE EXPLORATÓRIA DOS DADOS")
    print("=" * 50)
    
    print("📊 Informações básicas do dataset:")
    print(f"   • Shape: {df.shape}")
    print(f"   • Tipos de dados: {df.dtypes.value_counts().to_dict()}")
    print(f"   • Valores nulos: {df.isnull().sum().sum()}")
    
    print("\n📈 Estatísticas descritivas:")
    print(df.describe().round(2))
    
    print("\n📊 Distribuição por classe:")
    print(f"   • Normal (0): {len(df[df['anomaly'] == 0])} amostras ({len(df[df['anomaly'] == 0])/len(df):.1%})")
    print(f"   • Anomalia (1): {len(df[df['anomaly'] == 1])} amostras ({len(df[df['anomaly'] == 1])/len(df):.1%})")
    
    # Visualizar distribuição dos dados
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Distribuição dos Dados IoT por Classe', fontsize=16, fontweight='bold')
    
    features = ['temperature', 'humidity', 'pressure', 'vibration_mag', 'level', 'luminosity']
    
    for i, feature in enumerate(features):
        row = i // 3
        col = i % 3
        ax = axes[row, col]
        
        # Plotar distribuição por classe
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
    plt.savefig('distribuicao_dados_treino.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return df

def preparar_dados(df):
    """
    Preparação dos dados para treinamento
    """
    print("\n🔧 FASE 3: PREPARAÇÃO DOS DADOS")
    print("=" * 50)
    
    # Selecionar features para treinamento
    feature_columns = [
        'temperature', 'humidity', 'pressure', 'vibration_mag', 
        'level', 'luminosity', 'movement',
        'temp_humidity_ratio', 'pressure_vibration', 'level_luminosity'
    ]
    
    print(f"Features selecionadas para treinamento:")
    for i, feature in enumerate(feature_columns, 1):
        print(f"   {i:2d}. {feature}")
    
    # Separar features e target
    X = df[feature_columns].copy()
    y = df['anomaly'].copy()
    
    print(f"\n📊 Informações das features:")
    print(f"   • Shape X: {X.shape}")
    print(f"   • Shape y: {y.shape}")
    print(f"   • Distribuição do target: {y.value_counts().to_dict()}")
    
    # Tratar valores infinitos e NaN
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(X.median())
    
    print(f"   • Valores infinitos tratados: {np.isinf(X).sum().sum()}")
    print(f"   • Valores NaN tratados: {X.isnull().sum().sum()}")
    
    return X, y, feature_columns

def dividir_dados(X, y):
    """
    Divisão dos dados em treino e teste
    """
    print("\n📊 FASE 4: DIVISÃO DOS DADOS")
    print("=" * 50)
    
    # Dividir dados
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Divisão dos dados:")
    print(f"   • Treino: {X_train.shape[0]} amostras ({X_train.shape[0]/len(X):.1%})")
    print(f"   • Teste: {X_test.shape[0]} amostras ({X_test.shape[0]/len(X):.1%})")
    print(f"   • Features: {X_train.shape[1]}")
    
    print(f"\nDistribuição do target:")
    print(f"   • Treino - Normal: {len(y_train[y_train == 0])} ({len(y_train[y_train == 0])/len(y_train):.1%})")
    print(f"   • Treino - Anomalia: {len(y_train[y_train == 1])} ({len(y_train[y_train == 1])/len(y_train):.1%})")
    print(f"   • Teste - Normal: {len(y_test[y_test == 0])} ({len(y_test[y_test == 0])/len(y_test):.1%})")
    print(f"   • Teste - Anomalia: {len(y_test[y_test == 1])} ({len(y_test[y_test == 1])/len(y_test):.1%})")
    
    return X_train, X_test, y_train, y_test

def normalizar_dados(X_train, X_test):
    """
    Normalização dos dados
    """
    print("\n🔧 FASE 5: NORMALIZAÇÃO DOS DADOS")
    print("=" * 50)
    
    # Criar e treinar scaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print("Normalização aplicada:")
    print(f"   • Método: StandardScaler (média=0, std=1)")
    print(f"   • Treino normalizado: {X_train_scaled.shape}")
    print(f"   • Teste normalizado: {X_test_scaled.shape}")
    
    # Verificar normalização
    print(f"\nVerificação da normalização:")
    print(f"   • Média treino: {X_train_scaled.mean():.6f}")
    print(f"   • Desvio padrão treino: {X_train_scaled.std():.6f}")
    print(f"   • Média teste: {X_test_scaled.mean():.6f}")
    print(f"   • Desvio padrão teste: {X_test_scaled.std():.6f}")
    
    return X_train_scaled, X_test_scaled, scaler

def treinar_modelo(X_train_scaled, y_train):
    """
    Treinamento do modelo Random Forest
    """
    print("\n🤖 FASE 6: TREINAMENTO DO MODELO")
    print("=" * 50)
    
    # Criar modelo
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        class_weight='balanced'
    )
    
    print("Parâmetros do modelo Random Forest:")
    print(f"   • n_estimators: {model.n_estimators}")
    print(f"   • max_depth: {model.max_depth}")
    print(f"   • min_samples_split: {model.min_samples_split}")
    print(f"   • min_samples_leaf: {model.min_samples_leaf}")
    print(f"   • class_weight: {model.class_weight}")
    print(f"   • random_state: {model.random_state}")
    
    # Treinar modelo
    print(f"\n🔄 Iniciando treinamento...")
    model.fit(X_train_scaled, y_train)
    print(f"✅ Modelo treinado com sucesso!")
    
    # Informações do modelo treinado
    print(f"\n📊 Informações do modelo treinado:")
    print(f"   • Número de árvores: {len(model.estimators_)}")
    print(f"   • Features importantes: {len(model.feature_importances_)}")
    print(f"   • Classes: {model.classes_}")
    print(f"   • Número de features: {model.n_features_in_}")
    
    return model

def validar_modelo(model, X_train_scaled, y_train):
    """
    Validação cruzada do modelo
    """
    print("\n🔄 FASE 7: VALIDAÇÃO CRUZADA")
    print("=" * 50)
    
    # Validação cruzada
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='roc_auc')
    
    print(f"Validação cruzada (5 folds):")
    print(f"   • Scores individuais: {cv_scores}")
    print(f"   • Score médio: {cv_scores.mean():.4f}")
    print(f"   • Desvio padrão: {cv_scores.std():.4f}")
    print(f"   • Intervalo de confiança: {cv_scores.mean():.4f} ± {cv_scores.std() * 2:.4f}")
    
    # Plotar resultados da validação cruzada
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 6), cv_scores, 'o-', linewidth=2, markersize=8, color='blue')
    plt.axhline(y=cv_scores.mean(), color='r', linestyle='--', 
               label=f'Média: {cv_scores.mean():.4f}')
    plt.fill_between(range(1, 6), 
                    cv_scores.mean() - cv_scores.std(),
                    cv_scores.mean() + cv_scores.std(),
                    alpha=0.2, label=f'±1 std: {cv_scores.std():.4f}')
    plt.title('Validação Cruzada - AUC Score por Fold', fontsize=14, fontweight='bold')
    plt.xlabel('Fold')
    plt.ylabel('AUC Score')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('validacao_cruzada_treino.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return cv_scores

def avaliar_modelo(model, X_test_scaled, y_test, feature_columns):
    """
    Avaliação do modelo no conjunto de teste
    """
    print("\n📈 FASE 8: AVALIAÇÃO DO MODELO")
    print("=" * 50)
    
    # Fazer predições
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    print("Predições realizadas:")
    print(f"   • Predições: {len(y_pred)}")
    print(f"   • Probabilidades: {len(y_pred_proba)}")
    print(f"   • Classes preditas: {np.unique(y_pred)}")
    
    # Calcular métricas
    accuracy = accuracy_score(y_test, y_pred)
    auc_score = roc_auc_score(y_test, y_pred_proba)
    
    # Matriz de confusão
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
    
    print(f"\n📊 Métricas de performance:")
    print(f"   • Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"   • Precision: {precision:.4f} ({precision*100:.2f}%)")
    print(f"   • Recall: {recall:.4f} ({recall*100:.2f}%)")
    print(f"   • F1-Score: {f1_score:.4f} ({f1_score*100:.2f}%)")
    print(f"   • Specificity: {specificity:.4f} ({specificity*100:.2f}%)")
    print(f"   • AUC Score: {auc_score:.4f} ({auc_score*100:.2f}%)")
    
    print(f"\n📊 Matriz de confusão:")
    print(f"   • Verdadeiros Negativos (TN): {tn}")
    print(f"   • Falsos Positivos (FP): {fp}")
    print(f"   • Falsos Negativos (FN): {fn}")
    print(f"   • Verdadeiros Positivos (TP): {tp}")
    
    # Relatório de classificação
    print(f"\n📋 Relatório de classificação:")
    print(classification_report(y_test, y_pred, target_names=['Normal', 'Anomalia']))
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'specificity': specificity,
        'auc_score': auc_score,
        'confusion_matrix': cm,
        'y_pred': y_pred,
        'y_pred_proba': y_pred_proba
    }

def plotar_resultados(model, X_test_scaled, y_test, y_pred, y_pred_proba, feature_columns):
    """
    Plotar gráficos dos resultados
    """
    print("\n📊 FASE 9: VISUALIZAÇÃO DOS RESULTADOS")
    print("=" * 50)
    
    # Matriz de confusão
    cm = confusion_matrix(y_test, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
               xticklabels=['Normal', 'Anomalia'],
               yticklabels=['Normal', 'Anomalia'])
    plt.title('Matriz de Confusão - Detecção de Anomalias IoT', fontsize=14, fontweight='bold')
    plt.xlabel('Predição')
    plt.ylabel('Valor Real')
    plt.tight_layout()
    plt.savefig('matriz_confusao_treino.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Curva ROC
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
    plt.savefig('curva_roc_treino.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Importância das features
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
    plt.savefig('importancia_features_treino.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Distribuição das probabilidades
    plt.figure(figsize=(12, 5))
    
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
    
    plt.subplot(1, 2, 2)
    data_to_plot = [normal_probs, anomaly_probs]
    labels = ['Normal', 'Anomalia']
    
    plt.boxplot(data_to_plot, labels=labels)
    plt.ylabel('Probabilidade de Anomalia')
    plt.title('Boxplot das Probabilidades')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('distribuicao_probabilidades_treino.png', dpi=300, bbox_inches='tight')
    plt.show()

def salvar_modelo(model, scaler, feature_columns, metrics):
    """
    Salvar modelo e metadados
    """
    print("\n💾 FASE 10: SALVAMENTO DO MODELO")
    print("=" * 50)
    
    import joblib
    import json
    from datetime import datetime
    
    # Salvar modelo e scaler
    joblib.dump(model, 'iot_anomaly_model.pkl')
    joblib.dump(scaler, 'iot_scaler.pkl')
    
    # Salvar metadados
    model_metadata = {
        'model_name': 'IoT Anomaly Detection',
        'version': '1.0',
        'created_date': datetime.now().isoformat(),
        'features': feature_columns,
        'performance': {
            'accuracy': float(metrics['accuracy']),
            'precision': float(metrics['precision']),
            'recall': float(metrics['recall']),
            'f1_score': float(metrics['f1_score']),
            'specificity': float(metrics['specificity']),
            'auc_score': float(metrics['auc_score'])
        },
        'feature_importance': dict(zip(feature_columns, model.feature_importances_.tolist()))
    }
    
    with open('model_metadata.json', 'w') as f:
        json.dump(model_metadata, f, indent=2)
    
    print("Arquivos salvos:")
    print("   • iot_anomaly_model.pkl - Modelo treinado")
    print("   • iot_scaler.pkl - Scaler para normalização")
    print("   • model_metadata.json - Metadados do modelo")
    
    return model_metadata

def main():
    """
    Função principal - Processo completo de treino
    """
    print("🚀 PROCESSO COMPLETO DE TREINO DO MODELO ML")
    print("Sistema de Detecção de Anomalias IoT")
    print("=" * 60)
    
    # Fase 1: Gerar dados
    df = gerar_dados_sinteticos(2000)
    
    # Fase 2: Analisar dados
    df = analisar_dados(df)
    
    # Fase 3: Preparar dados
    X, y, feature_columns = preparar_dados(df)
    
    # Fase 4: Dividir dados
    X_train, X_test, y_train, y_test = dividir_dados(X, y)
    
    # Fase 5: Normalizar dados
    X_train_scaled, X_test_scaled, scaler = normalizar_dados(X_train, X_test)
    
    # Fase 6: Treinar modelo
    model = treinar_modelo(X_train_scaled, y_train)
    
    # Fase 7: Validar modelo
    cv_scores = validar_modelo(model, X_train_scaled, y_train)
    
    # Fase 8: Avaliar modelo
    metrics = avaliar_modelo(model, X_test_scaled, y_test, feature_columns)
    
    # Fase 9: Plotar resultados
    plotar_resultados(model, X_test_scaled, y_test, metrics['y_pred'], 
                     metrics['y_pred_proba'], feature_columns)
    
    # Fase 10: Salvar modelo
    model_metadata = salvar_modelo(model, scaler, feature_columns, metrics)
    
    # Resumo final
    print("\n" + "=" * 60)
    print("🎯 RESUMO FINAL DO TREINAMENTO")
    print("=" * 60)
    print(f"✅ Modelo treinado com sucesso!")
    print(f"📊 Performance:")
    print(f"   • Accuracy: {metrics['accuracy']:.4f}")
    print(f"   • Precision: {metrics['precision']:.4f}")
    print(f"   • Recall: {metrics['recall']:.4f}")
    print(f"   • F1-Score: {metrics['f1_score']:.4f}")
    print(f"   • AUC Score: {metrics['auc_score']:.4f}")
    print(f"   • Validação Cruzada: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
    
    print(f"\n📁 Arquivos gerados:")
    print(f"   • Gráficos: distribuicao_dados_treino.png, matriz_confusao_treino.png, etc.")
    print(f"   • Modelo: iot_anomaly_model.pkl")
    print(f"   • Scaler: iot_scaler.pkl")
    print(f"   • Metadados: model_metadata.json")
    
    print(f"\n🚀 Modelo pronto para implementação em produção!")
    
    return model, scaler, metrics, model_metadata

if __name__ == "__main__":
    model, scaler, metrics, metadata = main()
