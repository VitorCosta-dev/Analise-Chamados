 Suporte Analytics

Projeto de analise de chamados de suporte tecnico, desenvolvido para praticar SQL, Python, Streamlit e Power BI em um cenario proximo da rotina de TI.

O objetivo do projeto e transformar dados operacionais de chamados em indicadores uteis para acompanhar volume, fila ativa, criticidade, tempo medio de resolucao e principais causas de atendimento.

 Tecnologias utilizadas

- PostgreSQL
- SQL
- Python
- Streamlit
- Power BI
- DAX

 Objetivo do projeto

Este projeto simula uma base de chamados de suporte tecnico e permite analisar informacoes como:

- quantidade total de chamados;
- chamados resolvidos;
- chamados abertos;
- fila ativa;
- chamados criticos;
- tempo medio de resolucao;
- chamados por categoria;
- chamados por setor;
- chamados por prioridade;
- historico dos ultimos chamados.

 Estrutura do projeto

```text
suporte-analytics/
├── app.py
├── gerar_chamados.py
├── suporte_analytics.sql
├── dashboard_suporte_analytics.pdf
├── medidas_suporte_analytics.dax
├── requirements.txt
├── .gitignore
└── README.md
```

 Sobre os arquivos

| Arquivo | Descricao |
| --- | --- |
| `app.py` | Interface em Streamlit para visualizar os indicadores e aplicar filtros |
| `gerar_chamados.py` | Script Python para gerar chamados ficticios no banco |
| `suporte_analytics.sql` | Script de criacao das tabelas, inserts iniciais, indices e views |
| `dashboard_suporte_analytics.pdf` | Versao em PDF do dashboard final |
| `medidas_suporte_analytics.dax` | Medidas DAX usadas no Power BI |
| `.env.example` | Modelo das variaveis de ambiente usadas na conexao com o banco |
| `.gitignore` | Arquivos e pastas ignorados pelo Git |

 Indicadores analisados

| Indicador | Finalidade |
| --- | --- |
| Total de chamados | Medir o volume geral de atendimentos |
| Chamados resolvidos | Acompanhar a capacidade de fechamento |
| Chamados abertos | Identificar pendencias atuais |
| Fila ativa | Somar chamados abertos e em andamento |
| Chamados criticos | Monitorar ocorrencias de maior prioridade |
| Tempo medio de resolucao | Avaliar eficiencia no atendimento |
| Chamados por categoria | Identificar principais causas de incidentes |
| Chamados por setor | Entender areas com maior demanda |
| Chamados por prioridade | Analisar a distribuicao da criticidade |

## Como executar o projeto

### 1. Criar o banco de dados

No PostgreSQL, crie o banco:

```sql
CREATE DATABASE suporte_analytics;
```

Depois, execute o script SQL de criacao das tabelas, inserts iniciais e views do projeto.

```sql
\i suporte_analytics.sql
```

### 2. Configurar as variaveis de ambiente

Crie um arquivo chamado `.env` com base no arquivo `.env.example`:

```text
DB_HOST=localhost
DB_NAME=suporte_analytics
DB_USER=postgres
DB_PASSWORD=sua_senha_do_postgres
DB_PORT=5432
```

O arquivo `.env` nao deve ser enviado para o GitHub.

### 3. Instalar as dependencias

No terminal, dentro da pasta do projeto:

```bash
pip install -r requirements.txt
```

### 4. Gerar dados ficticios

Com o banco criado e configurado, execute:

```bash
python gerar_chamados.py
```

Esse script insere chamados ficticios para permitir a analise dos dados.

### 5. Abrir a interface Streamlit

Execute:

```bash
python -m streamlit run app.py
```

O Streamlit abrira o dashboard no navegador.

## Dashboard em Power BI

O projeto tambem possui uma versao visual desenvolvida no Power BI, com KPIs, graficos e analise executiva.

O arquivo `.pbix` nao foi incluido no repositorio para evitar arquivos pesados e dependencias locais. O resultado final pode ser visualizado pelo PDF:

```text
dashboard_suporte_analytics.pdf
```

## Observacao sobre seguranca

As credenciais do banco nao ficam diretamente no codigo. O projeto utiliza variaveis de ambiente carregadas a partir de um arquivo `.env`, que deve permanecer fora do GitHub.

## Aprendizados do projeto

Durante o desenvolvimento deste projeto, foram praticados conceitos importantes para analise de dados:

- modelagem de banco de dados;
- criacao de consultas SQL;
- geracao de dados com Python;
- conexao entre Python e PostgreSQL;
- criacao de dashboard interativo;
- definicao de KPIs;
- construcao de medidas DAX;
- apresentacao de dados para tomada de decisao.

## Autor

Vitor Costa

GitHub: [github.com/VitorCosta-dev](https://github.com/VitorCosta-dev)
