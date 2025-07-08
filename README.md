# Sistema de Análise de Viabilidade de Sêmen Ovino (API)

Este é o repositório do servidor web responsável pelo serviço de IA para detecção e realizar a contagem de espermatozoides, desenvolvido como parte do Trabalho de Conclusão de Curso (TCC) do IFCE. O sistema utiliza modelos de aprendizado de máquina para realizar a análise automática de imagens, oferecendo uma solução eficiente para o acompanhamento e estudo de células espermáticas.

## Visão Geral do Projeto

Este servidor é a espinha dorsal de uma aplicação que permite a análise automatizada da viabilidade de sêmen ovino. Ele expõe endpoints para:

* **Autenticação de Usuários:** Cadastro e login.
* **Análise de Imagens:** Recebe imagens de sêmen ovino, processa-as usando um modelo de Inteligência Artificial (YOLOv8) e retorna a contagem e localização de espermatozoides "corados" (mortos) e "não-corados" (vivos).

O objetivo é fornecer uma alternativa prática, de baixo custo e acessível para estudantes e pesquisadores em Zootecnia e Veterinária para análise reprodutiva.

## Tecnologias Utilizadas

* **Backend:** Python 3.9, Flask, Waitress (servidor WSGI)
* **Inteligência Artificial:** YOLOv8 (Ultralytics)
* **Contêineres:** Docker, Docker Compose

## Configuração do Ambiente

Para rodar o servidor localmente com Docker Compose, siga os passos abaixo:

### Pré-requisitos

* [Docker Desktop](https://www.docker.com/products/docker-desktop) (inclui Docker Engine e Docker Compose)
* Conexão à internet para baixar imagens Docker e o modelo YOLOv8 (se configurado para baixar na inicialização).

### Passos de Configuração

1.  **Clone o Repositório:**
    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd <pasta_do_seu_projeto> # Navegue até a raiz do seu projeto (onde está o docker-compose.yml)
    ```

2.  **Crie e Configure o Arquivo `.env`:**
    Na raiz do seu projeto, crie um arquivo chamado `.env` e preencha com suas variáveis de ambiente. Certifique-se de usar senhas fortes e uma chave secreta JWT complexa.

    ```dotenv
    # .env

    # Variáveis para o Modelo de IA
    MODEL_URL=https://drive.google.com/uc?export=download&id=1AHIswPP3LAirL9FNhmxjxqa0EYY4p0Eo # Ou a URL real do seu modelo
    MODEL_PATH=modelo-treinado.pt # Nome do arquivo do modelo dentro do contêiner

    **Importante:** O `MODEL_PATH` deve corresponder ao nome do arquivo que será criado ou copiado para `/app` no contêiner.

3.  **Crie o `requirements.txt`:**
    Certifique-se de que o arquivo `requirements.txt` na raiz do seu projeto contenha todas as dependências Python necessárias. Exemplo:

    ```
    Flask
    waitress
    ultralytics
    Pillow
    python-dotenv
    requests
    ```

4.  **Inicie os Serviços com Docker Compose:**
    Na raiz do seu projeto (onde está o `docker-compose.yml`), execute o seguinte comando:

    ```bash
    docker compose up --build -d
    ```
    * `--build`: Força a reconstrução das imagens Docker, garantindo que todas as suas alterações sejam aplicadas.
    * `-d`: Inicia os contêineres em modo "detached" (em segundo plano).

    Aguarde alguns minutos para que as imagens sejam baixadas (MySQL) e construídas (seu app Flask), e para que o MySQL inicie completamente.

## Uso da API

A API estará disponível em `http://localhost:5000`.

### Endpoints

* **`GET /teste`**
    * **Descrição:** Verifica a conectividade básica do servidor.
    * **Resposta esperada:** `{"message": "Conexão bem-sucedida!", "status_code": 200}`

* **`POST /analise`**
    * **Descrição:** Realiza a análise de viabilidade de sêmen em uma imagem.
    * **Autenticação:** Bearer Token (JWT obtido no `/login` ou `/cadastro`).
    * **Cabeçalho `Authorization`:** `Bearer <seu_jwt_token>`
    * **Corpo da Requisição:** `multipart/form-data` contendo o arquivo da imagem sob a chave `image`.
    * **Resposta de Sucesso:** Uma lista de detecções (células coradas/não-coradas), com coordenadas, confiança e rótulo.
        ```json
        [
            {
                "nome": "corada",
                "indice": 0,
                "confianca": 0.95,
                "caixa": {"x1": 10.0, "y1": 20.0, "x2": 30.0, "y2": 40.0}
            },
            {
                "nome": "nao-corada",
                "indice": 1,
                "confianca": 0.88,
                "caixa": {"x1": 50.0, "y1": 60.0, "x2": 70.0, "y2": 80.0}
            }
        ]
        ```

## Acesso ao MySQL (Opcional)

Se você precisar acessar o banco de dados MySQL diretamente no seu host (por exemplo, com MySQL Workbench ou DBeaver), ele estará disponível em `localhost:3306` com as credenciais definidas no seu arquivo `.env`.

## Parar e Limpar os Contêineres

Para parar e remover os contêineres e suas redes:

```bash
docker compose down