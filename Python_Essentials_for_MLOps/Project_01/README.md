# Sistema de Recomendação de Filmes

Este projeto tem como objetivo a refatoração, a aplicação dos princípios de código limpo, linting, tratamento de exceções, logging e testes unitários. Trata-se de um sistema de recomendação de filmes baseado em conteúdo e filtragem colaborativa. Este projeto faz parte do portfólio de projetos da Dataquest.io. 

O projeto utiliza o conjunto de dados [MovieLens 25M](https://grouplens.org/datasets/movielens/25m/) para recomendar filmes com base em títulos, gêneros e avaliações dos usuários.



## Uso

- `movie_recommendations_reafctored.py` é o script principal que permite realizar pesquisas e obter recomendações de filmes com base em títulos.No script ta já está selecionado o título Toy Story.

- As funções do projeto estão organizadas em módulos para facilitar a manutenção e expansão.

## Funcionalidades Principais

- **Refatoração:** O projeto foi refatorado para melhorar a estrutura, organização e legibilidade do código.

- **Princípios de Código Limpo:** Foram aplicados princípios de código limpo para garantir que o código seja fácil de entender e manter.

- **Linting com Pylint:** O Pylint foi usado para verificar o código em busca de possíveis problemas, garantindo um código mais consistente.

- **Tratamento de Exceções:** Foram implementados tratamentos de exceções para lidar com erros de forma adequada, melhorando a robustez do sistema.

- **Logging:** Foi implementado um sistema de logging para registrar informações detalhadas sobre as operações do sistema, facilitando a depuração e monitoramento.
    ```log
    2023-10-08 01:51:31,942 [INFO] - Arquivos CSV extraídos com sucesso.
    2023-10-08 01:51:40,521 [INFO] - Dados carregados com sucesso.
    2023-10-08 01:51:40,788 [INFO] - Título limpo
    2023-10-08 01:51:41,870 [INFO] - Títulos vetorizados
    2023-10-08 23:31:48,881 [INFO] - Diretório './movielens_data/' já existe.
    2023-10-08 23:31:53,386 [INFO] - O arquivo ZIP já existe. Não é necessário fazer o download novamente.
    2023-10-08 23:32:03,998 [INFO] - Arquivos CSV extraídos com sucesso.
    2023-10-08 23:35:12,552 [INFO] - Dados carregados com sucesso.

    ```

- **Testes Unitários:** Testes unitários foram desenvolvidos para garantir o funcionamento correto das funcionalidades.
    ```
    pytest tests_project_01.py
    ```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir problemas (issues) e enviar solicitações de pull (pull requests) para melhorar o projeto.

## Licença

Este projeto é licenciado sob a Licença MIT - consulte o arquivo [LICENSE](LICENSE) para obter detalhes.

## Agradecimentos

- [MovieLens](https://grouplens.org/datasets/movielens/25m/) por fornecer o conjunto de dados.

