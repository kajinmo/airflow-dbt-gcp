# airflow-dbt-gcp

### Checklist
Ok
- Setup do ambiente de desenvolvimento
- Inicializar o Airflow - Criar o ambiente
- Inicializar o Airflow - Inicializar o ambiente
- GCP - Criar o projeto
- GCP - Criar um bucket
- GCP - Ativar o BigQuery API
- GCP - Criar uma conta de serviço (IAM) para GC Storage e BigQuery
- GCP - Salvar o json e renomear
- Pydantic - Criar regras de Validação
- BotSlack - Criar Bot para mandar mensagem
- Pegar o arquivo mais recente da pasta data
- Ler o arquivo csv e aplicar a validação
- incorporar logging
- incorporar unit testing
- incorporar mensagem de erro no slack

Em Andamento
- criar dockerfile (instalar bibliotecas dentro do docker / uv / arquivo csv dentro do docker)
- Arrumar as variaveis de ambiente no docker-compose
- Construir a DAG
- GCP - Subir o csv para o bucket gcs
- criar o dataset no bigquery
- gcs-to-raw 
- Construir o conector no airflow com as credenciais do GCP

parte 2: dbt
- conteúdo dbt
- Inserir validação de dados entre as camadas
- Definir as mensagens de erro para o BotSlack
- fazer a apresentação

FROM astrocrpublic.azurecr.io/runtime:12.9.0
