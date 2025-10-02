#!/usr/bin/env python3
"""
Simulador de Dados ESP32 - Sistema IoT Monitoring
Enterprise Challenge Sprint 3 - Reply

Este script simula dados de sensores do ESP32
para desenvolvimento e teste sem hardware real.
"""

import json
import csv
import time
import random
import math
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
import argparse
import sys

class SimuladorDadosESP32:
    """Simulador de dados de sensores ESP32"""
    
    def __init__(self, duracao: int = 60, frequencia: int = 1, sensores: List[str] = None):
        self.duracao = duracao
        self.frequencia = frequencia
        self.sensores = sensores or ['DHT22', 'LDR', 'PIR', 'BME280']
        self.dados_simulados = []
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('ingest/dados/logs_simulador.txt'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Parâmetros de simulação
        self.parametros = {
            'DHT22': {
                'temperature': {'base': 25.0, 'variacao': 5.0, 'tendencia': 0.1},
                'humidity': {'base': 60.0, 'variacao': 10.0, 'tendencia': -0.05}
            },
            'LDR': {
                'light': {'base': 450.0, 'variacao': 200.0, 'tendencia': 0.0}
            },
            'PIR': {
                'motion': {'probabilidade': 0.1, 'duracao_min': 2, 'duracao_max': 10}
            },
            'BME280': {
                'pressure': {'base': 1013.25, 'variacao': 10.0, 'tendencia': 0.0}
            }
        }
        
        # Estado da simulação
        self.tempo_inicio = time.time()
        self.leitura_count = 0
        self.motion_state = False
        self.motion_end_time = 0
        
        self.logger.info("=== Simulador de Dados ESP32 ===")
        self.logger.info("Enterprise Challenge Sprint 3 - Reply")
        self.logger.info("================================")
    
    def gerar_temperatura(self, timestamp: float) -> float:
        """Gera temperatura simulada com variação realística"""
        params = self.parametros['DHT22']['temperature']
        
        # Variação baseada no tempo (ciclo diário)
        ciclo_diario = math.sin((timestamp % 86400) / 86400 * 2 * math.pi) * 3
        
        # Variação aleatória
        variacao_aleatoria = random.gauss(0, params['variacao'] * 0.3)
        
        # Tendência temporal
        tendencia = (timestamp - self.tempo_inicio) * params['tendencia']
        
        temperatura = params['base'] + ciclo_diario + variacao_aleatoria + tendencia
        
        # Limitar entre -10 e 50°C
        return max(-10, min(50, round(temperatura, 1)))
    
    def gerar_umidade(self, timestamp: float, temperatura: float) -> float:
        """Gera umidade simulada baseada na temperatura"""
        params = self.parametros['DHT22']['humidity']
        
        # Umidade inversamente relacionada à temperatura
        correlacao_temp = (25 - temperatura) * 2
        
        # Variação aleatória
        variacao_aleatoria = random.gauss(0, params['variacao'] * 0.2)
        
        # Tendência temporal
        tendencia = (timestamp - self.tempo_inicio) * params['tendencia']
        
        umidade = params['base'] + correlacao_temp + variacao_aleatoria + tendencia
        
        # Limitar entre 0 e 100%
        return max(0, min(100, round(umidade, 1)))
    
    def gerar_luminosidade(self, timestamp: float) -> int:
        """Gera luminosidade simulada com padrão diário"""
        params = self.parametros['LDR']['light']
        
        # Ciclo diário (mais luz durante o dia)
        hora_dia = (timestamp % 86400) / 3600  # Hora do dia (0-24)
        
        if 6 <= hora_dia <= 18:  # Dia
            ciclo_diario = math.sin((hora_dia - 6) / 12 * math.pi) * params['variacao']
        else:  # Noite
            ciclo_diario = -params['variacao'] * 0.8
        
        # Variação aleatória
        variacao_aleatoria = random.gauss(0, params['variacao'] * 0.3)
        
        luminosidade = params['base'] + ciclo_diario + variacao_aleatoria
        
        # Limitar entre 0 e 1000 lux
        return max(0, min(1000, int(luminosidade)))
    
    def gerar_movimento(self, timestamp: float) -> int:
        """Gera movimento simulado (PIR)"""
        params = self.parametros['PIR']['motion']
        
        # Se já está em estado de movimento, verificar se deve terminar
        if self.motion_state:
            if timestamp >= self.motion_end_time:
                self.motion_state = False
            return 1
        
        # Verificar se deve iniciar movimento
        if random.random() < params['probabilidade']:
            self.motion_state = True
            duracao = random.randint(params['duracao_min'], params['duracao_max'])
            self.motion_end_time = timestamp + duracao
            return 1
        
        return 0
    
    def gerar_pressao(self, timestamp: float) -> float:
        """Gera pressão atmosférica simulada"""
        params = self.parametros['BME280']['pressure']
        
        # Variação aleatória suave
        variacao_aleatoria = random.gauss(0, params['variacao'] * 0.2)
        
        # Tendência temporal
        tendencia = (timestamp - self.tempo_inicio) * params['tendencia']
        
        pressao = params['base'] + variacao_aleatoria + tendencia
        
        # Limitar entre 950 e 1050 hPa
        return max(950, min(1050, round(pressao, 2)))
    
    def calcular_qualidade_dados(self, dados: Dict[str, Any]) -> str:
        """Calcula qualidade dos dados simulados"""
        score = 100
        
        # Verificar temperatura
        temp = dados['sensors']['DHT22']['temperature']
        if temp < 0 or temp > 40:
            score -= 20
        
        # Verificar umidade
        umid = dados['sensors']['DHT22']['humidity']
        if umid < 20 or umid > 90:
            score -= 20
        
        # Verificar luminosidade
        luz = dados['sensors']['LDR']['light']
        if luz < 0 or luz > 1000:
            score -= 15
        
        # Verificar pressão
        pressao = dados['sensors']['BME280']['pressure']
        if pressao < 950 or pressao > 1050:
            score -= 15
        
        # Adicionar ruído ocasional
        if random.random() < 0.05:  # 5% de chance de dados ruins
            score -= 30
        
        if score >= 90:
            return "excelente"
        elif score >= 70:
            return "boa"
        elif score >= 50:
            return "regular"
        else:
            return "ruim"
    
    def gerar_dados_simulados(self):
        """Gera dados simulados por um período determinado"""
        self.logger.info(f"Iniciando simulação de dados...")
        self.logger.info(f"Duração: {self.duracao} segundos")
        self.logger.info(f"Frequência: {self.frequencia} Hz")
        self.logger.info(f"Sensores: {', '.join(self.sensores)}")
        
        intervalo = 1.0 / self.frequencia
        leituras_geradas = 0
        
        try:
            while time.time() - self.tempo_inicio < self.duracao:
                timestamp_atual = time.time()
                
                # Gerar dados dos sensores
                dados = {
                    'device': 'ESP32-Simulator',
                    'timestamp': int(timestamp_atual * 1000),  # Em milissegundos
                    'sensors': {},
                    'quality': '',
                    'read_count': leituras_geradas
                }
                
                # DHT22 - Temperatura e Umidade
                if 'DHT22' in self.sensores:
                    temperatura = self.gerar_temperatura(timestamp_atual)
                    umidade = self.gerar_umidade(timestamp_atual, temperatura)
                    dados['sensors']['DHT22'] = {
                        'temperature': temperatura,
                        'humidity': umidade
                    }
                
                # LDR - Luminosidade
                if 'LDR' in self.sensores:
                    luminosidade = self.gerar_luminosidade(timestamp_atual)
                    dados['sensors']['LDR'] = {
                        'light': luminosidade
                    }
                
                # PIR - Movimento
                if 'PIR' in self.sensores:
                    movimento = self.gerar_movimento(timestamp_atual)
                    dados['sensors']['PIR'] = {
                        'motion': movimento
                    }
                
                # BME280 - Pressão
                if 'BME280' in self.sensores:
                    pressao = self.gerar_pressao(timestamp_atual)
                    dados['sensors']['BME280'] = {
                        'pressure': pressao
                    }
                
                # Calcular qualidade
                dados['quality'] = self.calcular_qualidade_dados(dados)
                
                # Adicionar timestamp de processamento
                dados['processed_at'] = datetime.now().isoformat()
                
                # Adicionar aos dados coletados
                self.dados_simulados.append(dados)
                leituras_geradas += 1
                
                # Log da leitura
                self.logger.info(f"Leitura #{leituras_geradas} gerada")
                
                # Aguardar próximo intervalo
                time.sleep(intervalo)
                
        except KeyboardInterrupt:
            self.logger.info("Simulação interrompida pelo usuário")
        
        self.logger.info(f"Simulação concluída! Total de leituras: {leituras_geradas}")
        return leituras_geradas > 0
    
    def salvar_dados_csv(self, arquivo: str = 'ingest/dados/dados_simulados.csv'):
        """Salva os dados simulados em formato CSV"""
        if not self.dados_simulados:
            self.logger.warning("Nenhum dado para salvar")
            return False
        
        try:
            with open(arquivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Cabeçalho
                writer.writerow([
                    'timestamp', 'device', 'temperature', 'humidity', 
                    'light', 'motion', 'pressure', 'quality', 'read_count', 'processed_at'
                ])
                
                # Dados
                for dados in self.dados_simulados:
                    sensores = dados.get('sensors', {})
                    dht22 = sensores.get('DHT22', {})
                    ldr = sensores.get('LDR', {})
                    pir = sensores.get('PIR', {})
                    bme280 = sensores.get('BME280', {})
                    
                    writer.writerow([
                        dados.get('timestamp', ''),
                        dados.get('device', ''),
                        dht22.get('temperature', ''),
                        dht22.get('humidity', ''),
                        ldr.get('light', ''),
                        pir.get('motion', ''),
                        bme280.get('pressure', ''),
                        dados.get('quality', ''),
                        dados.get('read_count', ''),
                        dados.get('processed_at', '')
                    ])
            
            self.logger.info(f"Dados salvos em CSV: {arquivo}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar CSV: {e}")
            return False
    
    def salvar_dados_json(self, arquivo: str = 'ingest/dados/dados_simulados.json'):
        """Salva os dados simulados em formato JSON"""
        if not self.dados_simulados:
            self.logger.warning("Nenhum dado para salvar")
            return False
        
        try:
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.dados_simulados, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Dados salvos em JSON: {arquivo}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar JSON: {e}")
            return False
    
    def gerar_relatorio(self):
        """Gera relatório da simulação"""
        if not self.dados_simulados:
            return
        
        # Estatísticas básicas
        total_leituras = len(self.dados_simulados)
        qualidades = [d['quality'] for d in self.dados_simulados]
        
        # Estatísticas de temperatura
        temperaturas = []
        umidades = []
        luminosidades = []
        pressoes = []
        
        for dados in self.dados_simulados:
            sensores = dados.get('sensors', {})
            
            if 'DHT22' in sensores:
                temp = sensores['DHT22'].get('temperature')
                umid = sensores['DHT22'].get('humidity')
                if temp is not None:
                    temperaturas.append(temp)
                if umid is not None:
                    umidades.append(umid)
            
            if 'LDR' in sensores:
                luz = sensores['LDR'].get('light')
                if luz is not None:
                    luminosidades.append(luz)
            
            if 'BME280' in sensores:
                pressao = sensores['BME280'].get('pressure')
                if pressao is not None:
                    pressoes.append(pressao)
        
        # Calcular estatísticas
        def calcular_stats(valores):
            if not valores:
                return {'media': 0, 'min': 0, 'max': 0, 'std': 0}
            media = sum(valores) / len(valores)
            return {
                'media': round(media, 2),
                'min': round(min(valores), 2),
                'max': round(max(valores), 2),
                'std': round(math.sqrt(sum((x - media) ** 2 for x in valores) / len(valores)), 2)
            }
        
        stats_temp = calcular_stats(temperaturas)
        stats_umid = calcular_stats(umidades)
        stats_luz = calcular_stats(luminosidades)
        stats_pressao = calcular_stats(pressoes)
        
        # Relatório
        relatorio = {
            'simulacao': {
                'inicio': self.dados_simulados[0]['processed_at'] if self.dados_simulados else None,
                'fim': self.dados_simulados[-1]['processed_at'] if self.dados_simulados else None,
                'duracao_segundos': self.duracao,
                'frequencia_hz': self.frequencia,
                'total_leituras': total_leituras,
                'leituras_por_segundo': total_leituras / self.duracao if self.duracao > 0 else 0
            },
            'sensores_simulados': self.sensores,
            'qualidade_dados': {
                'excelente': qualidades.count('excelente'),
                'boa': qualidades.count('boa'),
                'regular': qualidades.count('regular'),
                'ruim': qualidades.count('ruim')
            },
            'estatisticas': {
                'temperatura': stats_temp,
                'umidade': stats_umid,
                'luminosidade': stats_luz,
                'pressao': stats_pressao
            }
        }
        
        # Salvar relatório
        with open('ingest/dados/relatorio_simulacao.json', 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        
        self.logger.info("Relatório gerado: ingest/dados/relatorio_simulacao.json")
        
        # Imprimir resumo
        print("\n" + "="*60)
        print("RELATÓRIO DE SIMULAÇÃO DE DADOS")
        print("="*60)
        print(f"Total de leituras: {total_leituras}")
        print(f"Frequência: {self.frequencia} Hz")
        print(f"Leituras por segundo: {relatorio['simulacao']['leituras_por_segundo']:.2f}")
        print(f"Sensores simulados: {', '.join(self.sensores)}")
        print()
        print("Estatísticas dos sensores:")
        print(f"  Temperatura: {stats_temp['media']:.1f}°C (min: {stats_temp['min']:.1f}, max: {stats_temp['max']:.1f})")
        print(f"  Umidade: {stats_umid['media']:.1f}% (min: {stats_umid['min']:.1f}, max: {stats_umid['max']:.1f})")
        print(f"  Luminosidade: {stats_luz['media']:.0f} lux (min: {stats_luz['min']:.0f}, max: {stats_luz['max']:.0f})")
        print(f"  Pressão: {stats_pressao['media']:.1f} hPa (min: {stats_pressao['min']:.1f}, max: {stats_pressao['max']:.1f})")
        print()
        print("Qualidade dos dados:")
        for qualidade, count in relatorio['qualidade_dados'].items():
            print(f"  {qualidade}: {count}")
        print("="*60)

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Simulador de Dados ESP32 - Sistema IoT Monitoring')
    parser.add_argument('--duracao', type=int, default=60, help='Duração em segundos (padrão: 60)')
    parser.add_argument('--frequencia', type=int, default=1, help='Frequência em Hz (padrão: 1)')
    parser.add_argument('--sensores', nargs='+', default=['DHT22', 'LDR', 'PIR', 'BME280'], 
                       help='Sensores a simular (padrão: DHT22 LDR PIR BME280)')
    
    args = parser.parse_args()
    
    # Criar simulador
    simulador = SimuladorDadosESP32(
        duracao=args.duracao,
        frequencia=args.frequencia,
        sensores=args.sensores
    )
    
    # Gerar dados simulados
    sucesso = simulador.gerar_dados_simulados()
    
    if sucesso:
        # Salvar dados
        simulador.salvar_dados_csv()
        simulador.salvar_dados_json()
        simulador.gerar_relatorio()
        
        print("\n✅ Simulação de dados concluída com sucesso!")
        print("📁 Arquivos gerados:")
        print("  - ingest/dados/dados_simulados.csv")
        print("  - ingest/dados/dados_simulados.json")
        print("  - ingest/dados/relatorio_simulacao.json")
        print("  - ingest/dados/logs_simulador.txt")
    else:
        print("\n❌ Falha na simulação de dados.")
        sys.exit(1)

if __name__ == "__main__":
    main()
