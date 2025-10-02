# Guia de Contribuição

Obrigado por considerar contribuir para o Sistema de Monitoramento Industrial com ESP32! Este documento fornece diretrizes para contribuir com o projeto.

## Código de Conduta

Este projeto e todos os participantes estão sujeitos ao [Código de Conduta](CODE_OF_CONDUCT.md). Ao participar, espera-se que você respeite este código.

## Como posso contribuir?

### Reportando Bugs

Bugs são rastreados como issues no GitHub. Ao criar uma issue para um bug, inclua:

- Um título claro e descritivo
- Passos detalhados para reproduzir o problema
- Comportamento esperado vs. comportamento observado
- Capturas de tela, se aplicável
- Informações sobre seu ambiente (sistema operacional, versão do Python, etc.)

### Sugerindo Melhorias

Melhorias também são rastreadas como issues no GitHub. Ao sugerir uma melhoria, inclua:

- Um título claro e descritivo
- Descrição detalhada da melhoria proposta
- Justificativa para a melhoria (por que ela seria útil)
- Exemplos de como a melhoria funcionaria, se aplicável

### Pull Requests

1. Faça um fork do repositório
2. Clone seu fork: `git clone https://github.com/seu-usuario/sistema-monitoramento-industrial.git`
3. Crie uma branch para sua feature: `git checkout -b feature/nova-feature`
4. Faça suas alterações
5. Execute os testes: `pytest`
6. Commit suas alterações: `git commit -m 'Adiciona nova feature'`
7. Push para a branch: `git push origin feature/nova-feature`
8. Abra um Pull Request

## Padrões de Código

### Python

- Siga a [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use docstrings no formato [Google Style](https://google.github.io/styleguide/pyguide.html)
- Mantenha a cobertura de testes acima de 80%
- Use type hints quando apropriado

### MicroPython

- Siga as mesmas diretrizes do Python quando possível
- Otimize para uso de memória
- Documente limitações específicas do MicroPython

### Documentação

- Use Markdown para toda a documentação
- Mantenha a documentação atualizada com o código
- Inclua exemplos quando apropriado

## Processo de Desenvolvimento

### Branches

- `main`: Branch principal, sempre estável
- `develop`: Branch de desenvolvimento
- `feature/*`: Branches para novas features
- `bugfix/*`: Branches para correções de bugs
- `release/*`: Branches para preparação de releases

### Commits

Use mensagens de commit claras e descritivas, seguindo o padrão:

```
<tipo>(<escopo>): <descrição>

<corpo>

<rodapé>
```

Tipos: feat, fix, docs, style, refactor, test, chore

### Versionamento

Este projeto segue o [Versionamento Semântico](https://semver.org/).

## Testes

- Escreva testes unitários para novas funcionalidades
- Execute todos os testes antes de submeter um Pull Request
- Mantenha a cobertura de testes alta

## Revisão de Código

- Todos os Pull Requests requerem revisão de pelo menos um mantenedor
- Feedback deve ser construtivo e respeitoso
- Resolva todos os comentários antes de solicitar nova revisão

## Recursos Adicionais

- [Documentação do ESP32](https://docs.espressif.com/projects/esp-idf/en/latest/)
- [Documentação do MicroPython](https://docs.micropython.org/)
- [Guia de Estilo Python](https://www.python.org/dev/peps/pep-0008/)
- [Guia de Contribuição do GitHub](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors)

## Agradecimentos

Suas contribuições são valiosas e muito apreciadas. Obrigado por ajudar a melhorar este projeto!