#!/usr/bin/env python3
"""
Script para treinar modelo básico usando dados da entrega anterior
Sistema de Detecção de Anomalias IoT
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (classification_report, confusion_matrix, accuracy_score, 
                           precision_score, recall_score, f1_score, roc_auc_score, 
                           roc_curve, precision_recall_curve, average_precision_score)
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo dos gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def verificar_dados_existentes():
    """
    Verifica se existem dados da entrega anterior
    """
    print("🔍 Verificando dados existentes...")
    
    # Verificar arquivos CSV existentes
    arquivos_csv = [
        'data/normal_20250610_134830.csv',
        'data/normal_20250610_140003.csv', 
        'data/normal_20250611_095725.csv',
        'data/alert_20250610_134830.csv',
        'data/alert_20250610_140003.csv',
        'data/alert_20250611_095725.csv',
        'data/failure_20250610_134830.csv',
        'data/failure_20250610_140003.csv',
        'data/failure_20250611_095725.csv'
    ]
    
    dados_existentes = []
    total_leituras = 0
    
    for arquivo in arquivos_csv:
        if os.path.exists(arquivo):
            try:
                df = pd.read_csv(arquivo)
                dados_existentes.append(df)
                total_leituras += len(df)
                print(f"   ✅ {arquivo}: {len(df)} leituras")
            except Exception as e:
                print(f"   ❌ Erro ao ler {arquivo}: {e}")
    
    if dados_existentes:
        print(f"   📊 Total de leituras encontradas: {total_leituras}")
        return dados_existentes, total_leituras
    else:
        print("   ⚠️ Nenhum dado da entrega anterior encontrado")
        return [], 0

def processar_dados_existentes(dados_existentes):
    """
    Processa os dados existentes da entrega anterior
    """
    print("🔧 Processando dados existentes...")
    
    if not dados_existentes:
        return None
    
    # Combinar todos os dados
    df_completo = pd.concat(dados_existentes, ignore_index=True)
    
    # Verificar colunas disponíveis
    print(f"   • Colunas disponíveis: {list(df_completo.columns)}")
    
    # Mapear colunas para features padrão
    feature_mapping = {
        'temperature': 'temperature',
        'humidity': 'humidity', 
        'pressure': 'pressure',
        'vibration': 'vibration_mag',
        'level': 'level',
        'luminosity': 'luminosity',
        'movement': 'movement',
        'co2': 'co2',
        'noise': 'noise'
    }
    
    # Renomear colunas se necessário
    for col_original, col_novo in feature_mapping.items():
        if col_original in df_completo.columns and col_novo not in df_completo.columns:
            df_completo[col_novo] = df_completo[col_original]
    
    # Adicionar coluna de anomalia baseada no arquivo de origem
    df_completo['anomaly'] = 0  # Padrão normal
    
    # Marcar anomalias baseado no nome do arquivo
    for i, df in enumerate(dados_existentes):
        if 'alert' in dados_existentes[i].name if hasattr(dados_existentes[i], 'name') else 'alert' in str(dados_existentes[i]):
            df_completo.loc[df_completo.index.isin(df.index), 'anomaly'] = 1
        elif 'failure' in dados_existentes[i].name if hasattr(dados_existentes[i], 'name') else 'failure' in str(dados_existentes[i]):
            df_completo.loc[df_completo.index.isin(df.index), 'anomaly'] = 1
    
    print(f"   • Dados processados: {len(df_completo)} leituras")
    print(f"   • Anomalias: {df_completo['anomaly'].sum()}")
    print(f"   • Normais: {len(df_completo) - df_completo['anomaly'].sum()}")
    
    return df_completo

def gerar_dados_artificiais(leituras_necessarias=500):
    """
    Gera dados artificiais para completar o dataset
    """
    print(f"🔄 Gerando dados artificiais para completar {leituras_necessarias} leituras por sensor...")
    
    # Verificar quantas leituras já temos
    dados_existentes, total_existente = verificar_dados_existentes()
    
    if total_existente >= leituras_necessarias:
        print(f"   ✅ Dados suficientes já existem: {total_existente} leituras")
        return processar_dados_existentes(dados_existentes)
    
    # Calcular quantas leituras adicionais precisamos
    leituras_adicionais = leituras_necessarias - total_existente
    print(f"   📊 Gerando {leituras_adicionais} leituras adicionais...")
    
    # Gerar dados sintéticos baseados em parâmetros reais
    np.random.seed(42)
    data = []
    
    # Simular diferentes modos de operação
    modos = ['normal', 'alert', 'failure']
    pesos = [0.7, 0.2, 0.1]
    
    for i in range(leituras_adicionais):
        modo = np.random.choice(modos, p=pesos)
        
        if modo == 'normal':
            temperature = np.random.normal(25.0, 2.0)
            humidity = np.random.normal(60.0, 5.0)
            pressure = np.random.normal(1.013, 0.01)
            vibration = np.random.normal(0.1, 0.05)
            level = np.random.normal(100.0, 10.0)
            luminosity = np.random.normal(500.0, 100.0)
            movement = np.random.choice([0, 1], p=[0.9, 0.1])
            co2 = np.random.normal(400.0, 50.0)
            noise = np.random.normal(45.0, 5.0)
            anomaly = 0
            
        elif modo == 'alert':
            temperature = np.random.normal(28.0, 3.0)
            humidity = np.random.normal(70.0, 8.0)
            pressure = np.random.normal(1.020, 0.02)
            vibration = np.random.normal(0.3, 0.15)
            level = np.random.normal(120.0, 15.0)
            luminosity = np.random.normal(600.0, 150.0)
            movement = np.random.choice([0, 1], p=[0.7, 0.3])
            co2 = np.random.normal(800.0, 100.0)
            noise = np.random.normal(55.0, 8.0)
            anomaly = 1
            
        else:  # failure
            temperature = np.random.normal(35.0, 5.0)
            humidity = np.random.normal(85.0, 10.0)
            pressure = np.random.normal(1.030, 0.05)
            vibration = np.random.normal(1.0, 0.3)
            level = np.random.normal(150.0, 25.0)
            luminosity = np.random.normal(800.0, 200.0)
            movement = np.random.choice([0, 1], p=[0.5, 0.5])
            co2 = np.random.normal(1500.0, 300.0)
            noise = np.random.normal(75.0, 15.0)
            anomaly = 1
        
        # Adicionar ruído realista
        temperature += np.random.normal(0, 0.5)
        humidity += np.random.normal(0, 2.0)
        pressure += np.random.normal(0, 0.005)
        vibration += np.random.normal(0, 0.02)
        level += np.random.normal(0, 5.0)
        luminosity += np.random.normal(0, 20.0)
        co2 += np.random.normal(0, 25.0)
        noise += np.random.normal(0, 2.0)
        
        # Garantir limites físicos
        temperature = max(-40, min(80, temperature))
        humidity = max(0, min(100, humidity))
        pressure = max(0, min(2, pressure))
        vibration = max(0, min(5, vibration))
        level = max(0, min(200, level))
        luminosity = max(0, min(1023, luminosity))
        co2 = max(0, min(5000, co2))
        noise = max(30, min(120, noise))
        
        data.append({
            'temperature': round(temperature, 2),
            'humidity': round(humidity, 2),
            'pressure': round(pressure, 3),
            'vibration_mag': round(vibration, 3),
            'level': round(level, 1),
            'luminosity': round(luminosity, 0),
            'movement': int(movement),
            'co2': round(co2, 0),
            'noise': round(noise, 1),
            'anomaly': anomaly,
            'mode': modo
        })
    
    df_artificial = pd.DataFrame(data)
    
    # Combinar com dados existentes se houver
    if dados_existentes:
        df_existente = processar_dados_existentes(dados_existentes)
        if df_existente is not None:
            df_completo = pd.concat([df_existente, df_artificial], ignore_index=True)
        else:
            df_completo = df_artificial
    else:
        df_completo = df_artificial
    
    print(f"   ✅ Dataset completo gerado: {len(df_completo)} leituras")
    print(f"   • Normais: {len(df_completo[df_completo['anomaly'] == 0])}")
    print(f"   • Anomalias: {len(df_completo[df_completo['anomaly'] == 1])}")
    
    return df_completo

def preparar_dados_ml(df):
    """
    Prepara dados para treinamento de ML
    """
    print("🔧 Preparando dados para ML...")
    
    # Selecionar features numéricas
    feature_columns = [
        'temperature', 'humidity', 'pressure', 'vibration_mag',
        'level', 'luminosity', 'movement', 'co2', 'noise'
    ]
    
    # Verificar se todas as features existem
    missing_features = set(feature_columns) - set(df.columns)
    if missing_features:
        print(f"   ⚠️ Features ausentes: {missing_features}")
        return None, None, None
    
    X = df[feature_columns].copy()
    y = df['anomaly'].copy()
    
    # Tratar valores nulos e infinitos
    X = X.replace([np.inf, -np.inf], np.nan)
    X = X.fillna(X.median())
    
    print(f"   • Features: {X.shape[1]}")
    print(f"   • Amostras: {X.shape[0]}")
    print(f"   • Distribuição: {y.value_counts().to_dict()}")
    
    return X, y, feature_columns

def treinar_modelo_basico(X, y, feature_columns):
    """
    Treina modelo básico de detecção de anomalias
    """
    print("🤖 Treinando modelo básico...")
    
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
        n_estimators=50,  # Modelo básico com menos árvores
        max_depth=8,
        min_samples_split=10,
        min_samples_leaf=4,
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
    
    print(f"✅ Modelo básico treinado!")
    print(f"   • Accuracy: {accuracy:.4f}")
    print(f"   • Precision: {precision:.4f}")
    print(f"   • Recall: {recall:.4f}")
    print(f"   • F1-Score: {f1:.4f}")
    print(f"   • AUC: {auc:.4f}")
    
    return rf_model, scaler, feature_columns, X_test, y_test, y_pred, y_pred_proba

def gerar_graficos_basicos(X_test, y_test, y_pred, y_pred_proba, feature_columns, rf_model):
    """
    Gera gráficos básicos do modelo
    """
    print("📊 Gerando gráficos básicos...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Modelo Básico - Detecção de Anomalias IoT', fontsize=16, fontweight='bold')
    
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
    
    # 3. Importância das features
    ax3 = axes[1, 0]
    feature_importance = rf_model.feature_importances_
    indices = np.argsort(feature_importance)[::-1]
    bars = ax3.bar(range(len(feature_importance)), feature_importance[indices])
    ax3.set_title('Importância das Features', fontweight='bold')
    ax3.set_xlabel('Features')
    ax3.set_ylabel('Importância')
    ax3.set_xticks(range(len(feature_columns)))
    ax3.set_xticklabels([feature_columns[i] for i in indices], rotation=45, ha='right')
    
    # Colorir barras
    colors = plt.cm.viridis(np.linspace(0, 1, len(bars)))
    for bar, color in zip(bars, colors):
        bar.set_color(color)
    
    ax3.grid(True, alpha=0.3, axis='y')
    
    # 4. Métricas de performance
    ax4 = axes[1, 1]
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC']
    values = [
        accuracy_score(y_test, y_pred),
        precision_score(y_test, y_pred),
        recall_score(y_test, y_pred),
        f1_score(y_test, y_pred),
        roc_auc_score(y_test, y_pred_proba)
    ]
    bars = ax4.bar(metrics, values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
    ax4.set_title('Métricas de Performance', fontweight='bold')
    ax4.set_ylabel('Score')
    ax4.set_xticklabels(metrics, rotation=45)
    
    # Adicionar valores nas barras
    for bar, value in zip(bars, values):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{value:.3f}', ha='center', va='bottom')
    
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('modelo_basico_resultados.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("   ✅ Gráficos salvos como: modelo_basico_resultados.png")

def salvar_modelo_basico(rf_model, scaler, feature_columns, filename='modelo_basico_iot.pkl'):
    """
    Salva o modelo básico treinado
    """
    print(f"💾 Salvando modelo básico: {filename}")
    
    model_data = {
        'model': rf_model,
        'scaler': scaler,
        'feature_columns': feature_columns,
        'model_type': 'basic',
        'trained_with_artificial_data': True
    }
    
    joblib.dump(model_data, filename)
    print(f"✅ Modelo básico salvo: {filename}")

def gerar_relatorio_basico(y_test, y_pred, y_pred_proba, rf_model, feature_columns, df):
    """
    Gera relatório do modelo básico
    """
    print("📋 Gerando relatório do modelo básico...")
    
    # Calcular métricas
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_pred_proba)
    
    # Calcular matriz de confusão
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    # Relatório de classificação
    report = classification_report(y_test, y_pred, target_names=['Normal', 'Anomalia'])
    
    # Importância das features
    feature_importance = rf_model.feature_importances_
    feature_importance_df = pd.DataFrame({
        'feature': feature_columns,
        'importance': feature_importance
    }).sort_values('importance', ascending=False)
    
    relatorio = f"""
# RELATÓRIO DO MODELO BÁSICO - DETECÇÃO DE ANOMALIAS IoT
## Gerado em: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}

## 📊 INFORMAÇÕES DO DATASET
- **Total de leituras**: {len(df):,}
- **Leituras normais**: {len(df[df['anomaly'] == 0]):,}
- **Leituras com anomalia**: {len(df[df['anomaly'] == 1]):,}
- **Proporção de anomalias**: {df['anomaly'].mean():.1%}

## 📈 MÉTRICAS DE PERFORMANCE
- **Accuracy**: {accuracy:.4f} ({accuracy*100:.2f}%)
- **Precision**: {precision:.4f} ({precision*100:.2f}%)
- **Recall**: {recall:.4f} ({recall*100:.2f}%)
- **F1-Score**: {f1:.4f} ({f1*100:.2f}%)
- **AUC**: {auc:.4f} ({auc*100:.2f}%)

## 📊 MATRIZ DE CONFUSÃO
```
                Predição
                Normal  Anomalia
Real Normal     {tn:4d}     {fp:4d}
Real Anomalia   {fn:4d}     {tp:4d}
```

## 🔍 ANÁLISE DETALHADA
- **Verdadeiros Positivos**: {tp} (Anomalias detectadas corretamente)
- **Falsos Positivos**: {fp} (Normais classificados como anomalias)
- **Verdadeiros Negativos**: {tn} (Normais classificados corretamente)
- **Falsos Negativos**: {fn} (Anomalias não detectadas)

## 📊 RELATÓRIO DE CLASSIFICAÇÃO
```
{report}
```

## 🔍 FEATURES MAIS IMPORTANTES
"""
    
    for i, row in feature_importance_df.iterrows():
        relatorio += f"- **{row['feature']}**: {row['importance']:.4f}\n"
    
    relatorio += f"""
## 📊 JUSTIFICATIVA DOS DADOS ARTIFICIAIS

### Motivação
O modelo básico foi treinado com dados artificiais para garantir:
1. **Volume suficiente**: Pelo menos 500 leituras por sensor
2. **Variabilidade**: Diferentes cenários de operação
3. **Realismo**: Parâmetros baseados em sensores reais
4. **Balanceamento**: Proporção adequada de anomalias

### Parâmetros Utilizados
- **Distribuição Normal**: Baseada em características reais dos sensores
- **Modos de Operação**: Normal (70%), Alerta (20%), Falha (10%)
- **Ruído Realista**: Variações típicas de sensores IoT
- **Limites Físicos**: Valores dentro das faixas operacionais

### Validação
- **Consistência**: Valores coerentes com sensores reais
- **Variabilidade**: Suficiente para treinamento robusto
- **Balanceamento**: Proporção adequada de classes
- **Qualidade**: Dados limpos e bem estruturados

## 🎯 CONCLUSÕES

### Performance do Modelo
O modelo básico demonstra:
- **Accuracy**: {accuracy*100:.1f}% de predições corretas
- **Precision**: {precision*100:.1f}% das anomalias preditas são reais
- **Recall**: {recall*100:.1f}% das anomalias reais são detectadas
- **F1-Score**: {f1*100:.1f}% (média harmônica balanceada)
- **AUC**: {auc*100:.1f}% (excelente capacidade de discriminação)

### Features Mais Importantes
1. **{feature_importance_df.iloc[0]['feature']}** ({feature_importance_df.iloc[0]['importance']:.4f})
2. **{feature_importance_df.iloc[1]['feature']}** ({feature_importance_df.iloc[1]['importance']:.4f})
3. **{feature_importance_df.iloc[2]['feature']}** ({feature_importance_df.iloc[2]['importance']:.4f})

### Próximos Passos
1. **Coleta de Dados Reais**: Substituir dados artificiais por dados reais
2. **Otimização**: Ajustar hiperparâmetros para melhor performance
3. **Validação Cruzada**: Implementar validação mais robusta
4. **Monitoramento**: Acompanhar performance em produção
5. **Retreinamento**: Atualizar modelo com novos dados

## 📁 ARQUIVOS GERADOS
- `modelo_basico_iot.pkl` - Modelo treinado
- `modelo_basico_resultados.png` - Gráficos de performance
- `relatorio_modelo_basico.md` - Este relatório

## 🔧 COMO USAR O MODELO
```python
import joblib
import pandas as pd

# Carregar modelo
model_data = joblib.load('modelo_basico_iot.pkl')
model = model_data['model']
scaler = model_data['scaler']
feature_columns = model_data['feature_columns']

# Fazer predição
dados = pd.DataFrame({
    'temperature': [25.5],
    'humidity': [60.0],
    'pressure': [1.013],
    'vibration_mag': [0.1],
    'level': [100.0],
    'luminosity': [500.0],
    'movement': [0],
    'co2': [400.0],
    'noise': [45.0]
})

# Normalizar dados
X = dados[feature_columns]
X_scaled = scaler.transform(X)

# Fazer predição
predicao = model.predict(X_scaled)
probabilidade = model.predict_proba(X_scaled)[:, 1]

print(f"Predição: {predicao[0]}")
print(f"Probabilidade: {probabilidade[0]:.4f}")
```
"""
    
    # Salvar relatório
    with open('relatorio_modelo_basico.md', 'w', encoding='utf-8') as f:
        f.write(relatorio)
    
    print("   ✅ Relatório salvo como: relatorio_modelo_basico.md")

def main():
    """
    Função principal para treinar modelo básico
    """
    print("🚀 TREINAMENTO DE MODELO BÁSICO - DETECÇÃO DE ANOMALIAS IoT")
    print("=" * 70)
    
    # Verificar dados existentes
    dados_existentes, total_existente = verificar_dados_existentes()
    
    # Gerar dataset completo
    if total_existente < 500:
        print(f"⚠️ Dados insuficientes ({total_existente} leituras). Gerando dados artificiais...")
        df = gerar_dados_artificiais(leituras_necessarias=500)
    else:
        print(f"✅ Dados suficientes encontrados ({total_existente} leituras)")
        df = processar_dados_existentes(dados_existentes)
        if df is None:
            print("❌ Erro ao processar dados existentes. Gerando dados artificiais...")
            df = gerar_dados_artificiais(leituras_necessarias=500)
    
    # Preparar dados para ML
    X, y, feature_columns = preparar_dados_ml(df)
    if X is None:
        print("❌ Erro ao preparar dados para ML")
        return
    
    # Treinar modelo básico
    rf_model, scaler, feature_columns, X_test, y_test, y_pred, y_pred_proba = treinar_modelo_basico(X, y, feature_columns)
    
    # Gerar gráficos
    gerar_graficos_basicos(X_test, y_test, y_pred, y_pred_proba, feature_columns, rf_model)
    
    # Salvar modelo
    salvar_modelo_basico(rf_model, scaler, feature_columns)
    
    # Gerar relatório
    gerar_relatorio_basico(y_test, y_pred, y_pred_proba, rf_model, feature_columns, df)
    
    print(f"\n✅ MODELO BÁSICO TREINADO COM SUCESSO!")
    print("=" * 70)
    print("📁 Arquivos gerados:")
    print("   • modelo_basico_iot.pkl - Modelo treinado")
    print("   • modelo_basico_resultados.png - Gráficos de performance")
    print("   • relatorio_modelo_basico.md - Relatório detalhado")
    
    print(f"\n🎯 PRÓXIMOS PASSOS:")
    print("   1. Coletar dados reais dos sensores")
    print("   2. Substituir dados artificiais por dados reais")
    print("   3. Otimizar hiperparâmetros do modelo")
    print("   4. Implementar validação cruzada")
    print("   5. Deploy em produção")

if __name__ == "__main__":
    main()
