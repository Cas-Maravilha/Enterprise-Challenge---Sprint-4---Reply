#!/usr/bin/env python3
"""
Script para gerar diagrama ER do banco de dados IoT
Usa matplotlib para criar visualização do diagrama
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def criar_diagrama_er():
    """Cria diagrama ER usando matplotlib"""
    
    # Configuração da figura
    fig, ax = plt.subplots(1, 1, figsize=(20, 16))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 16)
    ax.axis('off')
    
    # Cores para diferentes tipos de entidades
    cores = {
        'principal': '#E3F2FD',      # Azul claro
        'configuracao': '#F3E5F5',   # Roxo claro
        'auditoria': '#E8F5E8',      # Verde claro
        'interface': '#FFF3E0'       # Laranja claro
    }
    
    # Definir posições das entidades
    entidades = {
        'DISPOSITIVOS': {'pos': (2, 12), 'cor': cores['principal'], 'tamanho': (3, 2)},
        'TIPOS_SENSOR': {'pos': (8, 12), 'cor': cores['configuracao'], 'tamanho': (3, 2)},
        'SENSORES': {'pos': (5, 8), 'cor': cores['principal'], 'tamanho': (3, 2)},
        'LEITURAS_SENSORES': {'pos': (5, 4), 'cor': cores['principal'], 'tamanho': (4, 2)},
        'MODOS_OPERACAO': {'pos': (12, 8), 'cor': cores['configuracao'], 'tamanho': (3, 2)},
        'ALERTAS': {'pos': (12, 4), 'cor': cores['principal'], 'tamanho': (3, 2)},
        'CONFIGURACOES_LIMITES': {'pos': (2, 4), 'cor': cores['configuracao'], 'tamanho': (3, 2)},
        'USUARIOS': {'pos': (16, 12), 'cor': cores['interface'], 'tamanho': (3, 2)},
        'LOGS_SISTEMA': {'pos': (16, 8), 'cor': cores['auditoria'], 'tamanho': (3, 2)},
        'DASHBOARDS': {'pos': (16, 4), 'cor': cores['interface'], 'tamanho': (3, 2)},
        'RELATORIOS': {'pos': (16, 0), 'cor': cores['interface'], 'tamanho': (3, 2)}
    }
    
    # Desenhar entidades
    for nome, info in entidades.items():
        x, y = info['pos']
        w, h = info['tamanho']
        cor = info['cor']
        
        # Retângulo principal
        rect = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.1",
            facecolor=cor,
            edgecolor='black',
            linewidth=1.5
        )
        ax.add_patch(rect)
        
        # Nome da entidade
        ax.text(x + w/2, y + h - 0.3, nome, 
                ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Linha separadora
        ax.plot([x + 0.1, x + w - 0.1], [y + h - 0.6, y + h - 0.6], 
                'k-', linewidth=1)
    
    # Desenhar relacionamentos
    relacionamentos = [
        # Dispositivos -> Sensores
        ((3.5, 12), (6.5, 10), '1', 'N'),
        # Tipos_Sensor -> Sensores  
        ((9.5, 12), (6.5, 10), '1', 'N'),
        # Sensores -> Leituras_Sensores
        ((6.5, 8), (7, 6), '1', 'N'),
        # Sensores -> Configuracoes_Limites
        ((5, 8), (3.5, 6), '1', 'N'),
        # Dispositivos -> Alertas
        ((3.5, 12), (13.5, 6), '1', 'N'),
        # Sensores -> Alertas
        ((6.5, 8), (13.5, 6), '1', 'N'),
        # Modos_Operacao -> Alertas
        ((13.5, 8), (13.5, 6), '1', 'N'),
        # Usuarios -> Logs_Sistema
        ((17.5, 12), (17.5, 10), '1', 'N'),
        # Usuarios -> Dashboards
        ((17.5, 12), (17.5, 6), '1', 'N'),
        # Usuarios -> Relatorios
        ((17.5, 12), (17.5, 2), '1', 'N')
    ]
    
    for (x1, y1), (x2, y2), card1, card2 in relacionamentos:
        # Linha do relacionamento
        ax.plot([x1, x2], [y1, y2], 'k-', linewidth=1.5, alpha=0.7)
        
        # Cardinalidades
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x - 0.2, mid_y, card1, fontsize=8, fontweight='bold')
        ax.text(mid_x + 0.2, mid_y, card2, fontsize=8, fontweight='bold')
    
    # Título
    ax.text(10, 15.5, 'DIAGRAMA ER - SISTEMA IoT MONITORING', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    # Legenda
    legend_elements = [
        patches.Patch(color=cores['principal'], label='Entidades Principais'),
        patches.Patch(color=cores['configuracao'], label='Configuração'),
        patches.Patch(color=cores['auditoria'], label='Auditoria'),
        patches.Patch(color=cores['interface'], label='Interface/Usuário')
    ]
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    # Adicionar informações sobre cardinalidades
    ax.text(1, 1, 'Cardinalidades:\n• 1:N = Um para Muitos\n• N:1 = Muitos para Um', 
            fontsize=9, bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgray'))
    
    plt.tight_layout()
    plt.savefig('diagrama_er_visual.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Diagrama ER salvo como 'diagrama_er_visual.png'")

def criar_diagrama_simplificado():
    """Cria diagrama ER simplificado focado nas entidades principais"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Entidades principais
    entidades_principais = {
        'DISPOSITIVOS': {'pos': (2, 7), 'cor': '#E3F2FD'},
        'SENSORES': {'pos': (7, 7), 'cor': '#E3F2FD'},
        'LEITURAS_SENSORES': {'pos': (7, 4), 'cor': '#E3F2FD'},
        'ALERTAS': {'pos': (11, 4), 'cor': '#FFCDD2'},
        'USUARIOS': {'pos': (2, 4), 'cor': '#F3E5F5'}
    }
    
    # Desenhar entidades principais
    for nome, info in entidades_principais.items():
        x, y = info['pos']
        cor = info['cor']
        
        rect = FancyBboxPatch(
            (x, y), 2.5, 1.5,
            boxstyle="round,pad=0.1",
            facecolor=cor,
            edgecolor='black',
            linewidth=2
        )
        ax.add_patch(rect)
        ax.text(x + 1.25, y + 0.75, nome, 
                ha='center', va='center', fontsize=11, fontweight='bold')
    
    # Relacionamentos principais
    relacionamentos_principais = [
        ((3.25, 7), (7, 7.75), '1', 'N'),  # Dispositivos -> Sensores
        ((7, 7), (8.25, 5.5), '1', 'N'),   # Sensores -> Leituras
        ((7, 4), (11, 4.75), '1', 'N'),    # Leituras -> Alertas
        ((2, 4), (7, 4.75), '1', 'N'),     # Usuarios -> Leituras
    ]
    
    for (x1, y1), (x2, y2), card1, card2 in relacionamentos_principais:
        ax.plot([x1, x2], [y1, y2], 'k-', linewidth=2)
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x - 0.15, mid_y, card1, fontsize=10, fontweight='bold')
        ax.text(mid_x + 0.15, mid_y, card2, fontsize=10, fontweight='bold')
    
    ax.text(7, 9.5, 'DIAGRAMA ER SIMPLIFICADO - ENTIDADES PRINCIPAIS', 
            ha='center', va='center', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('diagrama_er_simplificado.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Diagrama ER simplificado salvo como 'diagrama_er_simplificado.png'")

if __name__ == "__main__":
    print("Gerando diagramas ER...")
    criar_diagrama_er()
    criar_diagrama_simplificado()
    print("Diagramas gerados com sucesso!")
