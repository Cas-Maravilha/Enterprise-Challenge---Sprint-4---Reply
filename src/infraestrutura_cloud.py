import json
import yaml
from typing import Dict, List, Any, Optional

class InfraestruturaCloud:
    """Define a infraestrutura cloud (AWS) para o sistema de IA"""
    
    def __init__(self):
        self.recursos = {
            "compute": {
                "eks": {
                    "nome": "ml-platform-cluster",
                    "versao": "1.24",
                    "node_groups": [
                        {
                            "nome": "standard-workers",
                            "instancia": "t3.large",
                            "min_size": 2,
                            "max_size": 5,
                            "desired_size": 3
                        },
                        {
                            "nome": "gpu-workers",
                            "instancia": "g4dn.xlarge",
                            "min_size": 0,
                            "max_size": 3,
                            "desired_size": 0
                        }
                    ]
                }
            },
            "storage": {
                "s3": [
                    {
                        "nome": "ml-raw-data",
                        "versioning": True,
                        "lifecycle_rules": [
                            {
                                "prefix": "temp/",
                                "expiration_days": 7
                            }
                        ]
                    },
                    {
                        "nome": "ml-processed-data",
                        "versioning": True
                    },
                    {
                        "nome": "ml-models",
                        "versioning": True
                    }
                ],
                "efs": {
                    "nome": "ml-shared-storage",
                    "performance_mode": "generalPurpose"
                }
            },
            "database": {
                "dynamodb": [
                    {
                        "nome": "feature-store",
                        "hash_key": "feature_id",
                        "range_key": "timestamp"
                    },
                    {
                        "nome": "model-registry",
                        "hash_key": "model_id",
                        "range_key": "version"
                    },
                    {
                        "nome": "model-metrics",
                        "hash_key": "model_id",
                        "range_key": "timestamp"
                    }
                ],
                "rds": {
                    "nome": "ml-metadata",
                    "engine": "postgres",
                    "instancia": "db.t3.medium",
                    "storage": 20
                }
            },
            "ml_services": {
                "sagemaker": {
                    "notebook_instances": [
                        {
                            "nome": "ml-development",
                            "instancia": "ml.t3.medium"
                        }
                    ],
                    "endpoints": [
                        {
                            "nome": "model-inference",
                            "instancia": "ml.c5.large",
                            "auto_scaling": True,
                            "min_instances": 1,
                            "max_instances": 3
                        }
                    ]
                }
            },
            "monitoring": {
                "cloudwatch": {
                    "dashboards": ["ml-platform-metrics"],
                    "alarms": [
                        {
                            "nome": "high-latency",
                            "metrica": "p95_latency",
                            "threshold": 500,
                            "periodo": 60
                        },
                        {
                            "nome": "error-rate",
                            "metrica": "error_rate",
                            "threshold": 0.01,
                            "periodo": 60
                        }
                    ]
                }
            },
            "networking": {
                "vpc": {
                    "nome": "ml-platform-vpc",
                    "cidr": "10.0.0.0/16",
                    "subnets": 3
                }
            }
        }
    
    def gerar_terraform(self) -> Dict[str, str]:
        """
        Gera código Terraform para a infraestrutura
        
        Returns:
            Dict[str, str]: Dicionário com nome do arquivo e conteúdo
        """
        terraform_files = {}
        
        # Arquivo principal
        main_tf = """provider "aws" {
  region = "us-east-1"
}

terraform {
  backend "s3" {
    bucket = "terraform-state-ml-platform"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}
"""
        terraform_files["main.tf"] = main_tf
        
        # VPC
        vpc_tf = """module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "%(nome)s"
  cidr = "%(cidr)s"
  
  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  
  enable_nat_gateway = true
  single_nat_gateway = true
  
  tags = {
    Environment = "production"
    Project     = "ml-platform"
  }
}
""" % self.recursos["networking"]["vpc"]
        terraform_files["vpc.tf"] = vpc_tf
        
        # EKS
        eks_config = self.recursos["compute"]["eks"]
        eks_tf = """module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  
  cluster_name    = "%(nome)s"
  cluster_version = "%(versao)s"
  
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = module.vpc.private_subnets
  
  cluster_endpoint_private_access = true
  cluster_endpoint_public_access  = true
  
""" % eks_config
        
        # Node groups
        for i, ng in enumerate(eks_config["node_groups"]):
            eks_tf += f"""  eks_managed_node_groups = {{
    {ng['nome']} = {{
      instance_types = ["{ng['instancia']}"]
      min_size       = {ng['min_size']}
      max_size       = {ng['max_size']}
      desired_size   = {ng['desired_size']}
    }}
  }}
"""
        
        eks_tf += """  tags = {
    Environment = "production"
    Project     = "ml-platform"
  }
}
"""
        terraform_files["eks.tf"] = eks_tf
        
        # S3
        s3_tf = ""
        for bucket in self.recursos["storage"]["s3"]:
            s3_tf += f"""resource "aws_s3_bucket" "{bucket['nome']}" {{
  bucket = "{bucket['nome']}"
  
  tags = {{
    Environment = "production"
    Project     = "ml-platform"
  }}
}}

resource "aws_s3_bucket_versioning" "{bucket['nome']}_versioning" {{
  bucket = aws_s3_bucket.{bucket['nome']}.id
  versioning_configuration {{
    status = "{'Enabled' if bucket.get('versioning', False) else 'Disabled'}"
  }}
}}

"""
            
            # Lifecycle rules if present
            if "lifecycle_rules" in bucket:
                for rule in bucket["lifecycle_rules"]:
                    s3_tf += f"""resource "aws_s3_bucket_lifecycle_configuration" "{bucket['nome']}_lifecycle_rule_{rule['prefix'].replace('/', '_')}" {{
  bucket = aws_s3_bucket.{bucket['nome']}.id
  
  rule {{
    id     = "expire-{rule['prefix'].replace('/', '-')}"
    status = "Enabled"
    
    filter {{
      prefix = "{rule['prefix']}"
    }}
    
    expiration {{
      days = {rule['expiration_days']}
    }}
  }}
}}

"""
        
        terraform_files["s3.tf"] = s3_tf
        
        # DynamoDB
        dynamodb_tf = ""
        for table in self.recursos["database"]["dynamodb"]:
            dynamodb_tf += f"""resource "aws_dynamodb_table" "{table['nome']}" {{
  name           = "{table['nome']}"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "{table['hash_key']}"
  range_key      = "{table['range_key']}"
  
  attribute {{
    name = "{table['hash_key']}"
    type = "S"
  }}
  
  attribute {{
    name = "{table['range_key']}"
    type = "S"
  }}
  
  tags = {{
    Environment = "production"
    Project     = "ml-platform"
  }}
}}

"""
        
        terraform_files["dynamodb.tf"] = dynamodb_tf
        
        # RDS
        rds = self.recursos["database"]["rds"]
        rds_tf = f"""resource "aws_db_instance" "{rds['nome']}" {{
  identifier           = "{rds['nome']}"
  engine               = "{rds['engine']}"
  engine_version       = "13.4"
  instance_class       = "{rds['instancia']}"
  allocated_storage    = {rds['storage']}
  storage_type         = "gp2"
  db_name              = "mlmetadata"
  username             = "admin"
  password             = "{{var.db_password}}"
  skip_final_snapshot  = true
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.rds.name
  
  tags = {{
    Environment = "production"
    Project     = "ml-platform"
  }}
}}

resource "aws_db_subnet_group" "rds" {{
  name       = "ml-platform-rds"
  subnet_ids = module.vpc.private_subnets
  
  tags = {{
    Environment = "production"
    Project     = "ml-platform"
  }}
}}

resource "aws_security_group" "rds" {{
  name        = "ml-platform-rds"
  description = "Allow database traffic"
  vpc_id      = module.vpc.vpc_id
  
  ingress {{
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [module.vpc.vpc_cidr_block]
  }}
  
  tags = {{
    Environment = "production"
    Project     = "ml-platform"
  }}
}}
"""
        terraform_files["rds.tf"] = rds_tf
        
        # SageMaker
        sagemaker_tf = ""
        
        # Notebook instances
        for nb in self.recursos["ml_services"]["sagemaker"]["notebook_instances"]:
            sagemaker_tf += f"""resource "aws_sagemaker_notebook_instance" "{nb['nome']}" {{
  name          = "{nb['nome']}"
  role_arn      = aws_iam_role.sagemaker.arn
  instance_type = "{nb['instancia']}"
  
  tags = {{
    Environment = "production"
    Project     = "ml-platform"
  }}
}}

"""
        
        # IAM role for SageMaker
        sagemaker_tf += """resource "aws_iam_role" "sagemaker" {
  name = "sagemaker-execution-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "sagemaker.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "sagemaker_full_access" {
  role       = aws_iam_role.sagemaker.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSageMakerFullAccess"
}
"""
        
        terraform_files["sagemaker.tf"] = sagemaker_tf
        
        return terraform_files
    
    def estimar_custos_mensais(self) -> Dict[str, float]:
        """
        Estima custos mensais da infraestrutura
        
        Returns:
            Dict[str, float]: Estimativa de custos por categoria
        """
        # Preços aproximados (USD)
        precos = {
            # Compute
            "t3.large": 0.0832 * 24 * 30,  # por instância/mês
            "g4dn.xlarge": 0.526 * 24 * 30,  # por instância/mês
            "eks_cluster": 0.10 * 24 * 30,  # por cluster/mês
            
            # Storage
            "s3_gb_month": 0.023,  # por GB/mês
            "efs_gb_month": 0.30,  # por GB/mês
            
            # Database
            "db.t3.medium": 0.068 * 24 * 30,  # por instância/mês
            "rds_storage_gb": 0.115,  # por GB/mês
            "dynamodb": 0.25 * 30,  # estimativa básica por tabela/mês
            
            # ML Services
            "ml.t3.medium": 0.05 * 24 * 30,  # por instância/mês
            "ml.c5.large": 0.119 * 24 * 30,  # por instância/mês
            
            # Networking
            "nat_gateway": 0.045 * 24 * 30,  # por gateway/mês
            "data_transfer_gb": 0.09  # por GB
        }
        
        custos = {
            "compute": 0,
            "storage": 0,
            "database": 0,
            "ml_services": 0,
            "networking": 0,
            "outros": 0
        }
        
        # Compute - EKS
        eks = self.recursos["compute"]["eks"]
        custos["compute"] += precos["eks_cluster"]  # Custo do cluster
        
        # Node groups
        for ng in eks["node_groups"]:
            if "g4dn" in ng["instancia"]:
                custos["compute"] += precos["g4dn.xlarge"] * ng["desired_size"]
            else:
                custos["compute"] += precos["t3.large"] * ng["desired_size"]
        
        # Storage - S3 (estimativa de 100GB por bucket)
        for bucket in self.recursos["storage"]["s3"]:
            custos["storage"] += precos["s3_gb_month"] * 100
        
        # Storage - EFS (estimativa de 100GB)
        custos["storage"] += precos["efs_gb_month"] * 100
        
        # Database - DynamoDB
        for table in self.recursos["database"]["dynamodb"]:
            custos["database"] += precos["dynamodb"]
        
        # Database - RDS
        rds = self.recursos["database"]["rds"]
        custos["database"] += precos["db.t3.medium"]
        custos["database"] += precos["rds_storage_gb"] * rds["storage"]
        
        # ML Services - SageMaker
        for nb in self.recursos["ml_services"]["sagemaker"]["notebook_instances"]:
            custos["ml_services"] += precos["ml.t3.medium"]
        
        for endpoint in self.recursos["ml_services"]["sagemaker"]["endpoints"]:
            custos["ml_services"] += precos["ml.c5.large"] * endpoint["min_instances"]
        
        # Networking
        custos["networking"] += precos["nat_gateway"]  # NAT Gateway
        custos["networking"] += precos["data_transfer_gb"] * 100  # Estimativa de 100GB de transferência
        
        # Total
        total = sum(custos.values())
        
        return {
            **custos,
            "total": round(total, 2),
            "moeda": "USD",
            "periodo": "mensal"
        }
    
    def exportar_configuracao(self, caminho: str) -> None:
        """
        Exporta configuração da infraestrutura para arquivo JSON
        
        Args:
            caminho: Caminho do arquivo
        """
        with open(caminho, 'w') as f:
            json.dump({
                "recursos": self.recursos,
                "custos_estimados": self.estimar_custos_mensais()
            }, f, indent=2)


# Exemplo de uso
if __name__ == "__main__":
    infra = InfraestruturaCloud()
    
    # Gerar código Terraform
    terraform_files = infra.gerar_terraform()
    
    # Criar diretório para arquivos Terraform
    import os
    os.makedirs("terraform", exist_ok=True)
    
    # Salvar arquivos Terraform
    for nome, conteudo in terraform_files.items():
        with open(f"terraform/{nome}", 'w') as f:
            f.write(conteudo)
    
    # Exportar configuração
    infra.exportar_configuracao("infraestrutura_cloud.json")
    
    # Estimar custos
    custos = infra.estimar_custos_mensais()
    print(f"Custo mensal estimado: ${custos['total']} USD")
    for categoria, valor in {k: v for k, v in custos.items() if k != 'total' and k != 'moeda' and k != 'periodo'}.items():
        print(f"  {categoria}: ${valor:.2f} USD")