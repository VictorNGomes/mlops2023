# Podcast Summary - Dataquest.io Portfolio Project

Este projeto faz parte do portfólio de projetos do Dataquest.io e tem como objetivo criar um pipeline de dados usando o Apache Airflow. O pipeline baixa episódios de podcast automaticamente e os transcreve usando reconhecimento de fala, armazenando os resultados em um banco de dados SQLite para fácil consulta.

**Objetivos do Projeto:**

- Automatizar o processo de download de episódios de podcast.
- Transcrever automaticamente o conteúdo de áudio dos episódios.
- Armazenar os dados transcritos em um banco de dados para posterior análise.

**Modificações Realizadas:**

Foi relaizado o tratamento de exceções, registro de atividades (logging) e práticas de linting. Também incluímos uma seção sobre linting com o Pylint para garantir a qualidade e a consistência do código-fonte.

**Configuração e Instalação:**

**Configuração e Instalação:**

Para configurar o ambiente de desenvolvimento e executar este projeto localmente, siga estas etapas:

1. Instale o Apache Airflow 2.3+ e Python 3.8+ no seu sistema. Para instruções detalhadas sobre a instalação do Apache Airflow, consulte [este guia](https://github.com/dataquestio/project-walkthroughs/blob/master/podcast_summary/steps.md#instala%C3%A7%C3%A3o-do-apache-airflow).

2. Instale as bibliotecas Python necessárias, como `pandas`, `sqlite3`, `xmltodict`, `requests`, `vosk`, e `pydub`.

3. Configure as credenciais necessárias, como a URL do podcast e informações de autenticação, conforme aplicável.

4. Clone este repositório para o seu ambiente local.

5. Execute o arquivo `podcast_summary.py` para iniciar o pipeline de dados.

Para obter mais detalhes e instruções específicas sobre a configuração local, consulte a seção "Configuração Local" abaixo.

Este projeto oferece uma oportunidade prática de trabalhar com o Apache Airflow, processamento de áudio e integração de várias bibliotecas Python. Explore o código e utilize as instruções fornecidas para executar e personalizar o pipeline de acordo com as suas necessidades.



Este projeto oferece uma oportunidade prática de trabalhar com o Apache Airflow, processamento de áudio e integração de várias bibliotecas Python. Explore o código e utilize as instruções fornecidas para executar e personalizar o pipeline de acordo com as suas necessidades.



## Registo e Tratamento de Erros

Neste projeto, implementamos o tratamento de erros e o registo para garantir a confiabilidade e a rastreabilidade do nosso pipeline de dados. Abaixo, descrevemos como lidamos com exceções e geramos registos:

### Tratamento de Exceções

Integramos o tratamento de exceções em partes críticas do código para gerir com elegância situações inesperadas. Os principais tipos de exceções que tratamos incluem:

* `requests.exceptions.RequestException`: Capturamos esta exceção ao efetuar pedidos HTTP à fonte do podcast ou ao descarregar ficheiros de áudio. Permite-nos lidar com problemas de rede e evitar falhas no pipeline.

* `IOError`: Esta exceção é tratada ao trabalhar com ficheiros, especificamente durante o download e armazenamento de ficheiros de áudio. Ajuda-nos a lidar eficazmente com erros relacionados com ficheiros.

* `Exception`: Capturamos a classe genérica `Exception` para lidar com quaisquer erros imprevistos que possam surgir durante o processo de transcrição.

### Registo

O registo é um componente crucial deste projeto, e usamos o módulo Python `logging` para criar registos em vários níveis. Eis como utilizamos o registo:

* Nível `INFO`: Utilizamos registos `INFO` para fornecer informações de alto nível sobre o progresso do pipeline. Por exemplo, registamos o número de episódios encontrados, descarregados e transcritos.

* Nível `DEBUG`: Os registos `DEBUG` são usados para informações detalhadas e para efeitos de depuração. Durante a transcrição de áudio, registamos o progresso à medida que os segmentos de áudio são processados.

* Nível `ERROR`: Quando ocorre uma exceção que não pode ser tratada, registamos a mensagem de erro com o nível `ERROR`. Isso permite-nos identificar e resolver rapidamente problemas.

Ao incorporar o tratamento de exceções e o registo, garantimos que o pipeline pode lidar elegantemente com várias situações, fornecer informações sobre a sua execução e facilitar a resolução de problemas em caso de erros.

Sinta-se à vontade para explorar o código e os registos para obter uma compreensão mais profunda de como o pipeline opera. Se encontrar problemas ou tiver dúvidas, consulte os registos para obter informações valiosas.

## Linting e Qualidade de Código

Neste projeto, adotamos práticas de linting com o Pylint para garantir a qualidade e a consistência do nosso código-fonte. O Pylint é uma ferramenta amplamente utilizada para análise estática de código Python, que verifica o código em busca de conformidade com regras e diretrizes definidas. Aqui estão alguns detalhes sobre o linting realizado:

### Ferramenta de Linting

Utilizamos o [Pylint](https://www.pylint.org/) como a ferramenta de linting para analisar o nosso código Python. O Pylint aplica um conjunto de regras de estilo e boas práticas para identificar potenciais problemas e melhorar a legibilidade do código.

### Regras de Estilo

As regras de estilo abordadas pelo Pylint incluem, mas não estão limitadas a:

* [Exemplo de Regra 1]: missing-module-docstring / C0114
* [Exemplo de Regra 2]: line-too-long / C0301
* [Exemplo de Regra 3]: missing-function-docstring / C0116

### Benefícios do Linting

O linting com o Pylint oferece diversos benefícios, incluindo:

* Melhoria na legibilidade do código.
* Padronização e consistência do estilo de codificação.
* Identificação precoce de problemas potenciais.
* Facilitação da colaboração entre membros da equipe.

No geral, o linting com o Pylint faz parte da nossa abordagem para manter um código limpo, confiável e de alta qualidade. Se você estiver contribuindo para este projeto, recomendamos seguir as diretrizes de linting com o Pylint para garantir que o seu código esteja alinhado com os padrões estabelecidos.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir problemas (issues) e enviar solicitações de pull (pull requests) para melhorar o projeto.

## Licença

Este projeto é licenciado sob a Licença MIT - consulte o arquivo [LICENSE](LICENSE) para obter detalhes.





