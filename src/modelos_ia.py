import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

class ModeloEnsemble:
    def __init__(self):
        # Inicialização dos modelos
        self.random_forest = RandomForestClassifier(n_estimators=100, random_state=42)
        self.svm = SVC(probability=True, random_state=42)
        self.isolation_forest = IsolationForest(contamination=0.1, random_state=42)
        self.lstm = None
        self.pesos = {'random_forest': 0.5, 'lstm': 0.3, 'svm': 0.2}
        self.scaler = StandardScaler()
    
    def criar_modelo_lstm(self, input_shape):
        """Cria o modelo LSTM para séries temporais"""
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
        model.add(Dropout(0.2))
        model.add(LSTM(50))
        model.add(Dropout(0.2))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        self.lstm = model
        return model
    
    def treinar_modelos(self, X, y, X_temporal=None):
        """Treina todos os modelos do ensemble"""
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Normalizar dados
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Treinar Random Forest
        self.random_forest.fit(X_train_scaled, y_train)
        
        # Treinar SVM
        self.svm.fit(X_train_scaled, y_train)
        
        # Treinar Isolation Forest (apenas com dados normais)
        normal_indices = y_train == 0
        self.isolation_forest.fit(X_train_scaled[normal_indices])
        
        # Treinar LSTM se dados temporais forem fornecidos
        if X_temporal is not None:
            X_temp_train, X_temp_test, y_temp_train, y_temp_test = train_test_split(
                X_temporal, y, test_size=0.2, random_state=42)
            
            if self.lstm is None:
                self.criar_modelo_lstm((X_temporal.shape[1], X_temporal.shape[2]))
            
            self.lstm.fit(
                X_temp_train, y_temp_train,
                epochs=50,
                batch_size=32,
                validation_data=(X_temp_test, y_temp_test),
                verbose=0
            )
        
        # Avaliar modelos
        resultados = self.avaliar_modelos(X_test_scaled, y_test, X_temporal_test=X_temp_test if X_temporal is not None else None)
        return resultados
    
    def prever(self, X, X_temporal=None):
        """Faz previsões usando o ensemble de modelos"""
        X_scaled = self.scaler.transform(X)
        
        # Previsões individuais
        rf_pred = self.random_forest.predict_proba(X_scaled)[:, 1]
        svm_pred = self.svm.predict_proba(X_scaled)[:, 1]
        
        # Anomalias (Isolation Forest)
        # Converte scores para probabilidade (valores negativos = mais anômalos)
        iso_scores = self.isolation_forest.decision_function(X_scaled)
        iso_pred = 1 - (iso_scores - min(iso_scores)) / (max(iso_scores) - min(iso_scores))
        
        # LSTM (se disponível)
        if X_temporal is not None and self.lstm is not None:
            lstm_pred = self.lstm.predict(X_temporal).flatten()
        else:
            lstm_pred = np.zeros_like(rf_pred)
            self.pesos = {'random_forest': 0.7, 'svm': 0.3, 'lstm': 0}
        
        # Ensemble com pesos
        ensemble_pred = (
            rf_pred * self.pesos['random_forest'] +
            lstm_pred * self.pesos['lstm'] +
            svm_pred * self.pesos['svm']
        )
        
        # Classificação final (threshold 0.5)
        return (ensemble_pred >= 0.5).astype(int), ensemble_pred
    
    def avaliar_modelos(self, X_test, y_test, X_temporal_test=None):
        """Avalia o desempenho dos modelos individuais e do ensemble"""
        resultados = {}
        
        # Avaliação Random Forest
        rf_pred = self.random_forest.predict(X_test)
        resultados['random_forest'] = {
            'accuracy': accuracy_score(y_test, rf_pred),
            'precision': precision_score(y_test, rf_pred),
            'recall': recall_score(y_test, rf_pred),
            'f1': f1_score(y_test, rf_pred)
        }
        
        # Avaliação SVM
        svm_pred = self.svm.predict(X_test)
        resultados['svm'] = {
            'accuracy': accuracy_score(y_test, svm_pred),
            'precision': precision_score(y_test, svm_pred),
            'recall': recall_score(y_test, svm_pred),
            'f1': f1_score(y_test, svm_pred)
        }
        
        # Avaliação LSTM (se disponível)
        if X_temporal_test is not None and self.lstm is not None:
            lstm_pred = (self.lstm.predict(X_temporal_test) >= 0.5).astype(int).flatten()
            resultados['lstm'] = {
                'accuracy': accuracy_score(y_test, lstm_pred),
                'precision': precision_score(y_test, lstm_pred),
                'recall': recall_score(y_test, lstm_pred),
                'f1': f1_score(y_test, lstm_pred)
            }
        
        # Avaliação Ensemble
        ensemble_pred, _ = self.prever(X_test, X_temporal_test)
        resultados['ensemble'] = {
            'accuracy': accuracy_score(y_test, ensemble_pred),
            'precision': precision_score(y_test, ensemble_pred),
            'recall': recall_score(y_test, ensemble_pred),
            'f1': f1_score(y_test, ensemble_pred)
        }
        
        return resultados


# Exemplo de uso
if __name__ == "__main__":
    # Este é apenas um exemplo simplificado
    # Substitua por seus dados reais
    
    # Dados tabulares
    X = np.random.rand(1000, 10)
    y = np.random.randint(0, 2, 1000)
    
    # Dados temporais (para LSTM)
    # Formato: [amostras, timesteps, features]
    X_temporal = np.random.rand(1000, 5, 10)
    
    # Inicializar e treinar o ensemble
    modelo = ModeloEnsemble()
    resultados = modelo.treinar_modelos(X, y, X_temporal)
    
    # Imprimir resultados
    for nome_modelo, metricas in resultados.items():
        print(f"Modelo: {nome_modelo}")
        for metrica, valor in metricas.items():
            print(f"  {metrica}: {valor:.4f}")
        print()
    
    # Fazer previsões com novos dados
    X_novo = np.random.rand(10, 10)
    X_temporal_novo = np.random.rand(10, 5, 10)
    
    predicoes, probabilidades = modelo.prever(X_novo, X_temporal_novo)
    print("Previsões do ensemble:", predicoes)
    print("Probabilidades:", probabilidades)