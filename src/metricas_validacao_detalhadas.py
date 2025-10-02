import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_curve, auc, confusion_matrix, mean_absolute_error,
    mean_squared_error, r2_score, precision_recall_curve,
    average_precision_score, log_loss
)
from sklearn.model_selection import TimeSeriesSplit
import datetime as dt

class MetricasValidacaoDetalhadas:
    """Implementa métricas de validação detalhadas com valores-alvo e monitoramento"""
    
    def __init__(self):
        # Valores-alvo para métricas de classificação
        self.targets = {
            'accuracy': 0.85,
            'precision': 0.80,
            'recall': 0.85,
            'f1': 0.82,
            'auc_roc': 0.90,
            'log_loss': 0.35,
            'mae': 0.15,
            'rmse': 0.20,
            'r2': 0.75
        }
        
        # Histórico de métricas para monitoramento
        self.historico = []
    
    def validacao_cruzada_temporal(self, modelo, X, y, datas=None, n_splits=5):
        """
        Realiza validação cruzada temporal
        
        Args:
            modelo: Modelo a ser avaliado
            X: Features
            y: Target
            datas: Array com timestamps dos dados
            n_splits: Número de divisões temporais
            
        Returns:
            dict: Métricas por fold e média
        """
        tscv = TimeSeriesSplit(n_splits=n_splits)
        resultados = {
            'accuracy': [], 'precision': [], 'recall': [], 
            'f1': [], 'auc_roc': []
        }
        
        for fold, (train_idx, test_idx) in enumerate(tscv.split(X)):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            
            # Treinar modelo
            modelo.fit(X_train, y_train)
            
            # Prever
            y_pred = modelo.predict(X_test)
            if hasattr(modelo, "predict_proba"):
                y_proba = modelo.predict_proba(X_test)[:, 1]
            else:
                y_proba = y_pred
            
            # Calcular métricas
            resultados['accuracy'].append(accuracy_score(y_test, y_pred))
            resultados['precision'].append(precision_score(y_test, y_pred, average='weighted'))
            resultados['recall'].append(recall_score(y_test, y_pred, average='weighted'))
            resultados['f1'].append(f1_score(y_test, y_pred, average='weighted'))
            
            # AUC-ROC (se binário)
            if len(np.unique(y)) == 2:
                resultados['auc_roc'].append(roc_auc_score(y_test, y_proba))
        
        # Calcular médias
        medias = {k: np.mean(v) for k, v in resultados.items()}
        desvios = {k: np.std(v) for k, v in resultados.items()}
        
        return {
            'por_fold': resultados,
            'media': medias,
            'desvio': desvios
        }
    
    def monitorar_drift_temporal(self, X_ref, X_atual, datas_atual=None, threshold=0.05):
        """
        Monitora drift nos dados ao longo do tempo
        
        Args:
            X_ref: Dados de referência
            X_atual: Dados atuais
            datas_atual: Timestamps dos dados atuais
            threshold: Limiar para considerar drift
            
        Returns:
            dict: Métricas de drift
        """
        # Estatísticas básicas
        media_ref = X_ref.mean(axis=0)
        std_ref = X_ref.std(axis=0)
        
        # Calcular drift por feature
        drift_por_feature = {}
        for i in range(X_atual.shape[1]):
            # Estatísticas da feature atual
            media_atual = X_atual[:, i].mean()
            std_atual = X_atual[:, i].std()
            
            # Calcular diferenças relativas
            diff_media = abs((media_atual - media_ref[i]) / media_ref[i]) if media_ref[i] != 0 else 0
            diff_std = abs((std_atual - std_ref[i]) / std_ref[i]) if std_ref[i] != 0 else 0
            
            drift_por_feature[i] = {
                'diff_media': diff_media,
                'diff_std': diff_std,
                'drift_detectado': diff_media > threshold or diff_std > threshold
            }
        
        # Drift global
        features_com_drift = [i for i, info in drift_por_feature.items() 
                             if info['drift_detectado']]
        
        # Análise temporal se datas forem fornecidas
        drift_temporal = None
        if datas_atual is not None:
            # Agrupar por período (ex: semana)
            df_atual = pd.DataFrame(X_atual)
            df_atual['data'] = datas_atual
            
            # Converter para datetime se necessário
            if not isinstance(datas_atual[0], (dt.datetime, pd.Timestamp)):
                df_atual['data'] = pd.to_datetime(df_atual['data'])
            
            # Agrupar por semana
            df_atual['semana'] = df_atual['data'].dt.isocalendar().week
            
            # Calcular drift por semana
            drift_temporal = {}
            for semana, grupo in df_atual.groupby('semana'):
                X_semana = grupo.drop(['data', 'semana'], axis=1).values
                
                # Estatísticas da semana
                media_semana = X_semana.mean(axis=0)
                
                # Calcular diferença relativa
                diff_media = np.abs((media_semana - media_ref) / media_ref)
                diff_media[media_ref == 0] = 0
                
                drift_detectado = np.any(diff_media > threshold)
                
                drift_temporal[semana] = {
                    'diff_media_max': diff_media.max(),
                    'drift_detectado': drift_detectado,
                    'features_drift': np.where(diff_media > threshold)[0].tolist()
                }
        
        return {
            'drift_por_feature': drift_por_feature,
            'features_com_drift': features_com_drift,
            'percentual_features_drift': len(features_com_drift) / X_atual.shape[1],
            'drift_temporal': drift_temporal
        }
    
    def calcular_kpis(self, y_true, y_pred, y_proba=None, custo_fp=1, custo_fn=5):
        """
        Calcula KPIs técnicos e de negócio
        
        Args:
            y_true: Valores reais
            y_pred: Valores previstos
            y_proba: Probabilidades previstas
            custo_fp: Custo de falso positivo
            custo_fn: Custo de falso negativo
            
        Returns:
            dict: KPIs técnicos e de negócio
        """
        # KPIs técnicos
        kpis_tecnicos = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted'),
            'recall': recall_score(y_true, y_pred, average='weighted'),
            'f1': f1_score(y_true, y_pred, average='weighted')
        }
        
        # Matriz de confusão para análise de erros
        cm = confusion_matrix(y_true, y_pred)
        
        # KPIs de negócio
        # Exemplo: custo de erros (FP e FN têm custos diferentes)
        if len(cm) == 2:  # Caso binário
            tn, fp, fn, tp = cm.ravel()
            
            # Custo total de erros
            custo_total = (fp * custo_fp) + (fn * custo_fn)
            
            # Taxa de acerto em casos positivos (importante para negócio)
            taxa_deteccao = tp / (tp + fn) if (tp + fn) > 0 else 0
            
            # Taxa de falso alarme (importante para confiança no sistema)
            taxa_falso_alarme = fp / (fp + tn) if (fp + tn) > 0 else 0
            
            kpis_negocio = {
                'custo_total_erros': custo_total,
                'taxa_deteccao': taxa_deteccao,
                'taxa_falso_alarme': taxa_falso_alarme
            }
        else:
            kpis_negocio = {}
        
        # Comparação com valores-alvo
        comparacao_targets = {}
        for metrica, valor in kpis_tecnicos.items():
            if metrica in self.targets:
                target = self.targets[metrica]
                diff = valor - target
                status = 'OK' if valor >= target else 'Abaixo do alvo'
                
                comparacao_targets[metrica] = {
                    'valor': valor,
                    'target': target,
                    'diff': diff,
                    'status': status
                }
        
        # Registrar no histórico
        self.historico.append({
            'timestamp': dt.datetime.now(),
            'kpis_tecnicos': kpis_tecnicos,
            'kpis_negocio': kpis_negocio
        })
        
        return {
            'kpis_tecnicos': kpis_tecnicos,
            'kpis_negocio': kpis_negocio,
            'comparacao_targets': comparacao_targets,
            'matriz_confusao': cm
        }
    
    def plotar_evolucao_metricas(self):
        """
        Plota evolução das métricas ao longo do tempo
        
        Returns:
            matplotlib.figure: Figura com gráficos
        """
        if not self.historico:
            return None
        
        # Extrair dados do histórico
        timestamps = [h['timestamp'] for h in self.historico]
        metricas = {}
        
        # Coletar todas as métricas disponíveis
        for metrica in self.historico[0]['kpis_tecnicos'].keys():
            metricas[metrica] = [h['kpis_tecnicos'][metrica] for h in self.historico]
        
        # Plotar
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for metrica, valores in metricas.items():
            ax.plot(timestamps, valores, marker='o', label=metrica)
            
            # Adicionar linha de target se disponível
            if metrica in self.targets:
                ax.axhline(y=self.targets[metrica], linestyle='--', 
                          alpha=0.7, color='gray', label=f'Target {metrica}')
        
        ax.set_xlabel('Data')
        ax.set_ylabel('Valor')
        ax.set_title('Evolução das Métricas')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        return fig


# Exemplo de uso
if __name__ == "__main__":
    # Dados de exemplo
    np.random.seed(42)
    X = np.random.rand(1000, 5)
    y = (X[:, 0] + X[:, 1] > 1).astype(int)
    
    # Dividir em treino e teste
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    
    # Treinar modelo simples
    from sklearn.ensemble import RandomForestClassifier
    modelo = RandomForestClassifier(n_estimators=100)
    modelo.fit(X_train, y_train)
    
    # Prever
    y_pred = modelo.predict(X_test)
    y_proba = modelo.predict_proba(X_test)[:, 1]
    
    # Instanciar classe de métricas
    metricas = MetricasValidacaoDetalhadas()
    
    # Validação cruzada temporal
    resultados_cv = metricas.validacao_cruzada_temporal(modelo, X, y)
    print("Resultados da validação cruzada temporal:")
    for metrica, valor in resultados_cv['media'].items():
        print(f"  {metrica}: {valor:.4f} ± {resultados_cv['desvio'][metrica]:.4f}")
    
    # Monitorar drift
    # Simular dados com drift
    X_drift = X_test.copy()
    X_drift[:, 0] *= 1.2  # Aumentar valores da primeira feature
    
    # Criar datas fictícias
    datas = [dt.datetime(2023, 1, 1) + dt.timedelta(days=i) for i in range(len(X_drift))]
    
    drift_info = metricas.monitorar_drift_temporal(X_train, X_drift, datas)
    print("\nDrift detectado em features:", drift_info['features_com_drift'])
    print(f"Percentual de features com drift: {drift_info['percentual_features_drift']:.2%}")
    
    # Calcular KPIs
    kpis = metricas.calcular_kpis(y_test, y_pred, y_proba)
    print("\nKPIs Técnicos:")
    for k, v in kpis['kpis_tecnicos'].items():
        print(f"  {k}: {v:.4f}")
    
    print("\nComparação com targets:")
    for k, v in kpis['comparacao_targets'].items():
        print(f"  {k}: {v['valor']:.4f} vs target {v['target']:.4f} - {v['status']}")
    
    if kpis['kpis_negocio']:
        print("\nKPIs de Negócio:")
        for k, v in kpis['kpis_negocio'].items():
            print(f"  {k}: {v:.4f}")