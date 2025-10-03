import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import datetime as dt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

class MonitoramentoDrift:
    """Implementa monitoramento de drift em dados para modelos de IA"""
    
    def __init__(self, threshold_estatistico=0.05, threshold_distancia=0.1):
        """
        Inicializa o monitoramento de drift
        
        Args:
            threshold_estatistico: Limiar para testes estatísticos (p-valor)
            threshold_distancia: Limiar para distância entre distribuições
        """
        self.threshold_estatistico = threshold_estatistico
        self.threshold_distancia = threshold_distancia
        self.historico_drift = []
    
    def detectar_drift_estatistico(self, X_ref, X_atual, metodo='ks'):
        """
        Detecta drift usando testes estatísticos
        
        Args:
            X_ref: Dados de referência
            X_atual: Dados atuais
            metodo: Método estatístico ('ks' para Kolmogorov-Smirnov ou 'ttest')
            
        Returns:
            dict: Resultados do teste por feature
        """
        resultados = {}
        
        # Para cada feature
        for i in range(X_ref.shape[1]):
            # Extrair valores da feature
            valores_ref = X_ref[:, i]
            valores_atual = X_atual[:, i]
            
            # Aplicar teste estatístico
            if metodo == 'ks':
                # Teste Kolmogorov-Smirnov
                estatistica, p_valor = stats.ks_2samp(valores_ref, valores_atual)
                nome_teste = 'Kolmogorov-Smirnov'
            elif metodo == 'ttest':
                # Teste T
                estatistica, p_valor = stats.ttest_ind(valores_ref, valores_atual)
                nome_teste = 'T-test'
            else:
                raise ValueError(f"Método '{metodo}' não suportado")
            
            # Verificar se há drift
            drift_detectado = p_valor < self.threshold_estatistico
            
            resultados[i] = {
                'estatistica': estatistica,
                'p_valor': p_valor,
                'drift_detectado': drift_detectado,
                'teste': nome_teste
            }
        
        # Resumo global
        features_com_drift = [i for i, res in resultados.items() if res['drift_detectado']]
        
        return {
            'por_feature': resultados,
            'features_com_drift': features_com_drift,
            'percentual_features_drift': len(features_com_drift) / X_ref.shape[1],
            'drift_global': len(features_com_drift) > 0
        }
    
    def detectar_drift_distribuicao(self, X_ref, X_atual):
        """
        Detecta drift comparando distribuições
        
        Args:
            X_ref: Dados de referência
            X_atual: Dados atuais
            
        Returns:
            dict: Resultados da comparação por feature
        """
        resultados = {}
        
        # Para cada feature
        for i in range(X_ref.shape[1]):
            # Extrair valores da feature
            valores_ref = X_ref[:, i]
            valores_atual = X_atual[:, i]
            
            # Calcular estatísticas
            media_ref = np.mean(valores_ref)
            media_atual = np.mean(valores_atual)
            
            std_ref = np.std(valores_ref)
            std_atual = np.std(valores_atual)
            
            # Calcular diferenças relativas
            if media_ref != 0:
                diff_media = abs((media_atual - media_ref) / media_ref)
            else:
                diff_media = abs(media_atual - media_ref)
            
            if std_ref != 0:
                diff_std = abs((std_atual - std_ref) / std_ref)
            else:
                diff_std = abs(std_atual - std_ref)
            
            # Verificar se há drift
            drift_detectado = (diff_media > self.threshold_distancia or 
                              diff_std > self.threshold_distancia)
            
            resultados[i] = {
                'media_ref': media_ref,
                'media_atual': media_atual,
                'std_ref': std_ref,
                'std_atual': std_atual,
                'diff_media': diff_media,
                'diff_std': diff_std,
                'drift_detectado': drift_detectado
            }
        
        # Resumo global
        features_com_drift = [i for i, res in resultados.items() if res['drift_detectado']]
        
        return {
            'por_feature': resultados,
            'features_com_drift': features_com_drift,
            'percentual_features_drift': len(features_com_drift) / X_ref.shape[1],
            'drift_global': len(features_com_drift) > 0
        }
    
    def detectar_drift_pca(self, X_ref, X_atual, n_componentes=2):
        """
        Detecta drift usando PCA
        
        Args:
            X_ref: Dados de referência
            X_atual: Dados atuais
            n_componentes: Número de componentes PCA
            
        Returns:
            dict: Resultados da análise PCA
        """
        # Normalizar dados
        scaler = StandardScaler()
        X_ref_scaled = scaler.fit_transform(X_ref)
        X_atual_scaled = scaler.transform(X_atual)
        
        # Aplicar PCA
        pca = PCA(n_components=n_componentes)
        pca.fit(X_ref_scaled)
        
        # Transformar dados
        X_ref_pca = pca.transform(X_ref_scaled)
        X_atual_pca = pca.transform(X_atual_scaled)
        
        # Calcular centroides
        centroide_ref = np.mean(X_ref_pca, axis=0)
        centroide_atual = np.mean(X_atual_pca, axis=0)
        
        # Calcular distância entre centroides
        distancia = np.linalg.norm(centroide_atual - centroide_ref)
        
        # Verificar se há drift
        drift_detectado = distancia > self.threshold_distancia
        
        return {
            'distancia_centroides': distancia,
            'centroide_ref': centroide_ref,
            'centroide_atual': centroide_atual,
            'variancia_explicada': pca.explained_variance_ratio_,
            'drift_detectado': drift_detectado,
            'X_ref_pca': X_ref_pca,
            'X_atual_pca': X_atual_pca
        }
    
    def monitorar_drift_temporal(self, X_ref, X_janelas, datas=None):
        """
        Monitora drift ao longo do tempo
        
        Args:
            X_ref: Dados de referência
            X_janelas: Lista de arrays com dados de diferentes janelas temporais
            datas: Lista de datas para cada janela
            
        Returns:
            dict: Resultados do monitoramento temporal
        """
        resultados_temporais = []
        
        # Para cada janela temporal
        for i, X_janela in enumerate(X_janelas):
            # Detectar drift
            resultado_estatistico = self.detectar_drift_estatistico(X_ref, X_janela)
            resultado_distribuicao = self.detectar_drift_distribuicao(X_ref, X_janela)
            
            # Criar resultado para esta janela
            resultado_janela = {
                'janela': i,
                'data': datas[i] if datas else None,
                'drift_estatistico': resultado_estatistico['drift_global'],
                'drift_distribuicao': resultado_distribuicao['drift_global'],
                'percentual_features_drift': resultado_estatistico['percentual_features_drift'],
                'features_com_drift': resultado_estatistico['features_com_drift']
            }
            
            resultados_temporais.append(resultado_janela)
        
        # Registrar no histórico
        self.historico_drift.extend(resultados_temporais)
        
        return resultados_temporais
    
    def plotar_drift_pca(self, resultado_pca):
        """
        Plota visualização PCA do drift
        
        Args:
            resultado_pca: Resultado da análise PCA
            
        Returns:
            matplotlib.figure: Figura com gráfico
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Extrair dados
        X_ref_pca = resultado_pca['X_ref_pca']
        X_atual_pca = resultado_pca['X_atual_pca']
        
        # Plotar pontos
        ax.scatter(X_ref_pca[:, 0], X_ref_pca[:, 1], alpha=0.5, label='Referência')
        ax.scatter(X_atual_pca[:, 0], X_atual_pca[:, 1], alpha=0.5, label='Atual')
        
        # Plotar centroides
        centroide_ref = resultado_pca['centroide_ref']
        centroide_atual = resultado_pca['centroide_atual']
        
        ax.scatter(centroide_ref[0], centroide_ref[1], color='blue', 
                  marker='X', s=200, label='Centroide Ref')
        ax.scatter(centroide_atual[0], centroide_atual[1], color='red', 
                  marker='X', s=200, label='Centroide Atual')
        
        # Conectar centroides
        ax.plot([centroide_ref[0], centroide_atual[0]], 
               [centroide_ref[1], centroide_atual[1]], 
               'k--', label=f'Distância: {resultado_pca["distancia_centroides"]:.4f}')
        
        # Configurar gráfico
        ax.set_xlabel(f'PC1 ({resultado_pca["variancia_explicada"][0]:.2%})')
        ax.set_ylabel(f'PC2 ({resultado_pca["variancia_explicada"][1]:.2%})')
        ax.set_title('Visualização de Drift via PCA')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Adicionar texto com status
        status = "DRIFT DETECTADO" if resultado_pca["drift_detectado"] else "Sem drift"
        ax.text(0.05, 0.95, status, transform=ax.transAxes, 
               fontsize=14, va='top', 
               bbox=dict(boxstyle='round', facecolor='red' if resultado_pca["drift_detectado"] else 'green', 
                        alpha=0.5))
        
        return fig
    
    def plotar_drift_temporal(self, resultados_temporais):
        """
        Plota evolução do drift ao longo do tempo
        
        Args:
            resultados_temporais: Resultados do monitoramento temporal
            
        Returns:
            matplotlib.figure: Figura com gráfico
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Extrair dados
        janelas = [r['janela'] for r in resultados_temporais]
        datas = [r['data'] for r in resultados_temporais] if resultados_temporais[0]['data'] else janelas
        percentuais = [r['percentual_features_drift'] for r in resultados_temporais]
        
        # Plotar evolução do percentual de features com drift
        ax.plot(datas, percentuais, marker='o', linestyle='-')
        
        # Adicionar linha de threshold
        ax.axhline(y=0.1, color='r', linestyle='--', label='Threshold (10%)')
        
        # Configurar gráfico
        if resultados_temporais[0]['data']:
            ax.set_xlabel('Data')
            plt.xticks(rotation=45)
        else:
            ax.set_xlabel('Janela Temporal')
        
        ax.set_ylabel('% Features com Drift')
        ax.set_title('Evolução do Drift ao Longo do Tempo')
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Destacar janelas com drift significativo
        for i, resultado in enumerate(resultados_temporais):
            if resultado['percentual_features_drift'] > 0.1:
                if resultados_temporais[0]['data']:
                    x = resultado['data']
                else:
                    x = resultado['janela']
                
                ax.scatter(x, resultado['percentual_features_drift'], 
                          color='red', s=100, zorder=5)
        
        plt.tight_layout()
        return fig
    
    def plotar_distribuicoes_feature(self, X_ref, X_atual, feature_idx, nome_feature=None):
        """
        Plota comparação de distribuições para uma feature
        
        Args:
            X_ref: Dados de referência
            X_atual: Dados atuais
            feature_idx: Índice da feature
            nome_feature: Nome da feature (opcional)
            
        Returns:
            matplotlib.figure: Figura com gráfico
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Extrair valores da feature
        valores_ref = X_ref[:, feature_idx]
        valores_atual = X_atual[:, feature_idx]
        
        # Plotar histogramas
        ax.hist(valores_ref, bins=30, alpha=0.5, label='Referência')
        ax.hist(valores_atual, bins=30, alpha=0.5, label='Atual')
        
        # Calcular estatísticas
        media_ref = np.mean(valores_ref)
        media_atual = np.mean(valores_atual)
        
        std_ref = np.std(valores_ref)
        std_atual = np.std(valores_atual)
        
        # Adicionar linhas verticais para médias
        ax.axvline(x=media_ref, color='blue', linestyle='--', 
                  label=f'Média Ref: {media_ref:.4f}')
        ax.axvline(x=media_atual, color='orange', linestyle='--', 
                  label=f'Média Atual: {media_atual:.4f}')
        
        # Configurar gráfico
        nome = nome_feature if nome_feature else f'Feature {feature_idx}'
        ax.set_xlabel(nome)
        ax.set_ylabel('Frequência')
        ax.set_title(f'Comparação de Distribuições - {nome}')
        ax.legend()
        
        # Adicionar texto com estatísticas
        texto = f"Ref: média={media_ref:.4f}, std={std_ref:.4f}\n"
        texto += f"Atual: média={media_atual:.4f}, std={std_atual:.4f}\n"
        
        if media_ref != 0:
            diff_media = abs((media_atual - media_ref) / media_ref) * 100
            texto += f"Diff média: {diff_media:.2f}%\n"
        
        if std_ref != 0:
            diff_std = abs((std_atual - std_ref) / std_ref) * 100
            texto += f"Diff std: {diff_std:.2f}%"
        
        ax.text(0.05, 0.95, texto, transform=ax.transAxes, 
               fontsize=10, va='top', 
               bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        return fig


# Exemplo de uso
if __name__ == "__main__":
    # Dados de exemplo
    np.random.seed(42)
    n_amostras = 1000
    n_features = 5
    
    # Dados de referência
    X_ref = np.random.randn(n_amostras, n_features)
    
    # Dados atuais com drift
    X_atual = np.random.randn(n_amostras, n_features)
    X_atual[:, 0] += 0.5  # Drift na primeira feature
    X_atual[:, 2] *= 1.5  # Drift na terceira feature
    
    # Instanciar monitor de drift
    monitor = MonitoramentoDrift()
    
    # Detectar drift estatístico
    resultado_estatistico = monitor.detectar_drift_estatistico(X_ref, X_atual)
    print("Drift estatístico:")
    print(f"  Features com drift: {resultado_estatistico['features_com_drift']}")
    print(f"  Percentual: {resultado_estatistico['percentual_features_drift']:.2%}")
    
    # Detectar drift por distribuição
    resultado_distribuicao = monitor.detectar_drift_distribuicao(X_ref, X_atual)
    print("\nDrift por distribuição:")
    print(f"  Features com drift: {resultado_distribuicao['features_com_drift']}")
    print(f"  Percentual: {resultado_distribuicao['percentual_features_drift']:.2%}")
    
    # Detectar drift via PCA
    resultado_pca = monitor.detectar_drift_pca(X_ref, X_atual)
    print("\nDrift via PCA:")
    print(f"  Distância entre centroides: {resultado_pca['distancia_centroides']:.4f}")
    print(f"  Drift detectado: {resultado_pca['drift_detectado']}")
    
    # Plotar visualização PCA
    fig_pca = monitor.plotar_drift_pca(resultado_pca)
    fig_pca.savefig('drift_pca.png')
    
    # Plotar distribuição de uma feature com drift
    fig_dist = monitor.plotar_distribuicoes_feature(X_ref, X_atual, 0, 'Feature 0')
    fig_dist.savefig('drift_distribuicao_feature0.png')
    
    # Monitoramento temporal
    # Criar janelas temporais simuladas
    janelas = []
    for i in range(5):
        # Cada janela tem um drift progressivo
        X_janela = np.random.randn(n_amostras, n_features)
        X_janela[:, 0] += 0.1 * i  # Drift crescente
        janelas.append(X_janela)
    
    # Datas fictícias
    datas = [dt.datetime(2023, 1, 1) + dt.timedelta(days=30*i) for i in range(5)]
    
    # Monitorar drift temporal
    resultados_temporais = monitor.monitorar_drift_temporal(X_ref, janelas, datas)
    
    # Plotar evolução temporal
    fig_temporal = monitor.plotar_drift_temporal(resultados_temporais)
    fig_temporal.savefig('drift_temporal.png')