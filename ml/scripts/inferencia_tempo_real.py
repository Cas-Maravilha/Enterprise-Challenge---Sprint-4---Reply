#!/usr/bin/env python3
"""
Sistema IoT Monitoring - Inferência em Tempo Real
Enterprise Challenge Sprint 3 - Reply

Este script implementa inferência em tempo real para detecção de anomalias
usando modelos de Machine Learning treinados.
"""

import pandas as pd
import numpy as np
import joblib
import json
import time
from datetime import datetime
import mysql.connector
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings('ignore')

class IoTRealTimeInference:
    """Classe para inferência em tempo real de anomalias IoT"""
    
    def __init__(self, db_config, model_path='../modelos/'):
        self.db_config = db_config
        self.model_path = model_path
        self.model = None
        self.scaler = None
        self.label_encoders = {}
        self.is_loaded = False
        
        print("=== Sistema IoT Monitoring - Inferência Tempo Real ===")
        print("Enterprise Challenge Sprint 3 - Reply")
        print("====================================================")
    
    def load_models(self):
        """Carrega modelos treinados"""
        try:
            print("🔄 Carregando modelos...")
            
            # Carregar melhor modelo (Random Forest por padrão)
            self.model = joblib.load(f'{self.model_path}random_forest.pkl')
            self.scaler = joblib.load(f'{self.model_path}scaler.pkl')
            self.label_encoders['sensor'] = joblib.load(f'{self.model_path}label_encoder_sensor.pkl')
            self.label_encoders['qualidade'] = joblib.load(f'{self.model_path}label_encoder_qualidade.pkl')
            
            self.is_loaded = True
            print("✅ Modelos carregados com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar modelos: {e}")
            return False
    
    def prepare_features(self, data):
        """Prepara features para inferência"""
        # Converter timestamp para features temporais
        timestamp = pd.to_datetime(data['timestamp_datetime'])
        
        features = {
            'valor_numerico': data['valor_numerico'],
            'valor_booleano': data['valor_booleano'],
            'hour': timestamp.hour,
            'day_of_week': timestamp.dayofweek,
            'day_of_month': timestamp.day,
            'sensor_encoded': self.label_encoders['sensor'].transform([data['tipo_sensor']])[0],
            'qualidade_encoded': self.label_encoders['qualidade'].transform([data['qualidade_dados']])[0]
        }
        
        # Converter para array numpy
        X = np.array([list(features.values())]).reshape(1, -1)
        
        # Normalizar
        X_scaled = self.scaler.transform(X)
        
        return X_scaled
    
    def predict_anomaly(self, data):
        """Prediz se uma leitura é uma anomalia"""
        if not self.is_loaded:
            print("❌ Modelos não carregados!")
            return None
        
        try:
            # Preparar features
            X = self.prepare_features(data)
            
            # Fazer predição
            prediction = self.model.predict(X)[0]
            probability = None
            
            # Se for Random Forest, obter probabilidades
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(X)[0]
                probability = probabilities[1] if len(probabilities) > 1 else probabilities[0]
            
            return {
                'is_anomaly': bool(prediction),
                'probability': probability,
                'confidence': 'high' if probability and probability > 0.8 else 'medium' if probability and probability > 0.5 else 'low',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Erro na predição: {e}")
            return None
    
    def process_single_reading(self, reading_data):
        """Processa uma única leitura"""
        print(f"\n🔍 Processando leitura: {reading_data['sensor_nome']} - {reading_data['timestamp_datetime']}")
        
        # Fazer predição
        result = self.predict_anomaly(reading_data)
        
        if result:
            print(f"📊 Resultado: {'ANOMALIA' if result['is_anomaly'] else 'NORMAL'}")
            if result['probability']:
                print(f"🎯 Probabilidade: {result['probability']:.3f}")
            print(f"⭐ Confiança: {result['confidence']}")
            
            return result
        else:
            print("❌ Falha na predição")
            return None
    
    def process_batch_readings(self, readings_data):
        """Processa múltiplas leituras em lote"""
        print(f"\n📦 Processando lote de {len(readings_data)} leituras...")
        
        results = []
        
        for i, reading in enumerate(readings_data):
            print(f"  [{i+1}/{len(readings_data)}] {reading['sensor_nome']}")
            
            result = self.predict_anomaly(reading)
            if result:
                result['sensor_id'] = reading.get('id_sensor')
                result['sensor_nome'] = reading.get('sensor_nome')
                result['dispositivo_nome'] = reading.get('dispositivo_nome')
                results.append(result)
        
        # Estatísticas do lote
        total_anomalies = sum(1 for r in results if r['is_anomaly'])
        avg_confidence = np.mean([r['probability'] for r in results if r['probability']]) if any(r['probability'] for r in results) else 0
        
        print(f"\n📊 Estatísticas do lote:")
        print(f"  Total de leituras: {len(results)}")
        print(f"  Anomalias detectadas: {total_anomalies}")
        print(f"  Taxa de anomalias: {total_anomalies/len(results)*100:.2f}%")
        print(f"  Confiança média: {avg_confidence:.3f}")
        
        return results
    
    def get_recent_readings(self, engine, limit=100):
        """Obtém leituras recentes do banco"""
        query = """
        SELECT 
            l.id_leitura,
            l.timestamp_datetime,
            l.valor_numerico,
            l.valor_booleano,
            l.qualidade_dados,
            l.anomalia_detectada,
            s.nome as sensor_nome,
            ts.nome as tipo_sensor,
            ts.unidade_medida,
            d.nome as dispositivo_nome
        FROM leituras_sensores l
        JOIN sensores s ON l.id_sensor = s.id_sensor
        JOIN tipos_sensor ts ON s.id_tipo_sensor = ts.id_tipo_sensor
        JOIN dispositivos d ON s.id_dispositivo = d.id_dispositivo
        ORDER BY l.timestamp_datetime DESC
        LIMIT %s
        """ % limit
        
        try:
            df = pd.read_sql(query, engine)
            return df.to_dict('records')
        except Exception as e:
            print(f"❌ Erro ao carregar leituras: {e}")
            return []
    
    def run_real_time_monitoring(self, duration_minutes=5, interval_seconds=10):
        """Executa monitoramento em tempo real"""
        print(f"\n🚀 Iniciando monitoramento em tempo real...")
        print(f"⏱️ Duração: {duration_minutes} minutos")
        print(f"🔄 Intervalo: {interval_seconds} segundos")
        
        # Conectar ao banco
        engine = create_engine(
            f"mysql+pymysql://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}/{self.db_config['database']}"
        )
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        total_readings = 0
        total_anomalies = 0
        
        try:
            while time.time() < end_time:
                print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')} - Verificando leituras...")
                
                # Obter leituras recentes
                readings = self.get_recent_readings(engine, limit=10)
                
                if readings:
                    # Processar leituras
                    results = self.process_batch_readings(readings)
                    
                    # Atualizar estatísticas
                    total_readings += len(results)
                    total_anomalies += sum(1 for r in results if r['is_anomaly'])
                    
                    # Mostrar anomalias detectadas
                    anomalies = [r for r in results if r['is_anomaly']]
                    if anomalies:
                        print(f"\n🚨 ANOMALIAS DETECTADAS ({len(anomalies)}):")
                        for anomaly in anomalies:
                            print(f"  - {anomaly['sensor_nome']} ({anomaly['dispositivo_nome']}) - Confiança: {anomaly['confidence']}")
                else:
                    print("  ⚠️ Nenhuma leitura recente encontrada")
                
                # Aguardar próximo intervalo
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print("\n⏹️ Monitoramento interrompido pelo usuário")
        
        # Resumo final
        print(f"\n📊 RESUMO DO MONITORAMENTO:")
        print(f"  Duração: {duration_minutes} minutos")
        print(f"  Total de leituras: {total_readings}")
        print(f"  Anomalias detectadas: {total_anomalies}")
        print(f"  Taxa de anomalias: {total_anomalies/total_readings*100:.2f}%" if total_readings > 0 else "  Taxa de anomalias: 0%")
    
    def run_batch_processing(self, limit=1000):
        """Executa processamento em lote"""
        print(f"\n📦 Iniciando processamento em lote...")
        
        # Conectar ao banco
        engine = create_engine(
            f"mysql+pymysql://{self.db_config['user']}:{self.db_config['password']}@{self.db_config['host']}/{self.db_config['database']}"
        )
        
        # Obter leituras
        readings = self.get_recent_readings(engine, limit=limit)
        
        if not readings:
            print("❌ Nenhuma leitura encontrada")
            return
        
        # Processar lote
        results = self.process_batch_readings(readings)
        
        # Salvar resultados
        self.save_results(results)
        
        print(f"\n✅ Processamento em lote concluído!")
        print(f"📁 Resultados salvos em: ../metricas/inferencia_results.json")
    
    def save_results(self, results):
        """Salva resultados da inferência"""
        os.makedirs('../metricas', exist_ok=True)
        
        # Preparar dados para JSON
        json_results = []
        for result in results:
            json_result = {
                'timestamp': result['timestamp'],
                'sensor_nome': result.get('sensor_nome', ''),
                'dispositivo_nome': result.get('dispositivo_nome', ''),
                'is_anomaly': result['is_anomaly'],
                'probability': result.get('probability'),
                'confidence': result['confidence']
            }
            json_results.append(json_result)
        
        # Salvar em arquivo
        with open('../metricas/inferencia_results.json', 'w') as f:
            json.dump(json_results, f, indent=2)
        
        print("✅ Resultados salvos com sucesso!")

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Inferência em Tempo Real - Sistema IoT Monitoring')
    parser.add_argument('--mode', choices=['realtime', 'batch'], default='batch',
                       help='Modo de execução: realtime ou batch')
    parser.add_argument('--duration', type=int, default=5,
                       help='Duração do monitoramento em tempo real (minutos)')
    parser.add_argument('--interval', type=int, default=10,
                       help='Intervalo entre verificações (segundos)')
    parser.add_argument('--limit', type=int, default=1000,
                       help='Limite de leituras para processamento em lote')
    
    args = parser.parse_args()
    
    # Configurações do banco
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'password',
        'database': 'iot_monitoring_db'
    }
    
    # Criar inferência
    inference = IoTRealTimeInference(db_config)
    
    # Carregar modelos
    if not inference.load_models():
        return 1
    
    # Executar inferência
    if args.mode == 'realtime':
        inference.run_real_time_monitoring(
            duration_minutes=args.duration,
            interval_seconds=args.interval
        )
    else:
        inference.run_batch_processing(limit=args.limit)
    
    return 0

if __name__ == "__main__":
    import os
    exit(main())
