# 🚀 Projeto Final - Pipeline de Cotações Cambiais com Python + LLM


## Objetivo
1. Coleta taxas de câmbio da API https://www.exchangerate-api.com/.
2. Processar, validar e armazenar os dados em diferentes camadas (raw, silver, gold).
3. Integra uma LLM (ex.: ChatGPT) para gerar resumos e insights em linguagem natural, voltados a usuários de negócio.

## Fluxo do Projeto
<img width="539" height="207" alt="image" src="https://github.com/user-attachments/assets/928b934e-7201-42b5-aa37-b8dd593617d9" />

## 1. Ingestão (Ingest)
● Coletar dados da API https://www.exchangerate-api.com/.

● Salvar resposta JSON bruta em /raw/ com nome dos arquivos padronizados em YYYY-MM-DD.

💡 Configuração via .env ou YAML, nunca hardcode de chaves/API.

## 2. Transformação (Transform)
● Normalizar os dados (moeda, taxa, base_currency, timestamp).

● Garantir qualidade (nenhuma taxa negativa ou nula).

● Armazenar em /silver/.

## 3. Carga (Load)
● Gravar dados finais em formato Parquet em /gold/.

● (Opcional) Carregar também em banco relacional (Postgres/MySQL).

## 4. Enriquecimento com LLM (substitui orquestração)
### Usar o ChatGPT para interpretar as cotações e gerar um resumo em linguagem natural, como:

● “O Euro está 5% mais valorizado em relação ao mês passado.”

● “A volatilidade do JPY em relação ao USD está acima da média.”

### Criação de Explicações para Usuários de Negócio. Passar o dataset diário para o ChatGPT e pedir uma explicação executiva:

● “Explique em termos simples como está a variação das 5 principais moedas frente ao Real hoje.”

## 5. Testes e Observabilidade
● Testes unitários (ex.: validação de taxas numéricas).

● Logging estruturado durante ingestão e transformação. Usar biblioteca estruturada (logging ou structlog) com níveis (INFO,
ERROR).

● (Opcional) Logging do prompt/response do ChatGPT para auditoria.
