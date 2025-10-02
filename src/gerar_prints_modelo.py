#!/usr/bin/env python3
"""
Script para gerar prints e exportações gráficas do modelo de banco de dados
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np
import pandas as pd
from datetime import datetime
import json

def criar_diagrama_entidades():
    """Cria diagrama visual das entidades do banco"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Definir entidades e suas posições
    entidades = {
        'DISPOSITIVOS': {'pos': (1, 9), 'cor': '#E3F2FD', 'campos': 8},
        'TIPOS_SENSOR': {'pos': (6, 9), 'cor': '#F3E5F5', 'campos': 6},
        'SENSORES': {'pos': (11, 9), 'cor': '#E3F2FD', 'campos': 9},
        'LEITURAS_SENSORES': {'pos': (1, 6), 'cor': '#E8F5E8', 'campos': 8},
        'ALERTAS': {'pos': (6, 6), 'cor': '#FFCDD2', 'campos': 10},
        'CONFIGURACOES_LIMITES': {'pos': (11, 6), 'cor': '#F3E5F5', 'campos': 8},
        'USUARIOS': {'pos': (1, 3), 'cor': '#FFF3E0', 'campos': 8},
        'LOGS_SISTEMA': {'pos': (6, 3), 'cor': '#E8F5E8', 'campos': 9},
        'DASHBOARDS': {'pos': (11, 3), 'cor': '#FFF3E0', 'campos': 7}
    }
    
    # Desenhar entidades
    for nome, info in entidades.items():
        x, y = info['pos']
        cor = info['cor']
        
        # Retângulo principal
        rect = FancyBboxPatch(
            (x, y), 3.5, 2,
            boxstyle="round,pad=0.1",
            facecolor=cor,
            edgecolor='black',
            linewidth=1.5
        )
        ax.add_patch(rect)
        
        # Nome da entidade
        ax.text(x + 1.75, y + 1.7, nome, 
                ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Linha separadora
        ax.plot([x + 0.2, x + 3.3], [y + 1.4, y + 1.4], 'k-', linewidth=1)
        
        # Campos da entidade (simplificado)
        campos = ['id', 'nome', 'status', 'timestamp', '...']
        for i, campo in enumerate(campos[:min(4, info['campos'])]):
            ax.text(x + 0.3, y + 1.2 - i*0.25, f"• {campo}", 
                    fontsize=8, va='center')
    
    # Título
    ax.text(8, 11.5, 'ENTIDADES DO BANCO DE DADOS IoT', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    # Legenda
    legend_elements = [
        patches.Patch(color='#E3F2FD', label='Entidades Principais'),
        patches.Patch(color='#F3E5F5', label='Configuração'),
        patches.Patch(color='#E8F5E8', label='Auditoria'),
        patches.Patch(color='#FFCDD2', label='Alertas'),
        patches.Patch(color='#FFF3E0', label='Interface')
    ]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    plt.tight_layout()
    plt.savefig('diagrama_entidades.png', dpi=300, bbox_inches='tight')
    plt.show()

def criar_diagrama_relacionamentos():
    """Cria diagrama focado nos relacionamentos"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Posições das entidades principais
    posicoes = {
        'DISPOSITIVOS': (2, 7),
        'SENSORES': (7, 7),
        'LEITURAS_SENSORES': (7, 4),
        'ALERTAS': (11, 4),
        'USUARIOS': (2, 4)
    }
    
    # Desenhar entidades
    for nome, (x, y) in posicoes.items():
        rect = FancyBboxPatch(
            (x, y), 2.5, 1.5,
            boxstyle="round,pad=0.1",
            facecolor='#E3F2FD',
            edgecolor='black',
            linewidth=2
        )
        ax.add_patch(rect)
        ax.text(x + 1.25, y + 0.75, nome, 
                ha='center', va='center', fontsize=11, fontweight='bold')
    
    # Desenhar relacionamentos
    relacionamentos = [
        # Dispositivos -> Sensores
        ((3.25, 7), (7, 7.75), '1', 'N', 'possui'),
        # Sensores -> Leituras
        ((7, 7), (8.25, 5.5), '1', 'N', 'gera'),
        # Leituras -> Alertas
        ((7, 4), (11, 4.75), '1', 'N', 'gera'),
        # Usuarios -> Leituras
        ((2, 4), (7, 4.75), '1', 'N', 'monitora'),
        # Dispositivos -> Alertas
        ((3.25, 7), (11, 5.5), '1', 'N', 'gera')
    ]
    
    for (x1, y1), (x2, y2), card1, card2, label in relacionamentos:
        # Linha do relacionamento
        ax.plot([x1, x2], [y1, y2], 'k-', linewidth=2, alpha=0.7)
        
        # Cardinalidades
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x - 0.2, mid_y, card1, fontsize=10, fontweight='bold',
                bbox=dict(boxstyle="circle,pad=0.1", facecolor='white'))
        ax.text(mid_x + 0.2, mid_y, card2, fontsize=10, fontweight='bold',
                bbox=dict(boxstyle="circle,pad=0.1", facecolor='white'))
        
        # Label do relacionamento
        ax.text(mid_x, mid_y + 0.3, label, fontsize=8, ha='center',
                bbox=dict(boxstyle="round,pad=0.2", facecolor='yellow', alpha=0.7))
    
    ax.text(7, 9.5, 'RELACIONAMENTOS PRINCIPAIS', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('diagrama_relacionamentos.png', dpi=300, bbox_inches='tight')
    plt.show()

def criar_estatisticas_tabelas():
    """Cria gráfico com estatísticas das tabelas"""
    
    # Dados das tabelas
    dados_tabelas = {
        'Tabela': ['DISPOSITIVOS', 'TIPOS_SENSOR', 'SENSORES', 'LEITURAS_SENSORES', 
                  'ALERTAS', 'CONFIGURACOES_LIMITES', 'USUARIOS', 'LOGS_SISTEMA', 
                  'DASHBOARDS', 'RELATORIOS'],
        'Campos': [8, 6, 9, 8, 10, 8, 8, 9, 7, 7],
        'FKs': [0, 0, 2, 1, 3, 1, 0, 1, 1, 1],
        'Índices': [2, 1, 3, 4, 3, 3, 3, 4, 3, 2]
    }
    
    df = pd.DataFrame(dados_tabelas)
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Gráfico 1: Número de campos por tabela
    ax1.barh(df['Tabela'], df['Campos'], color='skyblue')
    ax1.set_xlabel('Número de Campos')
    ax1.set_title('Campos por Tabela')
    ax1.grid(axis='x', alpha=0.3)
    
    # Gráfico 2: Chaves estrangeiras
    ax2.barh(df['Tabela'], df['FKs'], color='lightcoral')
    ax2.set_xlabel('Número de Chaves Estrangeiras')
    ax2.set_title('Chaves Estrangeiras por Tabela')
    ax2.grid(axis='x', alpha=0.3)
    
    # Gráfico 3: Índices
    ax3.barh(df['Tabela'], df['Índices'], color='lightgreen')
    ax3.set_xlabel('Número de Índices')
    ax3.set_title('Índices por Tabela')
    ax3.grid(axis='x', alpha=0.3)
    
    # Gráfico 4: Resumo geral
    categorias = ['Total Tabelas', 'Total Campos', 'Total FKs', 'Total Índices']
    valores = [len(df), df['Campos'].sum(), df['FKs'].sum(), df['Índices'].sum()]
    cores = ['gold', 'lightblue', 'lightcoral', 'lightgreen']
    
    ax4.pie(valores, labels=categorias, colors=cores, autopct='%1.1f%%', startangle=90)
    ax4.set_title('Resumo Geral do Banco de Dados')
    
    plt.suptitle('ESTATÍSTICAS DO BANCO DE DADOS IoT', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.savefig('estatisticas_tabelas.png', dpi=300, bbox_inches='tight')
    plt.show()

def criar_diagrama_fluxo_dados():
    """Cria diagrama de fluxo de dados"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Componentes do fluxo
    componentes = {
        'ESP32': {'pos': (1, 8), 'cor': '#FFE0B2', 'tipo': 'retangulo'},
        'Sensores': {'pos': (1, 6), 'cor': '#E1F5FE', 'tipo': 'retangulo'},
        'Coleta de Dados': {'pos': (4, 7), 'cor': '#F3E5F5', 'tipo': 'elipse'},
        'Validação': {'pos': (7, 7), 'cor': '#E8F5E8', 'tipo': 'elipse'},
        'Banco de Dados': {'pos': (10, 7), 'cor': '#E3F2FD', 'tipo': 'retangulo'},
        'Análise': {'pos': (13, 7), 'cor': '#FFF3E0', 'tipo': 'elipse'},
        'Alertas': {'pos': (10, 5), 'cor': '#FFCDD2', 'tipo': 'retangulo'},
        'Dashboard': {'pos': (13, 5), 'cor': '#F3E5F5', 'tipo': 'retangulo'},
        'Usuários': {'pos': (13, 3), 'cor': '#E8F5E8', 'tipo': 'retangulo'}
    }
    
    # Desenhar componentes
    for nome, info in componentes.items():
        x, y = info['pos']
        cor = info['cor']
        
        if info['tipo'] == 'retangulo':
            rect = FancyBboxPatch(
                (x, y), 2, 1,
                boxstyle="round,pad=0.1",
                facecolor=cor,
                edgecolor='black',
                linewidth=1.5
            )
            ax.add_patch(rect)
        else:  # elipse
            ellipse = patches.Ellipse(
                (x + 1, y + 0.5), 2, 1,
                facecolor=cor,
                edgecolor='black',
                linewidth=1.5
            )
            ax.add_patch(ellipse)
        
        ax.text(x + 1, y + 0.5, nome, 
                ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Desenhar fluxos
    fluxos = [
        ((2, 8), (2, 7)),  # ESP32 -> Sensores
        ((2, 6), (4, 7)),  # Sensores -> Coleta
        ((5, 7), (7, 7)),  # Coleta -> Validação
        ((8, 7), (10, 7)), # Validação -> BD
        ((11, 7), (13, 7)), # BD -> Análise
        ((10, 6), (10, 5)), # BD -> Alertas
        ((11, 7), (13, 5)), # BD -> Dashboard
        ((13, 6), (13, 4)), # Dashboard -> Usuários
        ((13, 6), (11, 5))  # Dashboard -> Alertas
    ]
    
    for (x1, y1), (x2, y2) in fluxos:
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', lw=2, color='blue', alpha=0.7))
    
    ax.text(8, 9.5, 'FLUXO DE DADOS - SISTEMA IoT', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('fluxo_dados.png', dpi=300, bbox_inches='tight')
    plt.show()

def gerar_relatorio_json():
    """Gera relatório em formato JSON"""
    
    relatorio = {
        "banco_dados": {
            "nome": "iot_monitoring_db",
            "versao": "1.0",
            "data_criacao": datetime.now().isoformat(),
            "sgbd": "MySQL 8.0+",
            "charset": "utf8mb4",
            "engine": "InnoDB"
        },
        "estatisticas": {
            "total_tabelas": 11,
            "total_campos": 89,
            "total_indices": 28,
            "total_foreign_keys": 12,
            "total_stored_procedures": 2,
            "total_triggers": 1,
            "total_views": 2
        },
        "tabelas": [
            {
                "nome": "dispositivos",
                "campos": 8,
                "indices": 2,
                "foreign_keys": 0,
                "tipo": "principal"
            },
            {
                "nome": "tipos_sensor",
                "campos": 6,
                "indices": 1,
                "foreign_keys": 0,
                "tipo": "configuracao"
            },
            {
                "nome": "sensores",
                "campos": 9,
                "indices": 3,
                "foreign_keys": 2,
                "tipo": "principal"
            },
            {
                "nome": "leituras_sensores",
                "campos": 8,
                "indices": 4,
                "foreign_keys": 1,
                "tipo": "principal",
                "particionada": True
            },
            {
                "nome": "alertas",
                "campos": 10,
                "indices": 3,
                "foreign_keys": 3,
                "tipo": "principal"
            },
            {
                "nome": "configuracoes_limites",
                "campos": 8,
                "indices": 3,
                "foreign_keys": 1,
                "tipo": "configuracao"
            },
            {
                "nome": "usuarios",
                "campos": 8,
                "indices": 3,
                "foreign_keys": 0,
                "tipo": "interface"
            },
            {
                "nome": "logs_sistema",
                "campos": 9,
                "indices": 4,
                "foreign_keys": 1,
                "tipo": "auditoria"
            },
            {
                "nome": "dashboards",
                "campos": 7,
                "indices": 3,
                "foreign_keys": 1,
                "tipo": "interface"
            },
            {
                "nome": "relatorios",
                "campos": 7,
                "indices": 2,
                "foreign_keys": 1,
                "tipo": "interface"
            }
        ],
        "relacionamentos_principais": [
            "DISPOSITIVOS (1) -> SENSORES (N)",
            "TIPOS_SENSOR (1) -> SENSORES (N)",
            "SENSORES (1) -> LEITURAS_SENSORES (N)",
            "SENSORES (1) -> CONFIGURACOES_LIMITES (N)",
            "DISPOSITIVOS (1) -> ALERTAS (N)",
            "SENSORES (1) -> ALERTAS (N)",
            "USUARIOS (1) -> LOGS_SISTEMA (N)",
            "USUARIOS (1) -> DASHBOARDS (N)",
            "USUARIOS (1) -> RELATORIOS (N)"
        ],
        "otimizacoes": {
            "particionamento": "leituras_sensores por ano",
            "indices_compostos": 3,
            "views_otimizadas": 2,
            "stored_procedures": 2,
            "triggers": 1
        },
        "integracao_visualizacao": {
            "grafana": "MySQL Data Source",
            "power_bi": "MySQL Connector",
            "tableau": "MySQL via ODBC",
            "dashboards_sugeridos": [
                "Monitoramento em tempo real",
                "Análise de tendências",
                "Alertas e notificações",
                "Status de dispositivos"
            ]
        }
    }
    
    # Salvar relatório JSON
    with open('relatorio_banco_dados.json', 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)
    
    print("Relatório JSON salvo como 'relatorio_banco_dados.json'")
    return relatorio

def main():
    """Função principal"""
    print("Gerando prints e exportações do modelo de banco de dados...")
    
    # Gerar diagramas
    print("1. Criando diagrama de entidades...")
    criar_diagrama_entidades()
    
    print("2. Criando diagrama de relacionamentos...")
    criar_diagrama_relacionamentos()
    
    print("3. Criando estatísticas das tabelas...")
    criar_estatisticas_tabelas()
    
    print("4. Criando diagrama de fluxo de dados...")
    criar_diagrama_fluxo_dados()
    
    print("5. Gerando relatório JSON...")
    relatorio = gerar_relatorio_json()
    
    print("\n✅ Todos os prints e exportações foram gerados com sucesso!")
    print("\nArquivos criados:")
    print("- diagrama_entidades.png")
    print("- diagrama_relacionamentos.png") 
    print("- estatisticas_tabelas.png")
    print("- fluxo_dados.png")
    print("- relatorio_banco_dados.json")
    
    print(f"\n📊 Resumo do banco de dados:")
    print(f"- {relatorio['estatisticas']['total_tabelas']} tabelas")
    print(f"- {relatorio['estatisticas']['total_campos']} campos")
    print(f"- {relatorio['estatisticas']['total_indices']} índices")
    print(f"- {relatorio['estatisticas']['total_foreign_keys']} chaves estrangeiras")

if __name__ == "__main__":
    main()
