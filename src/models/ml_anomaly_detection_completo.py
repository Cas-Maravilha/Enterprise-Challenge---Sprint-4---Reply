#!/usr/bin/env python3
"""
Sistema de Machine Learning para Detecção de Anomalias IoT
Código-fonte completo do modelo de ML
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (classification_report, confusion_matrix, accuracy_score, 
                           precision_score, recall_score, f1_score, roc_auc_score, 
                           roc_curve, precision_recall_curve, average_precision_score)
from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
import joblib
import warnings
warnings.filterwarnings('ignore')

class IoTAnomalyDetector:
    """
    Classe principal para detecção de anomalias em dados IoT
    """
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.model = None
        self.feature_columns = None
        self.label_encoder = LabelEncoder()
        self.isolation_forest = None
        self.pca = None
        
    def gerar_dados_sinteticos(self, n_samples=5000):
        """
        Gera dados sintéticos baseados em parâmetros reais de sensores IoT
        """
        print("🔄 Gerando dados sintéticos para treinamento...")
        
        np.random.seed(self.random_state)
        data = []
        
        for i in range(n_samples):
            # Simular diferentes modos de operação
            mode = np.random.choice([0, 1, 2], p=[0.7, 0.2, 0.1])  # Normal, Alerta, Falha
            
            if mode == 0:  # Normal
                temperature = np.random.normal(25.0, 2.0)
                humidity = np.random.normal(60.0, 5.0)
                pressure = np.random.normal(1.013, 0.01)
                vibration_x = np.random.normal(0.0, 0.1)
                vibration_y = np.random.normal(0.0, 0.1)
                vibration_z = np.random.normal(0.0, 0.1)
                level = np.random.normal(100.0, 10.0)
                luminosity = np.random.normal(500.0, 100.0)
                movement = np.random.choice([0, 1], p=[0.9, 0.1])
                co2 = np.random.normal(400.0, 50.0)
                noise = np.random.normal(45.0, 5.0)
                
            elif mode == 1:  # Alerta
                temperature = np.random.normal(28.0, 3.0)
                humidity = np.random.normal(70.0, 8.0)
                pressure = np.random.normal(1.020, 0.02)
                vibration_x = np.random.normal(0.3, 0.2)
                vibration_y = np.random.normal(0.2, 0.15)
                vibration_z = np.random.normal(0.1, 0.1)
                level = np.random.normal(120.0, 15.0)
                luminosity = np.random.normal(600.0, 150.0)
                movement = np.random.choice([0, 1], p=[0.7, 0.3])
                co2 = np.random.normal(800.0, 100.0)
                noise = np.random.normal(55.0, 8.0)
                
            else:  # Falha
                temperature = np.random.normal(35.0, 5.0)
                humidity = np.random.normal(85.0, 10.0)
                pressure = np.random.normal(1.030, 0.05)
                vibration_x = np.random.normal(1.0, 0.5)
                vibration_y = np.random.normal(0.8, 0.4)
                vibration_z = np.random.normal(0.6, 0.3)
                level = np.random.normal(150.0, 25.0)
                luminosity = np.random.normal(800.0, 200.0)
                movement = np.random.choice([0, 1], p=[0.5, 0.5])
                co2 = np.random.normal(1500.0, 300.0)
                noise = np.random.normal(75.0, 15.0)
            
            # Adicionar anomalias ocasionais (5% de chance)
            if np.random.random() < 0.05:
                temperature += np.random.normal(0, 10)
                humidity += np.random.normal(0, 20)
                pressure += np.random.normal(0, 0.1)
                vibration_x += np.random.normal(0, 0.5)
                vibration_y += np.random.normal(0, 0.5)
                vibration_z += np.random.normal(0, 0.5)
                level += np.random.normal(0, 30)
                luminosity += np.random.normal(0, 300)
                co2 += np.random.normal(0, 500)
                noise += np.random.normal(0, 20)
                mode = 2  # Marcar como falha
            
            # Calcular magnitude da vibração
            vibration_mag = np.sqrt(vibration_x**2 + vibration_y**2 + vibration_z**2)
            
            # Features derivadas
            temp_humidity_ratio = temperature / (humidity + 1)
            pressure_vibration = pressure * vibration_mag
            level_luminosity = level * luminosity / 1000
            temp_pressure_ratio = temperature / (pressure + 0.1)
            humidity_level_ratio = humidity / (level + 1)
            co2_noise_ratio = co2 / (noise + 1)
            
            data.append({
                'temperature': max(-40, min(80, round(temperature, 2))),
                'humidity': max(0, min(100, round(humidity, 2))),
                'pressure': max(0, min(2, round(pressure, 3))),
                'vibration_x': round(vibration_x, 3),
                'vibration_y': round(vibration_y, 3),
                'vibration_z': round(vibration_z, 3),
                'vibration_mag': round(vibration_mag, 3),
                'level': max(0, min(200, round(level, 1))),
                'luminosity': max(0, min(1023, round(luminosity, 0))),
                'movement': int(movement),
                'co2': max(0, min(5000, round(co2, 0))),
                'noise': max(30, min(120, round(noise, 1))),
                'temp_humidity_ratio': round(temp_humidity_ratio, 4),
                'pressure_vibration': round(pressure_vibration, 4),
                'level_luminosity': round(level_luminosity, 2),
                'temp_pressure_ratio': round(temp_pressure_ratio, 2),
                'humidity_level_ratio': round(humidity_level_ratio, 4),
                'co2_noise_ratio': round(co2_noise_ratio, 2),
                'anomaly': 1 if mode == 2 else 0,
                'mode': mode
            })
        
        df = pd.DataFrame(data)
        print(f"✅ Dados sintéticos gerados: {len(df)} amostras")
        print(f"   • Normal: {len(df[df['anomaly'] == 0])} amostras")
        print(f"   • Anomalia: {len(df[df['anomaly'] == 1])} amostras")
        
        return df
    
    def preparar_dados(self, df):
        """
        Prepara os dados para treinamento
        """
        print("🔧 Preparando dados para treinamento...")
        
        # Selecionar features
        self.feature_columns = [
            'temperature', 'humidity', 'pressure', 'vibration_mag',
            'level', 'luminosity', 'movement', 'co2', 'noise',
            'temp_humidity_ratio', 'pressure_vibration', 'level_luminosity',
            'temp_pressure_ratio', 'humidity_level_ratio', 'co2_noise_ratio'
        ]
        
        X = df[self.feature_columns].copy()
        y = df['anomaly'].copy()
        
        # Tratar valores infinitos e nulos
        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.fillna(X.median())
        
        print(f"   • Features: {X.shape[1]}")
        print(f"   • Amostras: {X.shape[0]}")
        print(f"   • Distribuição: {y.value_counts().to_dict()}")
        
        return X, y
    
    def treinar_modelo(self, X, y):
        """
        Treina o modelo de detecção de anomalias
        """
        print("🤖 Treinando modelo de detecção de anomalias...")
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=self.random_state, stratify=y
        )
        
        # Normalizar dados
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Treinar Random Forest
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=self.random_state,
            class_weight='balanced'
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        # Treinar Isolation Forest para comparação
        self.isolation_forest = IsolationForest(
            contamination=0.1,
            random_state=self.random_state
        )
        self.isolation_forest.fit(X_train_scaled)
        
        # Fazer predições
        y_pred = self.model.predict(X_test_scaled)
        y_pred_proba = self.model.predict_proba(X_test_scaled)[:, 1]
        
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
        
        return X_test_scaled, y_test, y_pred, y_pred_proba
    
    def otimizar_hiperparametros(self, X, y):
        """
        Otimiza hiperparâmetros do modelo
        """
        print("🔍 Otimizando hiperparâmetros...")
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=self.random_state, stratify=y
        )
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Grid search
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [5, 10, 15],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        
        grid_search = GridSearchCV(
            RandomForestClassifier(random_state=self.random_state, class_weight='balanced'),
            param_grid, cv=5, scoring='roc_auc', n_jobs=-1
        )
        
        grid_search.fit(X_train_scaled, y_train)
        
        self.model = grid_search.best_estimator_
        
        print(f"✅ Melhores parâmetros: {grid_search.best_params_}")
        print(f"   • Melhor score: {grid_search.best_score_:.4f}")
        
        return grid_search.best_params_
    
    def validar_modelo(self, X, y):
        """
        Validação cruzada do modelo
        """
        print("🔄 Executando validação cruzada...")
        
        X_scaled = self.scaler.fit_transform(X)
        
        cv_scores = cross_val_score(
            self.model, X_scaled, y, cv=5, scoring='roc_auc'
        )
        
        print(f"✅ Validação cruzada (5 folds):")
        print(f"   • Scores: {cv_scores}")
        print(f"   • Média: {cv_scores.mean():.4f}")
        print(f"   • Desvio padrão: {cv_scores.std():.4f}")
        print(f"   • Intervalo: {cv_scores.mean():.4f} ± {cv_scores.std() * 2:.4f}")
        
        return cv_scores
    
    def plotar_resultados(self, X_test, y_test, y_pred, y_pred_proba):
        """
        Plota resultados do modelo
        """
        print("📊 Gerando visualizações dos resultados...")
        
        # Configurar estilo
        plt.style.use('seaborn-v0_8')
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Matriz de confusão
        plt.subplot(3, 3, 1)
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=['Normal', 'Anomalia'],
                   yticklabels=['Normal', 'Anomalia'])
        plt.title('Matriz de Confusão', fontsize=14, fontweight='bold')
        plt.xlabel('Predição')
        plt.ylabel('Valor Real')
        
        # 2. Curva ROC
        plt.subplot(3, 3, 2)
        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        auc_score = roc_auc_score(y_test, y_pred_proba)
        plt.plot(fpr, tpr, color='darkorange', lw=2, 
                label=f'ROC Curve (AUC = {auc_score:.4f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Taxa de Falsos Positivos')
        plt.ylabel('Taxa de Verdadeiros Positivos')
        plt.title('Curva ROC', fontsize=14, fontweight='bold')
        plt.legend(loc="lower right")
        plt.grid(True, alpha=0.3)
        
        # 3. Curva Precision-Recall
        plt.subplot(3, 3, 3)
        precision, recall, _ = precision_recall_curve(y_test, y_pred_proba)
        ap_score = average_precision_score(y_test, y_pred_proba)
        plt.plot(recall, precision, color='darkorange', lw=2,
                label=f'PR Curve (AP = {ap_score:.4f})')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Curva Precision-Recall', fontsize=14, fontweight='bold')
        plt.legend(loc="lower left")
        plt.grid(True, alpha=0.3)
        
        # 4. Importância das features
        plt.subplot(3, 3, 4)
        feature_importance = self.model.feature_importances_
        indices = np.argsort(feature_importance)[::-1]
        bars = plt.bar(range(len(feature_importance)), feature_importance[indices])
        plt.title('Importância das Features', fontsize=14, fontweight='bold')
        plt.xlabel('Features')
        plt.ylabel('Importância')
        plt.xticks(range(len(self.feature_columns)), 
                  [self.feature_columns[i] for i in indices], rotation=45)
        
        # Colorir barras
        colors = plt.cm.viridis(np.linspace(0, 1, len(bars)))
        for bar, color in zip(bars, colors):
            bar.set_color(color)
        
        plt.grid(True, alpha=0.3, axis='y')
        
        # 5. Distribuição das predições
        plt.subplot(3, 3, 5)
        plt.hist(y_pred_proba[y_test == 0], bins=30, alpha=0.7, label='Normal', color='blue')
        plt.hist(y_pred_proba[y_test == 1], bins=30, alpha=0.7, label='Anomalia', color='red')
        plt.xlabel('Probabilidade de Anomalia')
        plt.ylabel('Frequência')
        plt.title('Distribuição das Predições', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 6. Métricas de performance
        plt.subplot(3, 3, 6)
        metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC']
        values = [
            accuracy_score(y_test, y_pred),
            precision_score(y_test, y_pred),
            recall_score(y_test, y_pred),
            f1_score(y_test, y_pred),
            roc_auc_score(y_test, y_pred_proba)
        ]
        bars = plt.bar(metrics, values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
        plt.title('Métricas de Performance', fontsize=14, fontweight='bold')
        plt.ylabel('Score')
        plt.xticks(rotation=45)
        
        # Adicionar valores nas barras
        for bar, value in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f'{value:.3f}', ha='center', va='bottom')
        
        plt.grid(True, alpha=0.3, axis='y')
        
        # 7. Análise PCA (se houver muitas features)
        if len(self.feature_columns) > 2:
            plt.subplot(3, 3, 7)
            self.pca = PCA(n_components=2)
            X_pca = self.pca.fit_transform(X_test)
            
            scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y_test, cmap='viridis', alpha=0.6)
            plt.xlabel(f'PC1 ({self.pca.explained_variance_ratio_[0]:.2%})')
            plt.ylabel(f'PC2 ({self.pca.explained_variance_ratio_[1]:.2%})')
            plt.title('Análise PCA', fontsize=14, fontweight='bold')
            plt.colorbar(scatter, label='Anomalia')
            plt.grid(True, alpha=0.3)
        
        # 8. Distribuição das features principais
        plt.subplot(3, 3, 8)
        top_features = [self.feature_columns[i] for i in indices[:5]]
        for feature in top_features:
            plt.hist(X_test[feature], alpha=0.5, label=feature, bins=20)
        plt.xlabel('Valor')
        plt.ylabel('Frequência')
        plt.title('Distribuição das Features Principais', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 9. Resumo das métricas
        plt.subplot(3, 3, 9)
        plt.axis('off')
        metrics_text = f"""
        RESULTADOS DO MODELO
        
        Accuracy: {accuracy_score(y_test, y_pred):.4f}
        Precision: {precision_score(y_test, y_pred):.4f}
        Recall: {recall_score(y_test, y_pred):.4f}
        F1-Score: {f1_score(y_test, y_pred):.4f}
        AUC: {roc_auc_score(y_test, y_pred_proba):.4f}
        
        Features: {len(self.feature_columns)}
        Amostras: {len(X_test)}
        Anomalias: {sum(y_test)}
        """
        plt.text(0.1, 0.5, metrics_text, fontsize=12, verticalalignment='center',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.8))
        
        plt.tight_layout()
        plt.savefig('resultados_modelo_ml_completo.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✅ Visualizações salvas como: resultados_modelo_ml_completo.png")
    
    def salvar_modelo(self, filename='modelo_anomalia_iot.pkl'):
        """
        Salva o modelo treinado
        """
        print(f"💾 Salvando modelo como: {filename}")
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns,
            'isolation_forest': self.isolation_forest,
            'pca': self.pca
        }
        
        joblib.dump(model_data, filename)
        print(f"✅ Modelo salvo com sucesso!")
    
    def carregar_modelo(self, filename='modelo_anomalia_iot.pkl'):
        """
        Carrega o modelo treinado
        """
        print(f"📂 Carregando modelo: {filename}")
        
        model_data = joblib.load(filename)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_columns = model_data['feature_columns']
        self.isolation_forest = model_data['isolation_forest']
        self.pca = model_data['pca']
        
        print(f"✅ Modelo carregado com sucesso!")
    
    def predizer_anomalia(self, dados_novos):
        """
        Prediz anomalias em novos dados
        """
        if self.model is None:
            raise ValueError("Modelo não foi treinado ainda!")
        
        # Preparar dados
        X = dados_novos[self.feature_columns].copy()
        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.fillna(X.median())
        
        # Normalizar
        X_scaled = self.scaler.transform(X)
        
        # Fazer predições
        predicoes = self.model.predict(X_scaled)
        probabilidades = self.model.predict_proba(X_scaled)[:, 1]
        
        return predicoes, probabilidades
    
    def gerar_relatorio_detalhado(self, X_test, y_test, y_pred, y_pred_proba):
        """
        Gera relatório detalhado dos resultados
        """
        print("📋 Gerando relatório detalhado...")
        
        # Métricas principais
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_pred_proba)
        
        # Relatório de classificação
        report = classification_report(y_test, y_pred, target_names=['Normal', 'Anomalia'])
        
        # Importância das features
        feature_importance = self.model.feature_importances_
        feature_importance_df = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': feature_importance
        }).sort_values('importance', ascending=False)
        
        print("\n" + "="*60)
        print("RELATÓRIO DETALHADO - MODELO DE DETECÇÃO DE ANOMALIAS")
        print("="*60)
        print(f"\n📊 MÉTRICAS PRINCIPAIS:")
        print(f"   • Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
        print(f"   • Precision: {precision:.4f} ({precision*100:.2f}%)")
        print(f"   • Recall: {recall:.4f} ({recall*100:.2f}%)")
        print(f"   • F1-Score: {f1:.4f} ({f1*100:.2f}%)")
        print(f"   • AUC: {auc:.4f} ({auc*100:.2f}%)")
        
        print(f"\n📈 RELATÓRIO DE CLASSIFICAÇÃO:")
        print(report)
        
        print(f"\n🔍 TOP 10 FEATURES MAIS IMPORTANTES:")
        for i, row in feature_importance_df.head(10).iterrows():
            print(f"   {row['feature']}: {row['importance']:.4f}")
        
        print(f"\n📊 DISTRIBUIÇÃO DAS PREDIÇÕES:")
        print(f"   • Total de amostras: {len(y_test)}")
        print(f"   • Anomalias reais: {sum(y_test)}")
        print(f"   • Anomalias preditas: {sum(y_pred)}")
        print(f"   • Verdadeiros positivos: {sum((y_test == 1) & (y_pred == 1))}")
        print(f"   • Falsos positivos: {sum((y_test == 0) & (y_pred == 1))}")
        print(f"   • Verdadeiros negativos: {sum((y_test == 0) & (y_pred == 0))}")
        print(f"   • Falsos negativos: {sum((y_test == 1) & (y_pred == 0))}")
        
        print(f"\n✅ MODELO PRONTO PARA USO EM PRODUÇÃO!")
        print("="*60)

def main():
    """
    Função principal para demonstrar o uso do sistema
    """
    print("🚀 SISTEMA DE MACHINE LEARNING - DETECÇÃO DE ANOMALIAS IoT")
    print("="*70)
    
    # Criar instância do detector
    detector = IoTAnomalyDetector()
    
    # Gerar dados sintéticos
    df = detector.gerar_dados_sinteticos(n_samples=5000)
    
    # Preparar dados
    X, y = detector.preparar_dados(df)
    
    # Treinar modelo
    X_test, y_test, y_pred, y_pred_proba = detector.treinar_modelo(X, y)
    
    # Otimizar hiperparâmetros
    best_params = detector.otimizar_hiperparametros(X, y)
    
    # Validar modelo
    cv_scores = detector.validar_modelo(X, y)
    
    # Plotar resultados
    detector.plotar_resultados(X_test, y_test, y_pred, y_pred_proba)
    
    # Gerar relatório detalhado
    detector.gerar_relatorio_detalhado(X_test, y_test, y_pred, y_pred_proba)
    
    # Salvar modelo
    detector.salvar_modelo()
    
    print("\n🎯 SISTEMA COMPLETO E PRONTO PARA USO!")
    print("   • Modelo treinado e validado")
    print("   • Visualizações geradas")
    print("   • Relatório detalhado criado")
    print("   • Modelo salvo para uso em produção")
    
    return detector

if __name__ == "__main__":
    detector = main()
