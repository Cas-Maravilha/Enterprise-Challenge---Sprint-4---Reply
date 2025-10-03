import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class CronogramaDetalhado:
    """Define um cronograma detalhado com fases específicas para o projeto de IA"""
    
    def __init__(self, data_inicio=None):
        """
        Inicializa o cronograma
        
        Args:
            data_inicio: Data de início do projeto (opcional)
        """
        # Definir data de início (padrão: hoje)
        self.data_inicio = data_inicio or datetime.now().date()
        
        # Definir fases do projeto
        self.fases = {
            "planejamento": {
                "nome": "Planejamento e Definição de Requisitos",
                "duracao_dias": 14,
                "dependencias": [],
                "atividades": [
                    {
                        "nome": "Levantamento de requisitos de negócio",
                        "duracao_dias": 5,
                        "responsaveis": ["Product Owner", "Data Scientist"],
                        "entregaveis": ["Documento de requisitos de negócio"]
                    },
                    {
                        "nome": "Definição de métricas de sucesso",
                        "duracao_dias": 3,
                        "responsaveis": ["Product Owner", "Data Scientist"],
                        "entregaveis": ["Documento de métricas de sucesso"]
                    },
                    {
                        "nome": "Análise de viabilidade técnica",
                        "duracao_dias": 4,
                        "responsaveis": ["Data Scientist", "ML Engineer"],
                        "entregaveis": ["Relatório de viabilidade técnica"]
                    },
                    {
                        "nome": "Definição de arquitetura",
                        "duracao_dias": 5,
                        "responsaveis": ["ML Engineer", "DevOps Engineer"],
                        "entregaveis": ["Documento de arquitetura"]
                    }
                ]
            },
            "dados": {
                "nome": "Aquisição e Preparação de Dados",
                "duracao_dias": 21,
                "dependencias": ["planejamento"],
                "atividades": [
                    {
                        "nome": "Identificação de fontes de dados",
                        "duracao_dias": 3,
                        "responsaveis": ["Data Engineer", "Data Scientist"],
                        "entregaveis": ["Mapeamento de fontes de dados"]
                    },
                    {
                        "nome": "Extração de dados",
                        "duracao_dias": 5,
                        "responsaveis": ["Data Engineer"],
                        "entregaveis": ["Dados brutos extraídos"]
                    },
                    {
                        "nome": "Limpeza e pré-processamento",
                        "duracao_dias": 7,
                        "responsaveis": ["Data Engineer", "Data Scientist"],
                        "entregaveis": ["Dados limpos e pré-processados"]
                    },
                    {
                        "nome": "Análise exploratória",
                        "duracao_dias": 5,
                        "responsaveis": ["Data Scientist"],
                        "entregaveis": ["Relatório de análise exploratória"]
                    },
                    {
                        "nome": "Engenharia de features",
                        "duracao_dias": 7,
                        "responsaveis": ["Data Scientist"],
                        "entregaveis": ["Conjunto de features"]
                    }
                ]
            },
            "modelagem": {
                "nome": "Desenvolvimento e Treinamento de Modelos",
                "duracao_dias": 28,
                "dependencias": ["dados"],
                "atividades": [
                    {
                        "nome": "Seleção de algoritmos",
                        "duracao_dias": 3,
                        "responsaveis": ["Data Scientist"],
                        "entregaveis": ["Documento de seleção de algoritmos"]
                    },
                    {
                        "nome": "Implementação de modelos base",
                        "duracao_dias": 7,
                        "responsaveis": ["Data Scientist", "ML Engineer"],
                        "entregaveis": ["Modelos base implementados"]
                    },
                    {
                        "nome": "Treinamento e validação inicial",
                        "duracao_dias": 5,
                        "responsaveis": ["Data Scientist"],
                        "entregaveis": ["Modelos treinados e métricas iniciais"]
                    },
                    {
                        "nome": "Otimização de hiperparâmetros",
                        "duracao_dias": 7,
                        "responsaveis": ["Data Scientist", "ML Engineer"],
                        "entregaveis": ["Modelos otimizados"]
                    },
                    {
                        "nome": "Implementação de ensemble",
                        "duracao_dias": 5,
                        "responsaveis": ["Data Scientist", "ML Engineer"],
                        "entregaveis": ["Modelo ensemble implementado"]
                    },
                    {
                        "nome": "Avaliação final de modelos",
                        "duracao_dias": 3,
                        "responsaveis": ["Data Scientist"],
                        "entregaveis": ["Relatório de avaliação de modelos"]
                    }
                ]
            },
            "infraestrutura": {
                "nome": "Configuração de Infraestrutura",
                "duracao_dias": 21,
                "dependencias": ["planejamento"],
                "atividades": [
                    {
                        "nome": "Configuração de ambiente de desenvolvimento",
                        "duracao_dias": 3,
                        "responsaveis": ["DevOps Engineer"],
                        "entregaveis": ["Ambiente de desenvolvimento configurado"]
                    },
                    {
                        "nome": "Configuração de ambiente de treinamento",
                        "duracao_dias": 5,
                        "responsaveis": ["DevOps Engineer", "ML Engineer"],
                        "entregaveis": ["Ambiente de treinamento configurado"]
                    },
                    {
                        "nome": "Implementação de pipeline de dados",
                        "duracao_dias": 7,
                        "responsaveis": ["Data Engineer", "DevOps Engineer"],
                        "entregaveis": ["Pipeline de dados implementado"]
                    },
                    {
                        "nome": "Configuração de cluster Kubernetes",
                        "duracao_dias": 5,
                        "responsaveis": ["DevOps Engineer"],
                        "entregaveis": ["Cluster Kubernetes configurado"]
                    },
                    {
                        "nome": "Configuração de monitoramento",
                        "duracao_dias": 3,
                        "responsaveis": ["DevOps Engineer"],
                        "entregaveis": ["Sistema de monitoramento configurado"]
                    }
                ]
            },
            "mlops": {
                "nome": "Implementação de MLOps",
                "duracao_dias": 21,
                "dependencias": ["infraestrutura"],
                "atividades": [
                    {
                        "nome": "Configuração de versionamento de modelos",
                        "duracao_dias": 3,
                        "responsaveis": ["ML Engineer"],
                        "entregaveis": ["Sistema de versionamento configurado"]
                    },
                    {
                        "nome": "Implementação de pipeline CI/CD",
                        "duracao_dias": 7,
                        "responsaveis": ["DevOps Engineer", "ML Engineer"],
                        "entregaveis": ["Pipeline CI/CD implementado"]
                    },
                    {
                        "nome": "Configuração de testes automatizados",
                        "duracao_dias": 5,
                        "responsaveis": ["ML Engineer", "QA Engineer"],
                        "entregaveis": ["Testes automatizados configurados"]
                    },
                    {
                        "nome": "Implementação de monitoramento de modelos",
                        "duracao_dias": 5,
                        "responsaveis": ["ML Engineer", "DevOps Engineer"],
                        "entregaveis": ["Sistema de monitoramento de modelos implementado"]
                    },
                    {
                        "nome": "Configuração de retreinamento automático",
                        "duracao_dias": 3,
                        "responsaveis": ["ML Engineer"],
                        "entregaveis": ["Sistema de retreinamento automático configurado"]
                    }
                ]
            },
            "implantacao": {
                "nome": "Implantação e Validação",
                "duracao_dias": 14,
                "dependencias": ["modelagem", "mlops"],
                "atividades": [
                    {
                        "nome": "Empacotamento de modelos",
                        "duracao_dias": 2,
                        "responsaveis": ["ML Engineer"],
                        "entregaveis": ["Modelos empacotados"]
                    },
                    {
                        "nome": "Implantação em ambiente de homologação",
                        "duracao_dias": 3,
                        "responsaveis": ["ML Engineer", "DevOps Engineer"],
                        "entregaveis": ["Modelos implantados em homologação"]
                    },
                    {
                        "nome": "Testes de integração",
                        "duracao_dias": 5,
                        "responsaveis": ["QA Engineer"],
                        "entregaveis": ["Relatório de testes de integração"]
                    },
                    {
                        "nome": "Implantação em produção",
                        "duracao_dias": 2,
                        "responsaveis": ["ML Engineer", "DevOps Engineer"],
                        "entregaveis": ["Modelos implantados em produção"]
                    },
                    {
                        "nome": "Validação em produção",
                        "duracao_dias": 5,
                        "responsaveis": ["QA Engineer", "Product Owner"],
                        "entregaveis": ["Relatório de validação em produção"]
                    }
                ]
            },
            "monitoramento": {
                "nome": "Monitoramento e Melhoria Contínua",
                "duracao_dias": 30,
                "dependencias": ["implantacao"],
                "atividades": [
                    {
                        "nome": "Configuração de dashboards",
                        "duracao_dias": 5,
                        "responsaveis": ["ML Engineer", "Data Scientist"],
                        "entregaveis": ["Dashboards de monitoramento"]
                    },
                    {
                        "nome": "Monitoramento de performance",
                        "duracao_dias": 30,
                        "responsaveis": ["ML Engineer", "Data Scientist"],
                        "entregaveis": ["Relatórios de performance"]
                    },
                    {
                        "nome": "Detecção e análise de drift",
                        "duracao_dias": 30,
                        "responsaveis": ["Data Scientist"],
                        "entregaveis": ["Relatórios de drift"]
                    },
                    {
                        "nome": "Retreinamento de modelos",
                        "duracao_dias": 7,
                        "responsaveis": ["Data Scientist", "ML Engineer"],
                        "entregaveis": ["Modelos retreinados"]
                    },
                    {
                        "nome": "Documentação de lições aprendidas",
                        "duracao_dias": 5,
                        "responsaveis": ["Product Owner", "Data Scientist", "ML Engineer"],
                        "entregaveis": ["Documento de lições aprendidas"]
                    }
                ]
            }
        }
        
        # Calcular datas de início e fim para cada fase
        self.calcular_datas()
        
        # Definir marcos importantes
        self.marcos = self.gerar_marcos()
    
    def calcular_datas(self) -> None:
        """Calcula datas de início e fim para cada fase e atividade"""
        # Inicializar dicionário de datas de fim das fases
        datas_fim = {}
        
        # Para cada fase
        for fase_id, fase in self.fases.items():
            # Calcular data de início da fase
            if not fase["dependencias"]:
                # Se não tem dependências, começa na data de início do projeto
                data_inicio_fase = self.data_inicio
            else:
                # Se tem dependências, começa após a última dependência terminar
                datas_fim_deps = [datas_fim[dep] for dep in fase["dependencias"]]
                data_inicio_fase = max(datas_fim_deps) + timedelta(days=1)
            
            # Calcular data de fim da fase
            data_fim_fase = data_inicio_fase + timedelta(days=fase["duracao_dias"] - 1)
            
            # Armazenar datas na fase
            fase["data_inicio"] = data_inicio_fase
            fase["data_fim"] = data_fim_fase
            
            # Armazenar data de fim para cálculo de dependências
            datas_fim[fase_id] = data_fim_fase
            
            # Calcular datas para cada atividade
            data_atual = data_inicio_fase
            for atividade in fase["atividades"]:
                atividade["data_inicio"] = data_atual
                atividade["data_fim"] = data_atual + timedelta(days=atividade["duracao_dias"] - 1)
                data_atual = atividade["data_fim"] + timedelta(days=1)
    
    def gerar_marcos(self) -> List[Dict[str, Any]]:
        """
        Gera marcos importantes do projeto
        
        Returns:
            List[Dict[str, Any]]: Lista de marcos
        """
        marcos = []
        
        # Marco de início do projeto
        marcos.append({
            "nome": "Início do Projeto",
            "data": self.data_inicio,
            "descricao": "Kickoff do projeto",
            "responsaveis": ["Product Owner", "Data Scientist", "ML Engineer"]
        })
        
        # Marcos de fim de cada fase
        for fase_id, fase in self.fases.items():
            marcos.append({
                "nome": f"Conclusão da fase de {fase['nome']}",
                "data": fase["data_fim"],
                "descricao": f"Todos os entregáveis da fase de {fase['nome']} concluídos",
                "responsaveis": self.obter_responsaveis_fase(fase_id)
            })
        
        # Marco de fim do projeto
        data_fim_projeto = max(fase["data_fim"] for fase in self.fases.values())
        marcos.append({
            "nome": "Conclusão do Projeto",
            "data": data_fim_projeto,
            "descricao": "Todos os entregáveis do projeto concluídos",
            "responsaveis": ["Product Owner", "Data Scientist", "ML Engineer", "DevOps Engineer"]
        })
        
        return marcos
    
    def obter_responsaveis_fase(self, fase_id: str) -> List[str]:
        """
        Obtém lista de responsáveis únicos por uma fase
        
        Args:
            fase_id: ID da fase
            
        Returns:
            List[str]: Lista de responsáveis
        """
        responsaveis = set()
        for atividade in self.fases[fase_id]["atividades"]:
            for responsavel in atividade["responsaveis"]:
                responsaveis.add(responsavel)
        
        return list(responsaveis)
    
    def obter_duracao_total(self) -> int:
        """
        Calcula duração total do projeto em dias
        
        Returns:
            int: Duração total em dias
        """
        data_fim_projeto = max(fase["data_fim"] for fase in self.fases.values())
        return (data_fim_projeto - self.data_inicio).days + 1
    
    def obter_caminho_critico(self) -> List[str]:
        """
        Identifica o caminho crítico do projeto
        
        Returns:
            List[str]: Lista de fases no caminho crítico
        """
        # Construir grafo de dependências
        grafo = {fase_id: fase["dependencias"] for fase_id, fase in self.fases.items()}
        
        # Identificar fases finais (sem sucessores)
        fases_finais = []
        for fase_id in self.fases:
            is_final = True
            for deps in grafo.values():
                if fase_id in deps:
                    is_final = False
                    break
            if is_final:
                fases_finais.append(fase_id)
        
        # Encontrar o caminho mais longo até cada fase final
        caminhos = {}
        for fase_final in fases_finais:
            caminho = self._encontrar_caminho_mais_longo(fase_final, grafo)
            duracao = sum(self.fases[fase]["duracao_dias"] for fase in caminho)
            caminhos[fase_final] = (caminho, duracao)
        
        # Retornar o caminho mais longo
        caminho_critico = max(caminhos.values(), key=lambda x: x[1])[0]
        return caminho_critico
    
    def _encontrar_caminho_mais_longo(self, fase: str, grafo: Dict[str, List[str]]) -> List[str]:
        """
        Encontra o caminho mais longo até uma fase
        
        Args:
            fase: ID da fase
            grafo: Grafo de dependências
            
        Returns:
            List[str]: Caminho mais longo
        """
        if not grafo[fase]:
            return [fase]
        
        caminhos = []
        for dep in grafo[fase]:
            caminho = self._encontrar_caminho_mais_longo(dep, grafo)
            caminhos.append(caminho)
        
        # Escolher o caminho mais longo
        caminho_mais_longo = max(caminhos, key=lambda x: sum(self.fases[f]["duracao_dias"] for f in x))
        return caminho_mais_longo + [fase]
    
    def exportar_cronograma(self, caminho: str) -> None:
        """
        Exporta cronograma para arquivo JSON
        
        Args:
            caminho: Caminho do arquivo
        """
        # Converter datas para string
        cronograma_json = {
            "data_inicio": self.data_inicio.isoformat(),
            "duracao_total_dias": self.obter_duracao_total(),
            "caminho_critico": self.obter_caminho_critico(),
            "fases": {}
        }
        
        for fase_id, fase in self.fases.items():
            fase_json = {
                "nome": fase["nome"],
                "duracao_dias": fase["duracao_dias"],
                "dependencias": fase["dependencias"],
                "data_inicio": fase["data_inicio"].isoformat(),
                "data_fim": fase["data_fim"].isoformat(),
                "atividades": []
            }
            
            for atividade in fase["atividades"]:
                atividade_json = {
                    "nome": atividade["nome"],
                    "duracao_dias": atividade["duracao_dias"],
                    "responsaveis": atividade["responsaveis"],
                    "entregaveis": atividade["entregaveis"],
                    "data_inicio": atividade["data_inicio"].isoformat(),
                    "data_fim": atividade["data_fim"].isoformat()
                }
                fase_json["atividades"].append(atividade_json)
            
            cronograma_json["fases"][fase_id] = fase_json
        
        # Adicionar marcos
        cronograma_json["marcos"] = []
        for marco in self.marcos:
            marco_json = {
                "nome": marco["nome"],
                "data": marco["data"].isoformat(),
                "descricao": marco["descricao"],
                "responsaveis": marco["responsaveis"]
            }
            cronograma_json["marcos"].append(marco_json)
        
        with open(caminho, 'w') as f:
            json.dump(cronograma_json, f, indent=2)
    
    def gerar_relatorio_cronograma(self) -> str:
        """
        Gera relatório textual do cronograma
        
        Returns:
            str: Relatório do cronograma
        """
        relatorio = []
        
        # Cabeçalho
        relatorio.append("# CRONOGRAMA DETALHADO DO PROJETO")
        relatorio.append("")
        relatorio.append(f"Data de início: {self.data_inicio.strftime('%d/%m/%Y')}")
        data_fim = max(fase['data_fim'] for fase in self.fases.values())
        relatorio.append(f"Data de término: {data_fim.strftime('%d/%m/%Y')}")
        relatorio.append(f"Duração total: {self.obter_duracao_total()} dias")
        relatorio.append("")
        
        # Caminho crítico
        caminho_critico = self.obter_caminho_critico()
        relatorio.append("## Caminho Crítico")
        relatorio.append(" -> ".join([self.fases[fase]["nome"] for fase in caminho_critico]))
        relatorio.append("")
        
        # Fases
        relatorio.append("## Fases do Projeto")
        for fase_id, fase in self.fases.items():
            relatorio.append(f"### {fase['nome']}")
            relatorio.append(f"Duração: {fase['duracao_dias']} dias")
            relatorio.append(f"Período: {fase['data_inicio'].strftime('%d/%m/%Y')} a {fase['data_fim'].strftime('%d/%m/%Y')}")
            if fase["dependencias"]:
                deps = [self.fases[dep]["nome"] for dep in fase["dependencias"]]
                relatorio.append(f"Dependências: {', '.join(deps)}")
            relatorio.append("")
            
            relatorio.append("#### Atividades:")
            for atividade in fase["atividades"]:
                relatorio.append(f"- **{atividade['nome']}**")
                relatorio.append(f"  - Duração: {atividade['duracao_dias']} dias")
                relatorio.append(f"  - Período: {atividade['data_inicio'].strftime('%d/%m/%Y')} a {atividade['data_fim'].strftime('%d/%m/%Y')}")
                relatorio.append(f"  - Responsáveis: {', '.join(atividade['responsaveis'])}")
                relatorio.append(f"  - Entregáveis: {', '.join(atividade['entregaveis'])}")
                relatorio.append("")
        
        # Marcos
        relatorio.append("## Marcos Importantes")
        for marco in self.marcos:
            relatorio.append(f"- **{marco['nome']}**: {marco['data'].strftime('%d/%m/%Y')}")
            relatorio.append(f"  - {marco['descricao']}")
            relatorio.append(f"  - Responsáveis: {', '.join(marco['responsaveis'])}")
            relatorio.append("")
        
        return "\n".join(relatorio)


# Exemplo de uso
if __name__ == "__main__":
    # Criar cronograma com data de início específica
    data_inicio = datetime(2023, 9, 1).date()
    cronograma = CronogramaDetalhado(data_inicio)
    
    # Exportar cronograma
    cronograma.exportar_cronograma("cronograma_detalhado.json")
    
    # Gerar relatório
    relatorio = cronograma.gerar_relatorio_cronograma()
    with open("cronograma_detalhado.md", 'w') as f:
        f.write(relatorio)
    
    # Imprimir informações básicas
    print(f"Cronograma gerado com sucesso!")
    print(f"Data de início: {cronograma.data_inicio.strftime('%d/%m/%Y')}")
    data_fim = max(fase['data_fim'] for fase in cronograma.fases.values())
    print(f"Data de término: {data_fim.strftime('%d/%m/%Y')}")
    print(f"Duração total: {cronograma.obter_duracao_total()} dias")
    print(f"Caminho crítico: {' -> '.join([cronograma.fases[fase]['nome'] for fase in cronograma.obter_caminho_critico()])}")
    print(f"Número de fases: {len(cronograma.fases)}")
    print(f"Número de atividades: {sum(len(fase['atividades']) for fase in cronograma.fases.values())}")
    print(f"Número de marcos: {len(cronograma.marcos)}")