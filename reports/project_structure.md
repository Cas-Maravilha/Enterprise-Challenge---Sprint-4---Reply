# Estrutura de Arquivos do Projeto

Este documento descreve a estrutura de arquivos recomendada para o Sistema de Monitoramento Industrial com ESP32.

## Estrutura de Diretórios

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
├── .github/                       # Configurações do GitHub
│   ├── ISSUE_TEMPLATE/            # Templates para issues
│   └── workflows/                 # GitHub Actions workflows
│
├── README.md                      # Documentação principal
├── CONTRIBUTING.md                # Guia de contribuição
├── CODE_OF_CONDUCT.md             # Código de conduta
├── LICENSE                        # Licença do projeto
├── .gitignore                     # Configuração do Git
└── requirements.txt               # Dependências Python
```

## Organização dos Arquivos

### src

- `*.py`: Todos os scripts Python do projeto.
- `simulacao_esp32.ino`: Código de simulação para o ESP32 (Arduino).

### scripts

- Contém scripts de automação para executar tarefas comuns, como `run_simulation.bat` e `run_analysis.sh`.

### reports

- Contém toda a documentação do projeto em formato Markdown.

### notebooks

- Contém Jupyter Notebooks para análise exploratória e prototipagem.

### database

- Contém scripts SQL para criação de banco de dados e inserção de dados.

### config

- Contém arquivos de configuração para ferramentas como Wokwi.

### images

- Contém imagens estáticas como diagramas e logos.

### graficos

- Contém gráficos e visualizações gerados pelos scripts de análise.

### data

- Diretório para armazenar dados brutos e processados. Criado em tempo de execução.

### Arquivos na Raiz

- `README.md`: Documentação principal do projeto
- `CONTRIBUTING.md`: Guia para contribuição
- `CODE_OF_CONDUCT.md`: Código de conduta para contribuidores
- `LICENSE`: Licença do projeto (recomendado MIT)
- `.gitignore`: Configuração para ignorar arquivos no Git
- `requirements.txt`: Lista de dependências Python

## Convenções de Nomenclatura

1. **Arquivos Python**: Use snake_case para nomes de arquivos Python
   - Exemplo: `serial_data_collector.py`

2. **Documentação**: Use CamelCase para títulos de documentos
   - Exemplo: `SetupGuide.md`

3. **Diretórios**: Use lowercase para nomes de diretórios
   - Exemplo: `firmware/`

4. **Arquivos de Dados**: Use o formato `tipo_timestamp.csv`
   - Exemplo: `normal_20230615_120000.csv`

## Organização de Código

1. **Imports**: Organize imports em grupos (standard library, third-party, local)
2. **Classes**: Uma classe principal por arquivo
3. **Funções**: Funções relacionadas agrupadas em arquivos
4. **Constantes**: Definidas no topo do arquivo
5. **Documentação**: Docstrings para todas as funções e classes

## Versionamento

Utilize Git para controle de versão e siga o fluxo de trabalho:

1. `main`: Branch principal, sempre estável
2. `develop`: Branch de desenvolvimento
3. `feature/*`: Branches para novas features
4. `bugfix/*`: Branches para correções de bugs
5. `release/*`: Branches para preparação de releases

## Criação da Estrutura

Para criar esta estrutura de diretórios, execute:

```bash
# Criar diretórios principais
mkdir -p firmware scripts analysis data/normal data/alert data/failure docs/images .github/ISSUE_TEMPLATE .github/workflows

# Criar arquivos vazios para manter a estrutura no Git
touch firmware/.gitkeep scripts/.gitkeep analysis/.gitkeep data/.gitkeep docs/images/.gitkeep

# Criar arquivos de documentação básicos
touch README.md CONTRIBUTING.md CODE_OF_CONDUCT.md LICENSE .gitignore requirements.txt
touch docs/setup.md docs/hardware.md docs/analysis.md
```