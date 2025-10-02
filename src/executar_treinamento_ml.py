#!/usr/bin/env python3
"""
Script para executar o treinamento completo do modelo de ML
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

def main():
    """
    Função principal para executar o treinamento completo
    """
    print("🚀 SISTEMA DE MACHINE LEARNING - DETECÇÃO DE ANOMALIAS IoT")
    print("=" * 70)
    print("Executando treinamento completo do modelo...")
    
    # Lista de scripts para executar
    scripts = [
        ("ml_anomaly_detection_completo.py", "Treinamento do modelo de ML"),
        ("usar_modelo_ml.py", "Teste do modelo treinado")
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
    
    # Resumo final
    print(f"\n📊 RESUMO DA EXECUÇÃO")
    print("=" * 50)
    print(f"Scripts executados: {sucessos}/{total_scripts}")
    
    if sucessos == total_scripts:
        print("✅ Todos os scripts executados com sucesso!")
        print("\n🎯 SISTEMA COMPLETO E PRONTO!")
        print("   • Modelo de ML treinado")
        print("   • Arquivos de resultado gerados")
        print("   • Sistema pronto para uso")
        
        # Listar arquivos gerados
        print(f"\n📁 ARQUIVOS GERADOS:")
        arquivos_gerados = [
            "modelo_anomalia_iot_completo.pkl",
            "resultados_modelo_ml_completo.png",
            "ML_Anomaly_Detection_IoT_Completo.ipynb"
        ]
        
        for arquivo in arquivos_gerados:
            if os.path.exists(arquivo):
                print(f"   ✅ {arquivo}")
            else:
                print(f"   ❌ {arquivo} (não encontrado)")
                
    else:
        print("❌ Alguns scripts falharam!")
        print("   Verifique os erros acima e tente novamente.")
    
    print(f"\n⏰ Tempo total de execução: {time.strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
