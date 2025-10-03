import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (confusion_matrix, accuracy_score, precision_score, 
                           recall_score, f1_score, roc_auc_score)
import datetime as dt

class KPIsNegocio:
    """Implementa KPIs de negócio para modelos de IA - Sistema IoT Monitoring Sprint 3"""
    
    def __init__(self, targets=None):
        # Valores-alvo para KPIs de negócio específicos do IoT
        self.targets = targets or {
            # KPIs de Performance do Modelo
            'accuracy': 0.95,          # Precisão do modelo (95%)
            'precision': 0.90,         # Precisão das anomalias (90%)
            'recall': 0.85,            # Cobertura das anomalias (85%)
            'f1_score': 0.87,          # F1-Score balanceado (87%)
            'auc': 0.95,               # Área sob a curva ROC (95%)
            
            # KPIs de Negócio
            'roi': 3.0,                # Retorno sobre investimento (300%)
            'custo_por_erro': 50.0,    # Custo médio por erro (R$ 50)
            'economia_recursos': 0.4,   # Economia de recursos (40%)
            'tempo_resposta': 0.2,     # Tempo de resposta (0.2s)
            'satisfacao_usuario': 4.5, # Satisfação do usuário (4.5/5)
            
            # KPIs Específicos do IoT
            'taxa_falsos_positivos': 0.05,  # Taxa de falsos positivos (5%)
            'taxa_falsos_negativos': 0.10,  # Taxa de falsos negativos (10%)
            'tempo_deteccao_anomalia': 2.0, # Tempo para detectar anomalia (2s)
            'disponibilidade_sistema': 0.99, # Disponibilidade do sistema (99%)
            'economia_manutencao': 0.35,    # Economia em manutenção (35%)
            
            # KPIs de Qualidade dos Dados
            'qualidade_dados': 0.95,   # Qualidade dos dados (95%)
            'completude_dados': 0.98,  # Completude dos dados (98%)
            'atualidade_dados': 0.90,  # Atualidade dos dados (90%)
        }
        
        # Histórico de KPIs
        self.historico = []
    
    def calcular_metricas_modelo_ml(self, y_true, y_pred, y_pred_proba=None):
        """
        Calcula métricas específicas do modelo de Machine Learning
        
        Args:
            y_true: Valores reais
            y_pred: Valores previstos
            y_pred_proba: Probabilidades das predições (opcional)
            
        Returns:
            dict: Métricas do modelo ML
        """
        # Métricas básicas
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
        
        # AUC se probabilidades disponíveis
        auc = roc_auc_score(y_true, y_pred_proba) if y_pred_proba is not None else None
        
        # Matriz de confusão
        cm = confusion_matrix(y_true, y_pred)
        if len(cm) == 2:  # Caso binário
            tn, fp, fn, tp = cm.ravel()
            
            # Taxas específicas
            taxa_fp = fp / (fp + tn) if (fp + tn) > 0 else 0
            taxa_fn = fn / (fn + tp) if (fn + tp) > 0 else 0
            
            # Especificidade
            especificidade = tn / (tn + fp) if (tn + fp) > 0 else 0
            
            return {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'auc': auc,
                'especificidade': especificidade,
                'taxa_falsos_positivos': taxa_fp,
                'taxa_falsos_negativos': taxa_fn,
                'verdadeiros_positivos': int(tp),
                'falsos_positivos': int(fp),
                'verdadeiros_negativos': int(tn),
                'falsos_negativos': int(fn)
            }
        else:
            return {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'auc': auc
            }
    
    def calcular_impacto_negocio_iot(self, y_true, y_pred, custo_fp=100, custo_fn=1000):
        """
        Calcula impacto de negócio específico para sistema IoT
        
        Args:
            y_true: Valores reais
            y_pred: Valores previstos
            custo_fp: Custo de falso positivo (alerta desnecessário)
            custo_fn: Custo de falso negativo (anomalia não detectada)
            
        Returns:
            dict: Impacto de negócio
        """
        cm = confusion_matrix(y_true, y_pred)
        
        if len(cm) == 2:
            tn, fp, fn, tp = cm.ravel()
            
            # Custos específicos do IoT
            custo_falsos_positivos = fp * custo_fp  # Alertas desnecessários
            custo_falsos_negativos = fn * custo_fn  # Anomalias não detectadas
            custo_total = custo_falsos_positivos + custo_falsos_negativos
            
            # Benefícios
            beneficio_deteccao_correta = tp * custo_fn  # Anomalias detectadas corretamente
            beneficio_nao_alerta_desnecessario = tn * custo_fp  # Normais não alertados
            
            # ROI específico do modelo
            roi_modelo = (beneficio_deteccao_correta + beneficio_nao_alerta_desnecessario) / custo_total if custo_total > 0 else 0
            
            return {
                'custo_falsos_positivos': custo_falsos_positivos,
                'custo_falsos_negativos': custo_falsos_negativos,
                'custo_total': custo_total,
                'beneficio_deteccao_correta': beneficio_deteccao_correta,
                'beneficio_nao_alerta_desnecessario': beneficio_nao_alerta_desnecessario,
                'roi_modelo': roi_modelo,
                'economia_total': beneficio_deteccao_correta + beneficio_nao_alerta_desnecessario - custo_total
            }
        else:
            return {'erro': 'Matriz de confusão não é 2x2'}
    
    def calcular_qualidade_dados_iot(self, df_sensores):
        """
        Calcula qualidade dos dados de sensores IoT
        
        Args:
            df_sensores: DataFrame com dados dos sensores
            
        Returns:
            dict: Métricas de qualidade dos dados
        """
        total_registros = len(df_sensores)
        
        # Completude
        registros_completos = df_sensores.dropna().shape[0]
        completude = registros_completos / total_registros if total_registros > 0 else 0
        
        # Atualidade (dados dos últimos 24h)
        if 'timestamp' in df_sensores.columns:
            df_sensores['timestamp'] = pd.to_datetime(df_sensores['timestamp'])
            agora = pd.Timestamp.now()
            dados_recentes = df_sensores[df_sensores['timestamp'] >= agora - pd.Timedelta(hours=24)]
            atualidade = len(dados_recentes) / total_registros if total_registros > 0 else 0
        else:
            atualidade = 0.5  # Valor padrão se não houver timestamp
        
        # Consistência (valores dentro de faixas esperadas)
        faixas_validas = {
            'temperature': (-40, 80),
            'humidity': (0, 100),
            'pressure': (0, 2),
            'luminosity': (0, 1023),
            'co2': (0, 5000),
            'noise': (30, 120)
        }
        
        consistencia_total = 0
        colunas_verificadas = 0
        
        for col, (min_val, max_val) in faixas_validas.items():
            if col in df_sensores.columns:
                valores_validos = ((df_sensores[col] >= min_val) & (df_sensores[col] <= max_val)).sum()
                consistencia_col = valores_validos / total_registros if total_registros > 0 else 0
                consistencia_total += consistencia_col
                colunas_verificadas += 1
        
        consistencia = consistencia_total / colunas_verificadas if colunas_verificadas > 0 else 0
        
        # Qualidade geral (média ponderada)
        qualidade_geral = (completude * 0.4 + atualidade * 0.3 + consistencia * 0.3)
        
        return {
            'completude_dados': completude,
            'atualidade_dados': atualidade,
            'consistencia_dados': consistencia,
            'qualidade_dados': qualidade_geral,
            'total_registros': total_registros,
            'registros_completos': registros_completos
        }
    
    def calcular_roi(self, custo_implementacao, economia_mensal, periodo_meses=12):
        """
        Calcula o ROI do modelo
        
        Args:
            custo_implementacao: Custo total de implementação
            economia_mensal: Economia mensal gerada pelo modelo
            periodo_meses: Período de análise em meses
            
        Returns:
            float: ROI calculado
        """
        beneficio_total = economia_mensal * periodo_meses
        roi = (beneficio_total - custo_implementacao) / custo_implementacao
        
        return roi
    
    def calcular_custo_erros(self, y_true, y_pred, custo_fp=100, custo_fn=500):
        """
        Calcula o custo dos erros do modelo
        
        Args:
            y_true: Valores reais
            y_pred: Valores previstos
            custo_fp: Custo de um falso positivo
            custo_fn: Custo de um falso negativo
            
        Returns:
            dict: Custos calculados
        """
        cm = confusion_matrix(y_true, y_pred)
        
        if len(cm) == 2:  # Caso binário
            tn, fp, fn, tp = cm.ravel()
            
            # Custos totais
            custo_falsos_positivos = fp * custo_fp
            custo_falsos_negativos = fn * custo_fn
            custo_total = custo_falsos_positivos + custo_falsos_negativos
            
            # Custo médio por erro
            total_erros = fp + fn
            custo_medio = custo_total / total_erros if total_erros > 0 else 0
            
            return {
                'custo_falsos_positivos': custo_falsos_positivos,
                'custo_falsos_negativos': custo_falsos_negativos,
                'custo_total': custo_total,
                'custo_medio_por_erro': custo_medio,
                'total_erros': total_erros
            }
        else:
            # Para problemas multiclasse, simplificamos para um custo médio
            n_erros = np.sum(y_true != y_pred)
            custo_total = n_erros * custo_fp  # Simplificação
            
            return {
                'custo_total': custo_total,
                'custo_medio_por_erro': custo_fp,
                'total_erros': n_erros
            }
    
    def calcular_economia_recursos(self, tempo_manual, tempo_automatizado, 
                                  custo_hora=50, n_operacoes=1000):
        """
        Calcula economia de recursos com o modelo
        
        Args:
            tempo_manual: Tempo médio para operação manual (horas)
            tempo_automatizado: Tempo médio com modelo (horas)
            custo_hora: Custo por hora de trabalho
            n_operacoes: Número de operações no período
            
        Returns:
            dict: Métricas de economia
        """
        # Tempo total
        tempo_total_manual = tempo_manual * n_operacoes
        tempo_total_auto = tempo_automatizado * n_operacoes
        
        # Economia de tempo
        economia_tempo = tempo_total_manual - tempo_total_auto
        
        # Economia financeira
        economia_financeira = economia_tempo * custo_hora
        
        # Percentual de economia
        pct_economia = economia_tempo / tempo_total_manual if tempo_total_manual > 0 else 0
        
        return {
            'economia_tempo_horas': economia_tempo,
            'economia_financeira': economia_financeira,
            'percentual_economia': pct_economia
        }
    
    def calcular_tempo_resposta(self, tempos_execucao):
        """
        Calcula estatísticas de tempo de resposta
        
        Args:
            tempos_execucao: Lista de tempos de execução em segundos
            
        Returns:
            dict: Estatísticas de tempo
        """
        tempos = np.array(tempos_execucao)
        
        return {
            'tempo_medio': np.mean(tempos),
            'tempo_mediano': np.median(tempos),
            'tempo_p95': np.percentile(tempos, 95),
            'tempo_p99': np.percentile(tempos, 99),
            'tempo_minimo': np.min(tempos),
            'tempo_maximo': np.max(tempos)
        }
    
    def calcular_satisfacao_usuario(self, avaliacoes):
        """
        Calcula métricas de satisfação do usuário
        
        Args:
            avaliacoes: Lista de avaliações (1-5)
            
        Returns:
            dict: Métricas de satisfação
        """
        avaliacoes = np.array(avaliacoes)
        
        # Distribuição de avaliações
        distribuicao = {
            '1_estrela': np.sum(avaliacoes == 1) / len(avaliacoes),
            '2_estrelas': np.sum(avaliacoes == 2) / len(avaliacoes),
            '3_estrelas': np.sum(avaliacoes == 3) / len(avaliacoes),
            '4_estrelas': np.sum(avaliacoes == 4) / len(avaliacoes),
            '5_estrelas': np.sum(avaliacoes == 5) / len(avaliacoes)
        }
        
        # Satisfação geral
        media = np.mean(avaliacoes)
        
        # Percentual de avaliações positivas (4-5)
        pct_positivas = np.sum(avaliacoes >= 4) / len(avaliacoes)
        
        return {
            'media_avaliacoes': media,
            'mediana_avaliacoes': np.median(avaliacoes),
            'percentual_positivas': pct_positivas,
            'distribuicao': distribuicao
        }
    
    def registrar_kpis(self, kpis, data=None):
        """
        Registra KPIs no histórico
        
        Args:
            kpis: Dicionário com KPIs calculados
            data: Data do registro (opcional)
        """
        if data is None:
            data = dt.datetime.now()
        
        self.historico.append({
            'data': data,
            'kpis': kpis
        })
    
    def comparar_com_targets(self, kpis):
        """
        Compara KPIs com valores-alvo
        
        Args:
            kpis: Dicionário com KPIs calculados
            
        Returns:
            dict: Comparação com targets
        """
        comparacao = {}
        
        # KPIs onde maior é melhor
        kpis_maior_melhor = [
            'accuracy', 'precision', 'recall', 'f1_score', 'auc', 'especificidade',
            'roi', 'economia_recursos', 'satisfacao_usuario', 'disponibilidade_sistema',
            'qualidade_dados', 'completude_dados', 'atualidade_dados', 'consistencia_dados',
            'roi_modelo', 'economia_total', 'beneficio_deteccao_correta', 'beneficio_nao_alerta_desnecessario'
        ]
        
        # KPIs onde menor é melhor
        kpis_menor_melhor = [
            'custo_por_erro', 'tempo_resposta', 'taxa_falsos_positivos', 'taxa_falsos_negativos',
            'tempo_deteccao_anomalia', 'custo_total', 'custo_falsos_positivos', 'custo_falsos_negativos'
        ]
        
        for kpi, valor in kpis.items():
            if kpi in self.targets:
                target = self.targets[kpi]
                diff = valor - target
                pct_diff = diff / target if target != 0 else 0
                
                # Determinar status baseado no tipo de KPI
                if kpi in kpis_maior_melhor:
                    status = 'Acima do target' if valor >= target else 'Abaixo do target'
                    cor = 'green' if valor >= target else 'red'
                elif kpi in kpis_menor_melhor:
                    status = 'Abaixo do target' if valor <= target else 'Acima do target'
                    cor = 'green' if valor <= target else 'red'
                else:
                    # Para KPIs não categorizados, assumir que maior é melhor
                    status = 'Acima do target' if valor >= target else 'Abaixo do target'
                    cor = 'green' if valor >= target else 'red'
                
                # Calcular score de performance (0-100)
                if kpi in kpis_maior_melhor:
                    score = min(100, max(0, (valor / target) * 100)) if target > 0 else 0
                else:
                    score = min(100, max(0, (target / valor) * 100)) if valor > 0 else 0
                
                comparacao[kpi] = {
                    'valor': valor,
                    'target': target,
                    'diferenca': diff,
                    'diferenca_percentual': pct_diff,
                    'status': status,
                    'cor': cor,
                    'score_performance': score
                }
        
        return comparacao
    
    def gerar_dashboard(self, kpis, comparacao=None):
        """
        Gera dashboard visual dos KPIs - Sistema IoT Monitoring Sprint 3
        
        Args:
            kpis: Dicionário com KPIs calculados
            comparacao: Comparação com targets (opcional)
            
        Returns:
            matplotlib.figure: Figura com dashboard
        """
        # Criar figura com mais subplots
        fig, axs = plt.subplots(3, 3, figsize=(18, 15))
        fig.suptitle('Dashboard de KPIs - Sistema IoT Monitoring Sprint 3', fontsize=18, fontweight='bold')
        
        # 1. Métricas do Modelo ML
        ax = axs[0, 0]
        metricas_ml = ['accuracy', 'precision', 'recall', 'f1_score']
        valores_ml = [kpis.get(m, 0) for m in metricas_ml]
        cores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        
        bars = ax.bar(metricas_ml, valores_ml, color=cores)
        ax.set_title('Métricas do Modelo ML', fontweight='bold')
        ax.set_ylabel('Score')
        ax.set_ylim([0, 1.1])
        
        # Adicionar valores nas barras
        for bar, valor in zip(bars, valores_ml):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                   f'{valor:.3f}', ha='center', va='bottom', fontsize=10)
        
        # Adicionar linha de referência
        ax.axhline(y=0.9, color='red', linestyle='--', alpha=0.7, label='Target (0.9)')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        # 2. ROI e Impacto Financeiro
        ax = axs[0, 1]
        if 'roi' in kpis or 'roi_modelo' in kpis:
            roi_valor = kpis.get('roi_modelo', kpis.get('roi', 0))
            ax.bar(['ROI'], [roi_valor], color='green' if roi_valor >= 1 else 'red')
            
            if comparacao and ('roi' in comparacao or 'roi_modelo' in comparacao):
                roi_key = 'roi_modelo' if 'roi_modelo' in comparacao else 'roi'
                ax.axhline(y=comparacao[roi_key]['target'], color='blue', linestyle='--', 
                          label=f"Target: {comparacao[roi_key]['target']:.2f}")
            
            ax.set_title('Retorno sobre Investimento')
            ax.set_ylabel('ROI')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
        
        # 3. Custos de Erros
        ax = axs[0, 2]
        if 'custo_falsos_positivos' in kpis and 'custo_falsos_negativos' in kpis:
            custos = [kpis['custo_falsos_positivos'], kpis['custo_falsos_negativos']]
            ax.bar(['Falsos Positivos', 'Falsos Negativos'], custos, 
                  color=['orange', 'red'])
            ax.set_title('Custos por Tipo de Erro')
            ax.set_ylabel('Custo (R$)')
            ax.grid(axis='y', alpha=0.3)
        
        # 4. Qualidade dos Dados
        ax = axs[1, 0]
        if 'qualidade_dados' in kpis:
            qualidade = kpis['qualidade_dados'] * 100
            ax.pie([qualidade, 100-qualidade], labels=['Qualidade', 'Deficiente'], 
                  autopct='%1.1f%%', colors=['green', 'lightcoral'])
            ax.set_title('Qualidade dos Dados')
        
        # 5. Taxa de Erros
        ax = axs[1, 1]
        if 'taxa_falsos_positivos' in kpis and 'taxa_falsos_negativos' in kpis:
            taxas = [kpis['taxa_falsos_positivos'] * 100, kpis['taxa_falsos_negativos'] * 100]
            ax.bar(['Falsos Positivos', 'Falsos Negativos'], taxas, 
                  color=['orange', 'red'])
            ax.set_title('Taxa de Erros (%)')
            ax.set_ylabel('Taxa (%)')
            ax.grid(axis='y', alpha=0.3)
        
        # 6. Economia de Recursos
        ax = axs[1, 2]
        if 'economia_recursos' in kpis or 'economia_total' in kpis:
            economia = kpis.get('economia_recursos', kpis.get('economia_total', 0))
            if isinstance(economia, float) and economia <= 1:
                economia = economia * 100  # Converter para percentual
            
            ax.bar(['Economia'], [economia], color='green')
            ax.set_title('Economia de Recursos')
            ax.set_ylabel('Economia (%)' if economia <= 100 else 'Economia (R$)')
            ax.grid(axis='y', alpha=0.3)
        
        # 7. Score de Performance Geral
        ax = axs[2, 0]
        if comparacao:
            scores = [v['score_performance'] for v in comparacao.values() if 'score_performance' in v]
            if scores:
                score_medio = np.mean(scores)
                ax.bar(['Performance Geral'], [score_medio], 
                      color='green' if score_medio >= 80 else 'orange' if score_medio >= 60 else 'red')
                ax.set_title('Score de Performance Geral')
                ax.set_ylabel('Score (0-100)')
                ax.set_ylim([0, 100])
                ax.grid(axis='y', alpha=0.3)
        
        # 8. Distribuição de Predições (se disponível)
        ax = axs[2, 1]
        if 'verdadeiros_positivos' in kpis and 'falsos_positivos' in kpis:
            tp = kpis['verdadeiros_positivos']
            fp = kpis['falsos_positivos']
            tn = kpis.get('verdadeiros_negativos', 0)
            fn = kpis.get('falsos_negativos', 0)
            
            ax.pie([tp, fp, tn, fn], 
                  labels=['VP', 'FP', 'VN', 'FN'],
                  colors=['green', 'orange', 'blue', 'red'],
                  autopct='%1.1f%%')
            ax.set_title('Distribuição de Predições')
        
        # 9. Evolução Temporal (se houver histórico)
        ax = axs[2, 2]
        if self.historico and len(self.historico) > 1:
            # Plotar evolução do accuracy se disponível
            datas = [h['data'] for h in self.historico]
            valores = [h['kpis'].get('accuracy', 0) for h in self.historico]
            
            ax.plot(datas, valores, marker='o', linewidth=2, markersize=6)
            ax.set_title('Evolução do Accuracy')
            ax.set_ylabel('Accuracy')
            ax.grid(True, alpha=0.3)
            ax.tick_params(axis='x', rotation=45)
        else:
            # Mostrar resumo dos KPIs principais
            kpis_principais = ['accuracy', 'precision', 'recall', 'f1_score']
            valores_principais = [kpis.get(k, 0) for k in kpis_principais]
            
            ax.barh(kpis_principais, valores_principais, color=cores)
            ax.set_title('Resumo dos KPIs Principais')
            ax.set_xlabel('Score')
            ax.set_xlim([0, 1])
            ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        return fig


# Exemplo de uso
if __name__ == "__main__":
    print("🚀 SISTEMA DE KPIs - IOT MONITORING")
    print("=" * 50)
    
    # Instanciar classe
    kpis_negocio = KPIsNegocio()
    
    # Dados de exemplo para demonstração
    np.random.seed(42)
    n_samples = 1000
    
    # Simular dados de sensores IoT
    df_sensores = pd.DataFrame({
        'timestamp': pd.date_range('2024-01-01', periods=n_samples, freq='1H'),
        'temperature': np.random.normal(25, 5, n_samples),
        'humidity': np.random.normal(60, 10, n_samples),
        'pressure': np.random.normal(1.013, 0.01, n_samples),
        'luminosity': np.random.normal(500, 100, n_samples),
        'co2': np.random.normal(400, 50, n_samples),
        'noise': np.random.normal(45, 5, n_samples),
        'anomaly': np.random.choice([0, 1], n_samples, p=[0.8, 0.2])
    })
    
    # Simular predições do modelo
    y_true = df_sensores['anomaly'].values
    y_pred = np.random.choice([0, 1], n_samples, p=[0.75, 0.25])  # Simular predições
    y_pred_proba = np.random.random(n_samples)  # Simular probabilidades
    
    print("📊 Calculando métricas do modelo ML...")
    
    # Calcular métricas do modelo ML
    metricas_ml = kpis_negocio.calcular_metricas_modelo_ml(y_true, y_pred, y_pred_proba)
    print("Métricas do Modelo ML:")
    for k, v in metricas_ml.items():
        if isinstance(v, float):
            print(f"  {k}: {v:.4f}")
        else:
            print(f"  {k}: {v}")
    
    print("\n💰 Calculando impacto de negócio...")
    
    # Calcular impacto de negócio IoT
    impacto_negocio = kpis_negocio.calcular_impacto_negocio_iot(y_true, y_pred)
    print("Impacto de Negócio IoT:")
    for k, v in impacto_negocio.items():
        if isinstance(v, float):
            print(f"  {k}: R$ {v:.2f}")
        else:
            print(f"  {k}: {v}")
    
    print("\n📈 Calculando qualidade dos dados...")
    
    # Calcular qualidade dos dados
    qualidade_dados = kpis_negocio.calcular_qualidade_dados_iot(df_sensores)
    print("Qualidade dos Dados:")
    for k, v in qualidade_dados.items():
        if isinstance(v, float):
            print(f"  {k}: {v:.4f}")
        else:
            print(f"  {k}: {v}")
    
    print("\n💵 Calculando ROI tradicional...")
    
    # Calcular ROI tradicional
    roi = kpis_negocio.calcular_roi(
        custo_implementacao=100000,  # R$ 100k
        economia_mensal=25000        # R$ 25k/mês
    )
    print(f"ROI: {roi:.2f}")
    
    print("\n⏱️ Calculando economia de recursos...")
    
    # Calcular economia de recursos
    economia = kpis_negocio.calcular_economia_recursos(
        tempo_manual=2.0,      # 2 horas manual
        tempo_automatizado=0.1, # 6 minutos automatizado
        custo_hora=100,        # R$ 100/hora
        n_operacoes=1000       # 1000 operações/mês
    )
    print("Economia de Recursos:")
    for k, v in economia.items():
        if isinstance(v, float):
            print(f"  {k}: {v:.2f}")
        else:
            print(f"  {k}: {v}")
    
    print("\n📊 Consolidando KPIs...")
    
    # Consolidar todos os KPIs
    kpis_consolidados = {
        **metricas_ml,
        **impacto_negocio,
        **qualidade_dados,
        'roi': roi,
        'economia_recursos': economia['percentual_economia'],
        'tempo_resposta': 0.15,  # 150ms
        'satisfacao_usuario': 4.6,
        'disponibilidade_sistema': 0.995,
        'tempo_deteccao_anomalia': 1.5
    }
    
    # Registrar KPIs
    kpis_negocio.registrar_kpis(kpis_consolidados)
    
    print("\n🎯 Comparando com targets...")
    
    # Comparar com targets
    comparacao = kpis_negocio.comparar_com_targets(kpis_consolidados)
    print("Comparação com Targets:")
    for k, v in comparacao.items():
        if 'score_performance' in v:
            print(f"  {k}: {v['valor']:.4f} vs target {v['target']:.4f} - {v['status']} (Score: {v['score_performance']:.1f})")
        else:
            print(f"  {k}: {v['valor']:.4f} vs target {v['target']:.4f} - {v['status']}")
    
    print("\n📈 Gerando dashboard...")
    
    # Gerar dashboard
    fig = kpis_negocio.gerar_dashboard(kpis_consolidados, comparacao)
    plt.savefig('dashboard_kpis_iot.png', dpi=300, bbox_inches='tight')
    print("✅ Dashboard salvo como: dashboard_kpis_iot.png")
    
    print("\n🎉 ANÁLISE COMPLETA FINALIZADA!")
    print("=" * 50)
    
    # Resumo executivo
    print("\n📋 RESUMO EXECUTIVO:")
    print(f"• Accuracy do Modelo: {metricas_ml['accuracy']:.1%}")
    print(f"• ROI do Projeto: {roi:.1f}x")
    print(f"• Economia de Recursos: {economia['percentual_economia']:.1%}")
    print(f"• Qualidade dos Dados: {qualidade_dados['qualidade_dados']:.1%}")
    print(f"• Custo Total de Erros: R$ {impacto_negocio['custo_total']:,.2f}")
    
    # Calcular score geral
    scores = [v['score_performance'] for v in comparacao.values() if 'score_performance' in v]
    if scores:
        score_geral = np.mean(scores)
        print(f"• Score de Performance Geral: {score_geral:.1f}/100")
        
        if score_geral >= 80:
            print("🎯 Status: EXCELENTE - Todos os targets atingidos!")
        elif score_geral >= 60:
            print("⚠️ Status: BOM - Maioria dos targets atingidos")
        else:
            print("❌ Status: NECESSITA MELHORIAS - Targets não atingidos")