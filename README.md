# 💱 Projeto de Ingestão, Transformação e Análise de Taxas de Câmbio

Este projeto foi desenvolvido na plataforma **Databricks** por **Bruno Lima de Santana** e **Diogo Antonio da Silva** como parte da disciplina **Python for Data Engineer** do MBA. O objetivo é construir um pipeline completo de dados para ingestão, tratamento, enriquecimento, agregação e geração de insights sobre taxas de câmbio, com foco no **Real Brasileiro (BRL)**.

## 🔄 Pipeline de Dados

O projeto é composto por quatro notebooks principais que representam as etapas do pipeline:

### 1. `ingestao`
- Realiza requisição à API de taxas de câmbio.
- Utiliza variáveis de ambiente (`API_KEY`, `API_URL`, `DEFAULT_PATH`, `LOG_PATH`).
- Gera DataFrame com taxas de conversão.
- Salva os dados em JSON na camada **Raw**.
- Registra logs em `ingestao.log`.

### 2. `transformacao`
- Lê os dados da camada Raw.
- Aplica transformações com PySpark via `tratamento_uniao_df`.
- Enriquece os dados com a tabela `moedas`.
- Salva os dados tratados na camada **Silver** (Parquet).
- Registra logs em `transformacao.log`.

### 3. `load`
- Lê os dados da camada Silver.
- Realiza agregações por continente.
- Salva os dados agregados na camada **Gold**.
- Registra logs em `load.log`.

### 4. `LLM`
- Lê os dados da camada Gold.
- Converte os dados para JSON.
- Envia prompt para o modelo Gemini.
- Gera relatório com insights em Markdown.
- Salva o relatório em `.txt`.

---

## 🔧 Função de Transformação: `tratamento_uniao_df`

Esta função é responsável por aplicar as transformações nos dados brutos de câmbio:

### Entradas:
- `df`: DataFrame com colunas `currency` e `value`.
- `rate`: moeda base (ex: `"BRL"`).
- `current_datetime`: timestamp da execução.

### Transformações aplicadas:
1. Renomeia as colunas:
   - `currency` → `moeda`
   - `value` → `taxa`
2. Adiciona metadados:
   - `base_currency`: moeda base usada na conversão.
   - `timestamp`: data e hora da execução.
3. Converte tipos:
   - `moeda`: `string`
   - `taxa`: `double`
4. Filtra os dados:
   - Remove a moeda base (`moeda != rate`)
   - Remove taxas inválidas (`taxa <= 0` ou `null`)

### Resultado:
Um DataFrame limpo e padronizado, pronto para enriquecimento e persistência na camada Silver.

---

## 🧪 Testes Unitários

- Implementados com `unittest` e `PySpark`.
- Valida:
  - Renomeação de colunas.
  - Adição de metadados (`base_currency`, `timestamp`).
  - Filtragem de dados inválidos.
- Arquivo: `tests/test_transformacoes.py`

---

## 🤖 Integração com LLM

- Modelo utilizado: `gemini-2.5-flash` via `google-genai`.
- Gera insights automáticos:
  - Moedas mais fortes e mais fracas.
  - Média por continente.
  - 3 insights acionáveis para investidores.
- Salva relatório em `relatorio_llm_YYYY-MM-DD.txt`.

---

## 🛠️ Orquestração com Job do Databricks

O pipeline é automatizado por meio de um **Job no Databricks**, que executa os notebooks em sequência:

### 🔁 Fluxo de Execução

1. **Ingestão** (`ingestao`)
2. **Transformação** (`transformacao`)
3. **Carregamento** (`load`)

### 🕒 Agendamento

- **Horário**: Todos os dias às **08:00** (horário de São Paulo)
- **Cron**: `8 0 8 * * ?`
- **Status**: Ativo (`UNPAUSED`)


### ⚙️ Parâmetros do Job

- `rate`: moeda base para conversão (default: `BRL`)
- `current_datetime`: passado automaticamente como `{{job.start_time.iso_datetime}}`

---

## ⚙️ Tecnologias Utilizadas

- Databricks
- Python 3
- PySpark
- pandas
- dotenv
- requests
- google-genai
- AWS S3
- GitHub (com organização e merge requests)

---

## ✅ Conclusão

Este projeto representa uma solução completa de engenharia de dados com:

- **Automação**
- **Qualidade de dados**
- **Enriquecimento semântico**
- **Análise inteligente com IA**