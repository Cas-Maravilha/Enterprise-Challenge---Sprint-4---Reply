#!/usr/bin/env python3
"""
Script para automação da coleta de dados do ESP32 via porta serial.
Recebe os dados em formato CSV e os salva em um arquivo.
"""
import serial
import argparse
import time
import os
from datetime import datetime
import logging

# Configuração de logging
logging.basicConfig(filename='coleta_dados.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def collect_data(port, baud_rate, duration, output_file, append=False):
    """
    Coleta dados da porta serial por um período determinado.
    
    Args:
        port: Porta serial (ex: COM3, /dev/ttyUSB0)
        baud_rate: Taxa de transmissão (baud rate)
        duration: Duração da coleta em segundos (0 para coletar indefinidamente)
        output_file: Arquivo de saída para os dados CSV
        append: Se True, anexa ao arquivo existente em vez de sobrescrevê-lo
    """
    try:
        # Abre a conexão serial
        ser = serial.Serial(port, baud_rate, timeout=1)
        logging.info(f"Conectado à porta {port} com baud rate {baud_rate}")
        
        # Determina o modo de abertura do arquivo
        mode = 'a' if append else 'w'
        
        # Abre o arquivo de saída
        with open(output_file, mode) as f:
            # Se não estiver anexando, escreve um cabeçalho com timestamp
            if not append:
                f.write(f"# Coleta iniciada em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            # Calcula o tempo de término (se duration > 0)
            end_time = time.time() + duration if duration > 0 else float('inf')
            
            # Contador de linhas
            line_count = 0
            header_written = append  # Se estiver anexando, assume que o cabeçalho já existe
            
            print(f"Coletando dados para {output_file}...")
            print("Pressione Ctrl+C para interromper.")
            
            # Loop de coleta
            while time.time() < end_time:
                # Lê uma linha da porta serial
                line = ser.readline().decode('utf-8').strip()
                
                # Se a linha não estiver vazia
                if line:
                    # Validação de integridade: checar se é CSV e tem pelo menos 5 campos
                    if ',' in line and len(line.split(',')) >= 5:
                        # Se for a primeira linha e não estiver anexando, assume que é o cabeçalho
                        if not header_written and not line.startswith("ERROR"):
                            f.write(f"{line}\n")
                            header_written = True
                            print(f"Cabeçalho: {line}")
                        else:
                            # Escreve a linha no arquivo
                            f.write(f"{line}\n")
                            f.flush()  # Força a escrita no arquivo
                            
                            # Incrementa o contador e exibe progresso
                            line_count += 1
                            if line_count % 10 == 0:
                                print(f"Coletadas {line_count} linhas de dados...")
                            logging.info(f"Linha coletada: {line}")
                    else:
                        logging.warning(f"Linha inválida recebida: {line}")
                        print(f"Linha inválida ignorada: {line}")
                    if line.startswith("ERROR"):
                        print(f"ERRO: {line}")
                        logging.error(f"Erro recebido: {line}")
    
    except KeyboardInterrupt:
        print("\nColeta interrompida pelo usuário.")
        logging.info("Coleta interrompida pelo usuário.")
    except serial.SerialException as e:
        print(f"Erro na porta serial: {e}")
        logging.error(f"Erro na porta serial: {e}")
    finally:
        # Fecha a porta serial se estiver aberta
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Conexão serial fechada.")
            logging.info("Conexão serial fechada.")
        
        print(f"Coleta finalizada. {line_count} linhas de dados coletadas.")
        logging.info(f"Coleta finalizada. {line_count} linhas de dados coletadas.")

def collect_scenario(port, baud_rate, scenario, duration, output_dir):
    """
    Coleta dados para um cenário específico.
    
    Args:
        port: Porta serial
        baud_rate: Taxa de transmissão
        scenario: Nome do cenário (normal, alert, failure)
        duration: Duração da coleta em segundos
        output_dir: Diretório para salvar os arquivos de saída
    """
    # Cria o diretório de saída se não existir
    os.makedirs(output_dir, exist_ok=True)
    
    # Define o nome do arquivo de saída
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"{scenario}_{timestamp}.csv")
    
    print(f"\nIniciando coleta para cenário: {scenario.upper()}")
    print(f"Duração: {duration} segundos")
    print(f"Arquivo de saída: {output_file}")
    
    # Coleta os dados
    collect_data(port, baud_rate, duration, output_file)

def main():
    """Função principal"""
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(description='Coleta dados do ESP32 via porta serial.')
    parser.add_argument('--port', '-p', required=True, help='Porta serial (ex: COM3, /dev/ttyUSB0)')
    parser.add_argument('--baud', '-b', type=int, default=115200, help='Baud rate (padrão: 115200)')
    parser.add_argument('--output', '-o', default='sensor_data.csv', help='Arquivo de saída (padrão: sensor_data.csv)')
    parser.add_argument('--duration', '-d', type=int, default=60, help='Duração da coleta em segundos (0 para indefinido, padrão: 60)')
    parser.add_argument('--append', '-a', action='store_true', help='Anexar ao arquivo existente em vez de sobrescrevê-lo')
    parser.add_argument('--scenario', '-s', choices=['normal', 'alert', 'failure', 'all'], 
                        help='Cenário de simulação (normal, alert, failure, all)')
    parser.add_argument('--output-dir', default='data', help='Diretório para salvar os arquivos de saída (padrão: data)')
    
    args = parser.parse_args()
    
    # Se um cenário específico foi solicitado
    if args.scenario:
        if args.scenario == 'all':
            # Coleta dados para todos os cenários
            print("Coletando dados para todos os cenários...")
            
            # Coleta para cenário normal
            collect_scenario(args.port, args.baud, 'normal', args.duration, args.output_dir)
            
            # Coleta para cenário de alerta
            collect_scenario(args.port, args.baud, 'alert', args.duration, args.output_dir)
            
            # Coleta para cenário de falha
            collect_scenario(args.port, args.baud, 'failure', args.duration, args.output_dir)
            
            print("\nColeta para todos os cenários concluída.")
        else:
            # Coleta dados para o cenário especificado
            collect_scenario(args.port, args.baud, args.scenario, args.duration, args.output_dir)
    else:
        # Coleta dados normalmente
        collect_data(args.port, args.baud, args.duration, args.output, args.append)

if __name__ == "__main__":
    main()