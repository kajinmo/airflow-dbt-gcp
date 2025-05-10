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
- pegar o arquivo mais recente
- ler o arquivo csv

Em Andamento
- incorporar logging
- incorporar unit testing
- incorporar mensagem de erro no slack
- criar dockerfile (instalar bibliotecas dentro do docker / funciona bem com uv / arquivo csv dentro do docker)
- Arrumar as variaveis de ambiente no docker-compose
- GCP - Subir o csv para o bucket gcs
- criar o dataset no bigquery
- gcs-to-raw 
- Construir a DAG
- Construir o conector no airflow com as credenciais do GCP

parte 2: dbt
- ver conteúdo osbre dbt
- Inserir validação de dados entre as camadas
- Definir as mensagens de erro para o BotSlack
- fazer a apresentação