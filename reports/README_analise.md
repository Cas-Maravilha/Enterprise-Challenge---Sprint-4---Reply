# Análise e Visualização de Dados de Sensores Industriais

Este projeto implementa uma solução completa para análise e visualização de dados de sensores industriais, incluindo múltiplos tipos de gráficos, análise estatística básica e detecção de anomalias.

## Componentes do Sistema

1. **Análise e Visualização Básica (`sensor_analytics.py`)**
   - Múltiplos tipos de gráficos (linha, dispersão, histograma, box plot)
   - Análise estatística básica
   - Geração de relatórios

2. **Detecção de Anomalias (`anomaly_detection.py`)**
   - Implementação de múltiplos métodos de detecção:
     - Z-Score
     - IQR (Intervalo Interquartil)
     - Isolation Forest
     - LOF (Local Outlier Factor)
     - DBSCAN
   - Visualização de anomalias detectadas

3. **Dashboard Interativo (`interactive_dashboard.py`)**
   - Interface web interativa com Dash e Plotly
   - Seleção dinâmica de sensores e tipos de gráficos
   - Detecção de anomalias em tempo real

4. **Scripts de Automação**
   - `run_analysis.bat` (Windows)
   - `run_analysis.sh` (Linux/Mac)

## Tipos de Gráficos Implementados

### 1. Gráficos de Linha (Séries Temporais)
- Visualização da evolução dos valores dos sensores ao longo do tempo
- Identificação de tendências e padrões temporais
- Destaque para anomalias detectadas

### 2. Gráficos de Dispersão
- Análise da relação entre dois sensores
- Identificação de correlações e padrões
- Linhas de tendência para visualizar relacionamentos

### 3. Histogramas
- Visualização da distribuição dos valores dos sensores
- Identificação de padrões de distribuição (normal, enviesada, etc.)
- Comparação entre dados normais e anomalias

### 4. Box Plots
- Visualização da distribuição estatística dos dados
- Identificação de outliers
- Comparação entre diferentes sensores ou períodos

### 5. Mapas de Calor
- Visualização da matriz de correlação entre sensores
- Identificação de relações fortes entre diferentes sensores
- Detecção de grupos de sensores relacionados

## Análise Estatística

O sistema calcula e apresenta as seguintes estatísticas para cada sensor:

- **Medidas de Tendência Central**: Média, Mediana
- **Medidas de Dispersão**: Desvio Padrão, Mínimo, Máximo, IQR
- **Medidas de Forma**: Assimetria, Curtose
- **Outras Estatísticas**: Total de registros, Valores nulos, Anomalias detectadas

## Métodos de Detecção de Anomalias

### 1. Z-Score
- Detecta valores que estão a mais de N desvios padrão da média
- Simples e eficaz para distribuições aproximadamente normais
- Parâmetro ajustável: threshold (padrão: 3.0)

### 2. IQR (Intervalo Interquartil)
- Detecta valores abaixo de Q1-1.5*IQR ou acima de Q3+1.5*IQR
- Robusto a outliers e não assume distribuição normal
- Não requer parâmetros de ajuste

### 3. Isolation Forest
- Algoritmo baseado em árvores de decisão
- Isola observações dividindo valores de atributos
- Eficaz para conjuntos de dados de alta dimensão
- Parâmetro ajustável: contamination (proporção esperada de anomalias)

### 4. LOF (Local Outlier Factor)
- Compara a densidade local de um ponto com seus vizinhos
- Detecta anomalias em regiões de densidade variável
- Parâmetros ajustáveis: n_neighbors, contamination

### 5. DBSCAN
- Algoritmo de clustering baseado em densidade
- Pontos que não pertencem a nenhum cluster são considerados anomalias
- Parâmetros ajustáveis: eps, min_samples

## Como Usar

### Análise Básica

```bash
python src/sensor_analytics.py --input data/sensor_data.csv --output-dir results
```

### Detecção de Anomalias

```bash
python src/anomaly_detection.py --input data/sensor_data.csv --method zscore --threshold 3.0 --output-dir anomalies
```

### Dashboard Interativo

```bash
python src/interactive_dashboard.py
```
Acesse http://localhost:8050 no navegador.

### Execução Completa da Análise

No Windows:
```
run_analysis.bat
```

No Linux/Mac:
```
./run_analysis.sh
```

## Requisitos

- Python 3.6+
- Bibliotecas Python (ver requirements.txt):
  - numpy
  - pandas
  - matplotlib
  - seaborn
  - scipy
  - scikit-learn
  - plotly
  - dash

## Instalação

```bash
pip install -r requirements.txt
```

## Extensões Possíveis

1. Adicionar mais algoritmos de detecção de anomalias
2. Implementar análise preditiva e forecasting
3. Adicionar análise de frequência (FFT, wavelets)
4. Integrar com sistemas de alerta em tempo real
5. Implementar aprendizado não supervisionado para agrupamento de padrões