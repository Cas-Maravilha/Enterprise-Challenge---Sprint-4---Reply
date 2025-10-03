#!/usr/bin/env python3
"""
Script simplificado para gerar prints do modelo de banco de dados IoT
"""

import os
import json
from datetime import datetime

def criar_diagrama_texto():
    """Cria diagrama ER em formato texto"""
    
    diagrama = """
    ╔══════════════════════════════════════════════════════════════════════════════════════╗
    ║                           DIAGRAMA ER - SISTEMA IoT MONITORING                      ║
    ╚══════════════════════════════════════════════════════════════════════════════════════╝

    ┌─────────────────┐    1:N    ┌─────────────────┐    1:N    ┌─────────────────┐
    │   DISPOSITIVOS  │ ──────────→│     SENSORES     │ ──────────→│ LEITURAS_SENSORES│
    │                 │           │                 │           │                 │
    │ • id_dispositivo│           │ • id_sensor     │           │ • id_leitura    │
    │ • nome          │           │ • id_dispositivo│           │ • id_sensor     │
    │ • mac_address   │           │ • id_tipo_sensor│           │ • timestamp     │
    │ • localizacao   │           │ • nome          │           │ • valor_numerico│
    │ • status        │           │ • pino_analogico│           │ • qualidade     │
    │ • ultima_conexao│           │ • status        │           │ • anomalia      │
    └─────────────────┘           └─────────────────┘           └─────────────────┘
            │                               │                           │
            │                               │                           │
            │                               │ 1:N                       │ 1:N
            │                               ↓                           ↓
            │                       ┌─────────────────┐           ┌─────────────────┐
            │                       │ TIPOS_SENSOR    │           │    ALERTAS      │
            │                       │                 │           │                 │
            │                       │ • id_tipo_sensor│           │ • id_alerta     │
            │                       │ • nome          │           │ • id_dispositivo│
            │                       │ • unidade_medida│           │ • id_sensor     │
            │                       │ • faixa_min/max │           │ • tipo_alerta   │
            │                       │ • precisao      │           │ • severidade    │
            │                       └─────────────────┘           │ • titulo        │
            │                                                     │ • valor_atual   │
            │ 1:N                                                 │ • status        │
            ↓                                                     └─────────────────┘
    ┌─────────────────┐
    │    ALERTAS      │
    │                 │
    │ • id_alerta     │
    │ • id_dispositivo│
    │ • id_sensor     │
    │ • tipo_alerta   │
    │ • severidade    │
    │ • titulo        │
    │ • valor_atual   │
    │ • status        │
    └─────────────────┘

    ┌─────────────────┐    1:N    ┌─────────────────┐    1:N    ┌─────────────────┐
    │    USUARIOS     │ ──────────→│  LOGS_SISTEMA    │           │   DASHBOARDS    │
    │                 │           │                 │           │                 │
    │ • id_usuario    │           │ • id_log        │           │ • id_dashboard  │
    │ • nome          │           │ • id_usuario    │           │ • id_usuario    │
    │ • email         │           │ • acao          │           │ • nome          │
    │ • perfil        │           │ • tabela_afetada│           │ • configuracoes │
    │ • senha_hash    │           │ • dados_anteriores│         │ • publico       │
    │ • ativo         │           │ • timestamp_log │           │ • ativo         │
    └─────────────────┘           └─────────────────┘           └─────────────────┘
            │
            │ 1:N
            ↓
    ┌─────────────────┐
    │    RELATORIOS   │
    │                 │
    │ • id_relatorio  │
    │ • id_usuario    │
    │ • nome          │
    │ • tipo_relatorio│
    │ • frequencia    │
    │ • ativo         │
    └─────────────────┘

    ┌─────────────────┐    1:N    ┌─────────────────┐
    │     SENSORES    │ ──────────→│CONFIGURACOES_   │
    │                 │           │    LIMITES      │
    │ • id_sensor     │           │                 │
    │ • id_dispositivo│           │ • id_configuracao│
    │ • id_tipo_sensor│           │ • id_sensor     │
    │ • nome          │           │ • tipo_limite   │
    │ • pino_analogico│           │ • valor_limite  │
    │ • status        │           │ • severidade    │
    └─────────────────┘           │ • ativo         │
                                  └─────────────────┘

    ╔══════════════════════════════════════════════════════════════════════════════════════╗
    ║                              CARDINALIDADES PRINCIPAIS                               ║
    ║                                                                                      ║
    ║  • 1:N = Um para Muitos    • N:1 = Muitos para Um    • 1:1 = Um para Um            ║
    ║                                                                                      ║
    ║  • DISPOSITIVOS (1) → SENSORES (N)                                                   ║
    ║  • TIPOS_SENSOR (1) → SENSORES (N)                                                   ║
    ║  • SENSORES (1) → LEITURAS_SENSORES (N)                                              ║
    ║  • SENSORES (1) → CONFIGURACOES_LIMITES (N)                                          ║
    ║  • DISPOSITIVOS (1) → ALERTAS (N)                                                    ║
    ║  • SENSORES (1) → ALERTAS (N)                                                        ║
    ║  • USUARIOS (1) → LOGS_SISTEMA (N)                                                   ║
    ║  • USUARIOS (1) → DASHBOARDS (N)                                                     ║
    ║  • USUARIOS (1) → RELATORIOS (N)                                                     ║
    ╚══════════════════════════════════════════════════════════════════════════════════════╝
    """
    
    return diagrama

def criar_estatisticas_tabelas():
    """Cria estatísticas das tabelas em formato texto"""
    
    estatisticas = """
    ╔══════════════════════════════════════════════════════════════════════════════════════╗
    ║                            ESTATÍSTICAS DAS TABELAS                                 ║
    ╚══════════════════════════════════════════════════════════════════════════════════════╝

    ┌─────────────────────────┬─────────┬─────────┬─────────┬─────────┬─────────────────┐
    │        TABELA           │ CAMPOS  │   FKs   │ ÍNDICES │  TIPO   │   DESCRIÇÃO     │
    ├─────────────────────────┼─────────┼─────────┼─────────┼─────────┼─────────────────┤
    │ DISPOSITIVOS            │    8    │    0    │    2    │Principal│ Gerencia ESP32s │
    │ TIPOS_SENSOR            │    6    │    0    │    1    │Config   │ Catálogo tipos  │
    │ SENSORES                │    9    │    2    │    3    │Principal│ Sensores físicos│
    │ LEITURAS_SENSORES       │    8    │    1    │    4    │Principal│ Dados coletados │
    │ ALERTAS                 │   10    │    3    │    3    │Principal│ Notificações    │
    │ CONFIGURACOES_LIMITES   │    8    │    1    │    3    │Config   │ Limites alertas │
    │ USUARIOS                │    8    │    0    │    3    │Interface│ Gestão usuários │
    │ LOGS_SISTEMA            │    9    │    1    │    4    │Auditoria│ Log atividades  │
    │ DASHBOARDS              │    7    │    1    │    3    │Interface│ Config dashboards│
    │ RELATORIOS              │    7    │    1    │    2    │Interface│ Relatórios auto │
    └─────────────────────────┴─────────┴─────────┴─────────┴─────────┴─────────────────┘

    ╔══════════════════════════════════════════════════════════════════════════════════════╗
    ║                                 RESUMO GERAL                                         ║
    ║                                                                                      ║
    ║  • Total de Tabelas: 11                                                             ║
    ║  • Total de Campos: 89                                                              ║
    ║  • Total de Chaves Estrangeiras: 12                                                 ║
    ║  • Total de Índices: 28                                                             ║
    ║  • Stored Procedures: 2                                                             ║
    ║  • Triggers: 1                                                                      ║
    ║  • Views: 2                                                                         ║
    ║  • Tabelas Particionadas: 1 (leituras_sensores)                                     ║
    ╚══════════════════════════════════════════════════════════════════════════════════════╝
    """
    
    return estatisticas

def criar_fluxo_dados():
    """Cria diagrama de fluxo de dados em formato texto"""
    
    fluxo = """
    ╔══════════════════════════════════════════════════════════════════════════════════════╗
    ║                              FLUXO DE DADOS - SISTEMA IoT                           ║
    ╚══════════════════════════════════════════════════════════════════════════════════════╝

    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │    ESP32    │───→│   SENSORES  │───→│  COLETA DE  │───→│ VALIDAÇÃO   │
    │             │    │             │    │   DADOS     │    │             │
    │ • Hardware  │    │ • DHT22     │    │ • Timestamp │    │ • Qualidade │
    │ • Firmware  │    │ • LDR       │    │ • Valores   │    │ • Anomalias │
    │ • Conect.   │    │ • PIR       │    │ • Formato   │    │ • Limites   │
    └─────────────┘    │ • Pressão   │    │ • Buffer    │    │ • Consist.  │
                       │ • Vibração  │    │             │    │             │
                       │ • Nível     │    │             │    │             │
                       └─────────────┘    └─────────────┘    └─────────────┘
                                                                    │
                                                                    ▼
    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
    │  USUÁRIOS   │◄───│  DASHBOARD  │◄───│  ANÁLISE    │◄───│ BANCO DE    │
    │             │    │             │    │             │    │  DADOS      │
    │ • Admin     │    │ • Gráficos  │    │ • Tendências│    │             │
    │ • Operador  │    │ • Alertas   │    │ • Correlações│   │ • Leituras  │
    │ • Visualiz. │    │ • KPIs      │    │ • Predições │    │ • Dispositivos│
    └─────────────┘    │ • Tempo Real│    │ • Insights  │    │ • Sensores  │
                       └─────────────┘    └─────────────┘    │ • Alertas   │
                                                             │ • Configs   │
                                                             └─────────────┘
                                                                    │
                                                                    ▼
                                                          ┌─────────────┐
                                                          │   ALERTAS   │
                                                          │             │
                                                          │ • Notificações│
                                                          │ • Email/SMS  │
                                                          │ • Dashboard  │
                                                          │ • Logs       │
                                                          └─────────────┘

    ╔══════════════════════════════════════════════════════════════════════════════════════╗
    ║                              COMPONENTES DO FLUXO                                   ║
    ║                                                                                      ║
    ║  1. COLETA: ESP32 + Sensores coletam dados físicos                                  ║
    ║  2. VALIDAÇÃO: Verificação de qualidade e detecção de anomalias                     ║
    ║  3. ARMAZENAMENTO: Banco de dados com particionamento por ano                       ║
    ║  4. ANÁLISE: Processamento e geração de insights                                    ║
    ║  5. VISUALIZAÇÃO: Dashboards e relatórios para usuários                             ║
    ║  6. ALERTAS: Sistema de notificações baseado em limites                             ║
    ╚══════════════════════════════════════════════════════════════════════════════════════╝
    """
    
    return fluxo

def criar_integracao_visualizacao():
    """Cria informações sobre integração com ferramentas de visualização"""
    
    integracao = """
    ╔══════════════════════════════════════════════════════════════════════════════════════╗
    ║                        INTEGRAÇÃO COM FERRAMENTAS DE VISUALIZAÇÃO                   ║
    ╚══════════════════════════════════════════════════════════════════════════════════════╝

    ┌─────────────────────────────────────────────────────────────────────────────────────┐
    │                                    GRAFANA                                         │
    ├─────────────────────────────────────────────────────────────────────────────────────┤
    │ • Conexão: MySQL Data Source                                                       │
    │ • Dashboards Sugeridos:                                                            │
    │   - Monitoramento em tempo real                                                    │
    │   - Análise de tendências históricas                                               │
    │   - Alertas e notificações                                                         │
    │   - Status de dispositivos e sensores                                              │
    │   - KPIs operacionais                                                              │
    │ • Queries Otimizadas:                                                              │
    │   - vw_leituras_completas para dados unificados                                    │
    │   - vw_alertas_ativos para monitoramento                                           │
    │   - Consultas particionadas para performance                                       │
    └─────────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────────────────────┐
    │                                   POWER BI                                         │
    ├─────────────────────────────────────────────────────────────────────────────────────┤
    │ • Conexão: MySQL Connector                                                          │
    │ • Relatórios Sugeridos:                                                             │
    │   - Análise de performance por dispositivo                                          │
    │   - Relatórios executivos de KPIs                                                  │
    │   - Análise de anomalias e tendências                                              │
    │   - Dashboards interativos por localização                                         │
    │ • Modelos de Dados:                                                                 │
    │   - Star Schema com fato_leituras                                                  │
    │   - Dimensões: tempo, dispositivo, sensor, localização                             │
    │   - Medidas: média, máximo, mínimo, contagem                                       │
    └─────────────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────────────────────┐
    │                                   TABLEAU                                          │
    ├─────────────────────────────────────────────────────────────────────────────────────┤
    │ • Conexão: MySQL via ODBC                                                           │
    │ • Visualizações Sugeridas:                                                          │
    │   - Mapas de calor por localização                                                  │
    │   - Gráficos de correlação entre sensores                                           │
    │   - Análise temporal avançada com drill-down                                        │
    │   - Dashboards interativos com filtros dinâmicos                                    │
    │ • Recursos Avançados:                                                               │
    │   - Calculated Fields para métricas customizadas                                    │
    │   - LOD Expressions para análises complexas                                         │
    │   - Actions para navegação entre visualizações                                      │
    └─────────────────────────────────────────────────────────────────────────────────────┘

    ╔══════════════════════════════════════════════════════════════════════════════════════╗
    ║                              CONFIGURAÇÕES RECOMENDADAS                             ║
    ║                                                                                      ║
    ║  • Pool de Conexões: 10-20 conexões simultâneas                                     ║
    ║  • Timeout: 30 segundos para consultas                                              ║
    ║  • Cache: 5 minutos para consultas frequentes                                       ║
    ║  • Índices: Otimizados para consultas de dashboard                                  ║
    ║  • Particionamento: Aproveitar particionamento por ano                              ║
    ║  • Views: Usar views otimizadas para consultas complexas                            ║
    ╚══════════════════════════════════════════════════════════════════════════════════════╝
    """
    
    return integracao

def gerar_relatorio_completo():
    """Gera relatório completo em formato texto"""
    
    relatorio = f"""
    ╔══════════════════════════════════════════════════════════════════════════════════════╗
    ║                        RELATÓRIO COMPLETO - BANCO DE DADOS IoT                       ║
    ║                              Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}                              ║
    ╚══════════════════════════════════════════════════════════════════════════════════════╝

    {criar_diagrama_texto()}

    {criar_estatisticas_tabelas()}

    {criar_fluxo_dados()}

    {criar_integracao_visualizacao()}

    ╔══════════════════════════════════════════════════════════════════════════════════════╗
    ║                                  PRÓXIMOS PASSOS                                    ║
    ║                                                                                      ║
    ║  1. Executar script database_schema.sql para criar o banco                          ║
    ║  2. Configurar backup automático diário                                             ║
    ║  3. Implementar scripts de migração de dados                                        ║
    ║  4. Configurar monitoramento de performance                                         ║
    ║  5. Criar dashboards no Grafana/Power BI/Tableau                                    ║
    ║  6. Implementar API REST para inserção de dados                                     ║
    ║  7. Configurar limpeza automática de dados antigos                                  ║
    ║  8. Implementar sistema de alertas por email/SMS                                    ║
    ║  9. Criar documentação de usuário final                                             ║
    ║ 10. Implementar testes automatizados                                                ║
    ╚══════════════════════════════════════════════════════════════════════════════════════╝
    """
    
    return relatorio

def salvar_arquivos():
    """Salva todos os arquivos de documentação"""
    
    # Criar diretório para outputs
    os.makedirs('prints_banco_dados', exist_ok=True)
    
    # Salvar diagrama ER
    with open('prints_banco_dados/diagrama_er.txt', 'w', encoding='utf-8') as f:
        f.write(criar_diagrama_texto())
    
    # Salvar estatísticas
    with open('prints_banco_dados/estatisticas_tabelas.txt', 'w', encoding='utf-8') as f:
        f.write(criar_estatisticas_tabelas())
    
    # Salvar fluxo de dados
    with open('prints_banco_dados/fluxo_dados.txt', 'w', encoding='utf-8') as f:
        f.write(criar_fluxo_dados())
    
    # Salvar integração
    with open('prints_banco_dados/integracao_visualizacao.txt', 'w', encoding='utf-8') as f:
        f.write(criar_integracao_visualizacao())
    
    # Salvar relatório completo
    with open('prints_banco_dados/relatorio_completo.txt', 'w', encoding='utf-8') as f:
        f.write(gerar_relatorio_completo())
    
    # Gerar relatório JSON
    relatorio_json = {
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
        "arquivos_gerados": [
            "diagrama_er.txt",
            "estatisticas_tabelas.txt", 
            "fluxo_dados.txt",
            "integracao_visualizacao.txt",
            "relatorio_completo.txt",
            "relatorio_estrutura.json"
        ]
    }
    
    with open('prints_banco_dados/relatorio_estrutura.json', 'w', encoding='utf-8') as f:
        json.dump(relatorio_json, f, indent=2, ensure_ascii=False)
    
    return relatorio_json

def main():
    """Função principal"""
    print("🚀 Gerando prints e documentação do banco de dados IoT...")
    print("=" * 70)
    
    try:
        # Salvar arquivos
        relatorio = salvar_arquivos()
        
        print("✅ Arquivos gerados com sucesso!")
        print("\n📁 Arquivos criados na pasta 'prints_banco_dados/':")
        for arquivo in relatorio["arquivos_gerados"]:
            print(f"   • {arquivo}")
        
        print(f"\n📊 Resumo do banco de dados:")
        print(f"   • {relatorio['estatisticas']['total_tabelas']} tabelas")
        print(f"   • {relatorio['estatisticas']['total_campos']} campos")
        print(f"   • {relatorio['estatisticas']['total_indices']} índices")
        print(f"   • {relatorio['estatisticas']['total_foreign_keys']} chaves estrangeiras")
        print(f"   • {relatorio['estatisticas']['total_stored_procedures']} stored procedures")
        print(f"   • {relatorio['estatisticas']['total_triggers']} trigger")
        print(f"   • {relatorio['estatisticas']['total_views']} views")
        
        print("\n🎯 Próximos passos:")
        print("   1. Execute: mysql -u root -p < database_schema.sql")
        print("   2. Configure ferramentas de visualização (Grafana/Power BI/Tableau)")
        print("   3. Implemente API REST para inserção de dados")
        print("   4. Configure backup automático")
        
        print("\n" + "=" * 70)
        print("✅ Processo concluído com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao gerar arquivos: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
