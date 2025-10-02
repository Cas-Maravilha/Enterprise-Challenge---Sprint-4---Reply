# Arquitetura Final - Sistema IoT Monitoring Sprint 3

## Diagrama da Arquitetura Completa

```mermaid
graph TB
    %% FONTE DE DADOS
    subgraph FONTE["🔌 FONTE DE DADOS"]
        ESP32["ESP32 + Sensores<br/>• DHT22 (Temp/Umidade)<br/>• LDR (Luminosidade)<br/>• PIR (Movimento)<br/>• Pressão Barométrica<br/>• Vibração Triaxial<br/>• Nível Ultrassônico"]
        WOKWI["Simulação Wokwi<br/>• Ambiente Virtual<br/>• Dados Sintéticos<br/>• Testes de Integração"]
    end
    
    %% INGESTÃO
    subgraph INGESTAO["📥 INGESTÃO DE DADOS"]
        MQTT["MQTT Broker<br/>• HiveMQ Cloud<br/>• Tópico: industrial/sensors/data<br/>• QoS 1 (At Least Once)<br/>• Retenção de Mensagens"]
        PIPELINE["Pipeline Integrado ESP32<br/>• Recebimento MQTT<br/>• Validação de Dados<br/>• Processamento em Tempo Real<br/>• Cache Inteligente<br/>• Thread Pool"]
    end
    
    %% ARMAZENAMENTO
    subgraph ARMAZENAMENTO["💾 ARMAZENAMENTO"]
        MYSQL["MySQL Database<br/>• 11 Tabelas Relacionais<br/>• Índices Otimizados<br/>• Particionamento por Ano<br/>• Pool de Conexões<br/>• Triggers Automáticos"]
        TABELAS["Tabelas Principais<br/>• dispositivos<br/>• sensores<br/>• leituras_sensores<br/>• alertas<br/>• usuarios<br/>• logs_sistema"]
    end
    
    %% MACHINE LEARNING
    subgraph ML["🤖 MACHINE LEARNING"]
        MODELOS["Modelos de ML<br/>• Random Forest Classifier<br/>• Isolation Forest<br/>• Ensemble Híbrido<br/>• 10 Features (7 originais + 3 derivadas)<br/>• Retreinamento Automático"]
        DETECCAO["Detecção de Anomalias<br/>• Inferência em Tempo Real<br/>• Thresholds Configuráveis<br/>• Níveis de Confiança<br/>• Alertas Automáticos"]
    end
    
    %% VISUALIZAÇÃO E ALERTAS
    subgraph VISUALIZACAO["📊 VISUALIZAÇÃO E ALERTAS"]
        DASHBOARD["Dashboard Web<br/>• Interface Responsiva<br/>• KPIs em Tempo Real<br/>• Gráficos Interativos<br/>• Atualização Automática<br/>• API REST"]
        ALERTAS["Sistema de Alertas<br/>• Thresholds Configuráveis<br/>• Regras Simples<br/>• Classificação por Severidade<br/>• Notificações Visuais"]
        RELATORIOS["Relatórios Automáticos<br/>• Diários/Semanais/Mensais<br/>• Gráficos Personalizados<br/>• Templates HTML<br/>• Envio por Email"]
    end
    
    %% MONITORAMENTO
    subgraph MONITORAMENTO["📈 MONITORAMENTO"]
        KPIS["KPIs do Sistema<br/>• Dispositivos Ativos<br/>• Leituras por Segundo<br/>• Taxa de Anomalias<br/>• Disponibilidade<br/>• Performance ML"]
        OBSERVABILIDADE["Observabilidade<br/>• Logs Estruturados<br/>• Métricas de Performance<br/>• Monitoramento de Drift<br/>• Alertas de Sistema"]
    end
    
    %% INTEGRAÇÃO
    subgraph INTEGRACAO["🔗 INTEGRAÇÃO"]
        APIS["APIs REST<br/>• /api/kpis<br/>• /api/alertas<br/>• /api/graficos/*<br/>• /api/status<br/>• Documentação Swagger"]
        WEBHOOKS["Webhooks<br/>• Notificações Externas<br/>• Integração com Slack<br/>• Integração com Teams<br/>• Callbacks Customizados"]
    end
    
    %% SEGURANÇA
    subgraph SEGURANCA["🛡️ SEGURANÇA"]
        AUTENTICACAO["Autenticação<br/>• JWT Tokens<br/>• RBAC (Role-Based)<br/>• MFA (Multi-Factor)<br/>• Session Management"]
        CRIPTOGRAFIA["Criptografia<br/>• TLS 1.3<br/>• AES-256<br/>• Hash de Senhas<br/>• Certificados SSL"]
    end
    
    %% FLUXO PRINCIPAL
    ESP32 -->|"Dados Sensores"| MQTT
    WOKWI -->|"Dados Simulados"| MQTT
    MQTT -->|"MQTT Messages"| PIPELINE
    PIPELINE -->|"Dados Validados"| MYSQL
    MYSQL -->|"Dados Estruturados"| TABELAS
    MYSQL -->|"Dados para Treino"| MODELOS
    MODELOS -->|"Modelos Treinados"| DETECCAO
    DETECCAO -->|"Anomalias Detectadas"| ALERTAS
    MYSQL -->|"Dados para Visualização"| DASHBOARD
    MYSQL -->|"Métricas do Sistema"| KPIS
    DASHBOARD -->|"APIs Disponíveis"| APIS
    APIS -->|"Integrações"| WEBHOOKS
    
    %% FLUXOS SECUNDÁRIOS
    DETECCAO -->|"Alertas ML"| ALERTAS
    MYSQL -->|"Dados para Relatórios"| RELATORIOS
    MYSQL -->|"Métricas de Performance"| OBSERVABILIDADE
    DASHBOARD -->|"Autenticação"| AUTENTICACAO
    APIS -->|"Criptografia"| CRIPTOGRAFIA
    
    %% ESTILOS
    classDef fonte fill:#E1F5FE,stroke:#01579B,stroke-width:2px
    classDef ingestao fill:#E8F5E8,stroke:#2E7D32,stroke-width:2px
    classDef armazenamento fill:#FCE4EC,stroke:#C2185B,stroke-width:2px
    classDef ml fill:#FFF3E0,stroke:#E65100,stroke-width:2px
    classDef visualizacao fill:#E8F5E8,stroke:#2E7D32,stroke-width:2px
    classDef monitoramento fill:#FCE4EC,stroke:#C2185B,stroke-width:2px
    classDef integracao fill:#E1F5FE,stroke:#01579B,stroke-width:2px
    classDef seguranca fill:#FFEBEE,stroke:#C62828,stroke-width:2px
    
    class FONTE,ESP32,WOKWI fonte
    class INGESTAO,MQTT,PIPELINE ingestao
    class ARMAZENAMENTO,MYSQL,TABELAS armazenamento
    class ML,MODELOS,DETECCAO ml
    class VISUALIZACAO,DASHBOARD,ALERTAS,RELATORIOS visualizacao
    class MONITORAMENTO,KPIS,OBSERVABILIDADE monitoramento
    class INTEGRACAO,APIS,WEBHOOKS integracao
    class SEGURANCA,AUTENTICACAO,CRIPTOGRAFIA seguranca
```

## 🔄 Encadeamento dos Blocos

### **1. FONTE DE DADOS → INGESTÃO**
```
ESP32 + Sensores → MQTT Broker → Pipeline Integrado
```

**Fluxo:**
- Sensores ESP32 coletam dados físicos
- Dados enviados via MQTT para o broker
- Pipeline recebe e valida os dados
- Processamento em tempo real com cache

### **2. INGESTÃO → ARMAZENAMENTO**
```
Pipeline → MySQL Database → Tabelas Relacionais
```

**Fluxo:**
- Dados validados são persistidos no MySQL
- 11 tabelas relacionais com integridade referencial
- Índices otimizados para performance
- Triggers automáticos para atualizações

### **3. ARMAZENAMENTO → MACHINE LEARNING**
```
MySQL → Modelos ML → Detecção de Anomalias
```

**Fluxo:**
- Dados do banco são usados para treinar modelos
- Random Forest + Isolation Forest em ensemble
- Inferência em tempo real para novos dados
- Detecção automática de anomalias

### **4. ML → VISUALIZAÇÃO E ALERTAS**
```
Detecção ML → Sistema de Alertas → Dashboard Web
```

**Fluxo:**
- Anomalias detectadas geram alertas
- Alertas classificados por severidade
- Dashboard atualizado em tempo real
- Relatórios automáticos gerados

### **5. VISUALIZAÇÃO → INTEGRAÇÃO**
```
Dashboard → APIs REST → Webhooks Externos
```

**Fluxo:**
- Dashboard expõe APIs REST
- Integração com sistemas externos
- Webhooks para notificações
- Segurança com JWT e RBAC

## 📊 Características da Arquitetura

### **Escalabilidade**
- **Horizontal**: Microserviços independentes
- **Vertical**: Otimização de recursos
- **Cache**: Redis para performance
- **Load Balancing**: Distribuição de carga

### **Disponibilidade**
- **99.9% Uptime**: Redundância e failover
- **Monitoramento**: Alertas proativos
- **Backup**: Dados e configurações
- **Recuperação**: Processos automatizados

### **Segurança**
- **TLS 1.3**: Comunicação criptografada
- **JWT**: Autenticação stateless
- **RBAC**: Controle de acesso granular
- **AES-256**: Criptografia de dados

### **Performance**
- **Tempo Real**: Latência < 100ms
- **Throughput**: 1000+ leituras/segundo
- **Cache**: Dados frequentes em memória
- **Otimização**: Consultas e índices

## 🎯 Benefícios da Arquitetura

### **Operacionais**
- **Visibilidade Completa**: Monitoramento em tempo real
- **Alertas Proativos**: Detecção antecipada de problemas
- **Relatórios Automáticos**: Análises regulares
- **Interface Intuitiva**: Fácil uso e navegação

### **Técnicos**
- **Modularidade**: Componentes independentes
- **Manutenibilidade**: Código bem estruturado
- **Testabilidade**: Testes automatizados
- **Documentação**: Completa e atualizada

### **Negócio**
- **Redução de Custos**: Manutenção preventiva
- **Melhoria da Qualidade**: Detecção de anomalias
- **Tomada de Decisão**: Dados em tempo real
- **Compliance**: Auditoria e logs completos

---

**Arquitetura Final - Enterprise Challenge Sprint 3 - Reply**
