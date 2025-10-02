# Sistema de Monitoramento Industrial com ESP32

![Banner do Projeto](https://via.placeholder.com/1200x300/0078D7/FFFFFF?text=Sistema+de+Monitoramento+Industrial)

## Visão Geral

Este projeto implementa um sistema completo de monitoramento industrial utilizando ESP32 e sensores industriais. O sistema coleta dados de múltiplos sensores, processa as informações, detecta anomalias e disponibiliza visualizações e análises avançadas.

### Funcionalidades Principais

- Coleta de dados de 4 tipos de sensores industriais
- Simulação de diferentes cenários (normal, alerta, falha)
- Transmissão de dados via MQTT
- Coleta estruturada em formato CSV
- Análise estatística e visualização avançada
- Detecção de anomalias com múltiplos algoritmos
- Dashboard interativo para monitoramento em tempo real

## Estrutura do Projeto

```
sistema-monitoramento-industrial/
├── src/                           # Código fonte
│   ├── *.py                       # Scripts Python
│   └── simulacao_esp32.ino        # Código para o ESP32
│
├── scripts/                       # Scripts de automação (.sh, .bat)
│   ├── run_simulation.bat         # Script para Windows
│   └── run_simulation.sh          # Script para Linux/Mac
│
├── reports/                       # Documentação e relatórios (.md)
│
├── notebooks/                     # Jupyter Notebooks (.ipynb)
│
├── database/                      # Scripts de banco de dados (.sql)
│
├── config/                        # Arquivos de configuração
│
├── images/                        # Imagens e diagramas
│
├── graficos/                      # Gráficos gerados
│
├── data/                          # Dados coletados e simulados (criado em tempo de execução)
│
└── README.md                      # Documentação principal
```

## Requisitos

### Hardware
- ESP32 DevKit
- Sensores:
  - Sensor de temperatura PT100 (ou simulado com ADS1115/potenciômetro)
  - Sensor de pressão 4-20mA (ou simulado com ADS1115/potenciômetro)
  - Acelerômetro ADXL345 (ou simulado com joystick)
  - Sensor ultrassônico HC-SR04
- Componentes adicionais:
  - LEDs de status
  - Chaves para controle de modo

### Software
- Python 3.6+
- MicroPython para ESP32
- Bibliotecas Python (ver `requirements.txt`)
- Wokwi (para simulação)

## Instalação e Configuração

### Configuração do Hardware

1. Monte o circuito conforme o diagrama em `images/circuit_diagram.png`
2. Para simulação no Wokwi:
   - Acesse [Wokwi](https://wokwi.com/projects/new/esp32)
   - Importe o arquivo `config/wokwi_diagram.json`
   - Copie o código de `src/main.py` para o editor

### Configuração do Software

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/sistema-monitoramento-industrial.git
   cd sistema-monitoramento-industrial
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure o firmware no ESP32:
   - Instale MicroPython no ESP32
   - Transfira os arquivos da pasta `src` para o ESP32

## Uso

### Coleta de Dados

Para coletar dados do ESP32 via porta serial:

```bash
python src/serial_data_collector.py --port COM3 --duration 60 --output data/sensor_data.csv
```

Para simular diferentes cenários:

```bash
python src/scenario_simulator.py --scenario all --samples 100 --output-dir data
```

### Análise de Dados

Para analisar os dados coletados:

```bash
python src/sensor_analytics.py --input data/sensor_data.csv --output-dir results
```

Para detectar anomalias:

```bash
python src/anomaly_detection.py --input data/sensor_data.csv --method zscore --output-dir anomalies
```

### Dashboard Interativo

Para iniciar o dashboard interativo:

```bash
python src/interactive_dashboard.py
```

Acesse http://localhost:8050 no navegador.

## Screenshots Necessários

### 1. Simulação no Wokwi
![Simulação Wokwi](https://via.placeholder.com/800x450/0078D7/FFFFFF?text=Simulação+Wokwi)
*Descrição: Captura de tela da simulação do ESP32 com sensores no Wokwi*

### 2. Monitor Serial com Dados CSV
![Monitor Serial](https://via.placeholder.com/800x450/0078D7/FFFFFF?text=Monitor+Serial+CSV)
*Descrição: Captura de tela do monitor serial mostrando a saída de dados em formato CSV*

### 3. Dashboard Interativo
![Dashboard](https://via.placeholder.com/800x450/0078D7/FFFFFF?text=Dashboard+Interativo)
*Descrição: Captura de tela do dashboard interativo mostrando gráficos e controles*

### 4. Gráficos de Análise
![Análise de Dados](https://via.placeholder.com/800x450/0078D7/FFFFFF?text=Gráficos+de+Análise)
*Descrição: Captura de tela dos gráficos gerados pelo script de análise*

### 5. Detecção de Anomalias
![Detecção de Anomalias](https://via.placeholder.com/800x450/0078D7/FFFFFF?text=Detecção+de+Anomalias)
*Descrição: Captura de tela mostrando a detecção de anomalias nos dados*

### 6. Circuito Completo
![Circuito](https://via.placeholder.com/800x450/0078D7/FFFFFF?text=Circuito+Completo)
*Descrição: Diagrama ou foto do circuito completo com ESP32 e sensores*

## Exemplos de Uso Avançado

- Coleta de dados com logs e validação:
  ```bash
  python scripts/serial_data_collector.py --port COM3 --duration 120 --output data/normal.csv
  # Verifique logs em coleta_dados.log
  ```
- Simulação com configuração customizada:
  ```bash
  python scripts/scenario_simulator.py --scenario alert --samples 200 --config sim_params.json
  ```
- Exportação de análise para Excel e PDF:
  ```bash
  python analysis/sensor_analytics.py --input data/normal.csv --output-dir results
  # Resultados em .xlsx e .pdf
  ```
- Dashboard com autenticação:
  ```bash
  python analysis/interactive_dashboard.py
  # Usuário: admin, Senha: senha123
  ```

## Troubleshooting

- Se não conseguir conectar à porta serial, verifique se o ESP32 está corretamente conectado e o nome da porta está correto.
- Se receber muitos avisos de "Linha inválida ignorada", verifique o formato dos dados enviados pelo firmware.
- Para problemas de autenticação no dashboard, confira usuário e senha em interactive_dashboard.py.
- Para notificações por e-mail, configure corretamente o servidor SMTP e as credenciais no script.
- Para erros de dependências, execute:
  ```bash
  pip install -r requirements.txt
  ```

## Checklist para GitHub

### Configuração do Repositório
- [ ] Criar repositório no GitHub
- [ ] Adicionar descrição clara e concisa
- [ ] Configurar tópicos relevantes (ESP32, IoT, Industrial, Monitoring, etc.)
- [ ] Configurar página do projeto (GitHub Pages)
- [ ] Adicionar licença apropriada (MIT recomendada)

### Arquivos Essenciais
- [ ] README.md com documentação principal
- [ ] LICENSE com texto da licença
- [ ] CONTRIBUTING.md com instruções para contribuição
- [ ] CODE_OF_CONDUCT.md com código de conduta
- [ ] .gitignore configurado para Python e MicroPython
- [ ] requirements.txt com dependências

### Estrutura de Diretórios
- [ ] Organizar arquivos conforme estrutura documentada
- [ ] Criar diretórios vazios com arquivos .gitkeep
- [ ] Separar código-fonte de documentação

### Documentação
- [ ] README.md completo com instruções de instalação e uso
- [ ] Documentação adicional na pasta docs/
- [ ] Comentários adequados no código
- [ ] Docstrings em funções e classes
- [ ] Diagramas e imagens na pasta docs/images/

### Código
- [ ] Código formatado conforme PEP 8
- [ ] Nomes de variáveis e funções descritivos
- [ ] Tratamento de erros adequado
- [ ] Testes unitários (quando aplicável)
- [ ] Verificar ausência de credenciais ou informações sensíveis

### Extras
- [ ] Badges no README.md (status de build, cobertura de testes, etc.)
- [ ] Exemplos de uso
- [ ] FAQ ou Troubleshooting
- [ ] Roadmap ou Future Work
- [ ] Agradecimentos e créditos

## Organização de Arquivos

Para manter o projeto organizado, siga estas diretrizes:

1. **Nomes de arquivos**: Use snake_case para arquivos Python e documentação
2. **Estrutura de diretórios**: Mantenha a estrutura conforme documentado
3. **Arquivos de configuração**: Mantenha em diretórios específicos ou na raiz
4. **Dados**: Armazene dados em subdiretórios da pasta data/
5. **Documentação**: Mantenha toda documentação na pasta docs/
6. **Imagens**: Armazene todas as imagens em docs/images/
7. **Scripts**: Separe scripts por funcionalidade (coleta, análise, etc.)

## Contribuição

Para contribuir com este projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Contato

Seu Nome - [seu-email@example.com](mailto:seu-email@example.com)

Link do Projeto: [https://github.com/seu-usuario/sistema-monitoramento-industrial](https://github.com/seu-usuario/sistema-monitoramento-industrial)