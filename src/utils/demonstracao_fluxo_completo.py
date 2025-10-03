#!/usr/bin/env python3
"""
Demonstração do Fluxo Completo - Sistema IoT Monitoring
Enterprise Challenge Sprint 3 - Reply

Este script demonstra o fluxo completo de dados desde a coleta ESP32
até a visualização de resultados (gráficos, métricas e alertas).
"""

import json
import time
import random
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from typing import Dict, List, Any
import warnings
warnings.filterwarnings('ignore')

# Configurações
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class DemonstracaoFluxoCompleto:
    """Demonstração completa do fluxo de dados IoT"""
    
    def __init__(self):
        self.dados_coletados = []
        self.dados_processados = []
        self.alertas_gerados = []
        self.metricas_calculadas = {}
        self.timestamp_inicio = datetime.now()
        
        # Configurações de simulação
        self.num_dispositivos = 3
        self.num_sensores_por_dispositivo = 6
        self.duracao_simulacao = 60  # segundos
        
        print("🚀 Iniciando Demonstração do Fluxo Completo IoT Monitoring")
        print("=" * 60)
    
    def etapa_1_coleta_dados_esp32(self):
        """ETAPA 1: Simulação da coleta de dados do ESP32"""
        print("\n📡 ETAPA 1: Coleta de Dados ESP32")
        print("-" * 40)
        
        # Simular sensores ESP32
        sensores = {
            'DHT22': {'temp': (15, 35), 'umidade': (30, 80)},
            'LDR': {'luminosidade': (0, 1000)},
            'PIR': {'movimento': (0, 1)},
            'Pressao': {'pressao': (950, 1050)},
            'Vibracao': {'vibracao_x': (-2, 2), 'vibracao_y': (-2, 2), 'vibracao_z': (-2, 2)},
            'Nivel': {'nivel': (0, 100)}
        }
        
        print("🔌 Simulando sensores ESP32...")
        for i in range(10):  # 10 leituras de exemplo
            timestamp = datetime.now() - timedelta(seconds=random.randint(0, 300))
            dispositivo_id = f"ESP32_{random.randint(1, self.num_dispositivos):03d}"
            
            leitura = {
                'timestamp': timestamp.isoformat(),
                'dispositivo_id': dispositivo_id,
                'sensores': {}
            }
            
            # Simular leituras de cada sensor
            for sensor, ranges in sensores.items():
                for parametro, (min_val, max_val) in ranges.items():
                    # Adicionar variação realística
                    base_value = random.uniform(min_val, max_val)
                    # Adicionar tendência temporal
                    trend = np.sin(i * 0.5) * (max_val - min_val) * 0.1
                    valor = base_value + trend + random.gauss(0, (max_val - min_val) * 0.05)
                    valor = max(min_val, min(max_val, valor))  # Clamp
                    
                    leitura['sensores'][parametro] = round(valor, 2)
            
            # Adicionar qualidade da leitura
            leitura['qualidade'] = random.uniform(0.7, 1.0)
            leitura['bateria'] = random.uniform(20, 100)
            
            self.dados_coletados.append(leitura)
            
            print(f"  📊 {dispositivo_id}: Temp={leitura['sensores']['temp']:.1f}°C, "
                  f"Umidade={leitura['sensores']['umidade']:.1f}%, "
                  f"Luz={leitura['sensores']['luminosidade']:.0f}lx")
        
        print(f"✅ Coletados {len(self.dados_coletados)} registros de sensores")
        return self.dados_coletados
    
    def etapa_2_transmissao_mqtt(self):
        """ETAPA 2: Simulação da transmissão MQTT"""
        print("\n📡 ETAPA 2: Transmissão MQTT")
        print("-" * 40)
        
        print("🌐 Simulando envio via MQTT...")
        for i, leitura in enumerate(self.dados_coletados):
            # Simular tópico MQTT
            topico = f"industrial/sensors/{leitura['dispositivo_id']}/data"
            
            # Simular payload MQTT
            payload = {
                'topic': topico,
                'qos': 1,
                'retain': False,
                'payload': json.dumps(leitura),
                'timestamp': datetime.now().isoformat()
            }
            
            print(f"  📤 Tópico: {topico}")
            print(f"     Payload: {json.dumps(leitura, indent=2)[:100]}...")
            
            # Simular latência de rede
            time.sleep(0.1)
        
        print("✅ Dados transmitidos via MQTT com sucesso")
        return True
    
    def etapa_3_processamento_pipeline(self):
        """ETAPA 3: Processamento no Pipeline Integrado"""
        print("\n⚙️ ETAPA 3: Processamento no Pipeline")
        print("-" * 40)
        
        print("🔄 Processando dados no pipeline...")
        
        for leitura in self.dados_coletados:
            # Validação de dados
            if self._validar_dados(leitura):
                # Enriquecimento de dados
                dados_enriquecidos = self._enriquecer_dados(leitura)
                
                # Cálculo de features derivadas
                features_derivadas = self._calcular_features_derivadas(dados_enriquecidos)
                
                # Detecção de anomalias básica
                anomalia_detectada = self._detectar_anomalia_basica(dados_enriquecidos)
                
                dados_processados = {
                    **dados_enriquecidos,
                    'features_derivadas': features_derivadas,
                    'anomalia_detectada': anomalia_detectada,
                    'timestamp_processamento': datetime.now().isoformat()
                }
                
                self.dados_processados.append(dados_processados)
                
                status = "🚨 ANOMALIA" if anomalia_detectada else "✅ Normal"
                print(f"  {status} {leitura['dispositivo_id']}: "
                      f"Temp={dados_enriquecidos['sensores']['temp']:.1f}°C, "
                      f"Anomalia={anomalia_detectada}")
        
        print(f"✅ Processados {len(self.dados_processados)} registros")
        return self.dados_processados
    
    def etapa_4_persistencia_banco(self):
        """ETAPA 4: Persistência no Banco de Dados"""
        print("\n💾 ETAPA 4: Persistência no Banco")
        print("-" * 40)
        
        # Criar banco SQLite para demonstração
        conn = sqlite3.connect(':memory:')
        self._criar_tabelas_demo(conn)
        
        print("🗄️ Persistindo dados no banco...")
        
        for dados in self.dados_processados:
            # Inserir dispositivo
            self._inserir_dispositivo(conn, dados)
            
            # Inserir leituras
            self._inserir_leituras(conn, dados)
            
            # Inserir alertas se houver anomalia
            if dados['anomalia_detectada']:
                self._inserir_alerta(conn, dados)
        
        # Calcular métricas do banco
        self._calcular_metricas_banco(conn)
        
        print("✅ Dados persistidos com sucesso")
        print(f"📊 Métricas calculadas: {len(self.metricas_calculadas)}")
        
        conn.close()
        return True
    
    def etapa_5_inferencia_ml(self):
        """ETAPA 5: Inferência de Machine Learning"""
        print("\n🤖 ETAPA 5: Inferência Machine Learning")
        print("-" * 40)
        
        print("🧠 Executando inferência ML...")
        
        # Preparar dados para ML
        df_ml = self._preparar_dados_ml()
        
        # Simular modelo treinado
        modelo_resultados = self._simular_modelo_ml(df_ml)
        
        # Calcular métricas de performance
        self._calcular_metricas_ml(modelo_resultados)
        
        print("✅ Inferência ML concluída")
        print(f"📈 Acurácia: {self.metricas_calculadas.get('acuracia_ml', 0):.2%}")
        print(f"🎯 Precisão: {self.metricas_calculadas.get('precisao_ml', 0):.2%}")
        
        return modelo_resultados
    
    def etapa_6_visualizacao_resultados(self):
        """ETAPA 6: Visualização de Resultados"""
        print("\n📊 ETAPA 6: Visualização de Resultados")
        print("-" * 40)
        
        print("📈 Gerando visualizações...")
        
        # Criar gráficos
        self._criar_grafico_temperatura()
        self._criar_grafico_anomalias()
        self._criar_dashboard_kpis()
        self._criar_grafico_correlacao()
        
        print("✅ Visualizações geradas com sucesso")
        return True
    
    def etapa_7_alertas_notificacoes(self):
        """ETAPA 7: Sistema de Alertas e Notificações"""
        print("\n🚨 ETAPA 7: Sistema de Alertas")
        print("-" * 40)
        
        print("🔔 Gerando alertas e notificações...")
        
        # Analisar dados para alertas
        self._analisar_alertas()
        
        # Gerar notificações
        self._gerar_notificacoes()
        
        print("✅ Sistema de alertas ativado")
        return True
    
    def executar_demonstracao_completa(self):
        """Executa a demonstração completa do fluxo"""
        print("\n🎯 EXECUTANDO DEMONSTRAÇÃO COMPLETA")
        print("=" * 60)
        
        try:
            # Executar todas as etapas
            self.etapa_1_coleta_dados_esp32()
            self.etapa_2_transmissao_mqtt()
            self.etapa_3_processamento_pipeline()
            self.etapa_4_persistencia_banco()
            self.etapa_5_inferencia_ml()
            self.etapa_6_visualizacao_resultados()
            self.etapa_7_alertas_notificacoes()
            
            # Resumo final
            self._mostrar_resumo_final()
            
        except Exception as e:
            print(f"❌ Erro na demonstração: {e}")
            return False
        
        return True
    
    def _validar_dados(self, leitura: Dict) -> bool:
        """Valida dados de entrada"""
        try:
            # Verificar campos obrigatórios
            campos_obrigatorios = ['timestamp', 'dispositivo_id', 'sensores']
            for campo in campos_obrigatorios:
                if campo not in leitura:
                    return False
            
            # Verificar qualidade mínima
            if leitura.get('qualidade', 0) < 0.5:
                return False
            
            return True
        except:
            return False
    
    def _enriquecer_dados(self, leitura: Dict) -> Dict:
        """Enriquece dados com informações adicionais"""
        dados_enriquecidos = leitura.copy()
        
        # Adicionar metadados
        dados_enriquecidos['versao_protocolo'] = '1.0'
        dados_enriquecidos['regiao'] = 'Sul'
        dados_enriquecidos['tipo_ambiente'] = 'Industrial'
        
        # Adicionar timestamp de processamento
        dados_enriquecidos['timestamp_processamento'] = datetime.now().isoformat()
        
        return dados_enriquecidos
    
    def _calcular_features_derivadas(self, dados: Dict) -> Dict:
        """Calcula features derivadas para ML"""
        sensores = dados['sensores']
        
        features = {
            'temp_umidade_ratio': sensores['temp'] / (sensores['umidade'] + 1),
            'luminosidade_normalizada': sensores['luminosidade'] / 1000,
            'vibracao_magnitude': np.sqrt(
                sensores['vibracao_x']**2 + 
                sensores['vibracao_y']**2 + 
                sensores['vibracao_z']**2
            ),
            'pressao_normalizada': (sensores['pressao'] - 950) / 100,
            'nivel_normalizado': sensores['nivel'] / 100
        }
        
        return features
    
    def _detectar_anomalia_basica(self, dados: Dict) -> bool:
        """Detecção básica de anomalias"""
        sensores = dados['sensores']
        
        # Thresholds para detecção de anomalias
        thresholds = {
            'temp': (10, 40),
            'umidade': (20, 90),
            'luminosidade': (0, 1200),
            'pressao': (940, 1060)
        }
        
        # Verificar se algum valor está fora dos thresholds
        for parametro, (min_val, max_val) in thresholds.items():
            if parametro in sensores:
                if sensores[parametro] < min_val or sensores[parametro] > max_val:
                    return True
        
        return False
    
    def _criar_tabelas_demo(self, conn):
        """Cria tabelas para demonstração"""
        cursor = conn.cursor()
        
        # Tabela dispositivos
        cursor.execute('''
            CREATE TABLE dispositivos (
                id TEXT PRIMARY KEY,
                nome TEXT,
                tipo TEXT,
                localizacao TEXT,
                status TEXT,
                ultima_atualizacao TIMESTAMP
            )
        ''')
        
        # Tabela leituras
        cursor.execute('''
            CREATE TABLE leituras_sensores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dispositivo_id TEXT,
                timestamp TIMESTAMP,
                temperatura REAL,
                umidade REAL,
                luminosidade REAL,
                movimento INTEGER,
                pressao REAL,
                vibracao_x REAL,
                vibracao_y REAL,
                vibracao_z REAL,
                nivel REAL,
                qualidade REAL,
                anomalia_detectada BOOLEAN,
                FOREIGN KEY (dispositivo_id) REFERENCES dispositivos(id)
            )
        ''')
        
        # Tabela alertas
        cursor.execute('''
            CREATE TABLE alertas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dispositivo_id TEXT,
                timestamp TIMESTAMP,
                tipo TEXT,
                severidade TEXT,
                descricao TEXT,
                resolvido BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (dispositivo_id) REFERENCES dispositivos(id)
            )
        ''')
        
        conn.commit()
    
    def _inserir_dispositivo(self, conn, dados: Dict):
        """Insere dispositivo no banco"""
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO dispositivos 
            (id, nome, tipo, localizacao, status, ultima_atualizacao)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            dados['dispositivo_id'],
            f"Dispositivo {dados['dispositivo_id']}",
            'ESP32',
            'Sala Industrial',
            'Ativo',
            dados['timestamp']
        ))
        
        conn.commit()
    
    def _inserir_leituras(self, conn, dados: Dict):
        """Insere leituras no banco"""
        cursor = conn.cursor()
        
        sensores = dados['sensores']
        
        cursor.execute('''
            INSERT INTO leituras_sensores 
            (dispositivo_id, timestamp, temperatura, umidade, luminosidade, 
             movimento, pressao, vibracao_x, vibracao_y, vibracao_z, nivel, 
             qualidade, anomalia_detectada)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            dados['dispositivo_id'],
            dados['timestamp'],
            sensores['temp'],
            sensores['umidade'],
            sensores['luminosidade'],
            sensores['movimento'],
            sensores['pressao'],
            sensores['vibracao_x'],
            sensores['vibracao_y'],
            sensores['vibracao_z'],
            sensores['nivel'],
            dados['qualidade'],
            dados['anomalia_detectada']
        ))
        
        conn.commit()
    
    def _inserir_alerta(self, conn, dados: Dict):
        """Insere alerta no banco"""
        cursor = conn.cursor()
        
        # Determinar tipo de alerta baseado nos valores
        sensores = dados['sensores']
        tipo_alerta = "Temperatura Alta" if sensores['temp'] > 30 else "Anomalia Detectada"
        severidade = "Alta" if sensores['temp'] > 35 else "Média"
        
        cursor.execute('''
            INSERT INTO alertas 
            (dispositivo_id, timestamp, tipo, severidade, descricao)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            dados['dispositivo_id'],
            dados['timestamp'],
            tipo_alerta,
            severidade,
            f"Anomalia detectada: {tipo_alerta} - Temp: {sensores['temp']:.1f}°C"
        ))
        
        conn.commit()
    
    def _calcular_metricas_banco(self, conn):
        """Calcula métricas do banco"""
        cursor = conn.cursor()
        
        # Total de leituras
        cursor.execute('SELECT COUNT(*) FROM leituras_sensores')
        total_leituras = cursor.fetchone()[0]
        
        # Total de alertas
        cursor.execute('SELECT COUNT(*) FROM alertas')
        total_alertas = cursor.fetchone()[0]
        
        # Taxa de anomalias
        cursor.execute('SELECT COUNT(*) FROM leituras_sensores WHERE anomalia_detectada = 1')
        anomalias = cursor.fetchone()[0]
        taxa_anomalias = anomalias / total_leituras if total_leituras > 0 else 0
        
        self.metricas_calculadas.update({
            'total_leituras': total_leituras,
            'total_alertas': total_alertas,
            'taxa_anomalias': taxa_anomalias
        })
    
    def _preparar_dados_ml(self) -> pd.DataFrame:
        """Prepara dados para ML"""
        dados_ml = []
        
        for dados in self.dados_processados:
            sensores = dados['sensores']
            features = dados['features_derivadas']
            
            linha = {
                'temperatura': sensores['temp'],
                'umidade': sensores['umidade'],
                'luminosidade': sensores['luminosidade'],
                'pressao': sensores['pressao'],
                'vibracao_magnitude': features['vibracao_magnitude'],
                'temp_umidade_ratio': features['temp_umidade_ratio'],
                'luminosidade_normalizada': features['luminosidade_normalizada'],
                'pressao_normalizada': features['pressao_normalizada'],
                'nivel_normalizado': features['nivel_normalizado'],
                'qualidade': dados['qualidade'],
                'anomalia_real': dados['anomalia_detectada']
            }
            
            dados_ml.append(linha)
        
        return pd.DataFrame(dados_ml)
    
    def _simular_modelo_ml(self, df: pd.DataFrame) -> Dict:
        """Simula modelo ML treinado"""
        # Simular predições baseadas em regras simples
        predicoes = []
        probabilidades = []
        
        for _, row in df.iterrows():
            # Regra simples para simular modelo
            score = 0
            
            # Temperatura alta
            if row['temperatura'] > 30:
                score += 0.3
            
            # Umidade baixa
            if row['umidade'] < 40:
                score += 0.2
            
            # Vibração alta
            if row['vibracao_magnitude'] > 1.5:
                score += 0.3
            
            # Qualidade baixa
            if row['qualidade'] < 0.8:
                score += 0.2
            
            predicao = 1 if score > 0.5 else 0
            predicoes.append(predicao)
            probabilidades.append(score)
        
        return {
            'predicoes': predicoes,
            'probabilidades': probabilidades,
            'dados': df
        }
    
    def _calcular_metricas_ml(self, resultados: Dict):
        """Calcula métricas de performance do ML"""
        df = resultados['dados']
        predicoes = resultados['predicoes']
        
        # Calcular métricas
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        acuracia = accuracy_score(df['anomalia_real'], predicoes)
        precisao = precision_score(df['anomalia_real'], predicoes, zero_division=0)
        recall = recall_score(df['anomalia_real'], predicoes, zero_division=0)
        f1 = f1_score(df['anomalia_real'], predicoes, zero_division=0)
        
        self.metricas_calculadas.update({
            'acuracia_ml': acuracia,
            'precisao_ml': precisao,
            'recall_ml': recall,
            'f1_ml': f1
        })
    
    def _criar_grafico_temperatura(self):
        """Cria gráfico de temperatura"""
        plt.figure(figsize=(12, 6))
        
        # Preparar dados
        timestamps = [datetime.fromisoformat(d['timestamp']) for d in self.dados_processados]
        temperaturas = [d['sensores']['temp'] for d in self.dados_processados]
        dispositivos = [d['dispositivo_id'] for d in self.dados_processados]
        
        # Criar gráfico
        for dispositivo in set(dispositivos):
            mask = [d == dispositivo for d in dispositivos]
            plt.plot([timestamps[i] for i, m in enumerate(mask) if m],
                    [temperaturas[i] for i, m in enumerate(mask) if m],
                    marker='o', label=dispositivo, linewidth=2)
        
        plt.title('Temperatura ao Longo do Tempo', fontsize=16, fontweight='bold')
        plt.xlabel('Tempo')
        plt.ylabel('Temperatura (°C)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('grafico_temperatura_demo.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("📊 Gráfico de temperatura salvo: grafico_temperatura_demo.png")
    
    def _criar_grafico_anomalias(self):
        """Cria gráfico de anomalias"""
        plt.figure(figsize=(12, 6))
        
        # Preparar dados
        timestamps = [datetime.fromisoformat(d['timestamp']) for d in self.dados_processados]
        anomalias = [d['anomalia_detectada'] for d in self.dados_processados]
        temperaturas = [d['sensores']['temp'] for d in self.dados_processados]
        
        # Separar dados normais e anomalias
        normais = [(t, temp) for t, temp, anom in zip(timestamps, temperaturas, anomalias) if not anom]
        anomalias_data = [(t, temp) for t, temp, anom in zip(timestamps, temperaturas, anomalias) if anom]
        
        # Plotar dados normais
        if normais:
            plt.scatter([t for t, _ in normais], [temp for _, temp in normais], 
                       c='blue', alpha=0.6, label='Normal', s=50)
        
        # Plotar anomalias
        if anomalias_data:
            plt.scatter([t for t, _ in anomalias_data], [temp for _, temp in anomalias_data], 
                       c='red', alpha=0.8, label='Anomalia', s=100, marker='X')
        
        plt.title('Detecção de Anomalias - Temperatura', fontsize=16, fontweight='bold')
        plt.xlabel('Tempo')
        plt.ylabel('Temperatura (°C)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('grafico_anomalias_demo.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("🚨 Gráfico de anomalias salvo: grafico_anomalias_demo.png")
    
    def _criar_dashboard_kpis(self):
        """Cria dashboard com KPIs"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Dashboard KPIs - Sistema IoT Monitoring', fontsize=16, fontweight='bold')
        
        # KPI 1: Total de Leituras
        axes[0, 0].bar(['Total Leituras'], [self.metricas_calculadas.get('total_leituras', 0)], 
                      color='skyblue', alpha=0.7)
        axes[0, 0].set_title('Total de Leituras')
        axes[0, 0].set_ylabel('Quantidade')
        
        # KPI 2: Taxa de Anomalias
        taxa_anom = self.metricas_calculadas.get('taxa_anomalias', 0)
        axes[0, 1].pie([taxa_anom, 1-taxa_anom], labels=['Anomalias', 'Normal'], 
                      colors=['red', 'green'], autopct='%1.1f%%')
        axes[0, 1].set_title('Taxa de Anomalias')
        
        # KPI 3: Acurácia ML
        acuracia = self.metricas_calculadas.get('acuracia_ml', 0)
        axes[1, 0].bar(['Acurácia ML'], [acuracia], color='orange', alpha=0.7)
        axes[1, 0].set_title('Acurácia do Modelo ML')
        axes[1, 0].set_ylabel('Acurácia')
        axes[1, 0].set_ylim(0, 1)
        
        # KPI 4: Distribuição de Dispositivos
        dispositivos = [d['dispositivo_id'] for d in self.dados_processados]
        contagem = pd.Series(dispositivos).value_counts()
        axes[1, 1].bar(contagem.index, contagem.values, color='purple', alpha=0.7)
        axes[1, 1].set_title('Leituras por Dispositivo')
        axes[1, 1].set_ylabel('Quantidade')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('dashboard_kpis_demo.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("📊 Dashboard KPIs salvo: dashboard_kpis_demo.png")
    
    def _criar_grafico_correlacao(self):
        """Cria gráfico de correlação entre variáveis"""
        # Preparar dados
        dados_corr = []
        for d in self.dados_processados:
            sensores = d['sensores']
            features = d['features_derivadas']
            
            dados_corr.append({
                'Temperatura': sensores['temp'],
                'Umidade': sensores['umidade'],
                'Luminosidade': sensores['luminosidade'],
                'Pressão': sensores['pressao'],
                'Vibração': features['vibracao_magnitude'],
                'Qualidade': d['qualidade']
            })
        
        df_corr = pd.DataFrame(dados_corr)
        
        # Criar heatmap de correlação
        plt.figure(figsize=(10, 8))
        correlation_matrix = df_corr.corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=0.5)
        plt.title('Matriz de Correlação - Variáveis do Sistema', fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig('grafico_correlacao_demo.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("🔗 Gráfico de correlação salvo: grafico_correlacao_demo.png")
    
    def _analisar_alertas(self):
        """Analisa dados para gerar alertas"""
        print("🔍 Analisando dados para alertas...")
        
        # Contar alertas por tipo
        alertas_por_tipo = {}
        for dados in self.dados_processados:
            if dados['anomalia_detectada']:
                sensores = dados['sensores']
                
                if sensores['temp'] > 30:
                    alertas_por_tipo['Temperatura Alta'] = alertas_por_tipo.get('Temperatura Alta', 0) + 1
                
                if sensores['umidade'] < 40:
                    alertas_por_tipo['Umidade Baixa'] = alertas_por_tipo.get('Umidade Baixa', 0) + 1
                
                if sensores['luminosidade'] > 800:
                    alertas_por_tipo['Luminosidade Alta'] = alertas_por_tipo.get('Luminosidade Alta', 0) + 1
        
        self.alertas_gerados = alertas_por_tipo
        
        for tipo, quantidade in alertas_por_tipo.items():
            print(f"  🚨 {tipo}: {quantidade} ocorrências")
    
    def _gerar_notificacoes(self):
        """Gera notificações baseadas nos alertas"""
        print("📢 Gerando notificações...")
        
        total_alertas = sum(self.alertas_gerados.values())
        
        if total_alertas > 0:
            print(f"  🔔 {total_alertas} alertas gerados")
            print("  📧 Notificações enviadas para:")
            print("     - Email: admin@empresa.com")
            print("     - Slack: #iot-alerts")
            print("     - Teams: #monitoring")
        else:
            print("  ✅ Nenhum alerta crítico detectado")
    
    def _mostrar_resumo_final(self):
        """Mostra resumo final da demonstração"""
        print("\n" + "=" * 60)
        print("🎯 RESUMO FINAL DA DEMONSTRAÇÃO")
        print("=" * 60)
        
        print(f"📊 Dados Coletados: {len(self.dados_coletados)} leituras")
        print(f"⚙️ Dados Processados: {len(self.dados_processados)} registros")
        print(f"🚨 Alertas Gerados: {sum(self.alertas_gerados.values())} alertas")
        print(f"💾 Leituras Persistidas: {self.metricas_calculadas.get('total_leituras', 0)}")
        print(f"🤖 Acurácia ML: {self.metricas_calculadas.get('acuracia_ml', 0):.2%}")
        print(f"📈 Taxa de Anomalias: {self.metricas_calculadas.get('taxa_anomalias', 0):.2%}")
        
        print("\n📁 Arquivos Gerados:")
        print("  📊 grafico_temperatura_demo.png")
        print("  🚨 grafico_anomalias_demo.png")
        print("  📊 dashboard_kpis_demo.png")
        print("  🔗 grafico_correlacao_demo.png")
        
        print("\n✅ DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("🎉 Fluxo completo de dados demonstrado desde ESP32 até visualização!")


def main():
    """Função principal para executar a demonstração"""
    print("🚀 Sistema IoT Monitoring - Demonstração do Fluxo Completo")
    print("Enterprise Challenge Sprint 3 - Reply")
    print("=" * 60)
    
    # Criar instância da demonstração
    demo = DemonstracaoFluxoCompleto()
    
    # Executar demonstração completa
    sucesso = demo.executar_demonstracao_completa()
    
    if sucesso:
        print("\n🎯 Demonstração executada com sucesso!")
        print("📊 Verifique os gráficos gerados para visualizar os resultados.")
    else:
        print("\n❌ Erro na execução da demonstração.")


if __name__ == "__main__":
    main()
