import yaml
import json
from typing import Dict, List, Any, Optional

class PipelineCICDML:
    """Define o pipeline CI/CD específico para ML"""
    
    def __init__(self):
        self.etapas = {
            "code": {
                "descricao": "Validação de código",
                "acoes": [
                    {
                        "nome": "lint",
                        "ferramenta": "flake8",
                        "comando": "flake8 src/ tests/",
                        "criterio_sucesso": "Sem erros de lint"
                    },
                    {
                        "nome": "format",
                        "ferramenta": "black",
                        "comando": "black --check src/ tests/",
                        "criterio_sucesso": "Código formatado corretamente"
                    },
                    {
                        "nome": "type-check",
                        "ferramenta": "mypy",
                        "comando": "mypy src/",
                        "criterio_sucesso": "Sem erros de tipo"
                    },
                    {
                        "nome": "unit-test",
                        "ferramenta": "pytest",
                        "comando": "pytest tests/unit/",
                        "criterio_sucesso": "Todos os testes unitários passam"
                    }
                ]
            },
            "data": {
                "descricao": "Validação de dados",
                "acoes": [
                    {
                        "nome": "data-validation",
                        "ferramenta": "great-expectations",
                        "comando": "great_expectations checkpoint run data_validation",
                        "criterio_sucesso": "Dados atendem às expectativas"
                    },
                    {
                        "nome": "data-drift-check",
                        "ferramenta": "evidently",
                        "comando": "python src/validation/check_drift.py",
                        "criterio_sucesso": "Sem drift significativo detectado"
                    }
                ]
            },
            "model": {
                "descricao": "Treinamento e validação de modelo",
                "acoes": [
                    {
                        "nome": "train-model",
                        "ferramenta": "custom-script",
                        "comando": "python src/training/train.py --config=configs/train_config.json",
                        "criterio_sucesso": "Modelo treinado com sucesso"
                    },
                    {
                        "nome": "evaluate-model",
                        "ferramenta": "custom-script",
                        "comando": "python src/evaluation/evaluate.py --model-path=models/latest/",
                        "criterio_sucesso": "Métricas atendem aos thresholds"
                    },
                    {
                        "nome": "model-tests",
                        "ferramenta": "pytest",
                        "comando": "pytest tests/model/",
                        "criterio_sucesso": "Todos os testes de modelo passam"
                    }
                ]
            },
            "package": {
                "descricao": "Empacotamento do modelo",
                "acoes": [
                    {
                        "nome": "build-docker",
                        "ferramenta": "docker",
                        "comando": "docker build -t ml-model:latest -f Dockerfile .",
                        "criterio_sucesso": "Imagem Docker construída com sucesso"
                    },
                    {
                        "nome": "scan-vulnerabilities",
                        "ferramenta": "trivy",
                        "comando": "trivy image ml-model:latest",
                        "criterio_sucesso": "Sem vulnerabilidades críticas"
                    }
                ]
            },
            "deploy": {
                "descricao": "Implantação do modelo",
                "acoes": [
                    {
                        "nome": "deploy-staging",
                        "ferramenta": "kubectl",
                        "comando": "kubectl apply -f kubernetes/staging/",
                        "criterio_sucesso": "Implantação em staging concluída"
                    },
                    {
                        "nome": "integration-tests",
                        "ferramenta": "pytest",
                        "comando": "pytest tests/integration/ --url=https://staging-api.example.com",
                        "criterio_sucesso": "Todos os testes de integração passam"
                    },
                    {
                        "nome": "deploy-production",
                        "ferramenta": "kubectl",
                        "comando": "kubectl apply -f kubernetes/production/",
                        "criterio_sucesso": "Implantação em produção concluída"
                    },
                    {
                        "nome": "smoke-tests",
                        "ferramenta": "pytest",
                        "comando": "pytest tests/smoke/ --url=https://api.example.com",
                        "criterio_sucesso": "Todos os testes de fumaça passam"
                    }
                ]
            },
            "monitor": {
                "descricao": "Monitoramento do modelo",
                "acoes": [
                    {
                        "nome": "setup-monitoring",
                        "ferramenta": "prometheus",
                        "comando": "kubectl apply -f kubernetes/monitoring/",
                        "criterio_sucesso": "Monitoramento configurado"
                    },
                    {
                        "nome": "setup-alerts",
                        "ferramenta": "alertmanager",
                        "comando": "kubectl apply -f kubernetes/alerts/",
                        "criterio_sucesso": "Alertas configurados"
                    }
                ]
            }
        }
        
        self.ambientes = {
            "dev": {
                "descricao": "Ambiente de desenvolvimento",
                "url": "https://dev-api.example.com",
                "kubernetes_namespace": "ml-platform-dev",
                "recursos": {
                    "cpu": "2",
                    "memoria": "4Gi",
                    "replicas": 1
                },
                "variaveis_ambiente": {
                    "LOG_LEVEL": "DEBUG",
                    "FEATURE_FLAGS": "all=true"
                }
            },
            "staging": {
                "descricao": "Ambiente de homologação",
                "url": "https://staging-api.example.com",
                "kubernetes_namespace": "ml-platform-staging",
                "recursos": {
                    "cpu": "2",
                    "memoria": "4Gi",
                    "replicas": 2
                },
                "variaveis_ambiente": {
                    "LOG_LEVEL": "INFO",
                    "FEATURE_FLAGS": "experimental=true"
                }
            },
            "production": {
                "descricao": "Ambiente de produção",
                "url": "https://api.example.com",
                "kubernetes_namespace": "ml-platform-prod",
                "recursos": {
                    "cpu": "4",
                    "memoria": "8Gi",
                    "replicas": 3
                },
                "variaveis_ambiente": {
                    "LOG_LEVEL": "WARNING",
                    "FEATURE_FLAGS": "experimental=false"
                }
            }
        }
        
        self.gatilhos = {
            "push": {
                "descricao": "Acionado em push para branches",
                "branches": ["main", "develop", "feature/*"],
                "etapas": ["code"]
            },
            "pull_request": {
                "descricao": "Acionado em pull requests",
                "branches": ["main", "develop"],
                "etapas": ["code", "data"]
            },
            "merge": {
                "descricao": "Acionado em merge para develop",
                "branches": ["develop"],
                "etapas": ["code", "data", "model", "package", "deploy:staging"]
            },
            "release": {
                "descricao": "Acionado em criação de tag de release",
                "branches": ["main"],
                "etapas": ["code", "data", "model", "package", "deploy:production"]
            },
            "schedule": {
                "descricao": "Acionado por agendamento",
                "cron": "0 0 * * 0",  # Domingo à meia-noite
                "etapas": ["data", "model"]
            }
        }
    
    def gerar_github_workflows(self) -> Dict[str, str]:
        """
        Gera arquivos de workflow do GitHub Actions para CI/CD de ML
        
        Returns:
            Dict[str, str]: Dicionário com nome do arquivo e conteúdo YAML
        """
        workflows = {}
        
        # Workflow de validação de código
        code_validation_yaml = """name: Code Validation

on:
  push:
    branches: [main, develop, 'feature/*']
  pull_request:
    branches: [main, develop]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install flake8 black mypy
          if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
      - name: Lint with flake8
        run: flake8 src/ tests/
      - name: Check formatting with black
        run: black --check src/ tests/
      - name: Type check with mypy
        run: mypy src/

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest pytest-cov
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi
      - name: Test with pytest
        run: pytest tests/unit/ --cov=src/ --cov-report=xml
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v1
"""
        workflows["code-validation.yml"] = code_validation_yaml
        
        # Workflow de validação de dados
        data_validation_yaml = """name: Data Validation

on:
  pull_request:
    branches: [main, develop]
  schedule:
    - cron: '0 0 * * 0'  # Domingo à meia-noite

jobs:
  validate-data:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install great-expectations evidently
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      - name: Download test data
        run: |
          mkdir -p data/
          aws s3 cp s3://ml-platform-data/test-data/ data/ --recursive
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      - name: Validate data with Great Expectations
        run: great_expectations checkpoint run data_validation
      - name: Check for data drift
        run: python src/validation/check_drift.py
"""
        workflows["data-validation.yml"] = data_validation_yaml
        
        # Workflow de treinamento e avaliação de modelo
        model_training_yaml = """name: Model Training and Evaluation

on:
  push:
    branches: [develop]
  schedule:
    - cron: '0 0 * * 0'  # Domingo à meia-noite
  workflow_dispatch:
    inputs:
      config_file:
        description: 'Configuration file for training'
        required: false
        default: 'configs/train_config.json'

jobs:
  train-model:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      - name: Download training data
        run: |
          mkdir -p data/
          aws s3 cp s3://ml-platform-data/training-data/ data/ --recursive
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      - name: Train model
        run: python src/training/train.py --config=${{ github.event.inputs.config_file || 'configs/train_config.json' }}
      - name: Evaluate model
        run: python src/evaluation/evaluate.py --model-path=models/latest/
      - name: Run model tests
        run: pytest tests/model/
      - name: Upload model artifacts
        uses: actions/upload-artifact@v2
        with:
          name: model-artifacts
          path: models/latest/

  register-model:
    needs: train-model
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install mlflow boto3
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      - name: Download model artifacts
        uses: actions/download-artifact@v2
        with:
          name: model-artifacts
          path: models/latest/
      - name: Register model in MLflow
        run: python src/deployment/register_model.py --model-path=models/latest/
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
"""
        workflows["model-training.yml"] = model_training_yaml
        
        # Workflow de implantação
        deployment_yaml = """name: Model Deployment

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        default: 'staging'
        options:
          - staging
          - production
      model_version:
        description: 'Model version to deploy'
        required: false
        default: 'latest'

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1
      
      - name: Login to DockerHub
        uses: docker/login-action@v1
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      
      - name: Download model from MLflow
        run: python src/deployment/download_model.py --version=${{ github.event.inputs.model_version || 'latest' }} --output-dir=models/deploy/
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      
      - name: Build and push
        uses: docker/build-push-action@v2
        with:
          context: .
          push: true
          tags: |
            myorg/ml-model:${{ github.event.inputs.model_version || 'latest' }}
            myorg/ml-model:${{ github.sha }}

  deploy-staging:
    needs: build-and-push
    if: ${{ github.event.inputs.environment == 'staging' || github.ref == 'refs/heads/develop' }}
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up kubectl
        uses: azure/setup-kubectl@v1
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Update kubeconfig
        run: aws eks update-kubeconfig --name ml-platform-cluster --region us-east-1
      
      - name: Update deployment image
        run: |
          sed -i 's|image: myorg/ml-model:.*|image: myorg/ml-model:${{ github.sha }}|' kubernetes/staging/deployment.yaml
      
      - name: Deploy to staging
        run: kubectl apply -f kubernetes/staging/
      
      - name: Wait for deployment
        run: kubectl rollout status deployment/ml-model -n ml-platform-staging --timeout=300s
      
      - name: Run integration tests
        run: |
          pip install pytest requests
          pytest tests/integration/ --url=https://staging-api.example.com

  deploy-production:
    needs: build-and-push
    if: ${{ github.event.inputs.environment == 'production' || github.ref == 'refs/heads/main' }}
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up kubectl
        uses: azure/setup-kubectl@v1
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Update kubeconfig
        run: aws eks update-kubeconfig --name ml-platform-cluster --region us-east-1
      
      - name: Update deployment image
        run: |
          sed -i 's|image: myorg/ml-model:.*|image: myorg/ml-model:${{ github.sha }}|' kubernetes/production/deployment.yaml
      
      - name: Deploy to production
        run: kubectl apply -f kubernetes/production/
      
      - name: Wait for deployment
        run: kubectl rollout status deployment/ml-model -n ml-platform-prod --timeout=300s
      
      - name: Run smoke tests
        run: |
          pip install pytest requests
          pytest tests/smoke/ --url=https://api.example.com
"""
        workflows["model-deployment.yml"] = deployment_yaml
        
        # Workflow de monitoramento
        monitoring_yaml = """name: Model Monitoring

on:
  schedule:
    - cron: '0 */6 * * *'  # A cada 6 horas
  workflow_dispatch:

jobs:
  check-model-performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pandas numpy scikit-learn evidently
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      - name: Download production data
        run: |
          mkdir -p data/monitoring/
          aws s3 cp s3://ml-platform-data/monitoring/ data/monitoring/ --recursive
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
      - name: Check model performance
        run: python src/monitoring/check_performance.py
      - name: Check data drift
        run: python src/monitoring/check_drift.py
      - name: Generate monitoring report
        run: python src/monitoring/generate_report.py
      - name: Upload monitoring report
        run: aws s3 cp reports/monitoring/ s3://ml-platform-data/reports/monitoring/ --recursive
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
"""
        workflows["model-monitoring.yml"] = monitoring_yaml
        
        return workflows
    
    def gerar_estrutura_repositorio(self) -> Dict[str, str]:
        """
        Gera estrutura de diretórios e arquivos para o repositório
        
        Returns:
            Dict[str, str]: Dicionário com caminho do arquivo e descrição
        """
        estrutura = {
            ".github/workflows/": "Workflows do GitHub Actions para CI/CD",
            "src/": "Código-fonte do projeto",
            "src/data/": "Scripts para processamento de dados",
            "src/features/": "Scripts para engenharia de features",
            "src/training/": "Scripts para treinamento de modelos",
            "src/evaluation/": "Scripts para avaliação de modelos",
            "src/deployment/": "Scripts para implantação de modelos",
            "src/monitoring/": "Scripts para monitoramento de modelos",
            "src/utils/": "Utilitários e funções auxiliares",
            "tests/": "Testes automatizados",
            "tests/unit/": "Testes unitários",
            "tests/integration/": "Testes de integração",
            "tests/model/": "Testes específicos para modelos",
            "tests/smoke/": "Testes de fumaça para verificação rápida",
            "configs/": "Arquivos de configuração",
            "notebooks/": "Jupyter notebooks para exploração e análise",
            "data/": "Dados (ou links para dados externos)",
            "data/raw/": "Dados brutos",
            "data/processed/": "Dados processados",
            "data/features/": "Features extraídas",
            "models/": "Modelos treinados",
            "kubernetes/": "Manifestos Kubernetes para implantação",
            "kubernetes/dev/": "Configurações para ambiente de desenvolvimento",
            "kubernetes/staging/": "Configurações para ambiente de homologação",
            "kubernetes/production/": "Configurações para ambiente de produção",
            "kubernetes/monitoring/": "Configurações para monitoramento",
            "docs/": "Documentação do projeto",
            "scripts/": "Scripts utilitários",
            "Dockerfile": "Dockerfile para construção da imagem",
            "requirements.txt": "Dependências do projeto",
            "requirements-dev.txt": "Dependências de desenvolvimento",
            "setup.py": "Script de instalação do pacote",
            "README.md": "Documentação principal",
            ".gitignore": "Arquivos a serem ignorados pelo Git",
            "Makefile": "Comandos para automação de tarefas",
            ".pre-commit-config.yaml": "Configuração de hooks de pre-commit"
        }
        
        return estrutura
    
    def gerar_makefile(self) -> str:
        """
        Gera Makefile para automação de tarefas
        
        Returns:
            str: Conteúdo do Makefile
        """
        makefile = """# Makefile for ML project

.PHONY: setup lint format test train evaluate deploy-dev deploy-staging deploy-prod clean

# Setup environment
setup:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

# Code quality
lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/
	isort src/ tests/

# Testing
test:
	pytest tests/unit/

test-integration:
	pytest tests/integration/

test-model:
	pytest tests/model/

# Data processing
process-data:
	python src/data/process_data.py

# Training
train:
	python src/training/train.py --config=configs/train_config.json

# Evaluation
evaluate:
	python src/evaluation/evaluate.py --model-path=models/latest/

# Deployment
build-docker:
	docker build -t ml-model:latest .

deploy-dev: build-docker
	kubectl apply -f kubernetes/dev/

deploy-staging: build-docker
	kubectl apply -f kubernetes/staging/

deploy-prod: build-docker
	kubectl apply -f kubernetes/production/

# Monitoring
setup-monitoring:
	kubectl apply -f kubernetes/monitoring/

# Cleanup
clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
"""
        return makefile
    
    def gerar_pre_commit_config(self) -> str:
        """
        Gera configuração para pre-commit hooks
        
        Returns:
            str: Conteúdo do arquivo .pre-commit-config.yaml
        """
        pre_commit = """repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
    -   id: check-added-large-files
    -   id: check-json
    -   id: check-toml

-   repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
    -   id: black

-   repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
    -   id: isort
        args: ["--profile", "black"]

-   repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
    -   id: flake8
        additional_dependencies: [flake8-docstrings]

-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
    -   id: mypy
        additional_dependencies: [types-requests, types-PyYAML]
"""
        return pre_commit
    
    def exportar_configuracao(self, caminho: str) -> None:
        """
        Exporta configuração do pipeline CI/CD para arquivo JSON
        
        Args:
            caminho: Caminho do arquivo
        """
        with open(caminho, 'w') as f:
            json.dump({
                "etapas": self.etapas,
                "ambientes": self.ambientes,
                "gatilhos": self.gatilhos,
                "estrutura_repositorio": self.gerar_estrutura_repositorio()
            }, f, indent=2)


# Exemplo de uso
if __name__ == "__main__":
    pipeline = PipelineCICDML()
    
    # Gerar workflows do GitHub Actions
    workflows = pipeline.gerar_github_workflows()
    
    # Criar diretório para workflows
    import os
    os.makedirs(".github/workflows", exist_ok=True)
    
    # Salvar workflows
    for nome, conteudo in workflows.items():
        with open(f".github/workflows/{nome}", 'w') as f:
            f.write(conteudo)
    
    # Gerar Makefile
    makefile = pipeline.gerar_makefile()
    with open("Makefile", 'w') as f:
        f.write(makefile)
    
    # Gerar configuração pre-commit
    pre_commit = pipeline.gerar_pre_commit_config()
    with open(".pre-commit-config.yaml", 'w') as f:
        f.write(pre_commit)
    
    # Exportar configuração
    pipeline.exportar_configuracao("pipeline_cicd_ml.json")
    
    print("Pipeline CI/CD para ML configurado com sucesso!")
    print(f"- {len(pipeline.etapas)} etapas definidas")
    print(f"- {len(workflows)} workflows do GitHub Actions gerados")
    print(f"- {len(pipeline.gerar_estrutura_repositorio())} arquivos/diretórios na estrutura do repositório")