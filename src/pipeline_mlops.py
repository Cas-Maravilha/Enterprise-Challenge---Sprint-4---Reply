import yaml
import json
from typing import Dict, List, Any, Optional

class PipelineMLOps:
    """Define o pipeline de MLOps para o sistema de IA"""
    
    def __init__(self):
        self.etapas = {
            "data-ingestion": {
                "descricao": "Ingestão e validação de dados",
                "ferramentas": ["Apache Airflow", "Great Expectations"],
                "artefatos": ["raw-data", "validated-data"],
                "metricas": ["data_quality_score", "schema_validation"]
            },
            "feature-engineering": {
                "descricao": "Engenharia de features",
                "ferramentas": ["Feast", "Pandas", "Scikit-learn"],
                "artefatos": ["feature-store", "feature-definitions"],
                "metricas": ["feature_importance", "correlation_matrix"]
            },
            "model-training": {
                "descricao": "Treinamento de modelos",
                "ferramentas": ["MLflow", "Scikit-learn", "TensorFlow", "PyTorch"],
                "artefatos": ["trained-model", "hyperparameters", "metrics"],
                "metricas": ["accuracy", "precision", "recall", "f1", "auc_roc"]
            },
            "model-evaluation": {
                "descricao": "Avaliação de modelos",
                "ferramentas": ["MLflow", "Scikit-learn"],
                "artefatos": ["evaluation-results", "model-comparison"],
                "metricas": ["accuracy", "precision", "recall", "f1", "auc_roc"]
            },
            "model-registration": {
                "descricao": "Registro de modelos",
                "ferramentas": ["MLflow Model Registry", "DVC"],
                "artefatos": ["registered-model", "model-lineage"],
                "metricas": ["model_version", "approval_status"]
            },
            "model-deployment": {
                "descricao": "Implantação de modelos",
                "ferramentas": ["KServe", "Seldon Core", "BentoML"],
                "artefatos": ["deployment-config", "model-endpoint"],
                "metricas": ["deployment_time", "rollback_count"]
            },
            "model-monitoring": {
                "descricao": "Monitoramento de modelos",
                "ferramentas": ["Prometheus", "Grafana", "Evidently"],
                "artefatos": ["monitoring-dashboard", "alerts-config"],
                "metricas": ["prediction_drift", "data_drift", "model_performance"]
            },
            "feedback-loop": {
                "descricao": "Loop de feedback e retreinamento",
                "ferramentas": ["Apache Airflow", "MLflow"],
                "artefatos": ["feedback-data", "retraining-trigger"],
                "metricas": ["feedback_volume", "retraining_frequency"]
            }
        }
        
        self.integracao_ci_cd = {
            "repositorios": {
                "codigo": "github.com/empresa/ml-platform-code",
                "dados": "github.com/empresa/ml-platform-data",
                "configuracao": "github.com/empresa/ml-platform-config"
            },
            "ci_cd": {
                "ferramenta": "GitHub Actions",
                "workflows": [
                    {
                        "nome": "test-and-lint",
                        "trigger": ["push", "pull_request"],
                        "acoes": ["lint", "unit-test", "integration-test"]
                    },
                    {
                        "nome": "build-and-push",
                        "trigger": ["release"],
                        "acoes": ["build-docker", "test", "push-registry"]
                    },
                    {
                        "nome": "deploy-dev",
                        "trigger": ["workflow_dispatch", "push to develop"],
                        "acoes": ["deploy-to-dev", "smoke-test"]
                    },
                    {
                        "nome": "deploy-prod",
                        "trigger": ["workflow_dispatch", "release"],
                        "acoes": ["deploy-to-prod", "canary-deployment"]
                    },
                    {
                        "nome": "retrain-model",
                        "trigger": ["schedule", "workflow_dispatch"],
                        "acoes": ["data-ingestion", "training", "evaluation", "approval"]
                    }
                ]
            }
        }
    
    def gerar_github_workflows(self) -> Dict[str, str]:
        """
        Gera arquivos de workflow do GitHub Actions
        
        Returns:
            Dict[str, str]: Dicionário com nome do arquivo e conteúdo YAML
        """
        workflows = {}
        
        # Workflow de teste e lint
        test_lint_yaml = """name: Test and Lint

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

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
          pip install flake8 black isort
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      - name: Lint with flake8
        run: flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
      - name: Check formatting with black
        run: black --check .
      - name: Check imports with isort
        run: isort --check-only --profile black .

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
      - name: Test with pytest
        run: pytest --cov=./ --cov-report=xml
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v1
"""
        workflows["test-and-lint.yml"] = test_lint_yaml
        
        # Workflow de build e push
        build_push_yaml = """name: Build and Push

on:
  release:
    types: [published]

jobs:
  build:
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
      
      - name: Build and push
        uses: docker/build-push-action@v2
        with:
          context: .
          push: true
          tags: |
            myorg/ml-platform:latest
            myorg/ml-platform:${{ github.event.release.tag_name }}
"""
        workflows["build-and-push.yml"] = build_push_yaml
        
        # Workflow de retreinamento de modelo
        retrain_model_yaml = """name: Retrain Model

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday
  workflow_dispatch:
    inputs:
      dataset_version:
        description: 'Dataset version to use'
        required: false
        default: 'latest'

jobs:
  data-ingestion:
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
          pip install -r requirements.txt
      - name: Run data ingestion
        run: python scripts/data_ingestion.py --version ${{ github.event.inputs.dataset_version || 'latest' }}
      - name: Validate data
        run: python scripts/validate_data.py
      - name: Upload data artifact
        uses: actions/upload-artifact@v2
        with:
          name: processed-data
          path: data/processed/

  training:
    needs: data-ingestion
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
          pip install -r requirements.txt
      - name: Download data artifact
        uses: actions/download-artifact@v2
        with:
          name: processed-data
          path: data/processed/
      - name: Train model
        run: python scripts/train_model.py
      - name: Upload model artifact
        uses: actions/upload-artifact@v2
        with:
          name: trained-model
          path: models/

  evaluation:
    needs: training
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
          pip install -r requirements.txt
      - name: Download model artifact
        uses: actions/download-artifact@v2
        with:
          name: trained-model
          path: models/
      - name: Download data artifact
        uses: actions/download-artifact@v2
        with:
          name: processed-data
          path: data/processed/
      - name: Evaluate model
        run: python scripts/evaluate_model.py
      - name: Upload evaluation results
        uses: actions/upload-artifact@v2
        with:
          name: evaluation-results
          path: reports/

  register:
    needs: evaluation
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
          pip install -r requirements.txt
      - name: Download model artifact
        uses: actions/download-artifact@v2
        with:
          name: trained-model
          path: models/
      - name: Download evaluation results
        uses: actions/download-artifact@v2
        with:
          name: evaluation-results
          path: reports/
      - name: Register model
        run: python scripts/register_model.py
"""
        workflows["retrain-model.yml"] = retrain_model_yaml
        
        # Workflow de deploy
        deploy_yaml = """name: Deploy Model

on:
  workflow_dispatch:
    inputs:
      model_version:
        description: 'Model version to deploy'
        required: true
      environment:
        description: 'Environment to deploy to'
        required: true
        default: 'staging'
        options:
          - staging
          - production

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ github.event.inputs.environment }}
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      - name: Deploy model
        run: python scripts/deploy_model.py --version ${{ github.event.inputs.model_version }} --env ${{ github.event.inputs.environment }}
      - name: Run smoke tests
        run: python scripts/smoke_test.py --env ${{ github.event.inputs.environment }}
"""
        workflows["deploy-model.yml"] = deploy_yaml
        
        return workflows
    
    def gerar_airflow_dag(self) -> str:
        """
        Gera código para DAG do Airflow para o pipeline de MLOps
        
        Returns:
            str: Código Python para DAG do Airflow
        """
        dag_code = """import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.operators.sagemaker_training import SageMakerTrainingOperator
from airflow.providers.amazon.aws.operators.sagemaker_model import SageMakerModelOperator
from airflow.providers.amazon.aws.operators.sagemaker_endpoint import SageMakerEndpointOperator

# Define default arguments
default_args = {
    'owner': 'ml-platform',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email': ['ml-alerts@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Define DAG
dag = DAG(
    'ml_training_pipeline',
    default_args=default_args,
    description='End-to-end ML training pipeline',
    schedule_interval=timedelta(days=7),
    catchup=False
)

# Define tasks
def data_ingestion(**kwargs):
    # Code to ingest data from source
    print("Ingesting data...")
    # Example: download data from S3
    s3_hook = S3Hook(aws_conn_id='aws_default')
    s3_hook.download_file(
        key='raw-data/latest.csv',
        bucket_name='ml-raw-data',
        local_path='/tmp/raw_data.csv'
    )
    return '/tmp/raw_data.csv'

def validate_data(**kwargs):
    # Code to validate data quality
    print("Validating data...")
    # Example: use Great Expectations
    import great_expectations as ge
    data_path = kwargs['ti'].xcom_pull(task_ids='data_ingestion')
    df = ge.read_csv(data_path)
    validation_result = df.expect_column_values_to_not_be_null('target')
    return validation_result.success

def feature_engineering(**kwargs):
    # Code for feature engineering
    print("Engineering features...")
    # Example: transform data and save features
    import pandas as pd
    data_path = kwargs['ti'].xcom_pull(task_ids='data_ingestion')
    df = pd.read_csv(data_path)
    # Feature transformations...
    df.to_csv('/tmp/features.csv', index=False)
    return '/tmp/features.csv'

def split_data(**kwargs):
    # Code to split data into train/test
    print("Splitting data...")
    import pandas as pd
    from sklearn.model_selection import train_test_split
    
    features_path = kwargs['ti'].xcom_pull(task_ids='feature_engineering')
    df = pd.read_csv(features_path)
    
    X = df.drop('target', axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    train_df = pd.concat([X_train, y_train], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)
    
    train_path = '/tmp/train.csv'
    test_path = '/tmp/test.csv'
    
    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)
    
    return {'train_path': train_path, 'test_path': test_path}

def train_model(**kwargs):
    # Code to train model
    print("Training model...")
    import pandas as pd
    import pickle
    from sklearn.ensemble import RandomForestClassifier
    
    split_data_output = kwargs['ti'].xcom_pull(task_ids='split_data')
    train_path = split_data_output['train_path']
    
    train_df = pd.read_csv(train_path)
    X_train = train_df.drop('target', axis=1)
    y_train = train_df['target']
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    model_path = '/tmp/model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    return model_path

def evaluate_model(**kwargs):
    # Code to evaluate model
    print("Evaluating model...")
    import pandas as pd
    import pickle
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    
    model_path = kwargs['ti'].xcom_pull(task_ids='train_model')
    split_data_output = kwargs['ti'].xcom_pull(task_ids='split_data')
    test_path = split_data_output['test_path']
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    test_df = pd.read_csv(test_path)
    X_test = test_df.drop('target', axis=1)
    y_test = test_df['target']
    
    y_pred = model.predict(X_test)
    
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'precision': precision_score(y_test, y_pred),
        'recall': recall_score(y_test, y_pred),
        'f1': f1_score(y_test, y_pred)
    }
    
    print(f"Model metrics: {metrics}")
    return metrics

def register_model(**kwargs):
    # Code to register model in MLflow
    print("Registering model...")
    import mlflow
    
    model_path = kwargs['ti'].xcom_pull(task_ids='train_model')
    metrics = kwargs['ti'].xcom_pull(task_ids='evaluate_model')
    
    mlflow.set_tracking_uri('http://mlflow-server:5000')
    mlflow.set_experiment('ml-pipeline')
    
    with mlflow.start_run():
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(
            sk_model=model_path,
            artifact_path="model",
            registered_model_name="ml-model"
        )
    
    return "Model registered successfully"

# Create tasks
t1 = PythonOperator(
    task_id='data_ingestion',
    python_callable=data_ingestion,
    provide_context=True,
    dag=dag,
)

t2 = PythonOperator(
    task_id='validate_data',
    python_callable=validate_data,
    provide_context=True,
    dag=dag,
)

t3 = PythonOperator(
    task_id='feature_engineering',
    python_callable=feature_engineering,
    provide_context=True,
    dag=dag,
)

t4 = PythonOperator(
    task_id='split_data',
    python_callable=split_data,
    provide_context=True,
    dag=dag,
)

t5 = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    provide_context=True,
    dag=dag,
)

t6 = PythonOperator(
    task_id='evaluate_model',
    python_callable=evaluate_model,
    provide_context=True,
    dag=dag,
)

t7 = PythonOperator(
    task_id='register_model',
    python_callable=register_model,
    provide_context=True,
    dag=dag,
)

# Define dependencies
t1 >> t2 >> t3 >> t4 >> t5 >> t6 >> t7
"""
        return dag_code
    
    def gerar_diagrama_pipeline(self) -> Dict[str, Any]:
        """
        Gera representação do pipeline para visualização
        
        Returns:
            Dict: Representação do pipeline
        """
        nodes = []
        edges = []
        
        # Adicionar nós
        for i, (nome, config) in enumerate(self.etapas.items()):
            nodes.append({
                "id": nome,
                "label": nome,
                "description": config["descricao"],
                "tools": config["ferramentas"]
            })
            
            # Adicionar arestas para conectar etapas sequenciais
            if i > 0:
                prev_nome = list(self.etapas.keys())[i-1]
                edges.append({
                    "from": prev_nome,
                    "to": nome
                })
        
        # Adicionar aresta de feedback
        edges.append({
            "from": "model-monitoring",
            "to": "data-ingestion",
            "label": "feedback loop"
        })
        
        return {
            "nodes": nodes,
            "edges": edges
        }
    
    def exportar_configuracao(self, caminho: str) -> None:
        """
        Exporta configuração do pipeline para arquivo JSON
        
        Args:
            caminho: Caminho do arquivo
        """
        with open(caminho, 'w') as f:
            json.dump({
                "etapas": self.etapas,
                "integracao_ci_cd": self.integracao_ci_cd,
                "diagrama": self.gerar_diagrama_pipeline()
            }, f, indent=2)


# Exemplo de uso
if __name__ == "__main__":
    pipeline = PipelineMLOps()
    
    # Gerar workflows do GitHub Actions
    workflows = pipeline.gerar_github_workflows()
    
    # Criar diretório para workflows
    import os
    os.makedirs(".github/workflows", exist_ok=True)
    
    # Salvar workflows
    for nome, conteudo in workflows.items():
        with open(f".github/workflows/{nome}", 'w') as f:
            f.write(conteudo)
    
    # Gerar DAG do Airflow
    dag_code = pipeline.gerar_airflow_dag()
    
    # Criar diretório para DAGs
    os.makedirs("airflow/dags", exist_ok=True)
    
    # Salvar DAG
    with open("airflow/dags/ml_pipeline_dag.py", 'w') as f:
        f.write(dag_code)
    
    # Exportar configuração
    pipeline.exportar_configuracao("pipeline_mlops.json")
    
    print("Pipeline MLOps configurado com sucesso!")
    print(f"- {len(pipeline.etapas)} etapas definidas")
    print(f"- {len(workflows)} workflows do GitHub Actions gerados")
    print("- DAG do Airflow gerado")