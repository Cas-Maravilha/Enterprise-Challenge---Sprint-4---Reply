import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

class ValidacaoCruzadaTemporal:
    """Implementa estratégias de validação cruzada temporal para séries temporais"""
    
    def __init__(self, n_splits=5, gap=0):
        """
        Inicializa a validação cruzada temporal
        
        Args:
            n_splits: Número de divisões (folds)
            gap: Número de amostras a ignorar entre treino e teste
        """
        self.n_splits = n_splits
        self.gap = gap
        self.tscv = TimeSeriesSplit(n_splits=n_splits, gap=gap)
    
    def validar_modelo(self, modelo, X, y, datas=None, classificacao=True):
        """
        Valida modelo usando validação cruzada temporal
        
        Args:
            modelo: Modelo a ser validado
            X: Features
            y: Target
            datas: Array de datas (opcional)
            classificacao: Se True, usa métricas de classificação, senão regressão
            
        Returns:
            dict: Resultados da validação
        """
        resultados_folds = []
        indices_folds = []
        
        # Para cada fold
        for fold, (train_idx, test_idx) in enumerate(self.tscv.split(X)):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            
            # Treinar modelo
            modelo.fit(X_train, y_train)
            
            # Prever
            y_pred = modelo.predict(X_test)
            
            # Calcular métricas
            if classificacao:
                # Métricas de classificação
                metricas = self._calcular_metricas_classificacao(y_test, y_pred, modelo)
            else:
                # Métricas de regressão
                metricas = self._calcular_metricas_regressao(y_test, y_pred)
            
            # Adicionar informações do fold
            metricas['fold'] = fold
            metricas['n_treino'] = len(train_idx)
            metricas['n_teste'] = len(test_idx)
            
            # Adicionar datas se disponíveis
            if datas is not None:
                metricas['data_inicio_treino'] = datas[train_idx[0]]
                metricas['data_fim_treino'] = datas[train_idx[-1]]
                metricas['data_inicio_teste'] = datas[test_idx[0]]
                metricas['data_fim_teste'] = datas[test_idx[-1]]
            
            resultados_folds.append(metricas)
            indices_folds.append((train_idx, test_idx))
        
        # Calcular médias das métricas
        metricas_medias = self._calcular_metricas_medias(resultados_folds)
        
        return {
            'resultados_folds': resultados_folds,
            'metricas_medias': metricas_medias,
            'indices_folds': indices_folds
        }
    
    def _calcular_metricas_classificacao(self, y_true, y_pred, modelo):
        """Calcula métricas para problemas de classificação"""
        metricas = {
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, average='weighted'),
            'recall': recall_score(y_true, y_pred, average='weighted'),
            'f1': f1_score(y_true, y_pred, average='weighted')
        }
        
        # AUC-ROC para classificação binária
        if len(np.unique(y_true)) == 2 and hasattr(modelo, 'predict_proba'):
            y_proba = modelo.predict_proba(X_test)[:, 1]
            metricas['auc_roc'] = roc_auc_score(y_true, y_proba)
        
        return metricas
    
    def _calcular_metricas_regressao(self, y_true, y_pred):
        """Calcula métricas para problemas de regressão"""
        return {
            'mse': mean_squared_error(y_true, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
            'mae': mean_absolute_error(y_true, y_pred),
            'r2': r2_score(y_true, y_pred)
        }
    
    def _calcular_metricas_medias(self, resultados_folds):
        """Calcula médias das métricas de todos os folds"""
        metricas_medias = {}
        
        # Identificar todas as métricas disponíveis
        metricas_disponiveis = set()
        for resultado in resultados_folds:
            for metrica in resultado.keys():
                if isinstance(resultado[metrica], (int, float)):
                    metricas_disponiveis.add(metrica)
        
        # Calcular média e desvio padrão para cada métrica
        for metrica in metricas_disponiveis:
            valores = [r[metrica] for r in resultados_folds if metrica in r]
            if valores:
                metricas_medias[f'{metrica}_media'] = np.mean(valores)
                metricas_medias[f'{metrica}_std'] = np.std(valores)
        
        return metricas_medias
    
    def plotar_resultados(self, resultados, metrica='accuracy'):
        """
        Plota resultados da validação cruzada temporal
        
        Args:
            resultados: Resultados da validação
            metrica: Métrica a ser plotada
            
        Returns:
            matplotlib.figure: Figura com gráfico
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Extrair valores da métrica para cada fold
        folds = []
        valores = []
        
        for resultado in resultados['resultados_folds']:
            if metrica in resultado:
                folds.append(resultado['fold'])
                valores.append(resultado[metrica])
        
        # Plotar barras
        ax.bar(folds, valores)
        
        # Adicionar linha com média
        if f'{metrica}_media' in resultados['metricas_medias']:
            media = resultados['metricas_medias'][f'{metrica}_media']
            ax.axhline(y=media, color='r', linestyle='--', 
                      label=f'Média: {media:.4f}')
        
        ax.set_xlabel('Fold')
        ax.set_ylabel(metrica)
        ax.set_title(f'Resultados da Validação Cruzada Temporal - {metrica}')
        ax.grid(axis='y', alpha=0.3)
        ax.legend()
        
        return fig
    
    def plotar_evolucao_temporal(self, resultados, metrica='accuracy', datas_disponiveis=True):
        """
        Plota evolução temporal da métrica
        
        Args:
            resultados: Resultados da validação
            metrica: Métrica a ser plotada
            datas_disponiveis: Se True, usa datas, senão usa índices
            
        Returns:
            matplotlib.figure: Figura com gráfico
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Verificar se há datas nos resultados
        tem_datas = datas_disponiveis and 'data_inicio_teste' in resultados['resultados_folds'][0]
        
        # Extrair valores para plotagem
        x_values = []
        y_values = []
        
        for resultado in resultados['resultados_folds']:
            if metrica in resultado:
                if tem_datas:
                    x_values.append(resultado['data_inicio_teste'])
                else:
                    x_values.append(resultado['fold'])
                
                y_values.append(resultado[metrica])
        
        # Plotar evolução
        ax.plot(x_values, y_values, marker='o', linestyle='-')
        
        # Configurar eixos
        if tem_datas:
            ax.set_xlabel('Data')
            plt.xticks(rotation=45)
        else:
            ax.set_xlabel('Fold')
        
        ax.set_ylabel(metrica)
        ax.set_title(f'Evolução Temporal - {metrica}')
        ax.grid(True, alpha=0.3)
        
        # Adicionar tendência
        z = np.polyfit(range(len(y_values)), y_values, 1)
        p = np.poly1d(z)
        ax.plot(x_values, p(range(len(y_values))), "r--", 
               label=f'Tendência: {z[0]:.4f}x + {z[1]:.4f}')
        
        ax.legend()
        plt.tight_layout()
        
        return fig
    
    def plotar_janelas_validacao(self, X, indices_folds):
        """
        Plota as janelas de validação
        
        Args:
            X: Dados de entrada
            indices_folds: Índices dos folds
            
        Returns:
            matplotlib.figure: Figura com gráfico
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        n_amostras = len(X)
        
        for i, (train_idx, test_idx) in enumerate(indices_folds):
            # Criar arrays para visualização
            train = np.zeros(n_amostras)
            train[train_idx] = 1
            
            test = np.zeros(n_amostras)
            test[test_idx] = 1
            
            # Plotar
            ax.scatter(train_idx, [i + 0.1] * len(train_idx), 
                      c='blue', label='Treino' if i == 0 else "", s=10)
            
            ax.scatter(test_idx, [i + 0.2] * len(test_idx), 
                      c='red', label='Teste' if i == 0 else "", s=10)
        
        ax.set_yticks(np.arange(len(indices_folds)) + 0.15)
        ax.set_yticklabels([f'Fold {i}' for i in range(len(indices_folds))])
        ax.set_xlabel('Índice da Amostra')
        ax.set_title('Janelas de Validação Cruzada Temporal')
        ax.legend()
        
        return fig


# Exemplo de uso
if __name__ == "__main__":
    # Dados de exemplo (série temporal)
    np.random.seed(42)
    n_amostras = 100
    
    # Criar série temporal sintética
    t = np.linspace(0, 10, n_amostras)
    y = np.sin(t) + 0.1 * np.random.randn(n_amostras)
    
    # Features: valores passados
    X = np.zeros((n_amostras - 3, 3))
    for i in range(len(X)):
        X[i] = [y[i], y[i+1], y[i+2]]
    
    # Target: próximo valor
    y_target = y[3:]
    
    # Datas fictícias
    import datetime as dt
    datas = [dt.datetime(2023, 1, 1) + dt.timedelta(days=i) for i in range(len(X))]
    
    # Modelo simples
    from sklearn.linear_model import LinearRegression
    modelo = LinearRegression()
    
    # Validação cruzada temporal
    validador = ValidacaoCruzadaTemporal(n_splits=5)
    resultados = validador.validar_modelo(
        modelo, X, y_target, datas=datas, classificacao=False)
    
    # Imprimir resultados
    print("Métricas médias:")
    for k, v in resultados['metricas_medias'].items():
        print(f"  {k}: {v:.4f}")
    
    # Plotar resultados
    fig1 = validador.plotar_resultados(resultados, metrica='r2')
    fig1.savefig('validacao_cruzada_r2.png')
    
    fig2 = validador.plotar_evolucao_temporal(resultados, metrica='rmse')
    fig2.savefig('evolucao_temporal_rmse.png')
    
    fig3 = validador.plotar_janelas_validacao(X, resultados['indices_folds'])
    fig3.savefig('janelas_validacao.png')