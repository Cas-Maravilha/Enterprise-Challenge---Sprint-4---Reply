import os
import joblib
import json
import datetime
import numpy as np
import pandas as pd
from pathlib import Path

class EstrategiaEscalabilidade:
    """
    Implementa estratégias de escalabilidade para modelos de IA
    """
    
    def __init__(self, diretorio_base="modelos"):
        """
        Inicializa a estratégia de escalabilidade
        
        Args:
            diretorio_base: Diretório base para armazenar modelos e metadados
        """
        self.diretorio_base = Path(diretorio_base)
        self.diretorio_base.mkdir(exist_ok=True)
        
        # Subdiretórios
        self.dir_modelos = self.diretorio_base / "versoes"
        self.dir_modelos.mkdir(exist_ok=True)
        
        self.dir_metricas = self.diretorio_base / "metricas"
        self.dir_metricas.mkdir(exist_ok=True)
        
        self.dir_config = self.diretorio_base / "config"
        self.dir_config.mkdir(exist_ok=True)
        
        # Arquivo de registro de versões
        self.registro_versoes = self.diretorio_base / "registro_versoes.json"
        if not self.registro_versoes.exists():
            with open(self.registro_versoes, 'w') as f:
                json.dump({"versoes": [], "atual": None}, f)
    
    def salvar_modelo(self, modelo, nome, metricas=None, parametros=None):
        """
        Salva uma nova versão do modelo
        
        Args:
            modelo: Objeto do modelo treinado
            nome: Nome do modelo
            metricas: Dicionário com métricas de desempenho
            parametros: Dicionário com parâmetros do modelo
            
        Returns:
            str: ID da versão salva
        """
        # Gerar ID da versão (timestamp)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        versao_id = f"{nome}_{timestamp}"
        
        # Criar diretório para esta versão
        dir_versao = self.dir_modelos / versao_id
        dir_versao.mkdir(exist_ok=True)
        
        # Salvar modelo
        caminho_modelo = dir_versao / "modelo.joblib"
        joblib.dump(modelo, caminho_modelo)
        
        # Salvar métricas
        if metricas:
            caminho_metricas = dir_versao / "metricas.json"
            with open(caminho_metricas, 'w') as f:
                json.dump(metricas, f, indent=2)
        
        # Salvar parâmetros
        if parametros:
            caminho_params = dir_versao / "parametros.json"
            with open(caminho_params, 'w') as f:
                json.dump(parametros, f, indent=2)
        
        # Atualizar registro de versões
        with open(self.registro_versoes, 'r') as f:
            registro = json.load(f)
        
        registro["versoes"].append({
            "id": versao_id,
            "nome": nome,
            "timestamp": timestamp,
            "metricas": metricas
        })
        
        # Definir como versão atual se for a primeira
        if registro["atual"] is None:
            registro["atual"] = versao_id
        
        with open(self.registro_versoes, 'w') as f:
            json.dump(registro, f, indent=2)
        
        return versao_id
    
    def carregar_modelo(self, versao_id=None):
        """
        Carrega um modelo salvo
        
        Args:
            versao_id: ID da versão a carregar (se None, carrega a versão atual)
            
        Returns:
            object: Modelo carregado
        """
        if versao_id is None:
            # Carregar versão atual
            with open(self.registro_versoes, 'r') as f:
                registro = json.load(f)
            
            if registro["atual"] is None:
                raise ValueError("Nenhum modelo atual definido")
            
            versao_id = registro["atual"]
        
        caminho_modelo = self.dir_modelos / versao_id / "modelo.joblib"
        if not caminho_modelo.exists():
            raise FileNotFoundError(f"Modelo não encontrado: {caminho_modelo}")
        
        return joblib.load(caminho_modelo)
    
    def definir_modelo_atual(self, versao_id):
        """
        Define qual versão do modelo é a atual
        
        Args:
            versao_id: ID da versão a definir como atual
        """
        # Verificar se a versão existe
        dir_versao = self.dir_modelos / versao_id
        if not dir_versao.exists():
            raise ValueError(f"Versão não encontrada: {versao_id}")
        
        # Atualizar registro
        with open(self.registro_versoes, 'r') as f:
            registro = json.load(f)
        
        registro["atual"] = versao_id
        
        with open(self.registro_versoes, 'w') as f:
            json.dump(registro, f, indent=2)
    
    def listar_versoes(self):
        """
        Lista todas as versões disponíveis
        
        Returns:
            list: Lista de versões
        """
        with open(self.registro_versoes, 'r') as f:
            registro = json.load(f)
        
        return registro["versoes"]
    
    def comparar_versoes(self, versao_id1, versao_id2):
        """
        Compara duas versões de modelos
        
        Args:
            versao_id1: ID da primeira versão
            versao_id2: ID da segunda versão
            
        Returns:
            dict: Comparação de métricas
        """
        # Carregar métricas das versões
        metricas1 = self._carregar_metricas(versao_id1)
        metricas2 = self._carregar_metricas(versao_id2)
        
        # Comparar métricas comuns
        comparacao = {}
        for metrica in set(metricas1.keys()) & set(metricas2.keys()):
            if isinstance(metricas1[metrica], (int, float)) and isinstance(metricas2[metrica], (int, float)):
                diff = metricas2[metrica] - metricas1[metrica]
                diff_pct = diff / metricas1[metrica] * 100 if metricas1[metrica] != 0 else float('inf')
                
                comparacao[metrica] = {
                    "versao1": metricas1[metrica],
                    "versao2": metricas2[metrica],
                    "diferenca": diff,
                    "diferenca_percentual": diff_pct
                }
        
        return comparacao
    
    def _carregar_metricas(self, versao_id):
        """
        Carrega métricas de uma versão
        
        Args:
            versao_id: ID da versão
            
        Returns:
            dict: Métricas da versão
        """
        caminho_metricas = self.dir_modelos / versao_id / "metricas.json"
        if not caminho_metricas.exists():
            return {}
        
        with open(caminho_metricas, 'r') as f:
            return json.load(f)
    
    def salvar_configuracao(self, config, nome):
        """
        Salva uma configuração do sistema
        
        Args:
            config: Dicionário com configurações
            nome: Nome da configuração
        """
        caminho_config = self.dir_config / f"{nome}.json"
        with open(caminho_config, 'w') as f:
            json.dump(config, f, indent=2)
    
    def carregar_configuracao(self, nome):
        """
        Carrega uma configuração do sistema
        
        Args:
            nome: Nome da configuração
            
        Returns:
            dict: Configuração carregada
        """
        caminho_config = self.dir_config / f"{nome}.json"
        if not caminho_config.exists():
            raise FileNotFoundError(f"Configuração não encontrada: {nome}")
        
        with open(caminho_config, 'r') as f:
            return json.load(f)


# Exemplo de uso
if __name__ == "__main__":
    from sklearn.ensemble import RandomForestClassifier
    
    # Inicializar estratégia de escalabilidade
    estrategia = EstrategiaEscalabilidade(diretorio_base="modelos_teste")
    
    # Treinar modelo de exemplo
    X = np.random.rand(100, 5)
    y = np.random.randint(0, 2, 100)
    
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X, y)
    
    # Métricas de exemplo
    metricas = {
        "acuracia": 0.85,
        "precisao": 0.83,
        "recall": 0.81,
        "f1": 0.82
    }
    
    # Parâmetros do modelo
    parametros = {
        "n_estimators": 100,
        "max_depth": None,
        "random_state": 42
    }
    
    # Salvar modelo
    versao_id = estrategia.salvar_modelo(
        modelo, 
        "random_forest", 
        metricas=metricas,
        parametros=parametros
    )
    
    print(f"Modelo salvo com ID: {versao_id}")
    
    # Listar versões
    versoes = estrategia.listar_versoes()
    print(f"Versões disponíveis: {len(versoes)}")
    
    # Carregar modelo
    modelo_carregado = estrategia.carregar_modelo()
    
    # Salvar configuração
    config = {
        "threshold": 0.5,
        "features": ["feature1", "feature2", "feature3"],
        "preprocessamento": {
            "normalizar": True,
            "remover_outliers": False
        }
    }
    
    estrategia.salvar_configuracao(config, "config_producao")