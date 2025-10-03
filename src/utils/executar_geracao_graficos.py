#!/usr/bin/env python3
"""
Script para executar a geração completa de gráficos e resultados
Sistema de Detecção de Anomalias IoT
"""

import sys
import os
import subprocess
import time

def executar_script(script_path, descricao):
    """
    Executa um script Python e exibe o progresso
    """
    print(f"\n🔄 {descricao}")
    print("=" * 60)
    
    try:
        # Executar script
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ {descricao} - Concluído com sucesso!")
            if result.stdout:
                print("Saída:")
                print(result.stdout)
        else:
            print(f"❌ {descricao} - Erro!")
            if result.stderr:
                print("Erro:")
                print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {descricao} - Timeout (5 minutos)")
        return False
    except Exception as e:
        print(f"❌ {descricao} - Erro: {e}")
        return False
    
    return True

def verificar_arquivos_gerados():
    """
    Verifica se os arquivos foram gerados corretamente
    """
    print(f"\n🔍 Verificando arquivos gerados...")
    
    arquivos_esperados = [
        'grafico_1_matriz_confusao.png',
        'grafico_2_curva_roc.png',
        'grafico_3_precision_recall.png',
        'grafico_4_importancia_features.png',
        'grafico_5_distribuicao_predicoes.png',
        'grafico_6_metricas_performance.png',
        'grafico_7_analise_temporal.png',
        'grafico_8_correlacao_features.png',
        'relatorio_resultados_ml.md'
    ]
    
    arquivos_encontrados = []
    arquivos_faltando = []
    
    for arquivo in arquivos_esperados:
        if os.path.exists(arquivo):
            tamanho = os.path.getsize(arquivo)
            arquivos_encontrados.append((arquivo, tamanho))
        else:
            arquivos_faltando.append(arquivo)
    
    print(f"   📁 Arquivos encontrados: {len(arquivos_encontrados)}")
    for arquivo, tamanho in arquivos_encontrados:
        print(f"      ✅ {arquivo} ({tamanho:,} bytes)")
    
    if arquivos_faltando:
        print(f"   ❌ Arquivos faltando: {len(arquivos_faltando)}")
        for arquivo in arquivos_faltando:
            print(f"      ❌ {arquivo}")
    
    return len(arquivos_faltando) == 0

def main():
    """
    Função principal para executar a geração de gráficos
    """
    print("🚀 SISTEMA DE GERAÇÃO DE GRÁFICOS - MODELO ML IoT")
    print("=" * 70)
    print("Executando geração completa de gráficos e resultados...")
    
    # Script para executar
    script = "gerar_graficos_resultados_ml.py"
    descricao = "Geração de gráficos e resultados do modelo ML"
    
    if os.path.exists(script):
        if executar_script(script, descricao):
            print(f"✅ Script executado com sucesso!")
        else:
            print(f"❌ Falha na execução do script!")
            return
    else:
        print(f"❌ Arquivo não encontrado: {script}")
        return
    
    # Verificar arquivos gerados
    arquivos_ok = verificar_arquivos_gerados()
    
    # Resumo final
    print(f"\n📊 RESUMO DA EXECUÇÃO")
    print("=" * 50)
    print(f"Script executado: {'✅ Sim' if os.path.exists(script) else '❌ Não'}")
    print(f"Arquivos gerados: {'✅ Sim' if arquivos_ok else '❌ Não'}")
    
    if arquivos_ok:
        print("✅ Todos os gráficos e resultados gerados com sucesso!")
        print("\n🎯 SISTEMA COMPLETO E PRONTO!")
        print("   • 8 gráficos PNG de alta qualidade")
        print("   • 1 relatório detalhado em Markdown")
        print("   • Métricas de performance completas")
        print("   • Análise de features e correlações")
        
        # Listar arquivos gerados
        print(f"\n📁 GRÁFICOS GERADOS:")
        graficos = [
            "grafico_1_matriz_confusao.png",
            "grafico_2_curva_roc.png",
            "grafico_3_precision_recall.png",
            "grafico_4_importancia_features.png",
            "grafico_5_distribuicao_predicoes.png",
            "grafico_6_metricas_performance.png",
            "grafico_7_analise_temporal.png",
            "grafico_8_correlacao_features.png"
        ]
        
        for grafico in graficos:
            if os.path.exists(grafico):
                tamanho = os.path.getsize(grafico)
                print(f"   ✅ {grafico} ({tamanho:,} bytes)")
            else:
                print(f"   ❌ {grafico} (não encontrado)")
        
        print(f"\n📊 RELATÓRIOS GERADOS:")
        relatorios = [
            "relatorio_resultados_ml.md"
        ]
        
        for relatorio in relatorios:
            if os.path.exists(relatorio):
                tamanho = os.path.getsize(relatorio)
                print(f"   ✅ {relatorio} ({tamanho:,} bytes)")
            else:
                print(f"   ❌ {relatorio} (não encontrado)")
                
    else:
        print("❌ Alguns arquivos não foram gerados!")
        print("   Verifique os erros acima e tente novamente.")
    
    print(f"\n⏰ Tempo total de execução: {time.strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
