import json
from typing import Dict, List, Any, Optional

class OtimizacaoPerformanceCustos:
    """Implementa estratégias de otimização de performance e custos para o sistema de IA"""
    
    def __init__(self):
        self.estrategias = {
            "computacao": {
                "auto_scaling": {
                    "descricao": "Escalonamento automático de recursos computacionais",
                    "tecnicas": [
                        {
                            "nome": "Horizontal Pod Autoscaler",
                            "aplicacao": "Kubernetes",
                            "metricas": ["cpu_utilization", "memory_utilization", "requests_per_second"],
                            "economia_estimada": 0.25
                        },
                        {
                            "nome": "Spot Instances",
                            "aplicacao": "AWS EC2/EKS",
                            "metricas": ["cost_savings"],
                            "economia_estimada": 0.70
                        },
                        {
                            "nome": "Scheduled Scaling",
                            "aplicacao": "Kubernetes/AWS",
                            "metricas": ["usage_patterns"],
                            "economia_estimada": 0.35
                        }
                    ]
                },
                "otimizacao_recursos": {
                    "descricao": "Otimização de alocação de recursos",
                    "tecnicas": [
                        {
                            "nome": "Resource Right-sizing",
                            "aplicacao": "Kubernetes/AWS",
                            "metricas": ["cpu_usage", "memory_usage"],
                            "economia_estimada": 0.20
                        },
                        {
                            "nome": "Vertical Pod Autoscaler",
                            "aplicacao": "Kubernetes",
                            "metricas": ["resource_utilization"],
                            "economia_estimada": 0.15
                        },
                        {
                            "nome": "GPU Sharing",
                            "aplicacao": "Kubernetes",
                            "metricas": ["gpu_utilization"],
                            "economia_estimada": 0.40
                        }
                    ]
                }
            },
            "armazenamento": {
                "lifecycle_policies": {
                    "descricao": "Políticas de ciclo de vida para dados",
                    "tecnicas": [
                        {
                            "nome": "S3 Lifecycle Rules",
                            "aplicacao": "AWS S3",
                            "metricas": ["storage_cost"],
                            "economia_estimada": 0.30
                        },
                        {
                            "nome": "Data Archiving",
                            "aplicacao": "AWS S3 Glacier",
                            "metricas": ["storage_cost"],
                            "economia_estimada": 0.80
                        }
                    ]
                },
                "compressao": {
                    "descricao": "Compressão de dados",
                    "tecnicas": [
                        {
                            "nome": "Parquet Format",
                            "aplicacao": "Data Storage",
                            "metricas": ["storage_size", "query_performance"],
                            "economia_estimada": 0.40
                        },
                        {
                            "nome": "Model Compression",
                            "aplicacao": "ML Models",
                            "metricas": ["model_size", "inference_time"],
                            "economia_estimada": 0.50
                        }
                    ]
                }
            },
            "inferencia": {
                "otimizacao_modelo": {
                    "descricao": "Otimização de modelos para inferência",
                    "tecnicas": [
                        {
                            "nome": "Quantization",
                            "aplicacao": "ML Models",
                            "metricas": ["model_size", "inference_time"],
                            "economia_estimada": 0.60
                        },
                        {
                            "nome": "Pruning",
                            "aplicacao": "ML Models",
                            "metricas": ["model_size", "inference_time"],
                            "economia_estimada": 0.40
                        },
                        {
                            "nome": "Knowledge Distillation",
                            "aplicacao": "ML Models",
                            "metricas": ["model_size", "inference_time"],
                            "economia_estimada": 0.50
                        }
                    ]
                },
                "batch_inference": {
                    "descricao": "Inferência em lote",
                    "tecnicas": [
                        {
                            "nome": "Batch Processing",
                            "aplicacao": "ML Inference",
                            "metricas": ["throughput", "cost_per_prediction"],
                            "economia_estimada": 0.70
                        },
                        {
                            "nome": "Serverless Inference",
                            "aplicacao": "AWS Lambda",
                            "metricas": ["idle_time", "cost_per_prediction"],
                            "economia_estimada": 0.60
                        }
                    ]
                },
                "caching": {
                    "descricao": "Cache de resultados de inferência",
                    "tecnicas": [
                        {
                            "nome": "Result Caching",
                            "aplicacao": "ML Inference",
                            "metricas": ["cache_hit_ratio", "latency"],
                            "economia_estimada": 0.30
                        },
                        {
                            "nome": "Feature Store Caching",
                            "aplicacao": "Feature Store",
                            "metricas": ["feature_computation_time"],
                            "economia_estimada": 0.25
                        }
                    ]
                }
            },
            "monitoramento": {
                "alertas_proativos": {
                    "descricao": "Alertas proativos para otimização",
                    "tecnicas": [
                        {
                            "nome": "Cost Anomaly Detection",
                            "aplicacao": "AWS Cost Explorer",
                            "metricas": ["cost_trend"],
                            "economia_estimada": 0.15
                        },
                        {
                            "nome": "Performance Degradation Alerts",
                            "aplicacao": "Prometheus/Grafana",
                            "metricas": ["latency_increase", "error_rate"],
                            "economia_estimada": 0.10
                        }
                    ]
                },
                "dashboards": {
                    "descricao": "Dashboards de monitoramento",
                    "tecnicas": [
                        {
                            "nome": "Cost vs Performance Dashboard",
                            "aplicacao": "Grafana",
                            "metricas": ["cost_per_request", "latency"],
                            "economia_estimada": 0.05
                        },
                        {
                            "nome": "Resource Utilization Dashboard",
                            "aplicacao": "Grafana",
                            "metricas": ["cpu_usage", "memory_usage", "gpu_usage"],
                            "economia_estimada": 0.10
                        }
                    ]
                }
            }
        }
    
    def gerar_configuracao_kubernetes(self) -> Dict[str, str]:
        """
        Gera configurações Kubernetes para otimização
        
        Returns:
            Dict[str, str]: Dicionário com nome do arquivo e conteúdo YAML
        """
        configs = {}
        
        # Horizontal Pod Autoscaler
        hpa_yaml = """apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: model-serving-hpa
  namespace: ml-platform
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: model-serving
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  - type: Pods
    pods:
      metric:
        name: requests-per-second
      target:
        type: AverageValue
        averageValue: 1000
"""
        configs["model-serving-hpa.yaml"] = hpa_yaml
        
        # Vertical Pod Autoscaler
        vpa_yaml = """apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: model-serving-vpa
  namespace: ml-platform
spec:
  targetRef:
    apiVersion: "apps/v1"
    kind: Deployment
    name: model-serving
  updatePolicy:
    updateMode: "Auto"
  resourcePolicy:
    containerPolicies:
    - containerName: '*'
      minAllowed:
        cpu: 100m
        memory: 200Mi
      maxAllowed:
        cpu: 4
        memory: 8Gi
      controlledResources: ["cpu", "memory"]
"""
        configs["model-serving-vpa.yaml"] = vpa_yaml
        
        # Pod Disruption Budget para garantir disponibilidade durante escalonamento
        pdb_yaml = """apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: model-serving-pdb
  namespace: ml-platform
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: model-serving
"""
        configs["model-serving-pdb.yaml"] = pdb_yaml
        
        # Configuração de recursos para GPU sharing
        gpu_sharing_yaml = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: model-serving-gpu
  namespace: ml-platform
spec:
  replicas: 1
  selector:
    matchLabels:
      app: model-serving-gpu
  template:
    metadata:
      labels:
        app: model-serving-gpu
    spec:
      containers:
      - name: model-serving
        image: ml-platform/model-serving:latest
        resources:
          limits:
            nvidia.com/gpu: 1
          requests:
            nvidia.com/gpu: 0.5
        env:
        - name: NVIDIA_VISIBLE_DEVICES
          value: "all"
        - name: NVIDIA_DRIVER_CAPABILITIES
          value: "compute,utility"
        - name: NVIDIA_REQUIRE_CUDA
          value: "cuda>=11.0"
"""
        configs["model-serving-gpu.yaml"] = gpu_sharing_yaml
        
        return configs
    
    def gerar_configuracao_aws(self) -> Dict[str, str]:
        """
        Gera configurações AWS para otimização
        
        Returns:
            Dict[str, str]: Dicionário com nome do arquivo e conteúdo
        """
        configs = {}
        
        # Política de ciclo de vida do S3
        s3_lifecycle_json = """{
  "Rules": [
    {
      "ID": "MoveToGlacierAfter90Days",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "raw-data/"
      },
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        }
      ],
      "Expiration": {
        "Days": 365
      }
    },
    {
      "ID": "DeleteTempData",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "temp/"
      },
      "Expiration": {
        "Days": 7
      }
    }
  ]
}"""
        configs["s3-lifecycle-policy.json"] = s3_lifecycle_json
        
        # Configuração de Spot Instances para EKS
        spot_instances_json = """{
  "apiVersion": "eksctl.io/v1alpha5",
  "kind": "ClusterConfig",
  "metadata": {
    "name": "ml-platform-cluster",
    "region": "us-east-1"
  },
  "nodeGroups": [
    {
      "name": "spot-ng",
      "instanceType": "mixed",
      "minSize": 1,
      "maxSize": 5,
      "desiredCapacity": 2,
      "spot": true,
      "instancesDistribution": {
        "maxPrice": 0.15,
        "instanceTypes": ["t3.large", "t3.xlarge", "m5.large", "m5.xlarge"],
        "onDemandBaseCapacity": 0,
        "onDemandPercentageAboveBaseCapacity": 0,
        "spotInstancePools": 4
      },
      "labels": {
        "instance-type": "spot"
      },
      "taints": {
        "spot": "true:PreferNoSchedule"
      }
    }
  ]
}"""
        configs["eks-spot-instances.json"] = spot_instances_json
        
        # Configuração de AWS Lambda para inferência serverless
        lambda_config = """{
  "FunctionName": "model-inference",
  "Runtime": "python3.9",
  "Handler": "inference.handler",
  "MemorySize": 1024,
  "Timeout": 30,
  "Environment": {
    "Variables": {
      "MODEL_BUCKET": "ml-models",
      "MODEL_KEY": "latest/model.tar.gz",
      "BATCH_SIZE": "32"
    }
  },
  "EphemeralStorage": {
    "Size": 512
  },
  "ProvisionedConcurrencyConfig": {
    "ProvisionedConcurrentExecutions": 2
  }
}"""
        configs["lambda-inference-config.json"] = lambda_config
        
        return configs
    
    def calcular_economia_estimada(self) -> Dict[str, float]:
        """
        Calcula economia estimada por categoria
        
        Returns:
            Dict[str, float]: Economia estimada por categoria
        """
        economia = {}
        
        # Para cada categoria
        for categoria, estrategias in self.estrategias.items():
            economia_categoria = 0
            count = 0
            
            # Para cada estratégia na categoria
            for estrategia, config in estrategias.items():
                # Para cada técnica na estratégia
                for tecnica in config["tecnicas"]:
                    economia_categoria += tecnica["economia_estimada"]
                    count += 1
            
            # Calcular média
            if count > 0:
                economia[categoria] = economia_categoria / count
        
        # Economia total (média das categorias)
        total = sum(economia.values()) / len(economia) if economia else 0
        
        return {
            **economia,
            "total": total
        }
    
    def gerar_recomendacoes_otimizacao(self) -> List[Dict[str, Any]]:
        """
        Gera lista de recomendações de otimização
        
        Returns:
            List[Dict[str, Any]]: Lista de recomendações
        """
        recomendacoes = []
        
        # Para cada categoria
        for categoria, estrategias in self.estrategias.items():
            # Para cada estratégia na categoria
            for estrategia, config in estrategias.items():
                # Para cada técnica na estratégia
                for tecnica in config["tecnicas"]:
                    recomendacoes.append({
                        "categoria": categoria,
                        "estrategia": estrategia,
                        "tecnica": tecnica["nome"],
                        "aplicacao": tecnica["aplicacao"],
                        "economia_estimada": tecnica["economia_estimada"],
                        "metricas_monitoramento": tecnica["metricas"],
                        "prioridade": "Alta" if tecnica["economia_estimada"] > 0.5 else 
                                    "Média" if tecnica["economia_estimada"] > 0.3 else "Baixa"
                    })
        
        # Ordenar por economia estimada (decrescente)
        recomendacoes.sort(key=lambda x: x["economia_estimada"], reverse=True)
        
        return recomendacoes
    
    def exportar_configuracao(self, caminho: str) -> None:
        """
        Exporta configuração de otimização para arquivo JSON
        
        Args:
            caminho: Caminho do arquivo
        """
        with open(caminho, 'w') as f:
            json.dump({
                "estrategias": self.estrategias,
                "economia_estimada": self.calcular_economia_estimada(),
                "recomendacoes": self.gerar_recomendacoes_otimizacao()
            }, f, indent=2)


# Exemplo de uso
if __name__ == "__main__":
    otimizacao = OtimizacaoPerformanceCustos()
    
    # Gerar configurações Kubernetes
    k8s_configs = otimizacao.gerar_configuracao_kubernetes()
    
    # Criar diretório para configurações Kubernetes
    import os
    os.makedirs("kubernetes/otimizacao", exist_ok=True)
    
    # Salvar configurações Kubernetes
    for nome, conteudo in k8s_configs.items():
        with open(f"kubernetes/otimizacao/{nome}", 'w') as f:
            f.write(conteudo)
    
    # Gerar configurações AWS
    aws_configs = otimizacao.gerar_configuracao_aws()
    
    # Criar diretório para configurações AWS
    os.makedirs("aws/otimizacao", exist_ok=True)
    
    # Salvar configurações AWS
    for nome, conteudo in aws_configs.items():
        with open(f"aws/otimizacao/{nome}", 'w') as f:
            f.write(conteudo)
    
    # Exportar configuração
    otimizacao.exportar_configuracao("otimizacao_performance_custos.json")
    
    # Calcular economia estimada
    economia = otimizacao.calcular_economia_estimada()
    print(f"Economia total estimada: {economia['total']:.2%}")
    for categoria, valor in {k: v for k, v in economia.items() if k != 'total'}.items():
        print(f"  {categoria}: {valor:.2%}")
    
    # Gerar recomendações
    recomendacoes = otimizacao.gerar_recomendacoes_otimizacao()
    print(f"\nTop 5 recomendações de otimização:")
    for i, rec in enumerate(recomendacoes[:5]):
        print(f"  {i+1}. {rec['tecnica']} ({rec['aplicacao']}) - Economia: {rec['economia_estimada']:.2%} - Prioridade: {rec['prioridade']}")