# Suporte Analytics

Projeto de análise de chamados de suporte técnico, desenvolvido para praticar SQL, Python, Streamlit e Power BI em um cenário próximo da rotina de TI.

O objetivo do projeto é transformar dados operacionais de chamados em indicadores úteis para acompanhar volume, fila ativa, criticidade, tempo médio de resolução e principais causas de atendimento.

## Tecnologias utilizadas

- PostgreSQL
- SQL
- Python
- Streamlit
- Power BI
- DAX

## Objetivo do projeto

Este projeto simula uma base de chamados de suporte técnico e permite analisar informações como:

- quantidade total de chamados;
- chamados resolvidos;
- chamados abertos;
- fila ativa;
- chamados críticos;
- tempo médio de resolução;
- chamados por categoria;
- chamados por setor;
- chamados por prioridade;
- histórico dos últimos chamados.

## Estrutura do projeto

```text
suporte-analytics/
├── app.py
├── gerar_chamados.py
├── suporte_analytics.sql
├── dashboard_suporte_analytics.pdf
├── medidas_suporte_analytics.dax
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md