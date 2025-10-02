#!/usr/bin/env python3
"""
Coletor de Dados Serial - Sistema IoT Monitoring
Enterprise Challenge Sprint 3 - Reply

Este script coleta dados do ESP32 via Serial/USB,
valida os dados e salva em CSV e JSON.
"""

import serial
import json
import csv
import time
import logging
from datetime import datetime
from typing import Dict, List, Any
import argparse
import sys

class ColetorDadosSerial:
    """Coletor de dados via Serial/USB"""
    
    def __init__(self, port: str = 'COM3', baudrate: int = 115200, duracao: int = 60):
        self.port = port
        self.baudrate = baudrate
        self.duracao = duracao
        self.serial_conn = None
        self.dados_coletados = []
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('ingest/dados/logs_coletor_serial.txt'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("=== Coletor de Dados Serial ===")
        self.logger.info("Enterprise Challenge Sprint 3 - Reply")
        self.logger.info("===============================")
    
    def conectar_serial(self) -> bool:
        """Conecta ao ESP32 via Serial"""
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=1
            )
            self.logger.info(f"Conectado ao ESP32 na porta {self.port}")
            return True
        except serial.SerialException as e:
            self.logger.error(f"Erro ao conectar na porta {self.port}: {e}")
            return False
    
    def validar_dados(self, dados: Dict[str, Any]) -> bool:
        """Valida os dados coletados"""
        try:
            # Verificar campos obrigatórios
            campos_obrigatorios = ['device', 'timestamp', 'sensors', 'quality']
            for campo in campos_obrigatorios:
                if campo not in dados:
                    self.logger.warning(f"Campo obrigatório ausente: {campo}")
                    return False
            
            # Verificar sensores
            sensores = dados.get('sensors', {})
            if 'DHT22' not in sensores:
                self.logger.warning("Sensor DHT22 não encontrado")
                return False
            
            # Verificar temperatura
            temp = sensores['DHT22'].get('temperature', 0)
            if not isinstance(temp, (int, float)) or temp < -40 or temp > 80:
                self.logger.warning(f"Temperatura inválida: {temp}")
                return False
            
            # Verificar umidade
            umid = sensores['DHT22'].get('humidity', 0)
            if not isinstance(umid, (int, float)) or umid < 0 or umid > 100:
                self.logger.warning(f"Umidade inválida: {umid}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Erro na validação: {e}")
            return False
    
    def processar_dados(self, linha: str) -> Dict[str, Any]:
        """Processa uma linha de dados JSON"""
        try:
            dados = json.loads(linha.strip())
            
            # Adicionar timestamp de processamento
            dados['processed_at'] = datetime.now().isoformat()
            
            # Validar dados
            if not self.validar_dados(dados):
                return None
            
            return dados
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Erro ao decodificar JSON: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Erro ao processar dados: {e}")
            return None
    
    def coletar_dados(self):
        """Coleta dados do ESP32 por um período determinado"""
        if not self.conectar_serial():
            return False
        
        self.logger.info(f"Iniciando coleta de dados por {self.duracao} segundos...")
        self.logger.info(f"Porta: {self.port}, Baudrate: {self.baudrate}")
        
        inicio = time.time()
        leituras_validas = 0
        leituras_invalidas = 0
        
        try:
            while time.time() - inicio < self.duracao:
                if self.serial_conn.in_waiting > 0:
                    linha = self.serial_conn.readline().decode('utf-8').strip()
                    
                    if linha:
                        self.logger.info(f"Dados recebidos: {linha[:100]}...")
                        
                        dados = self.processar_dados(linha)
                        if dados:
                            self.dados_coletados.append(dados)
                            leituras_validas += 1
                            self.logger.info(f"✓ Dados válidos - Leitura #{leituras_validas}")
                        else:
                            leituras_invalidas += 1
                            self.logger.warning(f"✗ Dados inválidos - Total inválidas: {leituras_invalidas}")
                
                time.sleep(0.1)  # Pequena pausa para não sobrecarregar
                
        except KeyboardInterrupt:
            self.logger.info("Coleta interrompida pelo usuário")
        except Exception as e:
            self.logger.error(f"Erro durante a coleta: {e}")
        finally:
            if self.serial_conn:
                self.serial_conn.close()
                self.logger.info("Conexão Serial fechada")
        
        # Resumo da coleta
        self.logger.info("=== Resumo da Coleta ===")
        self.logger.info(f"Leituras válidas: {leituras_validas}")
        self.logger.info(f"Leituras inválidas: {leituras_invalidas}")
        self.logger.info(f"Total de dados coletados: {len(self.dados_coletados)}")
        
        return len(self.dados_coletados) > 0
    
    def salvar_dados_csv(self, arquivo: str = 'ingest/dados/dados_coletados.csv'):
        """Salva os dados coletados em formato CSV"""
        if not self.dados_coletados:
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
                for dados in self.dados_coletados:
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
    
    def salvar_dados_json(self, arquivo: str = 'ingest/dados/dados_coletados.json'):
        """Salva os dados coletados em formato JSON"""
        if not self.dados_coletados:
            self.logger.warning("Nenhum dado para salvar")
            return False
        
        try:
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.dados_coletados, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Dados salvos em JSON: {arquivo}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar JSON: {e}")
            return False
    
    def gerar_relatorio(self):
        """Gera relatório da coleta"""
        if not self.dados_coletados:
            return
        
        # Estatísticas básicas
        total_leituras = len(self.dados_coletados)
        dispositivos = set(d['device'] for d in self.dados_coletados)
        qualidades = [d['quality'] for d in self.dados_coletados]
        
        # Estatísticas de temperatura
        temperaturas = []
        for dados in self.dados_coletados:
            temp = dados.get('sensors', {}).get('DHT22', {}).get('temperature')
            if temp is not None:
                temperaturas.append(temp)
        
        temp_media = sum(temperaturas) / len(temperaturas) if temperaturas else 0
        temp_min = min(temperaturas) if temperaturas else 0
        temp_max = max(temperaturas) if temperaturas else 0
        
        # Relatório
        relatorio = {
            'coleta': {
                'inicio': self.dados_coletados[0]['processed_at'] if self.dados_coletados else None,
                'fim': self.dados_coletados[-1]['processed_at'] if self.dados_coletados else None,
                'duracao_segundos': self.duracao,
                'total_leituras': total_leituras,
                'leituras_por_segundo': total_leituras / self.duracao if self.duracao > 0 else 0
            },
            'dispositivos': list(dispositivos),
            'qualidade_dados': {
                'excelente': qualidades.count('excelente'),
                'boa': qualidades.count('boa'),
                'regular': qualidades.count('regular'),
                'ruim': qualidades.count('ruim')
            },
            'temperatura': {
                'media': round(temp_media, 2),
                'minima': round(temp_min, 2),
                'maxima': round(temp_max, 2)
            }
        }
        
        # Salvar relatório
        with open('ingest/dados/relatorio_coleta_serial.json', 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        
        self.logger.info("Relatório gerado: ingest/dados/relatorio_coleta_serial.json")
        
        # Imprimir resumo
        print("\n" + "="*50)
        print("RELATÓRIO DE COLETA SERIAL")
        print("="*50)
        print(f"Total de leituras: {total_leituras}")
        print(f"Leituras por segundo: {relatorio['coleta']['leituras_por_segundo']:.2f}")
        print(f"Dispositivos: {', '.join(dispositivos)}")
        print(f"Temperatura média: {temp_media:.2f}°C")
        print(f"Temperatura mínima: {temp_min:.2f}°C")
        print(f"Temperatura máxima: {temp_max:.2f}°C")
        print("Qualidade dos dados:")
        for qualidade, count in relatorio['qualidade_dados'].items():
            print(f"  {qualidade}: {count}")
        print("="*50)

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Coletor de Dados Serial - Sistema IoT Monitoring')
    parser.add_argument('--port', default='COM3', help='Porta Serial (padrão: COM3)')
    parser.add_argument('--baudrate', type=int, default=115200, help='Baudrate (padrão: 115200)')
    parser.add_argument('--duracao', type=int, default=60, help='Duração em segundos (padrão: 60)')
    
    args = parser.parse_args()
    
    # Criar coletor
    coletor = ColetorDadosSerial(
        port=args.port,
        baudrate=args.baudrate,
        duracao=args.duracao
    )
    
    # Coletar dados
    sucesso = coletor.coletar_dados()
    
    if sucesso:
        # Salvar dados
        coletor.salvar_dados_csv()
        coletor.salvar_dados_json()
        coletor.gerar_relatorio()
        
        print("\n✅ Coleta de dados concluída com sucesso!")
        print("📁 Arquivos gerados:")
        print("  - ingest/dados/dados_coletados.csv")
        print("  - ingest/dados/dados_coletados.json")
        print("  - ingest/dados/relatorio_coleta_serial.json")
        print("  - ingest/dados/logs_coletor_serial.txt")
    else:
        print("\n❌ Falha na coleta de dados.")
        sys.exit(1)

if __name__ == "__main__":
    main()
