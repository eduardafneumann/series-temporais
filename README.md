# DataSUS - Séries Temporais

O DataSUS é o departamento de informática do Sistema Único de Saúde (SUS), responsável por fornecer sistemas de informação e suporte tecnológico que auxiliam no planejamento, operação e controle das ações de saúde pública. Entre seus serviços, destaca-se o TABNET, uma plataforma que disponibiliza dados cruciais para análises da situação de saúde, tomadas de decisão baseadas em evidências e a formulação de políticas públicas.

## Objetivo

Desenvolver uma plataforma web para visualização de séries temporais, utilizando os dados disponibilizados pelo DataSUS, facilitando a análise de informações de saúde ao longo do tempo.

## Requisitos (Linux e Windows)

### Ambiente de desenvolvimento

- [Python](https://www.python.org/)
- [Git](https://git-scm.com/downloads)

### Ambiente de produção

- [Docker Desktop](https://www.docker.com/get-started)
- [Git](https://git-scm.com/downloads)

## Configuração do ambiente de desenvolvimento (Windows)

A seguintes etapas consideram que o Python e o Git estejam previamente configurados na máquina na qual se quer criar este ambiente.

### Configurando o ambiente virtual do Python

- Clone este repositório com o comando:

```
git clone https://github.com/eduardafneumann/series-temporais.git
```

- Crie o ambiente virtual com o seguinte comando:

```
python -m venv venv
```

- Ative o ambiente virtual com:

```
venv\Scripts\activate
```

- Instale as depêncidas do projeto com o seguinte comando:

```
pip install -r ./frontend/requirements.txt
```

- Acesse a pasta do frontend com o comando:

```
cd frontend
```

- Inicie o servidor do Streamlit com o comando:

```
streamlit run ./frontend/streamlit_app.py --server.port 8000
```

- Acesse o frontend pela URL [localhost](http://localhost:8000)
  
## Configuração do ambiente de desenvolvimento Docker (Linux e Windows)

A seguintes etapas consideram que o Docker e o Git estejam previamente configurados na máquina na qual se quer criar este ambiente.

### Contêineres Docker

- Inicie o servidor Streamlit por meio do Docker:

```
docker-compose -f docker-compose.dev.yaml up --build
```

- Acesse o frontend pela URL [localhost](http://localhost)
