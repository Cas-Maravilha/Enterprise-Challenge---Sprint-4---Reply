import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_curve, auc, confusion_matrix, mean_absolute_error,
    mean_squared_error, r2_score
)
from sklearn.model_selection import KFold, cross_val_score

class MetricasValidacao:
    @staticmethod
    def avaliar_classificacao(y_true, y_pred, y_proba=None):
        """
        Avalia métricas de classificação
        
        Args:
            y_true: Valores reais
            y_pred: Valores previstos (classes)
            y_proba: Probabilidades previstas (opcional)
            
        Returns:
            dict: Dicionário com métricas
        """
        metricas = {
            'acuracia': accuracy_score(y_true, y_pred),
            'precisao': precision_score(y_true, y_pred, average='weighted'),
            'recall': recall_score(y_true, y_pred, average='weighted'),
            'f1': f1_score(y_true, y_pred, average='weighted'),
        }
        
        # Matriz de confusão
        cm = confusion_matrix(y_true, y_pred)
        
        # AUC-ROC (se probabilidades forem fornecidas)
        if y_proba is not None and len(np.unique(y_true)) == 2:
            fpr, tpr, _ = roc_curve(y_true, y_proba)
            metricas['auc_roc'] = auc(fpr, tpr)
            metricas['fpr'] = fpr
            metricas['tpr'] = tpr
        
        return metricas, cm
    
    @staticmethod
    def avaliar_regressao(y_true, y_pred):
        """
        Avalia métricas de regressão
        
        Args:
            y_true: Valores reais
            y_pred: Valores previstos
            
        Returns:
            dict: Dicionário com métricas
        """
        metricas = {
            'mae': mean_absolute_error(y_true, y_pred),
            'mse': mean_squared_error(y_true, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
            'r2': r2_score(y_true, y_pred)
        }
        
        return metricas
    
    @staticmethod
    def validacao_cruzada(modelo, X, y, cv=5, scoring='accuracy'):
        """
        Realiza validação cruzada
        
        Args:
            modelo: Modelo a ser avaliado
            X: Features
            y: Target
            cv: Número de folds
            scoring: Métrica de avaliação
            
        Returns:
            tuple: Scores e média
        """
        kfold = KFold(n_splits=cv, shuffle=True, random_state=42)
        scores = cross_val_score(modelo, X, y, cv=kfold, scoring=scoring)
        
        return scores, scores.mean(), scores.std()
    
    @staticmethod
    def plotar_matriz_confusao(cm, classes=None, normalizar=False):
        """
        Plota matriz de confusão
        
        Args:
            cm: Matriz de confusão
            classes: Nomes das classes
            normalizar: Se True, normaliza a matriz
        """
        if normalizar:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        
        plt.figure(figsize=(8, 6))
        plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title('Matriz de Confusão')
        plt.colorbar()
        
        if classes is not None:
            tick_marks = np.arange(len(classes))
            plt.xticks(tick_marks, classes, rotation=45)
            plt.yticks(tick_marks, classes)
        
        fmt = '.2f' if normalizar else 'd'
        thresh = cm.max() / 2.
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                plt.text(j, i, format(cm[i, j], fmt),
                        horizontalalignment="center",
                        color="white" if cm[i, j] > thresh else "black")
        
        plt.tight_layout()
        plt.ylabel('Classe Real')
        plt.xlabel('Classe Prevista')
        
        return plt
    
    @staticmethod
    def plotar_curva_roc(fpr, tpr, auc_score):
        """
        Plota curva ROC
        
        Args:
            fpr: False Positive Rate
            tpr: True Positive Rate
            auc_score: Área sob a curva
        """
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, 
                 label=f'ROC curve (area = {auc_score:.2f})')
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic')
        plt.legend(loc="lower right")
        
        return plt
    
    @staticmethod
    def monitorar_drift(X_treino, X_atual, threshold=0.05):
        """
        Monitora drift nos dados
        
        Args:
            X_treino: Dados de treino originais
            X_atual: Dados atuais
            threshold: Limiar para considerar drift
            
        Returns:
            dict: Dicionário com métricas de drift
        """
        # Calcula estatísticas básicas
        media_treino = X_treino.mean(axis=0)
        media_atual = X_atual.mean(axis=0)
        
        std_treino = X_treino.std(axis=0)
        std_atual = X_atual.std(axis=0)
        
        # Calcula diferenças relativas
        diff_media = np.abs((media_atual - media_treino) / media_treino)
        diff_std = np.abs((std_atual - std_treino) / std_treino)
        
        # Identifica features com drift
        features_drift = np.where(diff_media > threshold)[0]
        
        return {
            'features_drift': features_drift,
            'diff_media': diff_media,
            'diff_std': diff_std,
            'drift_detectado': len(features_drift) > 0
        }


# Exemplo de uso
if __name__ == "__main__":
    # Dados de exemplo
    np.random.seed(42)
    y_true = np.random.randint(0, 2, 100)
    y_pred = np.random.randint(0, 2, 100)
    y_proba = np.random.rand(100)
    
    # Avaliação de classificação
    metricas, cm = MetricasValidacao.avaliar_classificacao(y_true, y_pred, y_proba)
    print("Métricas de classificação:")
    for metrica, valor in metricas.items():
        if isinstance(valor, (int, float)):
            print(f"  {metrica}: {valor:.4f}")
    
    # Plotar matriz de confusão
    plt_cm = MetricasValidacao.plotar_matriz_confusao(cm, classes=['Classe 0', 'Classe 1'])
    plt_cm.savefig('matriz_confusao.png')
    
    # Plotar curva ROC
    if 'auc_roc' in metricas:
        plt_roc = MetricasValidacao.plotar_curva_roc(
            metricas['fpr'], metricas['tpr'], metricas['auc_roc'])
        plt_roc.savefig('curva_roc.png')
    
    # Exemplo de monitoramento de drift
    X_treino = np.random.rand(100, 5)
    X_atual = np.random.rand(100, 5) * 1.1  # Simula pequeno drift
    
    drift_info = MetricasValidacao.monitorar_drift(X_treino, X_atual, threshold=0.05)
    print("\nMonitoramento de drift:")
    print(f"  Drift detectado: {drift_info['drift_detectado']}")
    if drift_info['drift_detectado']:
        print(f"  Features com drift: {drift_info['features_drift']}")