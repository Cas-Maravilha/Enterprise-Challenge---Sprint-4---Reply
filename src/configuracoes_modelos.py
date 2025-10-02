import json
from typing import Dict, Any, Optional

class ConfiguracoesModelos:
    """Define configurações específicas para cada modelo de IA"""
    
    def __init__(self):
        self.configuracoes = {
            "random_forest": {
                "parametros": {
                    "n_estimators": 100,
                    "max_depth": None,
                    "min_samples_split": 2,
                    "min_samples_leaf": 1,
                    "max_features": "sqrt",
                    "bootstrap": True,
                    "class_weight": "balanced",
                    "random_state": 42
                },
                "hyperparametros_busca": {
                    "n_estimators": [50, 100, 200],
                    "max_depth": [None, 10, 20, 30],
                    "min_samples_split": [2, 5, 10],
                    "min_samples_leaf": [1, 2, 4]
                },
                "metricas_otimizacao": "f1",
                "recursos_computacionais": {
                    "cpu": "2",
                    "memoria": "4Gi",
                    "paralelismo": 4
                }
            },
            "lstm": {
                "parametros": {
                    "unidades": [50, 50],
                    "dropout": 0.2,
                    "recurrent_dropout": 0.2,
                    "optimizer": "adam",
                    "loss": "binary_crossentropy",
                    "batch_size": 32,
                    "epochs": 50,
                    "validation_split": 0.2,
                    "early_stopping_patience": 10
                },
                "hyperparametros_busca": {
                    "unidades": [[32, 32], [50, 50], [100, 100]],
                    "dropout": [0.1, 0.2, 0.3],
                    "batch_size": [16, 32, 64],
                    "optimizer": ["adam", "rmsprop"]
                },
                "metricas_otimizacao": "val_loss",
                "recursos_computacionais": {
                    "cpu": "4",
                    "memoria": "8Gi",
                    "gpu": "1",
                    "gpu_memoria": "8Gi"
                }
            },
            "isolation_forest": {
                "parametros": {
                    "n_estimators": 100,
                    "contamination": 0.1,
                    "max_samples": "auto",
                    "max_features": 1.0,
                    "bootstrap": False,
                    "random_state": 42
                },
                "hyperparametros_busca": {
                    "n_estimators": [50, 100, 200],
                    "contamination": [0.05, 0.1, 0.15],
                    "max_samples": ["auto", 100, 200]
                },
                "metricas_otimizacao": "auc_roc",
                "recursos_computacionais": {
                    "cpu": "2",
                    "memoria": "4Gi",
                    "paralelismo": 4
                }
            },
            "svm": {
                "parametros": {
                    "C": 1.0,
                    "kernel": "rbf",
                    "gamma": "scale",
                    "probability": True,
                    "class_weight": "balanced",
                    "random_state": 42
                },
                "hyperparametros_busca": {
                    "C": [0.1, 1.0, 10.0],
                    "kernel": ["linear", "rbf", "poly"],
                    "gamma": ["scale", "auto", 0.1, 0.01]
                },
                "metricas_otimizacao": "accuracy",
                "recursos_computacionais": {
                    "cpu": "2",
                    "memoria": "4Gi",
                    "paralelismo": 1
                }
            },
            "ensemble": {
                "parametros": {
                    "pesos": {
                        "random_forest": 0.5,
                        "lstm": 0.3,
                        "svm": 0.2
                    },
                    "threshold": 0.5,
                    "metodo_combinacao": "weighted_average"
                },
                "hyperparametros_busca": {
                    "pesos": [
                        {"random_forest": 0.6, "lstm": 0.3, "svm": 0.1},
                        {"random_forest": 0.5, "lstm": 0.3, "svm": 0.2},
                        {"random_forest": 0.4, "lstm": 0.4, "svm": 0.2}
                    ],
                    "threshold": [0.3, 0.5, 0.7]
                },
                "metricas_otimizacao": "f1",
                "recursos_computacionais": {
                    "cpu": "4",
                    "memoria": "8Gi",
                    "paralelismo": 1
                }
            }
        }
        
        # Configurações de produção
        self.configuracoes_producao = {
            "batch_size": 64,
            "timeout": 30,  # segundos
            "max_concurrent_requests": 100,
            "autoscaling": {
                "min_replicas": 2,
                "max_replicas": 10,
                "target_cpu_utilization": 70,
                "target_memory_utilization": 80
            },
            "monitoring": {
                "latency_threshold_ms": 200,
                "error_rate_threshold": 0.01,
                "drift_check_frequency": "hourly"
            },
            "caching": {
                "enabled": True,
                "ttl_seconds": 3600,
                "max_size_mb": 1024
            }
        }
    
    def obter_configuracao(self, modelo: str) -> Dict[str, Any]:
        """
        Obtém configuração para um modelo específico
        
        Args:
            modelo: Nome do modelo
            
        Returns:
            Dict: Configuração do modelo
        """
        if modelo not in self.configuracoes:
            raise ValueError(f"Modelo '{modelo}' não encontrado nas configurações")
        
        return self.configuracoes[modelo]
    
    def obter_parametros_treinamento(self, modelo: str) -> Dict[str, Any]:
        """
        Obtém parâmetros de treinamento para um modelo específico
        
        Args:
            modelo: Nome do modelo
            
        Returns:
            Dict: Parâmetros de treinamento
        """
        return self.obter_configuracao(modelo)["parametros"]
    
    def obter_recursos_computacionais(self, modelo: str) -> Dict[str, Any]:
        """
        Obtém recursos computacionais para um modelo específico
        
        Args:
            modelo: Nome do modelo
            
        Returns:
            Dict: Recursos computacionais
        """
        return self.obter_configuracao(modelo)["recursos_computacionais"]
    
    def gerar_configuracao_kubernetes(self, modelo: str) -> str:
        """
        Gera configuração Kubernetes para um modelo específico
        
        Args:
            modelo: Nome do modelo
            
        Returns:
            str: Configuração Kubernetes em YAML
        """
        config = self.obter_configuracao(modelo)
        recursos = config["recursos_computacionais"]
        
        yaml = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {modelo}-model
  namespace: ml-platform
spec:
  replicas: {self.configuracoes_producao["autoscaling"]["min_replicas"]}
  selector:
    matchLabels:
      app: {modelo}-model
  template:
    metadata:
      labels:
        app: {modelo}-model
    spec:
      containers:
      - name: model-server
        image: ml-platform/{modelo}-model:latest
        resources:
          requests:
            cpu: "{recursos["cpu"]}"
            memory: "{recursos["memoria"]}"
          limits:
            cpu: "{recursos["cpu"]}"
            memory: "{recursos["memoria"]}"
"""
        
        # Adicionar GPU se necessário
        if "gpu" in recursos:
            yaml += f"""            nvidia.com/gpu: "{recursos["gpu"]}"
          limits:
            nvidia.com/gpu: "{recursos["gpu"]}"
"""
        
        # Adicionar configurações de ambiente
        yaml += """        env:
        - name: MODEL_NAME
          value: "%s"
        - name: BATCH_SIZE
          value: "%d"
        - name: TIMEOUT_SECONDS
          value: "%d"
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
""" % (modelo, self.configuracoes_producao["batch_size"], self.configuracoes_producao["timeout"])
        
        # Adicionar HPA
        yaml += f"""---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {modelo}-model-hpa
  namespace: ml-platform
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {modelo}-model
  minReplicas: {self.configuracoes_producao["autoscaling"]["min_replicas"]}
  maxReplicas: {self.configuracoes_producao["autoscaling"]["max_replicas"]}
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: {self.configuracoes_producao["autoscaling"]["target_cpu_utilization"]}
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: {self.configuracoes_producao["autoscaling"]["target_memory_utilization"]}
"""
        
        return yaml
    
    def exportar_configuracoes(self, caminho: str) -> None:
        """
        Exporta todas as configurações para arquivo JSON
        
        Args:
            caminho: Caminho do arquivo
        """
        with open(caminho, 'w') as f:
            json.dump({
                "modelos": self.configuracoes,
                "producao": self.configuracoes_producao
            }, f, indent=2)


# Exemplo de uso
if __name__ == "__main__":
    config = ConfiguracoesModelos()
    
    # Obter configuração para Random Forest
    rf_config = config.obter_configuracao("random_forest")
    print(f"Configuração Random Forest: {rf_config['parametros']}")
    
    # Obter recursos computacionais para LSTM
    lstm_recursos = config.obter_recursos_computacionais("lstm")
    print(f"Recursos LSTM: {lstm_recursos}")
    
    # Gerar configuração Kubernetes para modelo ensemble
    k8s_config = config.gerar_configuracao_kubernetes("ensemble")
    print("\nConfiguração Kubernetes para Ensemble:")
    print(k8s_config)
    
    # Exportar todas as configurações
    config.exportar_configuracoes("configuracoes_modelos.json")