#!/usr/bin/env python3
"""
Script para executar a geração completa dos datasets CSV
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
        'datasets/iot_sensor_data_completo.csv',
        'datasets/iot_sensor_data_treino.csv',
        'datasets/iot_sensor_data_teste.csv',
        'datasets/iot_sensor_data_ml.csv',
        'datasets/iot_sensor_data_anomalias.csv',
        'datasets/iot_sensor_data_normais.csv',
        'datasets/relatorio_dataset.md'
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
    Função principal para executar a geração de datasets CSV
    """
    print("🚀 SISTEMA DE GERAÇÃO DE DATASETS CSV - IoT MONITORING")
    print("=" * 70)
    print("Executando geração completa de datasets...")
    
    # Lista de scripts para executar
    scripts = [
        ("gerar_dataset_csv_ml.py", "Geração de datasets CSV"),
        ("treinar_com_csv.py", "Treinamento do modelo com CSV")
    ]
    
    sucessos = 0
    total_scripts = len(scripts)
    
    for script, descricao in scripts:
        if os.path.exists(script):
            if executar_script(script, descricao):
                sucessos += 1
            else:
                print(f"⚠️ Falha em: {script}")
        else:
            print(f"❌ Arquivo não encontrado: {script}")
    
    # Verificar arquivos gerados
    arquivos_ok = verificar_arquivos_gerados()
    
    # Resumo final
    print(f"\n📊 RESUMO DA EXECUÇÃO")
    print("=" * 50)
    print(f"Scripts executados: {sucessos}/{total_scripts}")
    print(f"Arquivos gerados: {'✅ Sim' if arquivos_ok else '❌ Não'}")
    
    if sucessos == total_scripts and arquivos_ok:
        print("✅ Todos os scripts executados com sucesso!")
        print("\n🎯 SISTEMA COMPLETO E PRONTO!")
        print("   • Datasets CSV gerados")
        print("   • Modelo treinado com dados CSV")
        print("   • Arquivos de resultado gerados")
        print("   • Sistema pronto para uso")
        
        # Listar datasets gerados
        print(f"\n📁 DATASETS GERADOS:")
        datasets = [
            "iot_sensor_data_completo.csv",
            "iot_sensor_data_treino.csv", 
            "iot_sensor_data_teste.csv",
            "iot_sensor_data_ml.csv",
            "iot_sensor_data_anomalias.csv",
            "iot_sensor_data_normais.csv"
        ]
        
        for dataset in datasets:
            caminho = f"datasets/{dataset}"
            if os.path.exists(caminho):
                tamanho = os.path.getsize(caminho)
                print(f"   ✅ {dataset} ({tamanho:,} bytes)")
            else:
                print(f"   ❌ {dataset} (não encontrado)")
        
        print(f"\n📊 ARQUIVOS DE RESULTADO:")
        resultados = [
            "resultados_modelo_csv.png",
            "modelo_anomalia_csv.pkl",
            "relatorio_dataset.md"
        ]
        
        for resultado in resultados:
            caminho = f"datasets/{resultado}" if resultado.endswith('.md') else resultado
            if os.path.exists(caminho):
                tamanho = os.path.getsize(caminho)
                print(f"   ✅ {resultado} ({tamanho:,} bytes)")
            else:
                print(f"   ❌ {resultado} (não encontrado)")
                
    else:
        print("❌ Alguns scripts falharam ou arquivos não foram gerados!")
        print("   Verifique os erros acima e tente novamente.")
    
    print(f"\n⏰ Tempo total de execução: {time.strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
