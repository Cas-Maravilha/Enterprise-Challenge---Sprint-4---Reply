#!/usr/bin/env python3
"""
Gerador de Imagem do Diagrama ER
Sistema IoT Monitoring - Sprint 3
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np
import os

def criar_diagrama_er():
    """
    Cria diagrama ER visual usando matplotlib
    """
    print("🔄 GERANDO DIAGRAMA ER VISUAL")
    print("=" * 50)
    
    # Configurar figura
    fig, ax = plt.subplots(1, 1, figsize=(20, 16))
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 16)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Cores para as tabelas
    cores_tabelas = {
        'dispositivos': '#E3F2FD',
        'tipos_sensor': '#F3E5F5',
        'sensores': '#E8F5E8',
        'leituras_sensores': '#FFF3E0',
        'modos_operacao': '#FCE4EC',
        'alertas': '#FFEBEE',
        'configuracoes_limites': '#F1F8E9',
        'usuarios': '#E0F2F1',
        'logs_sistema': '#FFF8E1',
        'dashboards': '#E8EAF6',
        'relatorios': '#F3E5F5'
    }
    
    # Posições das tabelas (x, y, largura, altura)
    tabelas = {
        'dispositivos': (2, 12, 3, 2.5),
        'tipos_sensor': (8, 12, 3, 2.5),
        'sensores': (5, 8, 3, 2.5),
        'leituras_sensores': (5, 4, 3, 2.5),
        'modos_operacao': (12, 8, 3, 2.5),
        'alertas': (12, 4, 3, 2.5),
        'configuracoes_limites': (2, 8, 3, 2.5),
        'usuarios': (2, 4, 3, 2.5),
        'logs_sistema': (2, 0.5, 3, 2.5),
        'dashboards': (8, 4, 3, 2.5),
        'relatorios': (8, 0.5, 3, 2.5)
    }
    
    # Campos de cada tabela
    campos_tabelas = {
        'dispositivos': [
            'id_dispositivo (PK)',
            'nome',
            'mac_address (UK)',
            'ip_address',
            'localizacao',
            'status',
            'data_cadastro',
            'ultima_conexao',
            'versao_firmware',
            'observacoes'
        ],
        'tipos_sensor': [
            'id_tipo_sensor (PK)',
            'nome (UK)',
            'descricao',
            'unidade_medida',
            'faixa_min',
            'faixa_max',
            'precisao',
            'ativo',
            'data_cadastro'
        ],
        'sensores': [
            'id_sensor (PK)',
            'id_dispositivo (FK)',
            'id_tipo_sensor (FK)',
            'nome',
            'pino_analogico',
            'pino_digital',
            'calibracao_min',
            'calibracao_max',
            'status',
            'data_instalacao',
            'ultima_calibracao',
            'observacoes'
        ],
        'leituras_sensores': [
            'id_leitura (PK)',
            'id_sensor (FK)',
            'timestamp_unix',
            'timestamp_datetime',
            'valor_numerico',
            'valor_booleano',
            'valor_string',
            'qualidade_dados',
            'anomalia_detectada',
            'data_coleta'
        ],
        'modos_operacao': [
            'id_modo (PK)',
            'nome (UK)',
            'descricao',
            'cor_indicador',
            'ativo',
            'data_cadastro'
        ],
        'alertas': [
            'id_alerta (PK)',
            'id_dispositivo (FK)',
            'id_sensor (FK)',
            'id_modo (FK)',
            'tipo_alerta',
            'severidade',
            'titulo',
            'descricao',
            'valor_atual',
            'valor_limite',
            'timestamp_alerta',
            'status',
            'data_resolucao',
            'usuario_resolucao',
            'observacoes_resolucao'
        ],
        'configuracoes_limites': [
            'id_configuracao (PK)',
            'id_sensor (FK)',
            'tipo_limite',
            'valor_limite',
            'severidade',
            'ativo',
            'data_criacao',
            'data_atualizacao',
            'usuario_criacao',
            'observacoes'
        ],
        'usuarios': [
            'id_usuario (PK)',
            'nome',
            'email (UK)',
            'senha_hash',
            'perfil',
            'ativo',
            'data_cadastro',
            'ultimo_login',
            'token_reset_senha',
            'data_expiracao_token'
        ],
        'logs_sistema': [
            'id_log (PK)',
            'id_usuario (FK)',
            'acao',
            'tabela_afetada',
            'id_registro_afetado',
            'dados_anteriores',
            'dados_novos',
            'ip_origem',
            'user_agent',
            'timestamp_log'
        ],
        'dashboards': [
            'id_dashboard (PK)',
            'id_usuario (FK)',
            'nome',
            'descricao',
            'configuracoes',
            'publico',
            'ativo',
            'data_criacao',
            'data_atualizacao'
        ],
        'relatorios': [
            'id_relatorio (PK)',
            'id_usuario (FK)',
            'nome',
            'tipo_relatorio',
            'configuracoes',
            'frequencia',
            'ativo',
            'proxima_execucao',
            'data_criacao'
        ]
    }
    
    # Desenhar tabelas
    for nome_tabela, (x, y, w, h) in tabelas.items():
        # Desenhar retângulo da tabela
        rect = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.1",
            facecolor=cores_tabelas[nome_tabela],
            edgecolor='black',
            linewidth=2
        )
        ax.add_patch(rect)
        
        # Título da tabela
        ax.text(x + w/2, y + h - 0.3, nome_tabela.upper(), 
                ha='center', va='center', fontsize=12, fontweight='bold')
        
        # Linha separadora
        ax.plot([x + 0.1, x + w - 0.1], [y + h - 0.5, y + h - 0.5], 
                'k-', linewidth=1)
        
        # Campos da tabela
        campos = campos_tabelas[nome_tabela]
        for i, campo in enumerate(campos):
            y_campo = y + h - 0.7 - (i * 0.25)
            if y_campo > y + 0.2:  # Só desenha se couber na tabela
                ax.text(x + 0.2, y_campo, campo, 
                       ha='left', va='center', fontsize=9)
    
    # Relacionamentos
    relacionamentos = [
        # Dispositivos -> Sensores (1:N)
        ('dispositivos', 'sensores', '1', 'N'),
        # Tipos Sensor -> Sensores (1:N)
        ('tipos_sensor', 'sensores', '1', 'N'),
        # Sensores -> Leituras Sensores (1:N)
        ('sensores', 'leituras_sensores', '1', 'N'),
        # Dispositivos -> Alertas (1:N)
        ('dispositivos', 'alertas', '1', 'N'),
        # Sensores -> Alertas (1:N)
        ('sensores', 'alertas', '1', 'N'),
        # Modos Operacao -> Alertas (1:N)
        ('modos_operacao', 'alertas', '1', 'N'),
        # Sensores -> Configuracoes Limites (1:N)
        ('sensores', 'configuracoes_limites', '1', 'N'),
        # Usuarios -> Logs Sistema (1:N)
        ('usuarios', 'logs_sistema', '1', 'N'),
        # Usuarios -> Dashboards (1:N)
        ('usuarios', 'dashboards', '1', 'N'),
        # Usuarios -> Relatorios (1:N)
        ('usuarios', 'relatorios', '1', 'N')
    ]
    
    # Desenhar relacionamentos
    for tabela_origem, tabela_destino, card_origem, card_destino in relacionamentos:
        if tabela_origem in tabelas and tabela_destino in tabelas:
            x1, y1, w1, h1 = tabelas[tabela_origem]
            x2, y2, w2, h2 = tabelas[tabela_destino]
            
            # Calcular pontos de conexão
            if x1 < x2:  # Tabela origem à esquerda
                x_start = x1 + w1
                y_start = y1 + h1/2
                x_end = x2
                y_end = y2 + h1/2 if abs(y1 - y2) < 2 else y2 + h2/2
            else:  # Tabela origem à direita
                x_start = x1
                y_start = y1 + h1/2
                x_end = x2 + w2
                y_end = y2 + h1/2 if abs(y1 - y2) < 2 else y2 + h2/2
            
            # Desenhar linha de relacionamento
            ax.plot([x_start, x_end], [y_start, y_end], 'k-', linewidth=2, alpha=0.7)
            
            # Desenhar cardinalidades
            mid_x = (x_start + x_end) / 2
            mid_y = (y_start + y_end) / 2
            
            # Cardinalidade origem
            ax.text(x_start + 0.2, y_start + 0.2, card_origem, 
                   ha='center', va='center', fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.2", facecolor='white', edgecolor='black'))
            
            # Cardinalidade destino
            ax.text(x_end - 0.2, y_end - 0.2, card_destino, 
                   ha='center', va='center', fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.2", facecolor='white', edgecolor='black'))
    
    # Título do diagrama
    ax.text(10, 15.5, 'DIAGRAMA ENTIDADE-RELACIONAMENTO', 
            ha='center', va='center', fontsize=20, fontweight='bold')
    ax.text(10, 15, 'Sistema IoT Monitoring - Sprint 3', 
            ha='center', va='center', fontsize=14, style='italic')
    
    # Legenda
    legenda_x = 16
    legenda_y = 12
    ax.text(legenda_x, legenda_y, 'LEGENDA:', 
            ha='left', va='center', fontsize=12, fontweight='bold')
    
    legenda_items = [
        'PK = Primary Key',
        'FK = Foreign Key', 
        'UK = Unique Key',
        '1 = Um',
        'N = Muitos'
    ]
    
    for i, item in enumerate(legenda_items):
        ax.text(legenda_x, legenda_y - 0.5 - (i * 0.3), item, 
                ha='left', va='center', fontsize=10)
    
    # Informações do banco
    info_x = 16
    info_y = 8
    ax.text(info_x, info_y, 'INFORMAÇÕES:', 
            ha='left', va='center', fontsize=12, fontweight='bold')
    
    info_items = [
        '11 Tabelas Principais',
        '10 Relacionamentos',
        'Suporte a Múltiplos SGBDs',
        'Índices Otimizados',
        'Triggers Automáticos',
        'Views para Consultas',
        'Stored Procedures'
    ]
    
    for i, item in enumerate(info_items):
        ax.text(info_x, info_y - 0.5 - (i * 0.3), f'• {item}', 
                ha='left', va='center', fontsize=10)
    
    plt.tight_layout()
    return fig

def salvar_diagrama(fig, nome_arquivo='diagrama_er_iot.png'):
    """
    Salva o diagrama em arquivo
    """
    print(f"💾 Salvando diagrama como: {nome_arquivo}")
    
    # Salvar em alta resolução
    fig.savefig(nome_arquivo, dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    print(f"✅ Diagrama salvo com sucesso!")
    return nome_arquivo

def criar_diagrama_simplificado():
    """
    Cria versão simplificada do diagrama ER
    """
    print("\n🔄 GERANDO DIAGRAMA ER SIMPLIFICADO")
    print("=" * 50)
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Tabelas principais em posições mais compactas
    tabelas_principais = {
        'dispositivos': (2, 9, 2.5, 2),
        'sensores': (6, 9, 2.5, 2),
        'leituras_sensores': (10, 9, 2.5, 2),
        'alertas': (6, 6, 2.5, 2),
        'usuarios': (2, 6, 2.5, 2),
        'tipos_sensor': (10, 6, 2.5, 2),
        'modos_operacao': (2, 3, 2.5, 2),
        'configuracoes_limites': (6, 3, 2.5, 2),
        'logs_sistema': (10, 3, 2.5, 2)
    }
    
    # Cores
    cores = ['#E3F2FD', '#E8F5E8', '#FFF3E0', '#FFEBEE', 
             '#E0F2F1', '#F3E5F5', '#FCE4EC', '#F1F8E9', '#FFF8E1']
    
    for i, (nome, (x, y, w, h)) in enumerate(tabelas_principais.items()):
        # Desenhar tabela
        rect = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.1",
            facecolor=cores[i % len(cores)],
            edgecolor='black',
            linewidth=1.5
        )
        ax.add_patch(rect)
        
        # Nome da tabela
        ax.text(x + w/2, y + h - 0.3, nome.upper(), 
                ha='center', va='center', fontsize=11, fontweight='bold')
        
        # Linha separadora
        ax.plot([x + 0.1, x + w - 0.1], [y + h - 0.5, y + h - 0.5], 
                'k-', linewidth=1)
        
        # Campos principais
        campos_principais = {
            'dispositivos': ['id_dispositivo (PK)', 'nome', 'mac_address', 'status'],
            'sensores': ['id_sensor (PK)', 'id_dispositivo (FK)', 'nome', 'status'],
            'leituras_sensores': ['id_leitura (PK)', 'id_sensor (FK)', 'timestamp', 'valor'],
            'alertas': ['id_alerta (PK)', 'id_dispositivo (FK)', 'severidade', 'status'],
            'usuarios': ['id_usuario (PK)', 'nome', 'email', 'perfil'],
            'tipos_sensor': ['id_tipo_sensor (PK)', 'nome', 'unidade_medida'],
            'modos_operacao': ['id_modo (PK)', 'nome', 'cor_indicador'],
            'configuracoes_limites': ['id_configuracao (PK)', 'id_sensor (FK)', 'valor_limite'],
            'logs_sistema': ['id_log (PK)', 'id_usuario (FK)', 'acao', 'timestamp']
        }
        
        campos = campos_principais.get(nome, [])
        for j, campo in enumerate(campos):
            y_campo = y + h - 0.7 - (j * 0.25)
            if y_campo > y + 0.2:
                ax.text(x + 0.2, y_campo, campo, 
                       ha='left', va='center', fontsize=8)
    
    # Relacionamentos principais
    relacionamentos_principais = [
        ('dispositivos', 'sensores'),
        ('tipos_sensor', 'sensores'),
        ('sensores', 'leituras_sensores'),
        ('dispositivos', 'alertas'),
        ('sensores', 'alertas'),
        ('usuarios', 'logs_sistema')
    ]
    
    for tabela_origem, tabela_destino in relacionamentos_principais:
        if tabela_origem in tabelas_principais and tabela_destino in tabelas_principais:
            x1, y1, w1, h1 = tabelas_principais[tabela_origem]
            x2, y2, w2, h2 = tabelas_principais[tabela_destino]
            
            # Conectar bordas das tabelas
            x_start = x1 + w1
            y_start = y1 + h1/2
            x_end = x2
            y_end = y2 + h2/2
            
            ax.plot([x_start, x_end], [y_start, y_end], 'k-', linewidth=1.5, alpha=0.6)
    
    # Título
    ax.text(8, 11.5, 'DIAGRAMA ER - SISTEMA IoT MONITORING', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    return fig

def main():
    """
    Função principal
    """
    print("🚀 GERADOR DE DIAGRAMA ER - SISTEMA IoT MONITORING")
    print("=" * 60)
    
    try:
        # Criar diagrama completo
        fig_completo = criar_diagrama_er()
        arquivo_completo = salvar_diagrama(fig_completo, 'diagrama_er_completo.png')
        
        # Criar diagrama simplificado
        fig_simplificado = criar_diagrama_simplificado()
        arquivo_simplificado = salvar_diagrama(fig_simplificado, 'diagrama_er_simplificado.png')
        
        print(f"\n✅ DIAGRAMAS GERADOS COM SUCESSO!")
        print(f"📁 Arquivos criados:")
        print(f"   • {arquivo_completo} - Diagrama ER completo")
        print(f"   • {arquivo_simplificado} - Diagrama ER simplificado")
        
        print(f"\n📊 Características dos diagramas:")
        print(f"   • Resolução: 300 DPI (alta qualidade)")
        print(f"   • Formato: PNG")
        print(f"   • Cores: Esquema profissional")
        print(f"   • Relacionamentos: Cardinalidades indicadas")
        print(f"   • Legenda: Incluída no diagrama")
        
        print(f"\n🎯 Pronto para uso em documentação!")
        
    except Exception as e:
        print(f"❌ Erro ao gerar diagramas: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
