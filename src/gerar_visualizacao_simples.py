#!/usr/bin/env python3
"""
Script para gerar visualização simples do resultado do modelo
Sistema de Detecção de Anomalias IoT
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (confusion_matrix, accuracy_score, 
                           precision_score, recall_score, f1_score, roc_auc_score)
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo dos gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def gerar_dados_demonstracao():
    """
    Gera dados de demonstração para visualização
    """
    print("🔄 Gerando dados de demonstração...")
    
    np.random.seed(42)
    data = []
    
    # Gerar 1000 amostras para demonstração
    for i in range(1000):
        # Simular diferentes modos de operação
        mode = np.random.choice([0, 1], p=[0.8, 0.2])  # 80% normal, 20% anomalia
        
        if mode == 0:  # Normal
            temperature = np.random.normal(25.0, 2.0)
            humidity = np.random.normal(60.0, 5.0)
            pressure = np.random.normal(1.013, 0.01)
            vibration = np.random.normal(0.1, 0.05)
            level = np.random.normal(100.0, 10.0)
            luminosity = np.random.normal(500.0, 100.0)
            movement = np.random.choice([0, 1], p=[0.9, 0.1])
            co2 = np.random.normal(400.0, 50.0)
            noise = np.random.normal(45.0, 5.0)
        else:  # Anomalia
            temperature = np.random.normal(35.0, 5.0)
            humidity = np.random.normal(85.0, 10.0)
            pressure = np.random.normal(1.030, 0.05)
            vibration = np.random.normal(1.0, 0.3)
            level = np.random.normal(150.0, 25.0)
            luminosity = np.random.normal(800.0, 200.0)
            movement = np.random.choice([0, 1], p=[0.5, 0.5])
            co2 = np.random.normal(1500.0, 300.0)
            noise = np.random.normal(75.0, 15.0)
        
        data.append({
            'temperature': max(-40, min(80, round(temperature, 2))),
            'humidity': max(0, min(100, round(humidity, 2))),
            'pressure': max(0, min(2, round(pressure, 3))),
            'vibration_mag': max(0, min(5, round(vibration, 3))),
            'level': max(0, min(200, round(level, 1))),
            'luminosity': max(0, min(1023, round(luminosity, 0))),
            'movement': int(movement),
            'co2': max(0, min(5000, round(co2, 0))),
            'noise': max(30, min(120, round(noise, 1))),
            'anomaly': mode
        })
    
    df = pd.DataFrame(data)
    print(f"✅ Dados gerados: {len(df)} amostras")
    print(f"   • Normal: {len(df[df['anomaly'] == 0])} amostras")
    print(f"   • Anomalia: {len(df[df['anomaly'] == 1])} amostras")
    
    return df

def treinar_modelo_simples(df):
    """
    Treina modelo simples para demonstração
    """
    print("🤖 Treinando modelo simples...")
    
    # Preparar dados
    feature_columns = [
        'temperature', 'humidity', 'pressure', 'vibration_mag',
        'level', 'luminosity', 'movement', 'co2', 'noise'
    ]
    
    X = df[feature_columns].copy()
    y = df['anomaly'].copy()
    
    # Dividir dados
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Normalizar dados
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Treinar modelo
    model = RandomForestClassifier(
        n_estimators=50,
        max_depth=8,
        random_state=42,
        class_weight='balanced'
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Fazer predições
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    # Calcular métricas
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_pred_proba)
    
    print(f"✅ Modelo treinado!")
    print(f"   • Accuracy: {accuracy:.4f}")
    print(f"   • Precision: {precision:.4f}")
    print(f"   • Recall: {recall:.4f}")
    print(f"   • F1-Score: {f1:.4f}")
    print(f"   • AUC: {auc:.4f}")
    
    return model, scaler, feature_columns, X_test, y_test, y_pred, y_pred_proba

def gerar_visualizacao_justificada(X_test, y_test, y_pred, y_pred_proba, feature_columns, model):
    """
    Gera visualização simples e justificada do resultado
    """
    print("📊 Gerando visualização simples e justificada...")
    
    # Criar figura com subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Visualização Simples - Resultados do Modelo de Detecção de Anomalias IoT', 
                fontsize=16, fontweight='bold')
    
    # 1. MATRIZ DE CONFUSÃO (Gráfico Principal)
    ax1 = axes[0, 0]
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
               xticklabels=['Normal', 'Anomalia'],
               yticklabels=['Normal', 'Anomalia'], ax=ax1)
    ax1.set_title('Matriz de Confusão', fontweight='bold', fontsize=14)
    ax1.set_xlabel('Predição', fontsize=12)
    ax1.set_ylabel('Valor Real', fontsize=12)
    
    # Adicionar valores percentuais
    total = cm.sum()
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            percentage = (cm[i, j] / total) * 100
            ax1.text(j + 0.5, i + 0.7, f'({percentage:.1f}%)', 
                   ha='center', va='center', fontsize=10, color='red')
    
    # 2. GRÁFICO DE BARRAS - MÉTRICAS DE PERFORMANCE
    ax2 = axes[0, 1]
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    values = [
        accuracy_score(y_test, y_pred),
        precision_score(y_test, y_pred),
        recall_score(y_test, y_pred),
        f1_score(y_test, y_pred)
    ]
    
    bars = ax2.bar(metrics, values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    ax2.set_title('Métricas de Performance', fontweight='bold', fontsize=14)
    ax2.set_ylabel('Score', fontsize=12)
    ax2.set_ylim([0, 1.1])
    
    # Adicionar valores nas barras
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{value:.3f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # Adicionar linha de referência
    ax2.axhline(y=0.9, color='red', linestyle='--', alpha=0.7, label='Referência (0.9)')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. SCATTER PLOT - DISTRIBUIÇÃO DAS PREDIÇÕES
    ax3 = axes[1, 0]
    
    # Separar dados por classe real
    normal_indices = y_test == 0
    anomaly_indices = y_test == 1
    
    # Plotar pontos normais
    ax3.scatter(y_pred_proba[normal_indices], 
               np.random.normal(0, 0.1, np.sum(normal_indices)), 
               alpha=0.6, label='Normal', color='blue', s=30)
    
    # Plotar pontos com anomalia
    ax3.scatter(y_pred_proba[anomaly_indices], 
               np.random.normal(1, 0.1, np.sum(anomaly_indices)), 
               alpha=0.6, label='Anomalia', color='red', s=30)
    
    # Adicionar linha de threshold
    ax3.axvline(x=0.5, color='black', linestyle='--', alpha=0.7, label='Threshold (0.5)')
    
    ax3.set_title('Distribuição das Predições', fontweight='bold', fontsize=14)
    ax3.set_xlabel('Probabilidade de Anomalia', fontsize=12)
    ax3.set_ylabel('Classe Real', fontsize=12)
    ax3.set_yticks([0, 1])
    ax3.set_yticklabels(['Normal', 'Anomalia'])
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. GRÁFICO DE LINHAS - IMPORTÂNCIA DAS FEATURES
    ax4 = axes[1, 1]
    feature_importance = model.feature_importances_
    indices = np.argsort(feature_importance)[::-1]
    
    # Plotar importância das features
    ax4.plot(range(len(feature_importance)), feature_importance[indices], 
            marker='o', linewidth=2, markersize=6)
    ax4.set_title('Importância das Features', fontweight='bold', fontsize=14)
    ax4.set_xlabel('Features', fontsize=12)
    ax4.set_ylabel('Importância', fontsize=12)
    ax4.set_xticks(range(len(feature_columns)))
    ax4.set_xticklabels([feature_columns[i] for i in indices], rotation=45, ha='right')
    
    # Adicionar valores nos pontos
    for i, (x, y) in enumerate(zip(range(len(feature_importance)), feature_importance[indices])):
        ax4.annotate(f'{y:.3f}', (x, y), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontsize=9)
    
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('visualizacao_simples_resultado.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("   ✅ Visualização salva como: visualizacao_simples_resultado.png")

def gerar_justificativa_visualizacao():
    """
    Gera justificativa da escolha dos gráficos
    """
    print("📋 Gerando justificativa da visualização...")
    
    justificativa = """
# JUSTIFICATIVA DA VISUALIZAÇÃO SIMPLES - RESULTADOS DO MODELO IoT

## 🎯 Objetivo da Visualização
Criar uma visualização simples e clara dos resultados do modelo de detecção de anomalias IoT, 
permitindo interpretação rápida e eficaz das métricas de performance.

## 📊 Gráficos Escolhidos e Justificativas

### 1. **MATRIZ DE CONFUSÃO** (Gráfico Principal)
**Tipo**: Heatmap com valores numéricos e percentuais

**Justificativa**:
- **Clareza**: Mostra diretamente quantas predições foram corretas/incorretas
- **Interpretabilidade**: Fácil de entender para qualquer público
- **Completude**: Inclui todos os tipos de erro (FP, FN, TP, TN)
- **Visualização**: Cores e anotações facilitam a leitura
- **Percentuais**: Valores relativos ajudam na interpretação

**Por que não outros gráficos**:
- Gráfico de barras: Não mostra a relação entre classes
- Scatter plot: Não é adequado para dados categóricos
- Gráfico de linha: Não representa matriz de confusão

### 2. **GRÁFICO DE BARRAS - MÉTRICAS DE PERFORMANCE**
**Tipo**: Barras horizontais com valores anotados

**Justificativa**:
- **Comparação**: Fácil comparação entre diferentes métricas
- **Valores**: Números exatos anotados nas barras
- **Referência**: Linha de referência (0.9) para contexto
- **Cores**: Diferentes cores para cada métrica
- **Escala**: Eixo Y de 0 a 1.1 para visualização clara

**Por que não outros gráficos**:
- Gráfico de pizza: Difícil comparar valores próximos
- Gráfico de linha: Não adequado para métricas independentes
- Scatter plot: Não representa métricas de performance

### 3. **SCATTER PLOT - DISTRIBUIÇÃO DAS PREDIÇÕES**
**Tipo**: Pontos dispersos com separação por classe

**Justificativa**:
- **Distribuição**: Mostra como as probabilidades se distribuem
- **Separação**: Visualiza a capacidade de discriminação do modelo
- **Threshold**: Linha de decisão (0.5) claramente marcada
- **Ruído**: Adiciona realismo à visualização
- **Interpretação**: Fácil identificar sobreposições

**Por que não outros gráficos**:
- Histograma: Não mostra separação por classe
- Gráfico de barras: Não representa distribuição contínua
- Box plot: Não mostra distribuição individual

### 4. **GRÁFICO DE LINHAS - IMPORTÂNCIA DAS FEATURES**
**Tipo**: Linha com pontos marcados e valores anotados

**Justificativa**:
- **Ranking**: Mostra ordem de importância das features
- **Valores**: Números exatos anotados nos pontos
- **Tendência**: Linha mostra a curva de importância
- **Interpretação**: Fácil identificar features mais importantes
- **Comparação**: Comparação visual entre features

**Por que não outros gráficos**:
- Gráfico de barras: Não mostra ranking visual
- Gráfico de pizza: Difícil comparar valores próximos
- Scatter plot: Não mostra ordenação

## 🎨 Elementos Visuais Escolhidos

### **Cores**
- **Azul**: Normal/Accuracy (confiabilidade)
- **Laranja**: Precision (precisão)
- **Verde**: Recall (cobertura)
- **Vermelho**: Anomalia/F1-Score (alerta)

### **Anotações**
- **Valores numéricos**: Para precisão
- **Percentuais**: Para contexto relativo
- **Linhas de referência**: Para benchmarks
- **Legendas**: Para clareza

### **Layout**
- **2x2**: Organização equilibrada
- **Tamanho**: 15x12 para clareza
- **DPI**: 300 para qualidade de impressão
- **Espaçamento**: Tight layout para aproveitamento do espaço

## 📈 Interpretação dos Resultados

### **Matriz de Confusão**
- **Verdadeiros Positivos**: Anomalias detectadas corretamente
- **Falsos Positivos**: Normais classificados como anomalias
- **Verdadeiros Negativos**: Normais classificados corretamente
- **Falsos Negativos**: Anomalias não detectadas

### **Métricas de Performance**
- **Accuracy**: Proporção de predições corretas
- **Precision**: Proporção de anomalias preditas que são reais
- **Recall**: Proporção de anomalias reais que foram detectadas
- **F1-Score**: Média harmônica de precision e recall

### **Distribuição das Predições**
- **Separação**: Quanto maior, melhor o modelo
- **Threshold**: Ponto de decisão (0.5)
- **Sobreposição**: Indica dificuldade de classificação

### **Importância das Features**
- **Ranking**: Ordem de importância para o modelo
- **Valores**: Magnitude da importância
- **Interpretação**: Features mais relevantes para detecção

## 🎯 Conclusão

A visualização escolhida combina:
1. **Simplicidade**: Fácil de entender
2. **Completude**: Cobre todos os aspectos importantes
3. **Clareza**: Elementos visuais bem definidos
4. **Interpretabilidade**: Resultados claros e diretos
5. **Profissionalismo**: Aparência adequada para apresentações

Esta combinação de gráficos oferece uma visão completa e clara dos resultados do modelo de detecção de anomalias IoT, permitindo interpretação rápida e eficaz das métricas de performance.
"""
    
    # Salvar justificativa
    with open('justificativa_visualizacao.md', 'w', encoding='utf-8') as f:
        f.write(justificativa)
    
    print("   ✅ Justificativa salva como: justificativa_visualizacao.md")

def main():
    """
    Função principal para gerar visualização simples
    """
    print("🚀 GERADOR DE VISUALIZAÇÃO SIMPLES - RESULTADOS DO MODELO IoT")
    print("=" * 70)
    
    # Gerar dados de demonstração
    df = gerar_dados_demonstracao()
    
    # Treinar modelo simples
    model, scaler, feature_columns, X_test, y_test, y_pred, y_pred_proba = treinar_modelo_simples(df)
    
    # Gerar visualização justificada
    gerar_visualizacao_justificada(X_test, y_test, y_pred, y_pred_proba, feature_columns, model)
    
    # Gerar justificativa
    gerar_justificativa_visualizacao()
    
    print(f"\n✅ VISUALIZAÇÃO SIMPLES GERADA COM SUCESSO!")
    print("=" * 70)
    print("📁 Arquivos gerados:")
    print("   • visualizacao_simples_resultado.png - Gráficos de resultado")
    print("   • justificativa_visualizacao.md - Justificativa detalhada")
    
    print(f"\n🎯 CARACTERÍSTICAS DA VISUALIZAÇÃO:")
    print("   • 4 gráficos organizados em 2x2")
    print("   • Matriz de confusão como gráfico principal")
    print("   • Métricas de performance em barras")
    print("   • Distribuição das predições em scatter plot")
    print("   • Importância das features em linha")
    print("   • Justificativa detalhada de cada escolha")
    
    print(f"\n📊 INTERPRETAÇÃO RÁPIDA:")
    print("   • Matriz de confusão: Mostra acertos e erros")
    print("   • Métricas: Performance quantificada")
    print("   • Distribuição: Capacidade de discriminação")
    print("   • Features: Variáveis mais importantes")

if __name__ == "__main__":
    main()
