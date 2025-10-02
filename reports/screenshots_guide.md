# Guia de Screenshots

Este documento descreve os screenshots necessários para documentar adequadamente o Sistema de Monitoramento Industrial com ESP32, incluindo instruções sobre como capturá-los e o que deve ser incluído em cada um.

## Screenshots Necessários

### 1. Simulação no Wokwi

**Descrição**: Captura de tela da simulação do ESP32 com sensores no Wokwi.

**O que incluir**:
- ESP32 conectado a todos os sensores
- Monitor serial mostrando dados
- Componentes claramente visíveis
- Simulação em execução

**Como capturar**:
1. Configure o circuito no Wokwi conforme o diagrama
2. Carregue o código `src/main.py`
3. Inicie a simulação
4. Abra o monitor serial
5. Capture a tela completa mostrando o circuito e o monitor serial

**Nome do arquivo**: `wokwi_simulation.png`

### 2. Monitor Serial com Dados CSV

**Descrição**: Captura de tela do monitor serial mostrando a saída de dados em formato CSV.

**O que incluir**:
- Janela do monitor serial
- Cabeçalho CSV visível
- Múltiplas linhas de dados
- Diferentes cenários (normal, alerta, falha) se possível

**Como capturar**:
1. Conecte o ESP32 ao computador ou use a simulação Wokwi
2. Abra o monitor serial (115200 baud)
3. Execute o código `src/main_csv.py`
4. Aguarde a geração de várias linhas de dados
5. Capture a tela do monitor serial

**Nome do arquivo**: `serial_csv_output.png`

### 3. Dashboard Interativo

**Descrição**: Captura de tela do dashboard interativo mostrando gráficos e controles.

**O que incluir**:
- Interface completa do dashboard
- Gráficos com dados reais
- Controles de seleção
- Estatísticas ou informações relevantes

**Como capturar**:
1. Execute o script `src/interactive_dashboard.py`
2. Acesse http://localhost:8050 no navegador
3. Carregue alguns dados
4. Configure a visualização desejada
5. Capture a tela completa do navegador

**Nome do arquivo**: `interactive_dashboard.png`

### 4. Gráficos de Análise

**Descrição**: Captura de tela dos gráficos gerados pelo script de análise.

**O que incluir**:
- Múltiplos tipos de gráficos (linha, histograma, box plot, etc.)
- Dados reais ou simulados
- Legendas e títulos visíveis
- Eixos claramente rotulados

**Como capturar**:
1. Execute o script `src/sensor_analytics.py` com dados reais ou simulados
2. Abra os gráficos gerados na pasta de saída
3. Capture cada gráfico individualmente ou organize-os em uma colagem

**Nome do arquivo**: `analysis_graphs.png`

### 5. Detecção de Anomalias

**Descrição**: Captura de tela mostrando a detecção de anomalias nos dados.

**O que incluir**:
- Gráfico com dados normais e anomalias destacadas
- Legenda indicando pontos normais e anômalos
- Informações sobre o método de detecção utilizado
- Estatísticas relevantes (opcional)

**Como capturar**:
1. Execute o script `src/anomaly_detection.py` com dados contendo anomalias
2. Abra o gráfico gerado na pasta de saída
3. Capture a tela mostrando claramente as anomalias detectadas

**Nome do arquivo**: `anomaly_detection.png`

### 6. Circuito Completo

**Descrição**: Diagrama ou foto do circuito completo com ESP32 e sensores.

**O que incluir**:
- ESP32 claramente visível
- Todos os sensores conectados
- Conexões claramente visíveis
- Componentes adicionais (LEDs, chaves, etc.)

**Como capturar**:
- **Para hardware real**: Tire uma foto do circuito montado
- **Para diagrama**: Exporte o diagrama do Wokwi ou crie um diagrama esquemático

**Nome do arquivo**: `circuit_diagram.png`

### 7. Coleta de Dados em Execução

**Descrição**: Captura de tela do script de coleta de dados em execução.

**O que incluir**:
- Terminal ou prompt de comando
- Saída do script `src/serial_data_collector.py`
- Informações sobre a coleta (porta, duração, etc.)
- Progresso da coleta

**Como capturar**:
1. Execute o script `src/serial_data_collector.py`
2. Aguarde alguns segundos para mostrar o progresso
3. Capture a tela do terminal ou prompt de comando

**Nome do arquivo**: `data_collection.png`

### 8. Estrutura de Arquivos

**Descrição**: Captura de tela mostrando a estrutura de arquivos do projeto.

**O que incluir**:
- Explorador de arquivos ou terminal
- Estrutura de diretórios completa
- Arquivos principais visíveis
- Organização conforme documentação

**Como capturar**:
1. Abra o explorador de arquivos ou terminal
2. Navegue até a pasta raiz do projeto
3. Expanda todos os diretórios relevantes
4. Capture a tela mostrando a estrutura

**Nome do arquivo**: `file_structure.png`

## Diretrizes para Screenshots

### Qualidade e Tamanho

- **Resolução mínima**: 1280x720 pixels
- **Formato**: PNG (preferido) ou JPEG de alta qualidade
- **Tamanho máximo**: 2MB por imagem

### Conteúdo

- Certifique-se de que o texto é legível
- Evite informações sensíveis (senhas, tokens, IPs internos)
- Inclua legendas ou anotações quando necessário
- Use zoom ou destaque para detalhes importantes

### Organização

- Nomeie os arquivos conforme especificado
- Armazene todos os screenshots na pasta `images/`
- Referencie os screenshots na documentação usando caminhos relativos
- Inclua descrições claras para cada screenshot

## Uso na Documentação

### No README.md

```markdown
## Screenshots

### Simulação no Wokwi
![Simulação Wokwi](images/wokwi_simulation.png)
*Simulação do sistema no Wokwi com ESP32 e sensores*

### Dashboard Interativo
![Dashboard](images/interactive_dashboard.png)
*Dashboard interativo mostrando dados dos sensores em tempo real*
```

### Em Documentos Específicos

```markdown
## Detecção de Anomalias

O sistema é capaz de detectar anomalias nos dados dos sensores utilizando múltiplos algoritmos.

![Detecção de Anomalias](../images/anomaly_detection.png)
*Exemplo de detecção de anomalias usando o algoritmo Z-Score*
```

## Atualizando Screenshots

Os screenshots devem ser atualizados quando:

1. Houver mudanças significativas na interface
2. Novos recursos forem adicionados
3. O layout ou design for alterado
4. A funcionalidade mudar de forma visível

Ao atualizar screenshots, mantenha os mesmos nomes de arquivo para evitar quebrar links na documentação.