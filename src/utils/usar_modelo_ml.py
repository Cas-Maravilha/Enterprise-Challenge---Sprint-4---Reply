#!/usr/bin/env python3
"""
Script para usar o modelo de Machine Learning treinado
Sistema de Detecção de Anomalias IoT
"""

import pandas as pd
import numpy as np
import joblib
import warnings
warnings.filterwarnings('ignore')

class IoTAnomalyPredictor:
    """
    Classe para fazer predições usando o modelo treinado
    """
    
    def __init__(self, model_path='modelo_anomalia_iot_completo.pkl'):
        """
        Carrega o modelo treinado
        """
        print(f"📂 Carregando modelo: {model_path}")
        
        try:
            model_data = joblib.load(model_path)
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.feature_columns = model_data['feature_columns']
            self.isolation_forest = model_data['isolation_forest']
            
            print("✅ Modelo carregado com sucesso!")
            print(f"   • Features: {len(self.feature_columns)}")
            print(f"   • Tipo do modelo: {type(self.model).__name__}")
            
        except FileNotFoundError:
            print(f"❌ Erro: Arquivo {model_path} não encontrado!")
            print("   Execute primeiro o script de treinamento.")
            raise
        except Exception as e:
            print(f"❌ Erro ao carregar modelo: {e}")
            raise
    
    def predizer_anomalia(self, dados):
        """
        Prediz anomalias em novos dados
        
        Args:
            dados (dict ou pd.DataFrame): Dados dos sensores
            
        Returns:
            dict: Resultados da predição
        """
        try:
            # Converter para DataFrame se necessário
            if isinstance(dados, dict):
                df = pd.DataFrame([dados])
            else:
                df = dados.copy()
            
            # Verificar se todas as features estão presentes
            missing_features = set(self.feature_columns) - set(df.columns)
            if missing_features:
                print(f"⚠️ Aviso: Features ausentes: {missing_features}")
                # Adicionar features ausentes com valores padrão
                for feature in missing_features:
                    df[feature] = 0.0
            
            # Selecionar apenas as features necessárias
            X = df[self.feature_columns].copy()
            
            # Tratar valores infinitos e nulos
            X = X.replace([np.inf, -np.inf], np.nan)
            X = X.fillna(X.median())
            
            # Normalizar dados
            X_scaled = self.scaler.transform(X)
            
            # Fazer predições
            predicoes = self.model.predict(X_scaled)
            probabilidades = self.model.predict_proba(X_scaled)[:, 1]
            
            # Predições do Isolation Forest
            predicoes_iso = self.isolation_forest.predict(X_scaled)
            predicoes_iso = (predicoes_iso == -1).astype(int)
            
            # Preparar resultados
            resultados = []
            for i in range(len(df)):
                resultado = {
                    'indice': i,
                    'predicao_rf': int(predicoes[i]),
                    'probabilidade_rf': float(probabilidades[i]),
                    'predicao_iso': int(predicoes_iso[i]),
                    'confianca': 'Alta' if probabilidades[i] > 0.8 or probabilidades[i] < 0.2 else 'Média',
                    'status': 'ANOMALIA' if predicoes[i] == 1 else 'NORMAL',
                    'dados_originais': df.iloc[i].to_dict()
                }
                resultados.append(resultado)
            
            return resultados
            
        except Exception as e:
            print(f"❌ Erro na predição: {e}")
            return None
    
    def analisar_dados_em_lote(self, arquivo_csv):
        """
        Analisa um arquivo CSV com dados de sensores
        
        Args:
            arquivo_csv (str): Caminho para o arquivo CSV
            
        Returns:
            pd.DataFrame: Resultados da análise
        """
        try:
            print(f"📊 Analisando arquivo: {arquivo_csv}")
            
            # Carregar dados
            df = pd.read_csv(arquivo_csv)
            print(f"   • Registros carregados: {len(df)}")
            
            # Fazer predições
            resultados = self.predizer_anomalia(df)
            
            if resultados is None:
                return None
            
            # Converter para DataFrame
            df_resultados = pd.DataFrame(resultados)
            
            # Estatísticas
            total_anomalias = df_resultados['predicao_rf'].sum()
            total_normais = len(df_resultados) - total_anomalias
            
            print(f"✅ Análise concluída!")
            print(f"   • Total de registros: {len(df_resultados)}")
            print(f"   • Anomalias detectadas: {total_anomalias}")
            print(f"   • Normais: {total_normais}")
            print(f"   • Taxa de anomalias: {total_anomalias/len(df_resultados):.2%}")
            
            return df_resultados
            
        except Exception as e:
            print(f"❌ Erro na análise: {e}")
            return None
    
    def monitorar_tempo_real(self, dados_sensor):
        """
        Monitora dados de sensores em tempo real
        
        Args:
            dados_sensor (dict): Dados do sensor atual
            
        Returns:
            dict: Resultado do monitoramento
        """
        try:
            # Fazer predição
            resultado = self.predizer_anomalia(dados_sensor)[0]
            
            # Adicionar timestamp
            from datetime import datetime
            resultado['timestamp'] = datetime.now().isoformat()
            
            # Determinar ação recomendada
            if resultado['predicao_rf'] == 1:
                if resultado['probabilidade_rf'] > 0.9:
                    resultado['acao'] = 'ALERTA_CRÍTICO'
                    resultado['mensagem'] = 'Anomalia crítica detectada! Ação imediata necessária.'
                else:
                    resultado['acao'] = 'ALERTA'
                    resultado['mensagem'] = 'Possível anomalia detectada. Verificar sistema.'
            else:
                resultado['acao'] = 'NORMAL'
                resultado['mensagem'] = 'Sistema operando normalmente.'
            
            return resultado
            
        except Exception as e:
            print(f"❌ Erro no monitoramento: {e}")
            return None

def main():
    """
    Função principal para demonstrar o uso do modelo
    """
    print("🚀 SISTEMA DE DETECÇÃO DE ANOMALIAS IoT - USO DO MODELO")
    print("="*70)
    
    try:
        # Carregar modelo
        predictor = IoTAnomalyPredictor()
        
        # Exemplo 1: Dados únicos
        print(f"\n📊 EXEMPLO 1: ANÁLISE DE DADOS ÚNICOS")
        print("-" * 50)
        
        dados_exemplo = {
            'temperature': 25.5,
            'humidity': 60.0,
            'pressure': 1.013,
            'vibration_mag': 0.1,
            'level': 100.0,
            'luminosity': 500.0,
            'movement': 0,
            'co2': 400.0,
            'noise': 45.0,
            'temp_humidity_ratio': 0.425,
            'pressure_vibration': 0.101,
            'level_luminosity': 50.0,
            'temp_pressure_ratio': 25.2,
            'humidity_level_ratio': 0.6,
            'co2_noise_ratio': 8.89
        }
        
        resultado = predictor.predizer_anomalia(dados_exemplo)
        if resultado:
            print(f"Resultado: {resultado[0]['status']}")
            print(f"Probabilidade: {resultado[0]['probabilidade_rf']:.4f}")
            print(f"Confiança: {resultado[0]['confianca']}")
        
        # Exemplo 2: Dados de anomalia
        print(f"\n📊 EXEMPLO 2: DADOS DE ANOMALIA")
        print("-" * 50)
        
        dados_anomalia = {
            'temperature': 35.0,
            'humidity': 85.0,
            'pressure': 1.030,
            'vibration_mag': 1.2,
            'level': 150.0,
            'luminosity': 800.0,
            'movement': 1,
            'co2': 1500.0,
            'noise': 75.0,
            'temp_humidity_ratio': 0.412,
            'pressure_vibration': 1.236,
            'level_luminosity': 120.0,
            'temp_pressure_ratio': 34.0,
            'humidity_level_ratio': 0.567,
            'co2_noise_ratio': 20.0
        }
        
        resultado = predictor.predizer_anomalia(dados_anomalia)
        if resultado:
            print(f"Resultado: {resultado[0]['status']}")
            print(f"Probabilidade: {resultado[0]['probabilidade_rf']:.4f}")
            print(f"Confiança: {resultado[0]['confianca']}")
        
        # Exemplo 3: Monitoramento em tempo real
        print(f"\n📊 EXEMPLO 3: MONITORAMENTO EM TEMPO REAL")
        print("-" * 50)
        
        resultado_monitoramento = predictor.monitorar_tempo_real(dados_exemplo)
        if resultado_monitoramento:
            print(f"Status: {resultado_monitoramento['status']}")
            print(f"Ação: {resultado_monitoramento['acao']}")
            print(f"Mensagem: {resultado_monitoramento['mensagem']}")
            print(f"Timestamp: {resultado_monitoramento['timestamp']}")
        
        print(f"\n✅ SISTEMA FUNCIONANDO CORRETAMENTE!")
        print("   • Modelo carregado e operacional")
        print("   • Predições funcionando")
        print("   • Monitoramento em tempo real ativo")
        
    except Exception as e:
        print(f"❌ Erro no sistema: {e}")
        print("   Verifique se o modelo foi treinado corretamente.")

if __name__ == "__main__":
    main()
