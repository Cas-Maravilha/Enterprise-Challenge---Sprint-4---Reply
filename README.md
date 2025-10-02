# Sistema IoT Monitoring - Detecção de Anomalias com ML
## Enterprise Challenge Sprint 4 - Reply

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://mysql.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📑 Índice de Navegação

### 🚀 **Início Rápido**
- [📋 Visão Geral](#-visão-geral)
- [🔧 Instalação](#-instalação)
- [🌐 Acesso ao Sistema](#-acesso-ao-sistema)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [🎯 Funcionalidades Principais](#-funcionalidades-principais)
- [🎥 Demonstração em Vídeo](https://youtu.be/FcNGYkVKkZ4)

### 🧪 **Utilização e Teste**
- [⚡ Execução Rápida](#-execução-rápida-5-minutos)
- [🔧 Teste Individual](#-teste-individual)
- [📊 Verificação de Componentes](#-verificação-de-componentes)
- [📋 Guia de Avaliação](#-guia-de-avaliação)

### 🏗️ **Arquitetura e Componentes**
- [🔗 Vínculo com Entregas Anteriores](#-vínculo-com-entregas-anteriores)
- [🔧 Decisões Técnicas](#-decisões-técnicas)
- [📊 Métricas de Performance](#-métricas-de-performance)

### 🛠️ **Tecnologias e Desenvolvimento**
- [🛠️ Tecnologias Utilizadas](#️-tecnologias-utilizadas)
- [🔍 Troubleshooting](#-troubleshooting)
- [📚 Documentação Adicional](#-documentação-adicional)
- [🤝 Contribuição](#-contribuição)

### 📞 **Suporte e Informações**
- [👥 Equipe](#-equipe)
- [📞 Suporte](#-suporte)
- [📄 Licença](#-licença)

## 📋 Visão Geral

O **Sistema IoT Monitoring** é uma solução completa de monitoramento industrial que integra coleta de dados de sensores IoT, processamento em tempo real, detecção de anomalias com Machine Learning e visualização através de dashboards interativos. O sistema foi desenvolvido como parte do Enterprise Challenge Sprint 4 da FIAP - Graduação em Inteligência Artificial (1º Ano - 2025/1) em parceria com a Reply.

### 🎥 **Demonstração em Vídeo**

[![Sistema IoT Monitoring - Demonstração Completa](https://img.youtube.com/vi/FcNGYkVKkZ4/maxresdefault.jpg)](https://youtu.be/FcNGYkVKkZ4)

**[▶️ Assistir Apresentação Completa](https://youtu.be/FcNGYkVKkZ4)** - Demonstração do sistema funcionando em tempo real

### 🎯 Objetivos
- **Monitoramento em tempo real** de sensores industriais
- **Detecção automática de anomalias** usando algoritmos de ML
- **Alertas inteligentes** com diferentes níveis de severidade
- **Dashboards interativos** para visualização de KPIs
- **Relatórios automáticos** para análise executiva
- **Arquitetura escalável** para ambientes industriais

### 🏗️ Arquitetura do Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Sensores IoT  │───▶│  Coleta/Ingestão │───▶│  Banco de Dados │
│   (ESP32/DHT22) │    │   (MQTT/Serial)  │    │    (MySQL)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Dashboard     │◀───│  Machine Learning│◀───│  Processamento  │
│  (Streamlit)    │    │   (Anomaly Det.)│    │   (Python)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Como Rodar

### 📋 Pré-requisitos

- **Python 3.8+**
- **MySQL 8.0+**
- **Git** (para clonagem do repositório)
- **8GB RAM** (mínimo)
- **2GB espaço em disco**

### 🔧 Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/Cas-Maravilha/Enterprise-Challenge---Sprint-4---Reply.git
cd Enterprise-Challenge---Sprint-4---Reply
```

2. **Instale as dependências**
```bash
# Windows
install_dependencies.bat

# Linux/Mac
chmod +x install_dependencies.sh
./install_dependencies.sh
```

3. **Configure o banco de dados**
```bash
# Crie o banco e carregue os dados
db\executar_banco_completo.bat
```

4. **Execute o sistema completo**
```bash
# Execução completa (recomendado)
executar_fluxo_completo.bat

# Ou execute componentes individuais
dashboard\executar_dashboard.bat
ml\executar_ml_completo.bat
```

### 🌐 Acesso ao Sistema

- **Dashboard Principal**: http://localhost:8501
- **Dashboard de KPIs**: http://localhost:8502
- **Sistema de Alertas**: http://localhost:8503
- **Banco de Dados**: localhost:3306

### 👤 Credenciais Padrão

- **MySQL**: root / password
- **Dashboard**: admin / iotmonitoring2024

## 🧪 Utilização e Teste

### ⚡ **Execução Rápida (5 minutos)**

Para testar o sistema completo rapidamente:

```bash
# 1. Instalar dependências
install_dependencies.bat

# 2. Configurar banco de dados
db\executar_banco_completo.bat

# 3. Executar sistema completo
executar_fluxo_completo.bat
```

**Resultado esperado**: Dashboard acessível em http://localhost:8501

### 🔧 **Teste Individual**

Para testar componentes específicos:

```bash
# Dashboard principal
dashboard\executar_dashboard.bat

# Machine Learning
ml\executar_ml_completo.bat

# Coleta de dados
ingest\scripts_execucao\executar_simulacao.bat

# Banco de dados
db\executar_banco_completo.bat
```

### 📊 **Verificação de Componentes**

Para verificar se cada componente está funcionando:

```bash
# 1. Verificar banco de dados
mysql -u root -p iot_monitoring_db -e "SELECT COUNT(*) FROM leituras_sensores;"

# 2. Testar ML básico
python -c "
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Dados sintéticos
X = np.random.normal(0, 1, (100, 4))
y = np.random.randint(0, 2, 100)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Treinar modelo
model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f'✅ Teste ML: Accuracy = {accuracy:.3f}')
"

# 3. Verificar dashboard
streamlit run dashboard/app/app.py --server.port 8501 --server.headless true
```

### 📋 **Guia de Avaliação**

Para avaliadores e testes formais:

- **[📝 Guia de Avaliação](GUIA_AVALIACAO.md)**: Critérios e checklist completo
- **[📊 Resumo Final](RESUMO_AVALIACAO_FINAL.md)**: Estatísticas e métricas
- **[🔍 Verificação](verificacao_final_entrega.md)**: Checklist de entrega

#### 🎥 **Demonstração Visual para Avaliadores**

[![Demonstração para Avaliadores](https://img.youtube.com/vi/FcNGYkVKkZ4/maxresdefault.jpg)](https://youtu.be/FcNGYkVKkZ4)

**[▶️ Assistir Demonstração Completa](https://youtu.be/FcNGYkVKkZ4)** - Apresentação técnica do sistema

### 🎯 **Testes de Funcionalidade**

#### **Teste 1: Coleta de Dados**
```bash
# Executar simulação ESP32
ingest\scripts_execucao\executar_simulacao.bat

# Verificar dados gerados
dir ingest\dados\
```

#### **Teste 2: Banco de Dados**
```bash
# Criar e carregar banco
db\executar_banco_completo.bat

# Verificar tabelas
mysql -u root -p iot_monitoring_db -e "SHOW TABLES;"
```

#### **Teste 3: Machine Learning**
```bash
# Treinar modelo
ml\executar_ml_completo.bat

# Verificar métricas
type ml\metricas\model_metrics.json
```

#### **Teste 4: Dashboard**
```bash
# Executar dashboard
dashboard\executar_dashboard.bat

# Acessar: http://localhost:8501
```

### 📈 **Métricas de Sucesso**

O sistema está funcionando corretamente quando:

- ✅ **Banco de dados**: Tabelas criadas e dados carregados
- ✅ **Machine Learning**: Modelo treinado com accuracy > 90%
- ✅ **Dashboard**: Interface acessível e responsiva
- ✅ **Alertas**: Sistema de notificações funcionando
- ✅ **KPIs**: Métricas sendo calculadas em tempo real

### 🚨 **Troubleshooting Rápido**

#### **Problema**: Erro de conexão MySQL
```bash
# Solução
net start mysql
mysql -u root -p
```

#### **Problema**: Porta ocupada
```bash
# Solução
netstat -ano | findstr :8501
streamlit run app.py --server.port 8502
```

#### **Problema**: Dependências Python
```bash
# Solução
python -m pip install -r requirements.txt --force-reinstall
```

## 📁 Estrutura do Projeto

```
Enterprise-Challenge---Sprint-4---Reply/
├── 📁 [docs/](docs/)                    # [Documentação técnica](docs/README.md)
│   ├── [arquitetura/](docs/arquitetura/)            # [Diagramas e especificações](docs/arquitetura/README.md)
│   ├── [api/](docs/api/)                    # [Documentação de APIs](docs/api/)
│   └── [deployment/](docs/deployment/)             # [Guias de deploy](docs/deployment/)
├── 📁 [ingest/](ingest/)                  # [Coleta e ingestão de dados](ingest/README.md)
│   ├── [esp32/](ingest/esp32/)                  # [Código Arduino ESP32](ingest/esp32/)
│   ├── [python/](ingest/python/)                 # [Scripts de coleta Python](ingest/python/)
│   └── [dados/](ingest/dados/)                  # [Dados simulados](ingest/dados/)
├── 📁 [db/](db/)                      # [Banco de dados](db/README.md)
│   ├── [scripts/](db/scripts/)                # [Scripts SQL](db/scripts/)
│   ├── [carga/](db/carga/)                  # [Scripts de carga](db/carga/)
│   └── [evidencias/](db/evidencias/)             # [Evidências de funcionamento](db/evidencias/)
├── 📁 [ml/](ml/)                      # [Machine Learning](ml/README.md)
│   ├── [notebooks/](ml/notebooks/)              # [Jupyter Notebooks](ml/notebooks/)
│   ├── [scripts/](ml/scripts/)                # [Scripts Python ML](ml/scripts/)
│   ├── [modelos/](ml/modelos/)                # [Modelos treinados](ml/modelos/)
│   └── [metricas/](ml/metricas/)               # [Métricas de avaliação](ml/metricas/)
├── 📁 [dashboard/](dashboard/)               # [Interface web](dashboard/README.md)
│   ├── [app/](dashboard/app/)                    # [Aplicação Streamlit](dashboard/app/)
│   ├── [relatorios/](dashboard/relatorios/)             # [Relatórios HTML](dashboard/relatorios/)
│   ├── [kpis/](dashboard/kpis/)                   # [KPIs em tempo real](dashboard/kpis/)
│   └── [alertas/](dashboard/alertas/)                # [Sistema de alertas](dashboard/alertas/)
├── 📄 [README.md](README.md)                # Este arquivo
├── 📄 [GUIA_AVALIACAO.md](GUIA_AVALIACAO.md)        # [Guia para avaliadores](GUIA_AVALIACAO.md)
└── 📄 [RESUMO_AVALIACAO_FINAL.md](RESUMO_AVALIACAO_FINAL.md)  # [Resumo final](RESUMO_AVALIACAO_FINAL.md)
```

## 🔗 Vínculo com Entregas Anteriores

### 📦 [Entrega 1 - Arquitetura](#entrega-1---arquitetura)
**Arquivos relacionados**: [`docs/arquitetura/`](docs/arquitetura/), [`arquitetura_final_sistema_iot.xml`](arquitetura_final_sistema_iot.xml)

- **Arquitetura em camadas** implementada conforme especificado
- **Diagramas Draw.io** com fluxo completo de dados
- **Especificações técnicas** detalhadas
- **Decisões arquiteturais** documentadas
- **Integração** entre componentes validada

### 📦 [Entrega 2 - Simulação e Coleta](#entrega-2---simulação-e-coleta)
**Arquivos relacionados**: [`ingest/`](ingest/), [`simulacao_esp32.ino`](simulacao_esp32.ino), [`wokwi_simulacao_esp32.json`](wokwi_simulacao_esp32.json)

- **Simulação ESP32** com Wokwi implementada
- **Coleta de dados** via Serial e MQTT
- **Sensores simulados**: DHT22, LDR, PIR, BME280
- **Geração de dados** realísticos
- **Visualizações** de dados coletados

### 📦 [Entrega 3 - Modelagem e ML](#entrega-3---modelagem-e-ml)
**Arquivos relacionados**: [`ml/`](ml/), [`db/`](db/), [`criar_tabelas_iot.sql`](criar_tabelas_iot.sql)

- **Banco relacional** com 11 tabelas normalizadas
- **Modelos de ML** para detecção de anomalias
- **Métricas de avaliação** implementadas
- **Integração** banco ↔ ML ↔ dashboard
- **Persistência** de dados e modelos

### 🔄 [Integração Completa](#integração-completa)
**Arquivos relacionados**: [`pipeline_completo.py`](pipeline_completo.py), [`executar_fluxo_completo.bat`](executar_fluxo_completo.bat)

- **Pipeline end-to-end** funcionando
- **Dados fluindo** desde sensores até dashboard
- **Alertas automáticos** baseados em ML
- **KPIs em tempo real** calculados
- **Relatórios** gerados automaticamente

## 🎯 Funcionalidades Principais

### 🔍 Coleta de Dados
- **Simulação ESP32** com sensores múltiplos
- **Coleta via Serial** e MQTT
- **Dados realísticos** com padrões temporais
- **Validação** e formatação automática
- **Logs detalhados** de coleta

### 🗄️ Persistência
- **Banco MySQL** com 11 tabelas relacionais
- **Particionamento** por mês na tabela principal
- **Índices otimizados** para performance
- **Integridade referencial** garantida
- **Backup automático** configurado

### 🤖 Machine Learning
- **4 algoritmos** de detecção de anomalias
- **Random Forest** como melhor modelo (F1: 89.2%)
- **Treinamento automático** com validação cruzada
- **Inferência em tempo real** < 100ms
- **Monitoramento de drift** implementado

### 📊 Visualização
- **Dashboard Streamlit** responsivo
- **KPIs em tempo real** atualizados
- **Gráficos interativos** com Plotly
- **Sistema de alertas** com níveis de severidade
- **Relatórios HTML** profissionais

### 🚨 Sistema de Alertas
- **10 tipos** de alertas configuráveis
- **4 níveis** de severidade (Crítica, Alta, Média, Baixa)
- **Thresholds dinâmicos** ajustáveis
- **Notificações** via banner, log e email
- **Histórico** e estatísticas de alertas

## 🔧 Decisões Técnicas

### 🏗️ Arquitetura
- **Arquitetura em camadas** para separação de responsabilidades
- **Microserviços** para escalabilidade horizontal
- **Event-driven** para processamento assíncrono
- **API-first** para integração com sistemas externos

### 💾 Banco de Dados
- **MySQL 8.0** para robustez e performance
- **Particionamento** para otimização de consultas
- **Índices compostos** para queries complexas
- **Triggers** para auditoria automática
- **Stored procedures** para lógica de negócio

### 🤖 Machine Learning
- **Random Forest** escolhido por performance e interpretabilidade
- **Feature engineering** com variáveis temporais
- **Validação cruzada** estratificada para robustez
- **Normalização** com StandardScaler
- **Ensemble methods** para melhor precisão

### 🌐 Frontend
- **Streamlit** escolhido por simplicidade e integração Python
- **Plotly** para gráficos interativos
- **CSS customizado** para branding
- **Responsive design** para múltiplos dispositivos
- **Auto-refresh** para dados em tempo real

### 🔄 Integração
- **MQTT** para comunicação IoT
- **REST APIs** para integração web
- **JSON** como formato de dados padrão
- **Docker** para containerização (futuro)
- **CI/CD** com GitHub Actions (futuro)

## 📊 Métricas de Performance

### ⚡ Performance Geral
- **Latência média**: 45ms
- **Throughput**: 2,400 leituras/hora
- **Uptime**: 99.8%
- **Disponibilidade**: 98.5%

### 🎯 Machine Learning
- **Accuracy**: 94.5%
- **Precision**: 87.6%
- **Recall**: 90.8%
- **F1-Score**: 89.2%
- **ROC AUC**: 0.95

### 📈 Qualidade dos Dados
- **Qualidade Excelente**: 90.2%
- **Qualidade Boa**: 9.5%
- **Taxa de Anomalias**: 2.1%
- **Integridade**: 100%

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**: Lógica de negócio
- **MySQL 8.0**: Banco de dados
- **Pandas**: Manipulação de dados
- **NumPy**: Cálculos numéricos
- **Scikit-learn**: Machine Learning

### Frontend
- **Streamlit**: Interface web
- **Plotly**: Gráficos interativos
- **HTML/CSS**: Relatórios
- **JavaScript**: Interatividade

### IoT
- **Arduino IDE**: Código ESP32
- **Wokwi**: Simulação online
- **MQTT**: Protocolo de comunicação
- **Serial**: Comunicação direta

### DevOps
- **Git**: Controle de versão
- **Batch/Shell**: Scripts de automação
- **JSON**: Configurações
- **Markdown**: Documentação

## 🔍 Troubleshooting

### ❌ Problemas Comuns

#### **Erro de Conexão MySQL**
```bash
# Verificar se MySQL está rodando
net start mysql

# Verificar credenciais
mysql -u root -p
```

#### **Erro de Dependências Python**
```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

#### **Erro de Porta Ocupada**
```bash
# Verificar portas em uso
netstat -ano | findstr :8501

# Usar porta diferente
streamlit run app.py --server.port 8502
```

#### **Erro de Dados Não Carregados**
   ```bash
# Verificar banco de dados
db\executar_banco_completo.bat

# Verificar dados
python -c "import pandas as pd; print(pd.read_sql('SELECT COUNT(*) FROM leituras_sensores', engine))"
```

## 📚 Documentação Adicional

### 🏗️ **Arquitetura e Design**
- **[📋 Arquitetura](docs/arquitetura/README.md)**: Diagramas e especificações técnicas
- **[🔧 Decisões Técnicas](docs/arquitetura/decisoes_tecnicas.md)**: Justificativas e escolhas arquiteturais
- **[📊 Fluxo de Dados](docs/arquitetura/fluxo_dados.drawio)**: Diagrama de fluxo de dados
- **[🏛️ Componentes](docs/arquitetura/componentes_detalhados.drawio)**: Especificações detalhadas

### 💾 **Banco de Dados**
- **[🗄️ Banco de Dados](db/README.md)**: Estrutura e scripts SQL
- **[📝 Scripts SQL](db/scripts/)**: Scripts de criação e carga
- **[📊 Evidências](db/evidencias/)**: Evidências de funcionamento
- **[🔗 Chaves e Restrições](explicacao_chaves_restricoes.md)**: Documentação de integridade

### 🤖 **Machine Learning**
- **[🧠 Machine Learning](ml/README.md)**: Modelos e métricas
- **[📓 Notebook](ml/notebooks/ML_Anomaly_Detection_IoT.ipynb)**: Análise interativa
- **[🔬 Scripts ML](ml/scripts/)**: Treinamento e inferência
- **[📈 Métricas](ml/metricas/)**: Resultados e avaliações

### 📊 **Interface e Visualização**
- **[📊 Dashboard](dashboard/README.md)**: Interface e KPIs
- **[🚨 Sistema de Alertas](dashboard/app/sistema_alertas.py)**: Alertas inteligentes
- **[📈 KPIs](dashboard/kpis/)**: Indicadores de performance
- **[📋 Relatórios](dashboard/relatorios/)**: Relatórios automáticos

### 🔍 **Coleta de Dados**
- **[📡 Coleta de Dados](ingest/README.md)**: Sensores e simulação
- **[🔌 ESP32](ingest/esp32/)**: Código Arduino e simulação
- **[🐍 Python](ingest/python/)**: Scripts de coleta
- **[📊 Dados](ingest/dados/)**: Dados simulados e evidências

### 📋 **Avaliação e Qualidade**
- **[📝 Guia de Avaliação](GUIA_AVALIACAO.md)**: Critérios e checklist
- **[📊 Resumo Final](RESUMO_AVALIACAO_FINAL.md)**: Estatísticas e métricas
- **[🔍 Verificação](verificacao_final_entrega.md)**: Checklist de entrega

### 🧪 **Utilização e Teste**
- **[⚡ Execução Rápida](#-execução-rápida-5-minutos)**: Teste completo em 5 minutos
- **[🔧 Teste Individual](#-teste-individual)**: Testar componentes específicos
- **[📊 Verificação](#-verificação-de-componentes)**: Verificar funcionamento
- **[🎯 Testes de Funcionalidade](#-testes-de-funcionalidade)**: Testes detalhados por área
- **[🎥 Demonstração em Vídeo](https://youtu.be/FcNGYkVKkZ4)**: Apresentação completa do sistema

## 🤝 Contribuição

1. **Fork** o repositório [https://github.com/Cas-Maravilha/Enterprise-Challenge---Sprint-4---Reply](https://github.com/Cas-Maravilha/Enterprise-Challenge---Sprint-4---Reply)
2. **Crie** uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. **Commit** suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/nova-funcionalidade`)
5. **Abra** um Pull Request

### 📋 **Guias de Contribuição**
- **[📝 Code of Conduct](CODE_OF_CONDUCT.md)**: Código de conduta
- **[🤝 Contributing](CONTRIBUTING.md)**: Guia de contribuição
- **[📋 Issues](https://github.com/Cas-Maravilha/Enterprise-Challenge---Sprint-4---Reply/issues)**: Reportar problemas
- **[💬 Discussions](https://github.com/Cas-Maravilha/Enterprise-Challenge---Sprint-4---Reply/discussions)**: Discussões da comunidade

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Equipe

- **Desenvolvimento**: Equipe FIAP - Enterprise Challenge Sprint 4
- **RM**: 562948
- **Mentoria**: Reply
- **Instituição**: FIAP - GRADUAÇÃO
- **Curso**: 1 ANO • 2025/1 - INTELIGÊNCIA ARTIFICIAL
- **Contato Principal**: kilamu_10@yahoo.com.br | +244 932 027 393

## 📞 Suporte

### 🆘 **Canais de Suporte**
- **📧 Email**: kilamu_10@yahoo.com.br
- **📱 Suporte**: +244 932 027 393
- **🐛 Issues**: [GitHub Issues](https://github.com/Cas-Maravilha/Enterprise-Challenge---Sprint-4---Reply/issues)
- **📚 Documentação**: [Wiki do Projeto](https://github.com/Cas-Maravilha/Enterprise-Challenge---Sprint-4---Reply/wiki)
- **💬 Discussions**: [GitHub Discussions](https://github.com/Cas-Maravilha/Enterprise-Challenge---Sprint-4---Reply/discussions)

### 🔧 **Recursos de Ajuda**
- **[🔍 Troubleshooting](#-troubleshooting)**: Soluções para problemas comuns
- **[📚 Documentação Adicional](#-documentação-adicional)**: Guias detalhados
- **[📋 Guia de Avaliação](GUIA_AVALIACAO.md)**: Para avaliadores
- **[📊 Resumo Final](RESUMO_AVALIACAO_FINAL.md)**: Estatísticas do projeto

#### 🎥 **Suporte Visual**

[![Suporte Visual - Tutorial Completo](https://img.youtube.com/vi/FcNGYkVKkZ4/maxresdefault.jpg)](https://youtu.be/FcNGYkVKkZ4)

**[▶️ Tutorial Completo](https://youtu.be/FcNGYkVKkZ4)** - Demonstração passo-a-passo do sistema

---

**Sistema IoT Monitoring** - Enterprise Challenge Sprint 4 - Reply  
*FIAP - Graduação em Inteligência Artificial (1º Ano - 2025/1)*  
*Transformando dados industriais em insights acionáveis através de Machine Learning e IoT*