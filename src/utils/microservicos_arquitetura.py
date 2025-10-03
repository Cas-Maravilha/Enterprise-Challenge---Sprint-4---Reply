import os
import json
from typing import Dict, List, Any, Optional

class ArquiteturaMicroservicos:
    """Define a arquitetura de microserviços para o sistema de IA"""
    
    def __init__(self):
        self.servicos = {
            "data-ingestion": {
                "descricao": "Serviço de ingestão de dados",
                "endpoints": ["/ingest", "/validate"],
                "dependencias": [],
                "recursos": {
                    "cpu": "1",
                    "memoria": "2Gi",
                    "replicas": 2
                }
            },
            "feature-store": {
                "descricao": "Serviço de armazenamento de features",
                "endpoints": ["/features", "/features/{id}"],
                "dependencias": ["data-ingestion"],
                "recursos": {
                    "cpu": "2",
                    "memoria": "4Gi",
                    "replicas": 2
                }
            },
            "model-training": {
                "descricao": "Serviço de treinamento de modelos",
                "endpoints": ["/train", "/hyperparams"],
                "dependencias": ["feature-store"],
                "recursos": {
                    "cpu": "4",
                    "memoria": "8Gi",
                    "replicas": 1
                }
            },
            "model-registry": {
                "descricao": "Serviço de registro de modelos",
                "endpoints": ["/models", "/models/{id}", "/versions/{id}"],
                "dependencias": ["model-training"],
                "recursos": {
                    "cpu": "1",
                    "memoria": "2Gi",
                    "replicas": 2
                }
            },
            "model-serving": {
                "descricao": "Serviço de disponibilização de modelos",
                "endpoints": ["/predict", "/batch-predict", "/health"],
                "dependencias": ["model-registry", "feature-store"],
                "recursos": {
                    "cpu": "2",
                    "memoria": "4Gi",
                    "replicas": 3
                }
            },
            "monitoring": {
                "descricao": "Serviço de monitoramento",
                "endpoints": ["/metrics", "/alerts", "/drift"],
                "dependencias": ["model-serving"],
                "recursos": {
                    "cpu": "2",
                    "memoria": "4Gi",
                    "replicas": 1
                }
            }
        }
    
    def gerar_kubernetes_manifests(self, namespace: str = "ml-platform") -> Dict[str, str]:
        """
        Gera manifestos Kubernetes para os microserviços
        
        Args:
            namespace: Namespace Kubernetes
            
        Returns:
            Dict[str, str]: Dicionário com nome do arquivo e conteúdo YAML
        """
        manifests = {}
        
        # Namespace
        manifests["00-namespace.yaml"] = f"""apiVersion: v1
kind: Namespace
metadata:
  name: {namespace}
"""
        
        # Serviços
        for nome, config in self.servicos.items():
            # Deployment
            deployment = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {nome}
  namespace: {namespace}
spec:
  replicas: {config['recursos']['replicas']}
  selector:
    matchLabels:
      app: {nome}
  template:
    metadata:
      labels:
        app: {nome}
    spec:
      containers:
      - name: {nome}
        image: ml-platform/{nome}:latest
        resources:
          requests:
            memory: "{config['recursos']['memoria']}"
            cpu: "{config['recursos']['cpu']}"
          limits:
            memory: "{config['recursos']['memoria']}"
            cpu: "{config['recursos']['cpu']}"
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
        env:
        - name: SERVICE_NAME
          value: "{nome}"
"""
            
            # Service
            service = f"""apiVersion: v1
kind: Service
metadata:
  name: {nome}
  namespace: {namespace}
spec:
  selector:
    app: {nome}
  ports:
  - port: 80
    targetPort: 8080
  type: ClusterIP
"""
            
            manifests[f"{nome}-deployment.yaml"] = deployment
            manifests[f"{nome}-service.yaml"] = service
        
        # Ingress para API Gateway
        ingress = f"""apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ml-platform-ingress
  namespace: {namespace}
  annotations:
    kubernetes.io/ingress.class: nginx
spec:
  rules:
  - host: ml-api.example.com
    http:
      paths:
      - path: /api/predict
        pathType: Prefix
        backend:
          service:
            name: model-serving
            port:
              number: 80
      - path: /api/models
        pathType: Prefix
        backend:
          service:
            name: model-registry
            port:
              number: 80
      - path: /api/features
        pathType: Prefix
        backend:
          service:
            name: feature-store
            port:
              number: 80
      - path: /api/metrics
        pathType: Prefix
        backend:
          service:
            name: monitoring
            port:
              number: 80
"""
        manifests["ml-platform-ingress.yaml"] = ingress
        
        return manifests
    
    def gerar_diagrama_arquitetura(self) -> Dict[str, Any]:
        """
        Gera representação da arquitetura para visualização
        
        Returns:
            Dict: Representação da arquitetura
        """
        nodes = []
        edges = []
        
        # Adicionar nós
        for nome, config in self.servicos.items():
            nodes.append({
                "id": nome,
                "label": nome,
                "description": config["descricao"],
                "resources": config["recursos"]
            })
            
            # Adicionar arestas para dependências
            for dep in config["dependencias"]:
                edges.append({
                    "from": dep,
                    "to": nome,
                    "label": "depends on"
                })
        
        return {
            "nodes": nodes,
            "edges": edges
        }
    
    def estimar_custos_aws(self, regiao: str = "us-east-1") -> Dict[str, float]:
        """
        Estima custos mensais na AWS
        
        Args:
            regiao: Região AWS
            
        Returns:
            Dict: Estimativa de custos
        """
        # Preços aproximados (USD/hora) para EKS e ECS
        precos = {
            "us-east-1": {
                "eks_cluster": 0.10,  # USD por hora
                "t3.medium": 0.0416,  # 2 vCPU, 4 GiB
                "t3.large": 0.0832,   # 2 vCPU, 8 GiB
                "t3.xlarge": 0.1664,  # 4 vCPU, 16 GiB
                "m5.large": 0.096,    # 2 vCPU, 8 GiB
                "m5.xlarge": 0.192,   # 4 vCPU, 16 GiB
            }
        }
        
        # Mapeamento de recursos para tipos de instância
        mapeamento_instancias = {
            "1-2Gi": "t3.medium",
            "2-4Gi": "t3.large",
            "4-8Gi": "t3.xlarge",
            "2-8Gi": "m5.large",
            "4-16Gi": "m5.xlarge"
        }
        
        # Calcular custo total
        custo_cluster = precos[regiao]["eks_cluster"] * 24 * 30  # 30 dias
        custo_instancias = 0
        
        for nome, config in self.servicos.items():
            cpu = config["recursos"]["cpu"]
            memoria = config["recursos"]["memoria"].replace("Gi", "")
            replicas = config["recursos"]["replicas"]
            
            # Determinar tipo de instância
            chave_mapeamento = f"{cpu}-{memoria}Gi"
            tipo_instancia = mapeamento_instancias.get(chave_mapeamento, "t3.medium")
            
            # Calcular custo
            custo_hora = precos[regiao][tipo_instancia]
            custo_servico = custo_hora * 24 * 30 * replicas
            custo_instancias += custo_servico
        
        return {
            "custo_cluster": round(custo_cluster, 2),
            "custo_instancias": round(custo_instancias, 2),
            "custo_total": round(custo_cluster + custo_instancias, 2),
            "moeda": "USD",
            "periodo": "mensal"
        }
    
    def exportar_configuracao(self, caminho: str) -> None:
        """
        Exporta configuração da arquitetura para arquivo JSON
        
        Args:
            caminho: Caminho do arquivo
        """
        with open(caminho, 'w') as f:
            json.dump({
                "servicos": self.servicos,
                "diagrama": self.gerar_diagrama_arquitetura(),
                "custos_estimados": self.estimar_custos_aws()
            }, f, indent=2)


# Exemplo de uso
if __name__ == "__main__":
    arquitetura = ArquiteturaMicroservicos()
    
    # Gerar manifestos Kubernetes
    manifests = arquitetura.gerar_kubernetes_manifests()
    
    # Criar diretório para manifestos
    os.makedirs("kubernetes", exist_ok=True)
    
    # Salvar manifestos
    for nome, conteudo in manifests.items():
        with open(f"kubernetes/{nome}", 'w') as f:
            f.write(conteudo)
    
    # Exportar configuração
    arquitetura.exportar_configuracao("arquitetura_microservicos.json")
    
    # Estimar custos
    custos = arquitetura.estimar_custos_aws()
    print(f"Custo mensal estimado na AWS: ${custos['custo_total']} USD")