#!/usr/bin/env python3
"""
Script para gerar gráficos dos dados simulados dos sensores
"""
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

def carregar_dados(arquivo):
    """Carrega dados do arquivo JSON"""
    with open(arquivo, 'r') as f:
        return json.load(f)

def gerar_grafico_temperatura_umidade(dados, output_dir):
    """Gera gráfico de temperatura e umidade"""
    plt.figure(figsize=(12, 6))
    
    # Extrai dados
    temp = dados['sensores']['dht22']['temperatura']
    umid = dados['sensores']['dht22']['umidade']
    
    # Cria subplots
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    
    # Plota temperatura
    ax1.plot([0], [temp], 'r-o', label='Temperatura')
    ax1.set_ylabel('Temperatura (°C)', color='r')
    ax1.tick_params(axis='y', labelcolor='r')
    ax1.set_ylim(15, 35)
    
    # Plota umidade
    ax2.plot([0], [umid], 'b-o', label='Umidade')
    ax2.set_ylabel('Umidade (%)', color='b')
    ax2.tick_params(axis='y', labelcolor='b')
    ax2.set_ylim(30, 90)
    
    # Configurações do gráfico
    plt.title('Temperatura e Umidade')
    plt.grid(True)
    
    # Adiciona legenda
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    
    # Salva o gráfico
    plt.savefig(os.path.join(output_dir, 'temperatura_umidade.png'))
    plt.close()

def gerar_grafico_luminosidade(dados, output_dir):
    """Gera gráfico de luminosidade"""
    plt.figure(figsize=(12, 6))
    
    # Extrai dados
    luz = dados['sensores']['ldr']['luminosidade']
    
    # Plota luminosidade
    plt.plot([0], [luz], 'g-o')
    plt.ylabel('Luminosidade (0-1023)')
    plt.title('Nível de Luminosidade')
    plt.grid(True)
    plt.ylim(0, 1023)
    
    # Salva o gráfico
    plt.savefig(os.path.join(output_dir, 'luminosidade.png'))
    plt.close()

def gerar_grafico_movimento(dados, output_dir):
    """Gera gráfico de detecção de movimento"""
    plt.figure(figsize=(12, 6))
    
    # Extrai dados
    movimento = dados['sensores']['pir']['movimento']
    
    # Plota movimento
    plt.plot([0], [movimento], 'k-o')
    plt.ylabel('Movimento (0=Não, 1=Sim)')
    plt.title('Detecção de Movimento')
    plt.grid(True)
    plt.ylim(-0.1, 1.1)
    
    # Salva o gráfico
    plt.savefig(os.path.join(output_dir, 'movimento.png'))
    plt.close()

def gerar_grafico_correlacao(dados, output_dir):
    """Gera gráfico de correlação entre temperatura e umidade"""
    plt.figure(figsize=(8, 8))
    
    # Extrai dados
    temp = dados['sensores']['dht22']['temperatura']
    umid = dados['sensores']['dht22']['umidade']
    
    # Plota correlação
    plt.scatter(temp, umid, c='purple', alpha=0.6)
    plt.xlabel('Temperatura (°C)')
    plt.ylabel('Umidade (%)')
    plt.title('Correlação: Temperatura vs Umidade')
    plt.grid(True)
    
    # Adiciona linha de tendência
    z = np.polyfit([temp], [umid], 1)
    p = np.poly1d(z)
    plt.plot([15, 35], p([15, 35]), "r--", alpha=0.8)
    
    # Salva o gráfico
    plt.savefig(os.path.join(output_dir, 'correlacao.png'))
    plt.close()

def main():
    # Cria diretório para gráficos
    output_dir = 'graficos'
    os.makedirs(output_dir, exist_ok=True)
    
    # Carrega dados
    dados = carregar_dados('data/ultima_leitura.json')
    
    # Gera gráficos
    gerar_grafico_temperatura_umidade(dados, output_dir)
    gerar_grafico_luminosidade(dados, output_dir)
    gerar_grafico_movimento(dados, output_dir)
    gerar_grafico_correlacao(dados, output_dir)
    
    print(f"Gráficos gerados com sucesso em: {output_dir}/")

if __name__ == '__main__':
    main() 