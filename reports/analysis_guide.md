# Guia de Análise de Dados

Este documento fornece instruções detalhadas sobre como analisar os dados coletados pelo Sistema de Monitoramento Industrial com ESP32, incluindo visualização, análise estatística e detecção de anomalias.

## Índice

1. [Visão Geral dos Dados](#visão-geral-dos-dados)
2. [Ferramentas de Análise](#ferramentas-de-análise)
3. [Análise Estatística Básica](#análise-estatística-básica)
4. [Visualização de Dados](#visualização-de-dados)
5. [Detecção de Anomalias](#detecção-de-anomalias)
6. [Dashboard Interativo](#dashboard-interativo)
7. [Interpretação dos Resultados](#interpretação-dos-resultados)
8. [Análises Avançadas](#análises-avançadas)

## Visão Geral dos Dados

### Formato dos Dados

Os dados são coletados em formato CSV com as seguintes colunas:

```
timestamp,mode,temperature,pressure,vibration_x,vibration_y,vibration_z,vibration_mag,level,status
```

Onde:
- `timestamp`: Timestamp Unix em segundos
- `mode`: Modo de operação (0=Normal, 1=Alerta, 2=Falha)
- `temperature`: Temperatura em °C
- `pressure`: Pressão em bar
- `vibration_x/y/z`: Componentes de vibração em g
- `vibration_mag`: Magnitude da vibração em g
- `level`: Nível em cm
- `status`: Status textual (NORMAL, ALERT, FAILURE)

### Cenários de Dados

Os dados são coletados em três cenários diferentes:

1. **Cenário Normal**: Operação normal do sistema
   - Temperatura: 20-30°C
   - Pressão: 4-6 bar
   - Vibração: 0.3-0.7g
   - Nível: 80-120cm

2. **Cenário de Alerta**: Condições próximas aos limites aceitáveis
   - Temperatura: 30-40°C
   - Pressão: 6-8 bar
   - Vibração: 0.8-1.5g
   - Nível: 130-170cm

3. **Cenário de Falha**: Condições anormais ou falhas de sensores
   - Valores extremos ou nulos
   - Temperatura: -10 a 120°C ou NULL
   - Pressão: 0 a 15 bar ou NULL
   - Vibração: 1.5 a 5.0g ou NULL
   - Nível: 0 a 300cm ou NULL

## Ferramentas de Análise

### Scripts Disponíveis

1. **sensor_analytics.py**: Análise e visualização básica
   ```bash
   python src/sensor_analytics.py --input data/sensor_data.csv --output-dir results
   ```

2. **anomaly_detection.py**: Detecção de anomalias
   ```bash
   python src/anomaly_detection.py --input data/sensor_data.csv --method zscore --output-dir anomalies
   ```

3. **interactive_dashboard.py**: Dashboard interativo
   ```bash
   python src/interactive_dashboard.py
   ```

4. **run_analysis.bat/sh**: Script para executar análise completa
   ```bash
   ./run_analysis.sh
   ```

### Bibliotecas Utilizadas

- **pandas**: Manipulação e análise de dados
- **numpy**: Operações numéricas
- **matplotlib/seaborn**: Visualização de dados
- **scipy**: Análise estatística
- **scikit-learn**: Algoritmos de machine learning para detecção de anomalias
- **plotly/dash**: Dashboard interativo

## Análise Estatística Básica

### Estatísticas Descritivas

Para cada sensor, são calculadas as seguintes estatísticas:

- **Medidas de Tendência Central**: Média, Mediana
- **Medidas de Dispersão**: Desvio Padrão, Mínimo, Máximo, IQR
- **Medidas de Forma**: Assimetria, Curtose
- **Outras Estatísticas**: Total de registros, Valores nulos

### Correlação entre Sensores

A correlação entre os diferentes sensores é calculada e visualizada em um mapa de calor. Isso permite identificar relações entre as variáveis, como:

- Correlação positiva: Quando uma variável aumenta, a outra também aumenta
- Correlação negativa: Quando uma variável aumenta, a outra diminui
- Sem correlação: Quando não há relação aparente entre as variáveis

### Análise por Cenário

As estatísticas são calculadas separadamente para cada cenário (normal, alerta, falha), permitindo comparar o comportamento dos sensores em diferentes condições.

## Visualização de Dados

### Tipos de Gráficos

1. **Gráficos de Linha (Séries Temporais)**
   - Visualização da evolução dos valores dos sensores ao longo do tempo
   - Identificação de tendências e padrões temporais
   - Destaque para anomalias detectadas

2. **Gráficos de Dispersão**
   - Análise da relação entre dois sensores
   - Identificação de correlações e padrões
   - Linhas de tendência para visualizar relacionamentos

3. **Histogramas**
   - Visualização da distribuição dos valores dos sensores
   - Identificação de padrões de distribuição (normal, enviesada, etc.)
   - Comparação entre dados normais e anomalias

4. **Box Plots**
   - Visualização da distribuição estatística dos dados
   - Identificação de outliers
   - Comparação entre diferentes sensores ou períodos

5. **Mapas de Calor**
   - Visualização da matriz de correlação entre sensores
   - Identificação de relações fortes entre diferentes sensores
   - Detecção de grupos de sensores relacionados

### Exemplos de Uso

Para gerar gráficos de séries temporais para todos os sensores:

```bash
python src/sensor_analytics.py --input data/sensor_data.csv --output-dir results --plot-type time_series
```

Para gerar histogramas para um sensor específico:

```bash
python src/sensor_analytics.py --input data/sensor_data.csv --output-dir results --plot-type histogram --sensor temperature
```

## Detecção de Anomalias

### Métodos Implementados

1. **Z-Score**
   - Detecta valores que estão a mais de N desvios padrão da média
   - Simples e eficaz para distribuições aproximadamente normais
   - Parâmetro ajustável: threshold (padrão: 3.0)

2. **IQR (Intervalo Interquartil)**
   - Detecta valores abaixo de Q1-1.5*IQR ou acima de Q3+1.5*IQR
   - Robusto a outliers e não assume distribuição normal
   - Não requer parâmetros de ajuste

3. **Isolation Forest**
   - Algoritmo baseado em árvores de decisão
   - Isola observações dividindo valores de atributos
   - Eficaz para conjuntos de dados de alta dimensão
   - Parâmetro ajustável: contamination (proporção esperada de anomalias)

4. **LOF (Local Outlier Factor)**
   - Compara a densidade local de um ponto com seus vizinhos
   - Detecta anomalias em regiões de densidade variável
   - Parâmetros ajustáveis: n_neighbors, contamination

5. **DBSCAN**
   - Algoritmo de clustering baseado em densidade
   - Pontos que não pertencem a nenhum cluster são considerados anomalias
   - Parâmetros ajustáveis: eps, min_samples

### Exemplos de Uso

Para detectar anomalias usando Z-Score:

```bash
python src/anomaly_detection.py --input data/sensor_data.csv --method zscore --threshold 3.0 --output-dir anomalies
```

Para detectar anomalias usando Isolation Forest:

```bash
python src/anomaly_detection.py --input data/sensor_data.csv --method isolation_forest --contamination 0.05 --output-dir anomalies
```

Para detecção multivariada (considerando múltiplos sensores):

```bash
python src/anomaly_detection.py --input data/sensor_data.csv --method multivariate --output-dir anomalies
```

## Dashboard Interativo

### Inicialização

Para iniciar o dashboard interativo:

```bash
python src/interactive_dashboard.py
```

Acesse http://localhost:8050 no navegador.

### Funcionalidades

O dashboard interativo oferece:

1. **Seleção de Dados**
   - Escolha do arquivo de dados
   - Seleção de sensores para análise
   - Seleção do período de tempo

2. **Visualização**
   - Múltiplos tipos de gráficos
   - Atualização em tempo real
   - Zoom e pan interativos

3. **Análise**
   - Estatísticas em tempo real
   - Detecção de anomalias interativa
   - Ajuste de parâmetros de detecção

4. **Exportação**
   - Download de gráficos
   - Exportação de dados filtrados
   - Geração de relatórios

## Interpretação dos Resultados

### Análise de Tendências

- **Tendência crescente/decrescente**: Pode indicar desgaste ou mudança nas condições
- **Ciclos**: Podem indicar operação cíclica do equipamento
- **Sazonalidade**: Pode estar relacionada a fatores externos (temperatura ambiente, etc.)

### Análise de Anomalias

- **Picos isolados**: Podem indicar eventos transitórios
- **Mudanças de nível**: Podem indicar alterações no processo
- **Valores ausentes**: Podem indicar falhas de sensores
- **Padrões anormais**: Podem indicar problemas no equipamento

### Correlação entre Sensores

- **Alta correlação positiva**: Sensores podem estar medindo fenômenos relacionados
- **Alta correlação negativa**: Sensores podem estar medindo fenômenos inversamente relacionados
- **Correlação variável**: Pode indicar mudanças nas condições de operação

## Análises Avançadas

### Análise de Frequência

Para análise de frequência (identificação de padrões cíclicos):

```bash
python src/frequency_analysis.py --input data/sensor_data.csv --sensor vibration_mag --output-dir frequency
```

### Previsão de Falhas

Para previsão de falhas baseada em dados históricos:

```bash
python src/failure_prediction.py --input data/sensor_data.csv --model random_forest --output-dir prediction
```

### Clustering de Comportamento

Para agrupar padrões de comportamento similares:

```bash
python src/behavior_clustering.py --input data/sensor_data.csv --n-clusters 3 --output-dir clusters
```

### Análise de Causa Raiz

Para análise de causa raiz de anomalias detectadas:

```bash
python src/root_cause_analysis.py --input data/sensor_data.csv --anomalies anomalies/anomalies.csv --output-dir root_cause
```

## Recursos Adicionais

- [Documentação do pandas](https://pandas.pydata.org/docs/)
- [Documentação do scikit-learn](https://scikit-learn.org/stable/documentation.html)
- [Documentação do Plotly](https://plotly.com/python/)
- [Guia de Detecção de Anomalias](https://scikit-learn.org/stable/modules/outlier_detection.html)
- [Análise de Séries Temporais com Python](https://otexts.com/fpp2/)