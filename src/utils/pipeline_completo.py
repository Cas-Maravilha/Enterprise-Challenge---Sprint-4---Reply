import os
import numpy as np
import pandas as pd
from modelos_ia import ModeloEnsemble
from metricas_validacao import MetricasValidacao
from estrategia_escalabilidade import EstrategiaEscalabilidade
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import logging
import json
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("Pipeline IA")

class PipelineIA:
    """
    Pipeline completo para treinamento, validação e implantação de modelos de IA
    """
    
    def __init__(self, config_path=None):
        """
        Inicializa o pipeline
        
        Args:
            config_path: Caminho para arquivo de configuração (opcional)
        """
        self.modelo = ModeloEnsemble()
        self.escalabilidade = EstrategiaEscalabilidade()
        
        # Carregar configuração se fornecida
        self.config = {
            "nome_modelo": "ensemble_ia",
            "pesos_ensemble": {'random_forest': 0.5, 'lstm': 0.3, 'svm': 0.2},
            "threshold_drift": 0.05,
            "usar_validacao_cruzada": True,
            "k_folds": 5,
            "test_size": 0.2,
            "random_state": 42
        }
        
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config.update(json.load(f))
        
        # Atualizar pesos do ensemble
        self.modelo.pesos = self.config["pesos_ensemble"]
        
        logger.info("Pipeline inicializado com configuração: %s", self.config)
    
    def preparar_dados(self, dados, target_col, colunas_temporais=None, 
                      timesteps=5, test_size=None):
        """
        Prepara os dados para treinamento
        
        Args:
            dados: DataFrame com os dados
            target_col: Nome da coluna alvo
            colunas_temporais: Lista de colunas para dados temporais (LSTM)
            timesteps: Número de timesteps para dados temporais
            test_size: Tamanho do conjunto de teste (sobrescreve config)
            
        Returns:
            tuple: X_train, X_test, y_train, y_test, X_temporal_train, X_temporal_test
        """
        logger.info("Preparando dados para treinamento")
        
        # Separar features e target
        X = dados.drop(columns=[target_col])
        y = dados[target_col]
        
        # Dividir em treino e teste
        test_size = test_size or self.config["test_size"]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=self.config["random_state"]
        )
        
        logger.info("Dados divididos: %d amostras de treino, %d amostras de teste", 
                   len(X_train), len(X_test))
        
        # Preparar dados temporais se necessário
        X_temporal_train = X_temporal_test = None
        if colunas_temporais:
            logger.info("Preparando dados temporais para LSTM")
            X_temporal_train = self._criar_sequencias_temporais(
                X_train[colunas_temporais], timesteps)
            X_temporal_test = self._criar_sequencias_temporais(
                X_test[colunas_temporais], timesteps)
        
        return X_train, X_test, y_train, y_test, X_temporal_train, X_temporal_test
    
    def _criar_sequencias_temporais(self, dados, timesteps):
        """
        Cria sequências temporais para LSTM
        
        Args:
            dados: DataFrame com dados temporais
            timesteps: Número de timesteps
            
        Returns:
            array: Array 3D [amostras, timesteps, features]
        """
        valores = dados.values
        n_amostras = valores.shape[0] - timesteps + 1
        n_features = valores.shape[1]
        
        sequencias = np.zeros((n_amostras, timesteps, n_features))
        
        for i in range(n_amostras):
            sequencias[i] = valores[i:i+timesteps]
        
        return sequencias
    
    def treinar(self, X_train, y_train, X_test, y_test, 
               X_temporal_train=None, X_temporal_test=None):
        """
        Treina o modelo ensemble
        
        Args:
            X_train, y_train: Dados de treino
            X_test, y_test: Dados de teste
            X_temporal_train, X_temporal_test: Dados temporais (opcional)
            
        Returns:
            dict: Resultados da avaliação
        """
        logger.info("Iniciando treinamento do modelo ensemble")
        
        # Treinar modelo
        resultados = self.modelo.treinar_modelos(
            X_train, y_train, 
            X_temporal=X_temporal_train
        )
        
        # Avaliar no conjunto de teste
        y_pred, y_proba = self.modelo.prever(
            X_test, 
            X_temporal=X_temporal_test
        )
        
        # Calcular métricas detalhadas
        metricas, cm = MetricasValidacao.avaliar_classificacao(
            y_test, y_pred, y_proba
        )
        
        # Validação cruzada (opcional)
        if self.config["usar_validacao_cruzada"]:
            logger.info("Realizando validação cruzada")
            # Nota: Simplificado para o exemplo, na prática seria mais complexo
            # para o ensemble completo
            cv_scores, cv_mean, cv_std = MetricasValidacao.validacao_cruzada(
                self.modelo.random_forest, X_train, y_train, 
                cv=self.config["k_folds"]
            )
            metricas["cv_scores"] = cv_scores.tolist()
            metricas["cv_mean"] = cv_mean
            metricas["cv_std"] = cv_std
        
        logger.info("Treinamento concluído. Métricas: %s", 
                   {k: v for k, v in metricas.items() if isinstance(v, (int, float))})
        
        return resultados, metricas, cm
    
    def salvar_modelo(self, metricas, parametros=None):
        """
        Salva o modelo treinado
        
        Args:
            metricas: Métricas de desempenho
            parametros: Parâmetros do modelo (opcional)
            
        Returns:
            str: ID da versão salva
        """
        logger.info("Salvando modelo")
        
        # Parâmetros padrão se não fornecidos
        if parametros is None:
            parametros = {
                "pesos_ensemble": self.modelo.pesos,
                "config": self.config
            }
        
        # Salvar modelo
        versao_id = self.escalabilidade.salvar_modelo(
            self.modelo,
            self.config["nome_modelo"],
            metricas=metricas,
            parametros=parametros
        )
        
        logger.info("Modelo salvo com ID: %s", versao_id)
        return versao_id
    
    def carregar_modelo(self, versao_id=None):
        """
        Carrega um modelo salvo
        
        Args:
            versao_id: ID da versão (opcional)
            
        Returns:
            ModeloEnsemble: Modelo carregado
        """
        logger.info("Carregando modelo%s", 
                   f" (versão {versao_id})" if versao_id else "")
        
        self.modelo = self.escalabilidade.carregar_modelo(versao_id)
        return self.modelo
    
    def monitorar_drift(self, X_referencia, X_atual):
        """
        Monitora drift nos dados
        
        Args:
            X_referencia: Dados de referência
            X_atual: Dados atuais
            
        Returns:
            dict: Informações sobre drift
        """
        logger.info("Monitorando drift nos dados")
        
        drift_info = MetricasValidacao.monitorar_drift(
            X_referencia, X_atual, 
            threshold=self.config["threshold_drift"]
        )
        
        if drift_info["drift_detectado"]:
            logger.warning("Drift detectado em %d features", 
                          len(drift_info["features_drift"]))
        else:
            logger.info("Nenhum drift significativo detectado")
        
        return drift_info
    
    def gerar_relatorio(self, resultados, metricas, cm, 
                       caminho_saida="relatorio_modelo.html"):
        """
        Gera relatório de desempenho do modelo
        
        Args:
            resultados: Resultados do treinamento
            metricas: Métricas detalhadas
            cm: Matriz de confusão
            caminho_saida: Caminho para salvar o relatório
        """
        logger.info("Gerando relatório de desempenho")
        
        # Aqui seria implementada a geração do relatório HTML
        # Simplificado para este exemplo
        
        # Salvar matriz de confusão
        plt_cm = MetricasValidacao.plotar_matriz_confusao(cm)
        plt_cm.savefig("matriz_confusao.png")
        
        # Salvar curva ROC se disponível
        if 'auc_roc' in metricas and 'fpr' in metricas and 'tpr' in metricas:
            plt_roc = MetricasValidacao.plotar_curva_roc(
                metricas['fpr'], metricas['tpr'], metricas['auc_roc'])
            plt_roc.savefig("curva_roc.png")
        
        # Salvar métricas em JSON
        with open("metricas_detalhadas.json", 'w') as f:
            # Filtrar arrays grandes para o JSON
            metricas_json = {k: v for k, v in metricas.items() 
                            if not isinstance(v, np.ndarray)}
            json.dump(metricas_json, f, indent=2)
        
        logger.info("Relatório gerado")


# Exemplo de uso
if __name__ == "__main__":
    # Dados de exemplo
    np.random.seed(42)
    n_amostras = 1000
    n_features = 10
    
    # Criar dados sintéticos
    X = np.random.rand(n_amostras, n_features)
    y = (X[:, 0] + X[:, 1] > 1).astype(int)  # Regra simples
    
    # Criar DataFrame
    colunas = [f"feature_{i}" for i in range(n_features)]
    df = pd.DataFrame(X, columns=colunas)
    df["target"] = y
    
    # Inicializar pipeline
    pipeline = PipelineIA()
    
    # Preparar dados
    X_train, X_test, y_train, y_test, X_temporal_train, X_temporal_test = \
        pipeline.preparar_dados(
            df, 
            target_col="target",
            colunas_temporais=colunas[:5],  # Primeiras 5 colunas para LSTM
            timesteps=3
        )
    
    # Treinar modelo
    resultados, metricas, cm = pipeline.treinar(
        X_train, y_train, X_test, y_test,
        X_temporal_train, X_temporal_test
    )
    
    # Salvar modelo
    versao_id = pipeline.salvar_modelo(metricas)
    
    # Gerar relatório
    pipeline.gerar_relatorio(resultados, metricas, cm)
    
    # Simular dados novos com drift
    X_novo = X_test * 1.2
    
    # Monitorar drift
    drift_info = pipeline.monitorar_drift(X_test, X_novo)
    
    print("\nResumo do pipeline:")
    print(f"- Modelo treinado e salvo com ID: {versao_id}")
    print(f"- Acurácia no conjunto de teste: {metricas['acuracia']:.4f}")
    if 'auc_roc' in metricas:
        print(f"- AUC-ROC: {metricas['auc_roc']:.4f}")
    print(f"- Drift detectado: {drift_info['drift_detectado']}")
    if drift_info['drift_detectado']:
        print(f"- Features com drift: {drift_info['features_drift']}")