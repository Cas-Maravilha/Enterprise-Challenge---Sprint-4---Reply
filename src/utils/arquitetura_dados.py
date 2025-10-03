import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

class ArquiteturaDados:
    """Define a arquitetura de dados hot/warm/cold para o sistema de IA"""
    
    def __init__(self):
        self.camadas = {
            "hot": {
                "descricao": "Dados de acesso frequente e alta performance",
                "tecnologias": ["Redis", "Amazon ElastiCache", "PostgreSQL"],
                "tempo_retencao": "7 dias",
                "latencia_alvo": "<10ms",
                "casos_uso": ["Feature store online", "Cache de predições", "Dados em processamento"],
                "custo_relativo": "Alto",
                "configuracao": {
                    "redis": {
                        "instance_type": "cache.m5.large",
                        "num_shards": 2,
                        "replicas_per_shard": 1
                    },
                    "postgres": {
                        "instance_type": "db.m5.large",
                        "storage": "100GB",
                        "read_replicas": 1
                    }
                }
            },
            "warm": {
                "descricao": "Dados de acesso moderado e performance balanceada",
                "tecnologias": ["Amazon S3", "Amazon DynamoDB", "MongoDB"],
                "tempo_retencao": "90 dias",
                "latencia_alvo": "<100ms",
                "casos_uso": ["Feature store offline", "Resultados de treinamento", "Dados processados"],
                "custo_relativo": "Médio",
                "configuracao": {
                    "s3": {
                        "storage_class": "STANDARD",
                        "lifecycle_rules": [
                            {
                                "prefix": "processed/",
                                "transition_days": 30,
                                "transition_to": "STANDARD_IA"
                            }
                        ]
                    },
                    "dynamodb": {
                        "read_capacity_units": "auto",
                        "write_capacity_units": "auto",
                        "point_in_time_recovery": True
                    }
                }
            },
            "cold": {
                "descricao": "Dados de acesso infrequente e baixo custo",
                "tecnologias": ["Amazon S3 Glacier", "Amazon S3 Deep Archive"],
                "tempo_retencao": "7 anos",
                "latencia_alvo": "<12h",
                "casos_uso": ["Dados históricos", "Backups", "Auditoria"],
                "custo_relativo": "Baixo",
                "configuracao": {
                    "s3_glacier": {
                        "storage_class": "GLACIER",
                        "retrieval_tier": "Standard",
                        "lifecycle_rules": [
                            {
                                "prefix": "historical/",
                                "transition_days": 365,
                                "transition_to": "DEEP_ARCHIVE"
                            }
                        ]
                    }
                }
            }
        }
        
        self.fluxos_dados = {
            "ingestao_para_hot": {
                "origem": "Fontes externas",
                "destino": "hot",
                "frequencia": "Tempo real / Near real-time",
                "volume": "Médio",
                "tecnologia": "Kafka / Kinesis"
            },
            "hot_para_warm": {
                "origem": "hot",
                "destino": "warm",
                "frequencia": "Diária",
                "volume": "Alto",
                "tecnologia": "Spark / Airflow"
            },
            "warm_para_cold": {
                "origem": "warm",
                "destino": "cold",
                "frequencia": "Mensal",
                "volume": "Muito alto",
                "tecnologia": "Airflow / AWS Data Pipeline"
            },
            "warm_para_treinamento": {
                "origem": "warm",
                "destino": "Ambiente de treinamento",
                "frequencia": "Sob demanda / Semanal",
                "volume": "Alto",
                "tecnologia": "Spark / S3"
            }
        }
        
        self.tipos_dados = {
            "raw": {
                "descricao": "Dados brutos sem processamento",
                "formato": ["CSV", "JSON", "Parquet"],
                "camada_inicial": "warm",
                "processamento_requerido": "Alto"
            },
            "processed": {
                "descricao": "Dados limpos e transformados",
                "formato": ["Parquet", "ORC"],
                "camada_inicial": "warm",
                "processamento_requerido": "Médio"
            },
            "features": {
                "descricao": "Features para modelos de ML",
                "formato": ["Parquet", "Redis Hash"],
                "camada_inicial": "hot/warm",
                "processamento_requerido": "Baixo"
            },
            "predictions": {
                "descricao": "Resultados de predições",
                "formato": ["JSON", "Parquet"],
                "camada_inicial": "hot",
                "processamento_requerido": "Nenhum"
            },
            "models": {
                "descricao": "Modelos treinados",
                "formato": ["Pickle", "SavedModel", "ONNX"],
                "camada_inicial": "warm",
                "processamento_requerido": "Nenhum"
            },
            "metrics": {
                "descricao": "Métricas de modelos e sistema",
                "formato": ["JSON", "Prometheus"],
                "camada_inicial": "hot/warm",
                "processamento_requerido": "Baixo"
            }
        }
    
    def gerar_politicas_lifecycle(self) -> Dict[str, Any]:
        """
        Gera políticas de ciclo de vida para dados
        
        Returns:
            Dict: Políticas de ciclo de vida
        """
        politicas = {}
        
        # Política para dados brutos
        politicas["raw_data"] = {
            "hot_retention": "1 dia",
            "warm_retention": "30 dias",
            "cold_retention": "5 anos",
            "regras": [
                {
                    "descricao": "Mover dados brutos de hot para warm",
                    "condicao": "Após 1 dia",
                    "acao": "Mover para warm"
                },
                {
                    "descricao": "Mover dados brutos de warm para cold",
                    "condicao": "Após 30 dias",
                    "acao": "Mover para cold"
                },
                {
                    "descricao": "Arquivar dados brutos",
                    "condicao": "Após 5 anos",
                    "acao": "Excluir ou arquivar permanentemente"
                }
            ]
        }
        
        # Política para dados processados
        politicas["processed_data"] = {
            "hot_retention": "7 dias",
            "warm_retention": "90 dias",
            "cold_retention": "3 anos",
            "regras": [
                {
                    "descricao": "Mover dados processados de hot para warm",
                    "condicao": "Após 7 dias",
                    "acao": "Mover para warm"
                },
                {
                    "descricao": "Mover dados processados de warm para cold",
                    "condicao": "Após 90 dias",
                    "acao": "Mover para cold"
                },
                {
                    "descricao": "Arquivar dados processados",
                    "condicao": "Após 3 anos",
                    "acao": "Excluir ou arquivar permanentemente"
                }
            ]
        }
        
        # Política para features
        politicas["features"] = {
            "hot_retention": "7 dias",
            "warm_retention": "90 dias",
            "cold_retention": "1 ano",
            "regras": [
                {
                    "descricao": "Mover features de hot para warm",
                    "condicao": "Após 7 dias",
                    "acao": "Mover para warm"
                },
                {
                    "descricao": "Mover features de warm para cold",
                    "condicao": "Após 90 dias",
                    "acao": "Mover para cold"
                },
                {
                    "descricao": "Arquivar features",
                    "condicao": "Após 1 ano",
                    "acao": "Excluir ou arquivar permanentemente"
                }
            ]
        }
        
        # Política para predições
        politicas["predictions"] = {
            "hot_retention": "1 dia",
            "warm_retention": "30 dias",
            "cold_retention": "1 ano",
            "regras": [
                {
                    "descricao": "Mover predições de hot para warm",
                    "condicao": "Após 1 dia",
                    "acao": "Mover para warm"
                },
                {
                    "descricao": "Mover predições de warm para cold",
                    "condicao": "Após 30 dias",
                    "acao": "Mover para cold"
                },
                {
                    "descricao": "Arquivar predições",
                    "condicao": "Após 1 ano",
                    "acao": "Excluir ou arquivar permanentemente"
                }
            ]
        }
        
        # Política para modelos
        politicas["models"] = {
            "hot_retention": "Atual + 1 versão anterior",
            "warm_retention": "Últimas 5 versões",
            "cold_retention": "Todas as versões",
            "regras": [
                {
                    "descricao": "Manter apenas modelos atuais em hot",
                    "condicao": "Quando nova versão é implantada",
                    "acao": "Mover versão anterior para warm"
                },
                {
                    "descricao": "Manter histórico limitado em warm",
                    "condicao": "Quando há mais de 5 versões em warm",
                    "acao": "Mover versão mais antiga para cold"
                },
                {
                    "descricao": "Preservar histórico completo em cold",
                    "condicao": "Indefinidamente",
                    "acao": "Manter em cold"
                }
            ]
        }
        
        return politicas
    
    def gerar_configuracao_aws(self) -> Dict[str, str]:
        """
        Gera configurações AWS para arquitetura de dados
        
        Returns:
            Dict[str, str]: Dicionário com nome do arquivo e conteúdo
        """
        configs = {}
        
        # Configuração S3 Lifecycle
        s3_lifecycle_json = """{
  "Rules": [
    {
      "ID": "RawDataLifecycle",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "raw/"
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
        "Days": 1825
      }
    },
    {
      "ID": "ProcessedDataLifecycle",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "processed/"
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
        "Days": 1095
      }
    },
    {
      "ID": "FeaturesLifecycle",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "features/"
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
      "ID": "PredictionsLifecycle",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "predictions/"
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
    }
  ]
}"""
        configs["s3-lifecycle-policy.json"] = s3_lifecycle_json
        
        # Configuração ElastiCache (Redis)
        elasticache_json = """{
  "CacheClusterId": "ml-feature-store",
  "CacheNodeType": "cache.m5.large",
  "Engine": "redis",
  "NumCacheNodes": 1,
  "AutoMinorVersionUpgrade": true,
  "CacheSubnetGroupName": "ml-platform-subnet-group",
  "SecurityGroupIds": ["sg-12345678"],
  "Tags": [
    {
      "Key": "Project",
      "Value": "ML Platform"
    },
    {
      "Key": "Environment",
      "Value": "Production"
    }
  ]
}"""
        configs["elasticache-config.json"] = elasticache_json
        
        # Configuração DynamoDB
        dynamodb_json = """{
  "TableName": "ml-feature-store",
  "BillingMode": "PAY_PER_REQUEST",
  "AttributeDefinitions": [
    {
      "AttributeName": "feature_id",
      "AttributeType": "S"
    },
    {
      "AttributeName": "timestamp",
      "AttributeType": "S"
    }
  ],
  "KeySchema": [
    {
      "AttributeName": "feature_id",
      "KeyType": "HASH"
    },
    {
      "AttributeName": "timestamp",
      "KeyType": "RANGE"
    }
  ],
  "PointInTimeRecoverySpecification": {
    "PointInTimeRecoveryEnabled": true
  },
  "SSESpecification": {
    "Enabled": true,
    "SSEType": "KMS"
  },
  "Tags": [
    {
      "Key": "Project",
      "Value": "ML Platform"
    },
    {
      "Key": "Environment",
      "Value": "Production"
    }
  ]
}"""
        configs["dynamodb-config.json"] = dynamodb_json
        
        return configs
    
    def calcular_custos_estimados(self) -> Dict[str, float]:
        """
        Calcula custos estimados para cada camada
        
        Returns:
            Dict[str, float]: Custos estimados
        """
        # Estimativas de custo mensal em USD
        custos = {
            "hot": {
                "elasticache": 200.00,  # Redis m5.large
                "rds": 250.00,          # RDS m5.large
                "total": 450.00
            },
            "warm": {
                "s3_standard": 50.00,   # 1TB de dados
                "dynamodb": 100.00,     # Capacidade sob demanda
                "total": 150.00
            },
            "cold": {
                "s3_glacier": 10.00,    # 5TB de dados
                "s3_deep_archive": 5.00,# 5TB de dados
                "total": 15.00
            }
        }
        
        # Total geral
        total = sum(layer["total"] for layer in custos.values())
        
        return {
            **custos,
            "total_mensal": total
        }
    
    def exportar_configuracao(self, caminho: str) -> None:
        """
        Exporta configuração da arquitetura de dados para arquivo JSON
        
        Args:
            caminho: Caminho do arquivo
        """
        with open(caminho, 'w') as f:
            json.dump({
                "camadas": self.camadas,
                "fluxos_dados": self.fluxos_dados,
                "tipos_dados": self.tipos_dados,
                "politicas_lifecycle": self.gerar_politicas_lifecycle(),
                "custos_estimados": self.calcular_custos_estimados()
            }, f, indent=2)


# Exemplo de uso
if __name__ == "__main__":
    arquitetura = ArquiteturaDados()
    
    # Gerar políticas de ciclo de vida
    politicas = arquitetura.gerar_politicas_lifecycle()
    print(f"Políticas de ciclo de vida geradas para {len(politicas)} tipos de dados")
    
    # Gerar configurações AWS
    configs = arquitetura.gerar_configuracao_aws()
    
    # Criar diretório para configurações
    import os
    os.makedirs("aws/data-architecture", exist_ok=True)
    
    # Salvar configurações
    for nome, conteudo in configs.items():
        with open(f"aws/data-architecture/{nome}", 'w') as f:
            f.write(conteudo)
    
    # Calcular custos estimados
    custos = arquitetura.calcular_custos_estimados()
    print(f"Custo mensal estimado: ${custos['total_mensal']:.2f} USD")
    for camada, info in {k: v for k, v in custos.items() if k != 'total_mensal'}.items():
        print(f"  {camada}: ${info['total']:.2f} USD")
    
    # Exportar configuração
    arquitetura.exportar_configuracao("arquitetura_dados.json")