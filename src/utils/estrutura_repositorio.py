import os
import json
from typing import Dict, List, Any, Optional

class EstruturaRepositorio:
    """Define uma estrutura de repositório robusta para o projeto de IA"""
    
    def __init__(self):
        self.estrutura = {
            # Diretórios principais
            "src": {
                "descricao": "Código-fonte do projeto",
                "subdiretorios": {
                    "data": {
                        "descricao": "Módulos para processamento de dados",
                        "arquivos": [
                            "ingestion.py",
                            "preprocessing.py",
                            "validation.py",
                            "feature_engineering.py",
                            "dataset.py",
                            "__init__.py"
                        ]
                    },
                    "models": {
                        "descricao": "Implementações dos modelos de IA",
                        "arquivos": [
                            "random_forest.py",
                            "lstm.py",
                            "isolation_forest.py",
                            "svm.py",
                            "ensemble.py",
                            "base.py",
                            "__init__.py"
                        ]
                    },
                    "training": {
                        "descricao": "Módulos para treinamento de modelos",
                        "arquivos": [
                            "trainer.py",
                            "hyperparameter_tuning.py",
                            "callbacks.py",
                            "metrics.py",
                            "__init__.py"
                        ]
                    },
                    "evaluation": {
                        "descricao": "Módulos para avaliação de modelos",
                        "arquivos": [
                            "evaluator.py",
                            "metrics.py",
                            "validation.py",
                            "cross_validation.py",
                            "__init__.py"
                        ]
                    },
                    "serving": {
                        "descricao": "Módulos para servir modelos",
                        "arquivos": [
                            "api.py",
                            "prediction.py",
                            "middleware.py",
                            "caching.py",
                            "__init__.py"
                        ]
                    },
                    "monitoring": {
                        "descricao": "Módulos para monitoramento de modelos",
                        "arquivos": [
                            "drift_detector.py",
                            "performance_monitor.py",
                            "alerting.py",
                            "logging.py",
                            "__init__.py"
                        ]
                    },
                    "utils": {
                        "descricao": "Utilitários e funções auxiliares",
                        "arquivos": [
                            "config.py",
                            "logging.py",
                            "io.py",
                            "visualization.py",
                            "__init__.py"
                        ]
                    },
                    "__init__.py": "Arquivo de inicialização do pacote"
                }
            },
            "tests": {
                "descricao": "Testes automatizados",
                "subdiretorios": {
                    "unit": {
                        "descricao": "Testes unitários",
                        "subdiretorios": {
                            "data": {"descricao": "Testes para módulos de dados"},
                            "models": {"descricao": "Testes para implementações de modelos"},
                            "training": {"descricao": "Testes para módulos de treinamento"},
                            "evaluation": {"descricao": "Testes para módulos de avaliação"},
                            "serving": {"descricao": "Testes para módulos de serving"},
                            "monitoring": {"descricao": "Testes para módulos de monitoramento"},
                            "utils": {"descricao": "Testes para utilitários"}
                        }
                    },
                    "integration": {
                        "descricao": "Testes de integração",
                        "arquivos": [
                            "test_data_pipeline.py",
                            "test_training_pipeline.py",
                            "test_evaluation_pipeline.py",
                            "test_serving_pipeline.py"
                        ]
                    },
                    "e2e": {
                        "descricao": "Testes end-to-end",
                        "arquivos": [
                            "test_full_pipeline.py",
                            "test_api.py"
                        ]
                    },
                    "conftest.py": "Configurações para pytest"
                }
            },
            "configs": {
                "descricao": "Arquivos de configuração",
                "arquivos": [
                    "config.yaml",
                    "logging.yaml",
                    "models.yaml",
                    "training.yaml",
                    "evaluation.yaml",
                    "serving.yaml",
                    "monitoring.yaml"
                ]
            },
            "notebooks": {
                "descricao": "Jupyter notebooks para exploração e análise",
                "arquivos": [
                    "01_data_exploration.ipynb",
                    "02_feature_engineering.ipynb",
                    "03_model_prototyping.ipynb",
                    "04_model_evaluation.ipynb",
                    "05_model_interpretation.ipynb"
                ]
            },
            "scripts": {
                "descricao": "Scripts utilitários",
                "arquivos": [
                    "setup_environment.sh",
                    "download_data.py",
                    "train_model.py",
                    "evaluate_model.py",
                    "serve_model.py",
                    "monitor_model.py"
                ]
            },
            "data": {
                "descricao": "Diretório para dados (ou links para dados externos)",
                "subdiretorios": {
                    "raw": {"descricao": "Dados brutos"},
                    "processed": {"descricao": "Dados processados"},
                    "features": {"descricao": "Features extraídas"},
                    "external": {"descricao": "Dados externos"},
                    ".gitkeep": "Arquivo para manter diretório no Git"
                }
            },
            "models": {
                "descricao": "Diretório para modelos treinados",
                "subdiretorios": {
                    "random_forest": {"descricao": "Modelos Random Forest"},
                    "lstm": {"descricao": "Modelos LSTM"},
                    "isolation_forest": {"descricao": "Modelos Isolation Forest"},
                    "svm": {"descricao": "Modelos SVM"},
                    "ensemble": {"descricao": "Modelos Ensemble"},
                    ".gitkeep": "Arquivo para manter diretório no Git"
                }
            },
            "docs": {
                "descricao": "Documentação do projeto",
                "subdiretorios": {
                    "architecture": {
                        "descricao": "Documentação de arquitetura",
                        "arquivos": [
                            "overview.md",
                            "data_architecture.md",
                            "model_architecture.md",
                            "deployment_architecture.md"
                        ]
                    },
                    "api": {
                        "descricao": "Documentação da API",
                        "arquivos": [
                            "api_reference.md",
                            "endpoints.md",
                            "examples.md"
                        ]
                    },
                    "models": {
                        "descricao": "Documentação dos modelos",
                        "arquivos": [
                            "random_forest.md",
                            "lstm.md",
                            "isolation_forest.md",
                            "svm.md",
                            "ensemble.md"
                        ]
                    },
                    "user_guides": {
                        "descricao": "Guias de usuário",
                        "arquivos": [
                            "getting_started.md",
                            "data_preparation.md",
                            "model_training.md",
                            "model_deployment.md",
                            "monitoring.md"
                        ]
                    },
                    "development": {
                        "descricao": "Guias de desenvolvimento",
                        "arquivos": [
                            "contributing.md",
                            "code_standards.md",
                            "testing.md",
                            "ci_cd.md"
                        ]
                    }
                }
            },
            "kubernetes": {
                "descricao": "Manifestos Kubernetes para implantação",
                "subdiretorios": {
                    "base": {
                        "descricao": "Configurações base",
                        "arquivos": [
                            "deployment.yaml",
                            "service.yaml",
                            "configmap.yaml",
                            "secret.yaml",
                            "kustomization.yaml"
                        ]
                    },
                    "overlays": {
                        "descricao": "Overlays para diferentes ambientes",
                        "subdiretorios": {
                            "dev": {
                                "descricao": "Ambiente de desenvolvimento",
                                "arquivos": [
                                    "kustomization.yaml",
                                    "deployment-patch.yaml",
                                    "configmap-patch.yaml"
                                ]
                            },
                            "staging": {
                                "descricao": "Ambiente de homologação",
                                "arquivos": [
                                    "kustomization.yaml",
                                    "deployment-patch.yaml",
                                    "configmap-patch.yaml"
                                ]
                            },
                            "production": {
                                "descricao": "Ambiente de produção",
                                "arquivos": [
                                    "kustomization.yaml",
                                    "deployment-patch.yaml",
                                    "configmap-patch.yaml",
                                    "hpa.yaml"
                                ]
                            }
                        }
                    },
                    "monitoring": {
                        "descricao": "Configurações de monitoramento",
                        "arquivos": [
                            "prometheus.yaml",
                            "grafana.yaml",
                            "servicemonitor.yaml",
                            "alerts.yaml"
                        ]
                    }
                }
            },
            ".github": {
                "descricao": "Configurações do GitHub",
                "subdiretorios": {
                    "workflows": {
                        "descricao": "Workflows do GitHub Actions",
                        "arquivos": [
                            "lint.yml",
                            "test.yml",
                            "build.yml",
                            "train.yml",
                            "deploy.yml",
                            "monitor.yml"
                        ]
                    },
                    "ISSUE_TEMPLATE": {
                        "descricao": "Templates para issues",
                        "arquivos": [
                            "bug_report.md",
                            "feature_request.md",
                            "model_improvement.md"
                        ]
                    },
                    "PULL_REQUEST_TEMPLATE.md": "Template para pull requests"
                }
            },
            # Arquivos na raiz
            "README.md": "Documentação principal do projeto",
            "CONTRIBUTING.md": "Guia de contribuição",
            "LICENSE": "Licença do projeto",
            "setup.py": "Script de instalação do pacote",
            "requirements.txt": "Dependências do projeto",
            "requirements-dev.txt": "Dependências de desenvolvimento",
            "Dockerfile": "Dockerfile para construção da imagem",
            "docker-compose.yml": "Configuração do Docker Compose",
            ".gitignore": "Arquivos a serem ignorados pelo Git",
            ".dockerignore": "Arquivos a serem ignorados pelo Docker",
            ".env.example": "Exemplo de arquivo de variáveis de ambiente",
            "Makefile": "Comandos para automação de tarefas",
            "pyproject.toml": "Configuração de ferramentas Python",
            ".pre-commit-config.yaml": "Configuração de hooks de pre-commit"
        }
    
    def criar_estrutura(self, diretorio_base: str) -> None:
        """
        Cria a estrutura de diretórios e arquivos no sistema de arquivos
        
        Args:
            diretorio_base: Diretório base onde a estrutura será criada
        """
        self._criar_recursivamente(diretorio_base, self.estrutura)
    
    def _criar_recursivamente(self, diretorio_atual: str, estrutura: Dict[str, Any]) -> None:
        """
        Cria recursivamente a estrutura de diretórios e arquivos
        
        Args:
            diretorio_atual: Diretório atual
            estrutura: Estrutura a ser criada
        """
        # Garantir que o diretório atual existe
        os.makedirs(diretorio_atual, exist_ok=True)
        
        # Para cada item na estrutura
        for nome, conteudo in estrutura.items():
            caminho = os.path.join(diretorio_atual, nome)
            
            # Se for um arquivo
            if isinstance(conteudo, str) or nome.endswith('.py') or nome.endswith('.md') or nome.endswith('.yaml') or nome.endswith('.yml') or nome.endswith('.sh') or nome.endswith('.ipynb') or nome == '.gitkeep':
                # Criar arquivo vazio ou com conteúdo básico
                with open(caminho, 'w') as f:
                    if isinstance(conteudo, str):
                        f.write(f"# {conteudo}\n")
                    elif nome.endswith('.py'):
                        f.write('"""' + f"\n{nome}\n" + '"""\n\n')
                    elif nome.endswith('.md'):
                        f.write(f"# {nome.split('.')[0].replace('_', ' ').title()}\n\n")
                    elif nome.endswith('.yaml') or nome.endswith('.yml'):
                        f.write("# YAML configuration\n\n")
                    elif nome.endswith('.sh'):
                        f.write("#!/bin/bash\n\n")
                    elif nome == '.gitkeep':
                        # Arquivo vazio
                        pass
            
            # Se for um diretório com subdiretorios ou arquivos
            elif isinstance(conteudo, dict):
                # Se tiver subdiretorios ou arquivos
                if 'subdiretorios' in conteudo:
                    self._criar_recursivamente(caminho, conteudo['subdiretorios'])
                elif 'arquivos' in conteudo:
                    # Criar diretório
                    os.makedirs(caminho, exist_ok=True)
                    
                    # Criar arquivos
                    for arquivo in conteudo['arquivos']:
                        caminho_arquivo = os.path.join(caminho, arquivo)
                        with open(caminho_arquivo, 'w') as f:
                            if arquivo.endswith('.py'):
                                f.write('"""' + f"\n{arquivo}\n" + '"""\n\n')
                            elif arquivo.endswith('.md'):
                                f.write(f"# {arquivo.split('.')[0].replace('_', ' ').title()}\n\n")
                            elif arquivo.endswith('.yaml') or arquivo.endswith('.yml'):
                                f.write("# YAML configuration\n\n")
                            elif arquivo.endswith('.sh'):
                                f.write("#!/bin/bash\n\n")
                            elif arquivo == '.gitkeep':
                                # Arquivo vazio
                                pass
                else:
                    # Criar diretório vazio
                    os.makedirs(caminho, exist_ok=True)
    
    def gerar_readme(self) -> str:
        """
        Gera conteúdo para o arquivo README.md
        
        Returns:
            str: Conteúdo do README.md
        """
        readme = []
        
        # Cabeçalho
        readme.append("# Projeto de IA - Enterprise Challenge - Sprint 3")
        readme.append("")
        readme.append("Sistema de IA com múltiplos modelos e pipeline completo de MLOps.")
        readme.append("")
        
        # Modelos
        readme.append("## Modelos de IA")
        readme.append("")
        readme.append("Este projeto implementa os seguintes modelos:")
        readme.append("")
        readme.append("- **Random Forest**: Modelo principal para classificação/regressão")
        readme.append("- **LSTM**: Modelo para processamento de séries temporais")
        readme.append("- **Isolation Forest**: Modelo para detecção de anomalias")
        readme.append("- **SVM**: Modelo alternativo para comparação")
        readme.append("- **Ensemble**: Combinação ponderada dos modelos acima")
        readme.append("")
        
        # Estrutura do projeto
        readme.append("## Estrutura do Projeto")
        readme.append("")
        readme.append("```")
        readme.append(".")
        
        # Adicionar diretórios principais
        for nome in sorted(self.estrutura.keys()):
            if nome.startswith('.'):
                continue
            if isinstance(self.estrutura[nome], dict):
                readme.append(f"├── {nome}/  # {self.estrutura[nome].get('descricao', '')}")
            else:
                readme.append(f"├── {nome}  # {self.estrutura[nome]}")
        
        readme.append("```")
        readme.append("")
        
        # Instalação
        readme.append("## Instalação")
        readme.append("")
        readme.append("```bash")
        readme.append("# Clonar o repositório")
        readme.append("git clone https://github.com/empresa/projeto-ia.git")
        readme.append("cd projeto-ia")
        readme.append("")
        readme.append("# Criar ambiente virtual")
        readme.append("python -m venv venv")
        readme.append("source venv/bin/activate  # Linux/Mac")
        readme.append("# ou")
        readme.append("venv\\Scripts\\activate  # Windows")
        readme.append("")
        readme.append("# Instalar dependências")
        readme.append("pip install -r requirements.txt")
        readme.append("```")
        readme.append("")
        
        # Uso
        readme.append("## Uso")
        readme.append("")
        readme.append("### Treinamento de Modelos")
        readme.append("")
        readme.append("```bash")
        readme.append("# Treinar modelo Random Forest")
        readme.append("python scripts/train_model.py --model random_forest --config configs/training.yaml")
        readme.append("")
        readme.append("# Treinar modelo LSTM")
        readme.append("python scripts/train_model.py --model lstm --config configs/training.yaml")
        readme.append("")
        readme.append("# Treinar ensemble")
        readme.append("python scripts/train_model.py --model ensemble --config configs/training.yaml")
        readme.append("```")
        readme.append("")
        
        # Avaliação
        readme.append("### Avaliação de Modelos")
        readme.append("")
        readme.append("```bash")
        readme.append("# Avaliar modelo")
        readme.append("python scripts/evaluate_model.py --model-path models/ensemble/latest")
        readme.append("```")
        readme.append("")
        
        # Implantação
        readme.append("### Implantação")
        readme.append("")
        readme.append("```bash")
        readme.append("# Implantar em ambiente de desenvolvimento")
        readme.append("kubectl apply -k kubernetes/overlays/dev")
        readme.append("")
        readme.append("# Implantar em produção")
        readme.append("kubectl apply -k kubernetes/overlays/production")
        readme.append("```")
        readme.append("")
        
        # Monitoramento
        readme.append("### Monitoramento")
        readme.append("")
        readme.append("```bash")
        readme.append("# Configurar monitoramento")
        readme.append("kubectl apply -f kubernetes/monitoring/")
        readme.append("")
        readme.append("# Verificar drift")
        readme.append("python scripts/monitor_model.py --check-drift")
        readme.append("```")
        readme.append("")
        
        # Contribuição
        readme.append("## Contribuição")
        readme.append("")
        readme.append("Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre como contribuir para este projeto.")
        readme.append("")
        
        # Licença
        readme.append("## Licença")
        readme.append("")
        readme.append("Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.")
        
        return "\n".join(readme)
    
    def gerar_contributing(self) -> str:
        """
        Gera conteúdo para o arquivo CONTRIBUTING.md
        
        Returns:
            str: Conteúdo do CONTRIBUTING.md
        """
        contributing = []
        
        # Cabeçalho
        contributing.append("# Guia de Contribuição")
        contributing.append("")
        contributing.append("Obrigado por considerar contribuir para este projeto! Este documento fornece diretrizes para contribuir com o projeto.")
        contributing.append("")
        
        # Fluxo de trabalho
        contributing.append("## Fluxo de Trabalho")
        contributing.append("")
        contributing.append("1. Faça um fork do repositório")
        contributing.append("2. Clone seu fork: `git clone https://github.com/seu-usuario/projeto-ia.git`")
        contributing.append("3. Crie uma branch para sua feature: `git checkout -b feature/nova-feature`")
        contributing.append("4. Faça suas alterações")
        contributing.append("5. Execute os testes: `make test`")
        contributing.append("6. Commit suas alterações: `git commit -m 'Adiciona nova feature'`")
        contributing.append("7. Push para a branch: `git push origin feature/nova-feature`")
        contributing.append("8. Abra um Pull Request")
        contributing.append("")
        
        # Padrões de código
        contributing.append("## Padrões de Código")
        contributing.append("")
        contributing.append("- Siga a PEP 8 para código Python")
        contributing.append("- Escreva docstrings para todas as funções, classes e módulos")
        contributing.append("- Mantenha a cobertura de testes acima de 80%")
        contributing.append("- Use type hints")
        contributing.append("")
        
        # Testes
        contributing.append("## Testes")
        contributing.append("")
        contributing.append("Todos os novos recursos devem incluir testes. Execute os testes com:")
        contributing.append("")
        contributing.append("```bash")
        contributing.append("# Executar todos os testes")
        contributing.append("pytest")
        contributing.append("")
        contributing.append("# Executar testes com cobertura")
        contributing.append("pytest --cov=src")
        contributing.append("```")
        contributing.append("")
        
        # Commits
        contributing.append("## Mensagens de Commit")
        contributing.append("")
        contributing.append("Use mensagens de commit claras e descritivas, seguindo o padrão:")
        contributing.append("")
        contributing.append("```")
        contributing.append("<tipo>(<escopo>): <descrição>")
        contributing.append("")
        contributing.append("<corpo>")
        contributing.append("")
        contributing.append("<rodapé>")
        contributing.append("```")
        contributing.append("")
        contributing.append("Tipos: feat, fix, docs, style, refactor, test, chore")
        contributing.append("")
        
        # Pull Requests
        contributing.append("## Pull Requests")
        contributing.append("")
        contributing.append("- Descreva claramente o que seu PR faz")
        contributing.append("- Vincule issues relacionadas")
        contributing.append("- Certifique-se de que todos os testes passam")
        contributing.append("- Obtenha revisão de pelo menos um mantenedor")
        contributing.append("")
        
        # Código de conduta
        contributing.append("## Código de Conduta")
        contributing.append("")
        contributing.append("Este projeto segue um Código de Conduta. Ao participar, espera-se que você respeite este código.")
        
        return "\n".join(contributing)
    
    def exportar_estrutura(self, caminho: str) -> None:
        """
        Exporta a estrutura para um arquivo JSON
        
        Args:
            caminho: Caminho do arquivo
        """
        with open(caminho, 'w') as f:
            json.dump(self.estrutura, f, indent=2)


# Exemplo de uso
if __name__ == "__main__":
    estrutura = EstruturaRepositorio()
    
    # Exportar estrutura
    estrutura.exportar_estrutura("estrutura_repositorio.json")
    
    # Gerar README.md
    readme = estrutura.gerar_readme()
    with open("README_template.md", 'w') as f:
        f.write(readme)
    
    # Gerar CONTRIBUTING.md
    contributing = estrutura.gerar_contributing()
    with open("CONTRIBUTING_template.md", 'w') as f:
        f.write(contributing)
    
    # Criar estrutura (descomente para criar)
    # estrutura.criar_estrutura("projeto-ia")
    
    print("Estrutura de repositório definida com sucesso!")
    print(f"Número de diretórios principais: {len([k for k, v in estrutura.estrutura.items() if isinstance(v, dict)])}")
    print(f"Número de arquivos na raiz: {len([k for k, v in estrutura.estrutura.items() if isinstance(v, str)])}")
    print("Arquivos gerados: estrutura_repositorio.json, README_template.md, CONTRIBUTING_template.md")