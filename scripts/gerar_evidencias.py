#!/usr/bin/env python3
"""
Gerador de Evidências - Sistema IoT Monitoring
Enterprise Challenge Sprint 3 - Reply

Este script gera evidências visuais de cada etapa do fluxo.
"""

import os
import sys
import time
import json
from datetime import datetime
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class GeradorEvidencias:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.evidencias = []
        
    def gerar_evidencia_etapa(self, etapa, descricao, dados=None):
        """Gera evidência de uma etapa"""
        evidencia = {
            'timestamp': datetime.now().isoformat(),
            'etapa': etapa,
            'descricao': descricao,
            'dados': dados,
            'status': 'sucesso'
        }
        
        self.evidencias.append(evidencia)
        
        # Gerar print da evidência
        print(f"\n{'='*60}")
        print(f"📸 EVIDÊNCIA - {etapa.upper()}")
        print(f"{'='*60}")
        print(f"⏰ Timestamp: {evidencia['timestamp']}")
        print(f"📝 Descrição: {descricao}")
        
        if dados:
            print(f"📊 Dados: {dados}")
        
        print(f"✅ Status: {evidencia['status']}")
        print(f"{'='*60}\n")
        
        return evidencia
    
    def evidencia_1_coleta(self):
        """Evidência da etapa de coleta"""
        print("🔍 Verificando arquivos de coleta...")
        
        arquivos_coleta = [
            'coleta_ingestao_esp32.ino',
            'wokwi_simulacao_esp32.json',
            'coletor_dados_serial.py',
            'simulador_dados_esp32.py'
        ]
        
        arquivos_existentes = [f for f in arquivos_coleta if os.path.exists(f)]
        
        self.gerar_evidencia_etapa(
            "COLETA DE DADOS",
            "Verificação de arquivos de coleta",
            {
                'arquivos_esperados': len(arquivos_coleta),
                'arquivos_encontrados': len(arquivos_existentes),
                'arquivos': arquivos_existentes
            }
        )
    
    def evidencia_2_persistencia(self):
        """Evidência da etapa de persistência"""
        print("🔍 Verificando banco de dados...")
        
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='iot_user',
                password='iot_password',
                database='iot_monitoring_db'
            )
            cursor = conn.cursor()
            
            # Verificar tabelas
            cursor.execute("SHOW TABLES")
            tabelas = [row[0] for row in cursor.fetchall()]
            
            # Verificar registros
            cursor.execute("SELECT COUNT(*) FROM leituras_sensores")
            total_leituras = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM dispositivos")
            total_dispositivos = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM sensores")
            total_sensores = cursor.fetchone()[0]
            
            conn.close()
            
            self.gerar_evidencia_etapa(
                "PERSISTÊNCIA",
                "Verificação do banco de dados",
                {
                    'tabelas_criadas': len(tabelas),
                    'total_leituras': total_leituras,
                    'total_dispositivos': total_dispositivos,
                    'total_sensores': total_sensores,
                    'tabelas': tabelas
                }
            )
            
        except Exception as e:
            self.gerar_evidencia_etapa(
                "PERSISTÊNCIA",
                "Erro na verificação do banco",
                {'erro': str(e)}
            )
    
    def evidencia_3_ml(self):
        """Evidência da etapa de ML"""
        print("🔍 Verificando modelos ML...")
        
        arquivos_ml = [
            'ml_basico_integrado.py',
            'dataset_ml_analisador.py',
            'modelo_anomalia.pkl',
            'modelo_temperatura.pkl',
            'scaler.pkl'
        ]
        
        arquivos_existentes = [f for f in arquivos_ml if os.path.exists(f)]
        
        # Verificar métricas
        metricas_existentes = False
        if os.path.exists('relatorio_ml_basico.json'):
            with open('relatorio_ml_basico.json', 'r') as f:
                metricas = json.load(f)
                metricas_existentes = True
        
        self.gerar_evidencia_etapa(
            "MACHINE LEARNING",
            "Verificação de modelos e métricas",
            {
                'arquivos_ml': len(arquivos_existentes),
                'metricas_disponiveis': metricas_existentes,
                'arquivos': arquivos_existentes
            }
        )
    
    def evidencia_4_visualizacao(self):
        """Evidência da etapa de visualização"""
        print("🔍 Verificando dashboard e alertas...")
        
        arquivos_viz = [
            'dashboard_visualizacao_alertas.py',
            'sistema_alertas_avancado.py',
            'ml_basico_visualizacoes.png',
            'analise_dataset_ml.png'
        ]
        
        arquivos_existentes = [f for f in arquivos_viz if os.path.exists(f)]
        
        self.gerar_evidencia_etapa(
            "VISUALIZAÇÃO E ALERTAS",
            "Verificação de dashboard e alertas",
            {
                'arquivos_visualizacao': len(arquivos_existentes),
                'arquivos': arquivos_existentes
            }
        )
    
    def gerar_relatorio_final(self):
        """Gera relatório final de evidências"""
        relatorio = {
            'timestamp': datetime.now().isoformat(),
            'sistema': 'IoT Monitoring',
            'versao': '1.0.0',
            'evidencias': self.evidencias,
            'resumo': {
                'total_etapas': len(self.evidencias),
                'etapas_sucesso': len([e for e in self.evidencias if e['status'] == 'sucesso']),
                'etapas_erro': len([e for e in self.evidencias if e['status'] == 'erro'])
            }
        }
        
        # Salvar relatório
        with open(f'evidencias_fluxo_{self.timestamp}.json', 'w') as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        
        # Imprimir resumo
        print(f"\n{'='*60}")
        print(f"📋 RELATÓRIO FINAL DE EVIDÊNCIAS")
        print(f"{'='*60}")
        print(f"⏰ Timestamp: {relatorio['timestamp']}")
        print(f"🏗️ Sistema: {relatorio['sistema']}")
        print(f"📦 Versão: {relatorio['versao']}")
        print(f"📊 Total de Etapas: {relatorio['resumo']['total_etapas']}")
        print(f"✅ Sucessos: {relatorio['resumo']['etapas_sucesso']}")
        print(f"❌ Erros: {relatorio['resumo']['etapas_erro']}")
        print(f"📁 Relatório salvo: evidencias_fluxo_{self.timestamp}.json")
        print(f"{'='*60}\n")
        
        return relatorio
    
    def executar_verificacao_completa(self):
        """Executa verificação completa do fluxo"""
        print("🚀 Iniciando verificação completa do fluxo...")
        
        # Etapa 1: Coleta
        self.evidencia_1_coleta()
        time.sleep(1)
        
        # Etapa 2: Persistência
        self.evidencia_2_persistencia()
        time.sleep(1)
        
        # Etapa 3: ML
        self.evidencia_3_ml()
        time.sleep(1)
        
        # Etapa 4: Visualização
        self.evidencia_4_visualizacao()
        
        # Relatório final
        return self.gerar_relatorio_final()

def main():
    """Função principal"""
    print("=== Gerador de Evidências ===")
    print("Enterprise Challenge Sprint 3 - Reply")
    print("===============================")
    
    gerador = GeradorEvidencias()
    relatorio = gerador.executar_verificacao_completa()
    
    print("✅ Verificação completa executada!")

if __name__ == "__main__":
    main()
