#!/usr/bin/env python3
"""
Sistema Completo de ML - Treino e Inferência
Sistema IoT Monitoring Sprint 3 - Detecção de Anomalias

Autor: Enterprise Challenge - Sprint 3 - Reply
Data: 2024
"""

import os
import sys
import json
import time
import logging
import threading
import queue
import joblib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, 
    roc_auc_score, classification_report, confusion_matrix
)
import warnings
warnings.filterwarnings('ignore')

# Importar módulos do projeto
from persistencia_banco_relacional import (
    PersistenciaBancoRelacional, 
    ConfiguracaoBanco
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("SistemaML")

@dataclass
class ConfiguracaoML:
    """Configuração do sistema de ML"""
    modelo_path: str = "modelos/"
    retreinar_intervalo_horas: int = 24
    threshold_anomalia: float = 0.5
    min_amostras_treino: int = 1000
    features_principais: List[str] = None
    random_state: int = 42
    
    def __post_init__(self):
        if self.features_principais is None:
            self.features_principais = [
                'temperature', 'humidity', 'pressure', 'vibration_mag',
                'level', 'luminosity', 'movement', 'temp_humidity_ratio',
                'pressure_vibration', 'level_luminosity'
            ]

class SistemaMLCompleto:
    """
    Sistema completo de Machine Learning para detecção de anomalias IoT
    """
    
    def __init__(self, config_banco: ConfiguracaoBanco, config_ml: ConfiguracaoML):
        self.config_banco = config_banco
        self.config_ml = config_ml
        
        # Inicializa persistência
        self.persistencia = PersistenciaBancoRelacional(config_banco)
        
        # Modelos ML
        self.modelo_rf = None
        self.modelo_iso = None
        self.scaler = StandardScaler()
        self.feature_columns = config_ml.features_principais
        
        # Estado do sistema
        self.modelo_treinado = False
        self.ultimo_treino = None
        self.estatisticas_modelo = {}
        
        # Threads
        self.executando = False
        self.thread_treino = None
        self.thread_inferencia = None
        
        # Fila de inferência
        self.fila_inferencia = queue.Queue(maxsize=1000)
        
        # Estatísticas
        self.estatisticas = {
            'inferencias_realizadas': 0,
            'anomalias_detectadas': 0,
            'falsos_positivos': 0,
            'falsos_negativos': 0,
            'inicio_execucao': datetime.now()
        }
        
        # Cria diretório de modelos
        os.makedirs(self.config_ml.modelo_path, exist_ok=True)
    
    def iniciar(self):
        """Inicia o sistema de ML"""
        try:
            logger.info("Iniciando sistema de ML completo")
            
            # Carrega modelo existente ou treina novo
            if not self._carregar_modelo_existente():
                logger.info("Modelo não encontrado, iniciando treinamento...")
                self._treinar_modelo_inicial()
            
            # Inicia threads
            self.executando = True
            self.thread_treino = threading.Thread(target=self._thread_treino_automatico, daemon=True)
            self.thread_treino.start()
            
            self.thread_inferencia = threading.Thread(target=self._thread_inferencia, daemon=True)
            self.thread_inferencia.start()
            
            logger.info("Sistema de ML iniciado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao iniciar sistema ML: {e}")
            raise
    
    def parar(self):
        """Para o sistema de ML"""
        try:
            logger.info("Parando sistema de ML")
            
            self.executando = False
            
            # Aguarda threads
            if self.thread_treino and self.thread_treino.is_alive():
                self.thread_treino.join(timeout=5)
            
            if self.thread_inferencia and self.thread_inferencia.is_alive():
                self.thread_inferencia.join(timeout=5)
            
            logger.info("Sistema de ML parado")
            
        except Exception as e:
            logger.error(f"Erro ao parar sistema ML: {e}")
    
    def _carregar_modelo_existente(self) -> bool:
        """Carrega modelo existente do disco"""
        try:
            modelo_path = os.path.join(self.config_ml.modelo_path, "modelo_ml_completo.pkl")
            
            if os.path.exists(modelo_path):
                modelo_data = joblib.load(modelo_path)
                
                self.modelo_rf = modelo_data['modelo_rf']
                self.modelo_iso = modelo_data['modelo_iso']
                self.scaler = modelo_data['scaler']
                self.feature_columns = modelo_data['feature_columns']
                self.estatisticas_modelo = modelo_data.get('estatisticas', {})
                self.ultimo_treino = modelo_data.get('ultimo_treino')
                
                self.modelo_treinado = True
                logger.info("Modelo existente carregado com sucesso")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {e}")
            return False
    
    def _salvar_modelo(self):
        """Salva modelo treinado no disco"""
        try:
            modelo_data = {
                'modelo_rf': self.modelo_rf,
                'modelo_iso': self.modelo_iso,
                'scaler': self.scaler,
                'feature_columns': self.feature_columns,
                'estatisticas': self.estatisticas_modelo,
                'ultimo_treino': self.ultimo_treino,
                'versao': '1.0'
            }
            
            modelo_path = os.path.join(self.config_ml.modelo_path, "modelo_ml_completo.pkl")
            joblib.dump(modelo_data, modelo_path)
            
            logger.info(f"Modelo salvo: {modelo_path}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar modelo: {e}")
    
    def _treinar_modelo_inicial(self):
        """Treina modelo inicial com dados sintéticos"""
        try:
            logger.info("Treinando modelo inicial com dados sintéticos")
            
            # Gera dados sintéticos para treinamento inicial
            df_treino = self._gerar_dados_sinteticos_treino()
            
            # Treina modelo
            self._treinar_modelo_com_dados(df_treino)
            
        except Exception as e:
            logger.error(f"Erro no treinamento inicial: {e}")
            raise
    
    def _gerar_dados_sinteticos_treino(self) -> pd.DataFrame:
        """Gera dados sintéticos para treinamento inicial"""
        try:
            np.random.seed(self.config_ml.random_state)
            n_samples = 2000
            
            # Dados normais (70%)
            n_normais = int(n_samples * 0.7)
            dados_normais = {
                'temperature': np.random.normal(25, 5, n_normais),
                'humidity': np.random.normal(60, 15, n_normais),
                'pressure': np.random.normal(1.013, 0.01, n_normais),
                'vibration_mag': np.random.exponential(0.1, n_normais),
                'level': np.random.normal(100, 20, n_normais),
                'luminosity': np.random.normal(500, 100, n_normais),
                'movement': np.random.choice([0, 1], n_normais, p=[0.8, 0.2]),
                'anomaly': 0
            }
            
            # Dados de anomalia (30%)
            n_anomalias = n_samples - n_normais
            dados_anomalias = {
                'temperature': np.random.normal(35, 10, n_anomalias),
                'humidity': np.random.normal(80, 20, n_anomalias),
                'pressure': np.random.normal(1.025, 0.02, n_anomalias),
                'vibration_mag': np.random.exponential(0.5, n_anomalias),
                'level': np.random.normal(150, 30, n_anomalias),
                'luminosity': np.random.normal(800, 200, n_anomalias),
                'movement': np.random.choice([0, 1], n_anomalias, p=[0.3, 0.7]),
                'anomaly': 1
            }
            
            # Combina dados
            dados_combinados = {}
            for col in dados_normais.keys():
                dados_combinados[col] = np.concatenate([
                    dados_normais[col], dados_anomalias[col]
                ])
            
            df = pd.DataFrame(dados_combinados)
            
            # Adiciona features derivadas
            df['temp_humidity_ratio'] = df['temperature'] / (df['humidity'] + 1)
            df['pressure_vibration'] = df['pressure'] * df['vibration_mag']
            df['level_luminosity'] = df['level'] / (df['luminosity'] + 1)
            
            # Embaralha dados
            df = df.sample(frac=1, random_state=self.config_ml.random_state).reset_index(drop=True)
            
            logger.info(f"Dados sintéticos gerados: {len(df)} amostras")
            return df
            
        except Exception as e:
            logger.error(f"Erro ao gerar dados sintéticos: {e}")
            raise
    
    def _treinar_modelo_com_dados(self, df: pd.DataFrame):
        """Treina modelo com dados fornecidos"""
        try:
            logger.info("Iniciando treinamento do modelo")
            
            # Prepara dados
            X, y = self._preparar_dados_treino(df)
            
            # Divide dados
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=self.config_ml.random_state, stratify=y
            )
            
            # Normaliza dados
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Treina Random Forest
            self.modelo_rf = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=self.config_ml.random_state,
                class_weight='balanced'
            )
            
            self.modelo_rf.fit(X_train_scaled, y_train)
            
            # Treina Isolation Forest
            self.modelo_iso = IsolationForest(
                contamination=0.1,
                random_state=self.config_ml.random_state
            )
            self.modelo_iso.fit(X_train_scaled)
            
            # Avalia modelo
            self._avaliar_modelo(X_test_scaled, y_test)
            
            # Atualiza estado
            self.modelo_treinado = True
            self.ultimo_treino = datetime.now()
            
            # Salva modelo
            self._salvar_modelo()
            
            logger.info("Modelo treinado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro no treinamento: {e}")
            raise
    
    def _preparar_dados_treino(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Prepara dados para treinamento"""
        try:
            # Seleciona features
            X = df[self.feature_columns].copy()
            y = df['anomaly'].values
            
            # Trata valores nulos e infinitos
            X = X.replace([np.inf, -np.inf], np.nan)
            X = X.fillna(X.median())
            
            return X.values, y
            
        except Exception as e:
            logger.error(f"Erro ao preparar dados: {e}")
            raise
    
    def _avaliar_modelo(self, X_test: np.ndarray, y_test: np.ndarray):
        """Avalia performance do modelo"""
        try:
            # Predições
            y_pred_rf = self.modelo_rf.predict(X_test)
            y_pred_proba_rf = self.modelo_rf.predict_proba(X_test)[:, 1]
            
            # Isolation Forest
            iso_scores = self.modelo_iso.decision_function(X_test)
            y_pred_iso = (iso_scores < 0).astype(int)
            
            # Métricas Random Forest
            self.estatisticas_modelo = {
                'accuracy': accuracy_score(y_test, y_pred_rf),
                'precision': precision_score(y_test, y_pred_rf),
                'recall': recall_score(y_test, y_pred_rf),
                'f1': f1_score(y_test, y_pred_rf),
                'auc': roc_auc_score(y_test, y_pred_proba_rf),
                'iso_accuracy': accuracy_score(y_test, y_pred_iso),
                'n_amostras_treino': len(X_test),
                'n_features': len(self.feature_columns)
            }
            
            logger.info("Métricas do modelo:")
            logger.info(f"  Accuracy: {self.estatisticas_modelo['accuracy']:.4f}")
            logger.info(f"  Precision: {self.estatisticas_modelo['precision']:.4f}")
            logger.info(f"  Recall: {self.estatisticas_modelo['recall']:.4f}")
            logger.info(f"  F1-Score: {self.estatisticas_modelo['f1']:.4f}")
            logger.info(f"  AUC: {self.estatisticas_modelo['auc']:.4f}")
            
        except Exception as e:
            logger.error(f"Erro na avaliação: {e}")
    
    def _thread_treino_automatico(self):
        """Thread de treinamento automático"""
        logger.info("Thread de treinamento automático iniciada")
        
        while self.executando:
            try:
                # Verifica se precisa retreinar
                if self._precisa_retreinar():
                    logger.info("Iniciando retreinamento automático")
                    self._retreinar_com_dados_banco()
                
                # Aguarda próximo ciclo
                time.sleep(3600)  # Verifica a cada hora
                
            except Exception as e:
                logger.error(f"Erro no treinamento automático: {e}")
                time.sleep(300)  # Aguarda 5 minutos em caso de erro
        
        logger.info("Thread de treinamento automático finalizada")
    
    def _thread_inferencia(self):
        """Thread de inferência em tempo real"""
        logger.info("Thread de inferência iniciada")
        
        while self.executando:
            try:
                # Processa fila de inferência
                if not self.fila_inferencia.empty():
                    dados = self.fila_inferencia.get(timeout=1)
                    self._processar_inferencia(dados)
                    self.fila_inferencia.task_done()
                else:
                    time.sleep(0.1)
                    
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Erro na inferência: {e}")
                time.sleep(1)
        
        logger.info("Thread de inferência finalizada")
    
    def _precisa_retreinar(self) -> bool:
        """Verifica se precisa retreinar o modelo"""
        if not self.ultimo_treino:
            return True
        
        tempo_decorrido = datetime.now() - self.ultimo_treino
        return tempo_decorrido.total_seconds() > (self.config_ml.retreinar_intervalo_horas * 3600)
    
    def _retreinar_com_dados_banco(self):
        """Retreina modelo com dados do banco"""
        try:
            logger.info("Coletando dados do banco para retreinamento")
            
            # Obtém dados das últimas 24h
            data_inicio = datetime.now() - timedelta(hours=24)
            data_fim = datetime.now()
            
            # Busca leituras do banco
            leituras = self._obter_leituras_banco(data_inicio, data_fim)
            
            if len(leituras) < self.config_ml.min_amostras_treino:
                logger.warning(f"Dados insuficientes para retreinamento: {len(leituras)} < {self.config_ml.min_amostras_treino}")
                return
            
            # Converte para DataFrame
            df = pd.DataFrame(leituras)
            
            # Treina modelo
            self._treinar_modelo_com_dados(df)
            
            logger.info("Retreinamento concluído com sucesso")
            
        except Exception as e:
            logger.error(f"Erro no retreinamento: {e}")
    
    def _obter_leituras_banco(self, data_inicio: datetime, data_fim: datetime) -> List[Dict[str, Any]]:
        """Obtém leituras do banco para treinamento"""
        try:
            # Busca leituras com informações completas
            with self.persistencia.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor(dictionary=True)
                
                query = """
                SELECT 
                    ls.valor_numerico,
                    ls.anomalia_detectada,
                    ts.nome as tipo_sensor,
                    d.nome as dispositivo
                FROM leituras_sensores ls
                JOIN sensores s ON ls.id_sensor = s.id_sensor
                JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
                JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
                WHERE ls.timestamp_datetime BETWEEN %s AND %s
                AND ls.valor_numerico IS NOT NULL
                ORDER BY ls.timestamp_datetime
                """
                
                cursor.execute(query, (data_inicio, data_fim))
                leituras = cursor.fetchall()
                cursor.close()
                
                return leituras
                
        except Exception as e:
            logger.error(f"Erro ao obter leituras do banco: {e}")
            return []
    
    def inferir_anomalia(self, dados_sensor: Dict[str, Any]) -> Dict[str, Any]:
        """Faz inferência de anomalia em dados de sensor"""
        try:
            if not self.modelo_treinado:
                return {
                    'anomalia_detectada': False,
                    'probabilidade': 0.0,
                    'confianca': 'Baixa',
                    'erro': 'Modelo não treinado'
                }
            
            # Prepara dados
            dados_preparados = self._preparar_dados_inferencia(dados_sensor)
            
            if dados_preparados is None:
                return {
                    'anomalia_detectada': False,
                    'probabilidade': 0.0,
                    'confianca': 'Baixa',
                    'erro': 'Dados inválidos'
                }
            
            # Normaliza dados
            X_scaled = self.scaler.transform([dados_preparados])
            
            # Predições
            predicao_rf = self.modelo_rf.predict(X_scaled)[0]
            probabilidade_rf = self.modelo_rf.predict_proba(X_scaled)[0, 1]
            
            # Isolation Forest
            iso_score = self.modelo_iso.decision_function(X_scaled)[0]
            predicao_iso = 1 if iso_score < 0 else 0
            
            # Determina anomalia final
            anomalia_detectada = predicao_rf == 1 or predicao_iso == 1
            probabilidade_final = max(probabilidade_rf, 1 - (iso_score + 1) / 2)
            
            # Determina confiança
            if probabilidade_final > 0.8 or probabilidade_final < 0.2:
                confianca = 'Alta'
            elif probabilidade_final > 0.6 or probabilidade_final < 0.4:
                confianca = 'Média'
            else:
                confianca = 'Baixa'
            
            # Atualiza estatísticas
            self.estatisticas['inferencias_realizadas'] += 1
            if anomalia_detectada:
                self.estatisticas['anomalias_detectadas'] += 1
            
            resultado = {
                'anomalia_detectada': anomalia_detectada,
                'probabilidade': float(probabilidade_final),
                'confianca': confianca,
                'predicao_rf': int(predicao_rf),
                'probabilidade_rf': float(probabilidade_rf),
                'predicao_iso': int(predicao_iso),
                'iso_score': float(iso_score),
                'timestamp': datetime.now().isoformat()
            }
            
            return resultado
            
        except Exception as e:
            logger.error(f"Erro na inferência: {e}")
            return {
                'anomalia_detectada': False,
                'probabilidade': 0.0,
                'confianca': 'Baixa',
                'erro': str(e)
            }
    
    def _preparar_dados_inferencia(self, dados_sensor: Dict[str, Any]) -> Optional[List[float]]:
        """Prepara dados para inferência"""
        try:
            # Mapeia dados do sensor para features
            dados_preparados = {}
            
            # Mapeamento básico
            mapeamento = {
                'temperature': 'temperature',
                'humidity': 'humidity',
                'pressure': 'pressure',
                'vibration': 'vibration_mag',
                'level': 'level',
                'luminosity': 'luminosity',
                'movement': 'movement'
            }
            
            for feature_ml, campo_sensor in mapeamento.items():
                if campo_sensor in dados_sensor:
                    dados_preparados[feature_ml] = float(dados_sensor[campo_sensor])
                else:
                    # Valor padrão se não encontrado
                    dados_preparados[feature_ml] = 0.0
            
            # Calcula features derivadas
            dados_preparados['temp_humidity_ratio'] = (
                dados_preparados['temperature'] / (dados_preparados['humidity'] + 1)
            )
            dados_preparados['pressure_vibration'] = (
                dados_preparados['pressure'] * dados_preparados['vibration_mag']
            )
            dados_preparados['level_luminosity'] = (
                dados_preparados['level'] / (dados_preparados['luminosity'] + 1)
            )
            
            # Converte para lista na ordem correta
            valores = [dados_preparados[feature] for feature in self.feature_columns]
            
            # Verifica valores válidos
            if any(np.isnan(valores) or np.isinf(valores) for valores in valores):
                return None
            
            return valores
            
        except Exception as e:
            logger.error(f"Erro ao preparar dados: {e}")
            return None
    
    def _processar_inferencia(self, dados: Dict[str, Any]):
        """Processa inferência em lote"""
        try:
            resultado = self.inferir_anomalia(dados)
            
            # Atualiza dados no banco se necessário
            if 'id_leitura' in dados:
                self._atualizar_anomalia_banco(dados['id_leitura'], resultado)
            
            logger.debug(f"Inferência processada: {resultado['anomalia_detectada']}")
            
        except Exception as e:
            logger.error(f"Erro no processamento de inferência: {e}")
    
    def _atualizar_anomalia_banco(self, id_leitura: int, resultado: Dict[str, Any]):
        """Atualiza flag de anomalia no banco"""
        try:
            with self.persistencia.gerenciador.obter_conexao() as conexao:
                cursor = conexao.cursor()
                
                query = """
                UPDATE leituras_sensores 
                SET anomalia_detectada = %s, qualidade_dados = %s
                WHERE id_leitura = %s
                """
                
                qualidade = 'ruim' if resultado['anomalia_detectada'] else 'bom'
                
                cursor.execute(query, (
                    resultado['anomalia_detectada'],
                    qualidade,
                    id_leitura
                ))
                
                cursor.close()
                
        except Exception as e:
            logger.error(f"Erro ao atualizar anomalia no banco: {e}")
    
    def adicionar_inferencia_fila(self, dados: Dict[str, Any]):
        """Adiciona dados à fila de inferência"""
        try:
            if not self.fila_inferencia.full():
                self.fila_inferencia.put(dados)
            else:
                logger.warning("Fila de inferência cheia, descartando dados")
                
        except Exception as e:
            logger.error(f"Erro ao adicionar à fila: {e}")
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Obtém estatísticas do sistema ML"""
        try:
            tempo_execucao = datetime.now() - self.estatisticas['inicio_execucao']
            
            return {
                'modelo_treinado': self.modelo_treinado,
                'ultimo_treino': self.ultimo_treino.isoformat() if self.ultimo_treino else None,
                'inferencias_realizadas': self.estatisticas['inferencias_realizadas'],
                'anomalias_detectadas': self.estatisticas['anomalias_detectadas'],
                'taxa_anomalias': (
                    self.estatisticas['anomalias_detectadas'] / 
                    max(self.estatisticas['inferencias_realizadas'], 1)
                ),
                'tamanho_fila': self.fila_inferencia.qsize(),
                'tempo_execucao_segundos': tempo_execucao.total_seconds(),
                'estatisticas_modelo': self.estatisticas_modelo
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            return {}
    
    def forcar_retreinamento(self):
        """Força retreinamento do modelo"""
        try:
            logger.info("Forçando retreinamento do modelo")
            self._retreinar_com_dados_banco()
            
        except Exception as e:
            logger.error(f"Erro no retreinamento forçado: {e}")

# =====================================================
# EXEMPLO DE USO
# =====================================================

def exemplo_uso():
    """Exemplo de uso do sistema ML completo"""
    
    # Configurações
    config_banco = ConfiguracaoBanco(
        host="localhost",
        port=3306,
        database="iot_monitoring_db",
        username="root",
        password="password"
    )
    
    config_ml = ConfiguracaoML(
        modelo_path="modelos/",
        retreinar_intervalo_horas=24,
        threshold_anomalia=0.5
    )
    
    # Inicializa sistema
    sistema_ml = SistemaMLCompleto(config_banco, config_ml)
    
    try:
        # Inicia sistema
        sistema_ml.iniciar()
        
        # Exemplo de inferência
        dados_sensor = {
            'temperature': 25.5,
            'humidity': 60.0,
            'pressure': 1.013,
            'vibration': 0.1,
            'level': 100.0,
            'luminosity': 500.0,
            'movement': 0
        }
        
        resultado = sistema_ml.inferir_anomalia(dados_sensor)
        print(f"Resultado da inferência: {resultado}")
        
        # Mostra estatísticas
        stats = sistema_ml.obter_estatisticas()
        print(f"Estatísticas: {json.dumps(stats, indent=2, default=str)}")
        
        # Executa por 60 segundos
        time.sleep(60)
        
    except KeyboardInterrupt:
        print("Parando sistema...")
    finally:
        sistema_ml.parar()

if __name__ == "__main__":
    exemplo_uso()

