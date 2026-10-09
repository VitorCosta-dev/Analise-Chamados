import os

import pg8000.dbapi
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Suporte Analytics",
    layout="wide"
)

st.title("Dashboard de Chamados de Suporte")
st.write("Projeto de análise de chamados técnicos usando PostgreSQL, Python e Streamlit.")

conexao = pg8000.dbapi.connect(
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_NAME", "suporte_analytics"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD"),
    port=int(os.getenv("DB_PORT", "5432"))
)

cursor = conexao.cursor()

st.sidebar.header("Filtros")

cursor.execute("SELECT DISTINCT status FROM chamado ORDER BY status;")
status_opcoes = [linha[0] for linha in cursor.fetchall()]

cursor.execute("SELECT DISTINCT prioridade FROM chamado ORDER BY prioridade;")
prioridade_opcoes = [linha[0] for linha in cursor.fetchall()]

cursor.execute("SELECT DISTINCT nome_setor FROM setor ORDER BY nome_setor;")
setor_opcoes = [linha[0] for linha in cursor.fetchall()]

cursor.execute("SELECT DISTINCT nome_categoria FROM categoria ORDER BY nome_categoria;")
categoria_opcoes = [linha[0] for linha in cursor.fetchall()]

status = st.sidebar.multiselect(
    "Status",
    status_opcoes,
    default=status_opcoes
)

prioridade = st.sidebar.multiselect(
    "Prioridade",
    prioridade_opcoes,
    default=prioridade_opcoes
)

setor = st.sidebar.multiselect(
    "Setor",
    setor_opcoes,
    default=setor_opcoes
)

categoria = st.sidebar.multiselect(
    "Categoria",
    categoria_opcoes,
    default=categoria_opcoes
)


def montar_lista_sql(lista):
    return ", ".join(["%s"] * len(lista))


def montar_filtros():
    filtros_sql = []
    parametros_sql = []

    if status:
        filtros_sql.append(f"c.status IN ({montar_lista_sql(status)})")
        parametros_sql.extend(status)

    if prioridade:
        filtros_sql.append(f"c.prioridade IN ({montar_lista_sql(prioridade)})")
        parametros_sql.extend(prioridade)

    if setor:
        filtros_sql.append(f"s.nome_setor IN ({montar_lista_sql(setor)})")
        parametros_sql.extend(setor)

    if categoria:
        filtros_sql.append(f"cat.nome_categoria IN ({montar_lista_sql(categoria)})")
        parametros_sql.extend(categoria)

    if filtros_sql:
        return "WHERE " + " AND ".join(filtros_sql), parametros_sql

    return "", parametros_sql


def adicionar_condicao(where_sql, condicao):
    if where_sql:
        return where_sql + " AND " + condicao

    return "WHERE " + condicao


def mostrar_grafico_barras(titulo, dados):
    st.subheader(titulo)

    if not dados:
        st.info("Nenhum dado encontrado.")
        return

    maior_valor = max([linha[1] for linha in dados])

    html = ""

    for nome, total in dados:
        largura = (total / maior_valor) * 100

        html += f"""
        <div style="margin-bottom: 12px;">
            <strong>{nome}</strong> - {total}
            <div style="background-color: #262730; border-radius: 6px; height: 24px; margin-top: 4px;">
                <div style="
                    background-color: #ff4b4b;
                    width: {largura}%;
                    height: 24px;
                    border-radius: 6px;
                "></div>
            </div>
        </div>
        """

    st.markdown(html, unsafe_allow_html=True)


where_sql, parametros = montar_filtros()

query_base = f"""
FROM chamado c
JOIN setor s ON c.id_setor = s.id_setor
JOIN categoria cat ON c.id_categoria = cat.id_categoria
LEFT JOIN tecnico t ON c.id_tecnico = t.id_tecnico
{where_sql}
"""

cursor.execute(
    f"""
    SELECT COUNT(*)
    {query_base};
    """,
    parametros
)
total_chamados = cursor.fetchone()[0]

cursor.execute(
    f"""
    SELECT COUNT(*)
    FROM chamado c
    JOIN setor s ON c.id_setor = s.id_setor
    JOIN categoria cat ON c.id_categoria = cat.id_categoria
    LEFT JOIN tecnico t ON c.id_tecnico = t.id_tecnico
    {adicionar_condicao(where_sql, "c.status = 'RESOLVIDO'")};
    """,
    parametros
)
resolvidos = cursor.fetchone()[0]

cursor.execute(
    f"""
    SELECT COUNT(*)
    FROM chamado c
    JOIN setor s ON c.id_setor = s.id_setor
    JOIN categoria cat ON c.id_categoria = cat.id_categoria
    LEFT JOIN tecnico t ON c.id_tecnico = t.id_tecnico
    {adicionar_condicao(where_sql, "c.status = 'ABERTO'")};
    """,
    parametros
)
abertos = cursor.fetchone()[0]

cursor.execute(
    f"""
    SELECT COUNT(*)
    FROM chamado c
    JOIN setor s ON c.id_setor = s.id_setor
    JOIN categoria cat ON c.id_categoria = cat.id_categoria
    LEFT JOIN tecnico t ON c.id_tecnico = t.id_tecnico
    {adicionar_condicao(where_sql, "c.prioridade = 'CRITICA'")};
    """,
    parametros
)
criticos = cursor.fetchone()[0]

cursor.execute(
    f"""
    SELECT ROUND(
        AVG(EXTRACT(EPOCH FROM (c.data_fechamento - c.data_abertura)) / 3600),
        2
    )
    FROM chamado c
    JOIN setor s ON c.id_setor = s.id_setor
    JOIN categoria cat ON c.id_categoria = cat.id_categoria
    LEFT JOIN tecnico t ON c.id_tecnico = t.id_tecnico
    {adicionar_condicao(where_sql, "c.data_fechamento IS NOT NULL")};
    """,
    parametros
)
tempo_medio = cursor.fetchone()[0]

if tempo_medio is None:
    tempo_medio = 0

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total", total_chamados)
col2.metric("Resolvidos", resolvidos)
col3.metric("Abertos", abertos)
col4.metric("Críticos", criticos)
col5.metric("Tempo médio", f"{tempo_medio}h")

st.divider()

cursor.execute(
    f"""
    SELECT cat.nome_categoria, COUNT(*) AS total
    {query_base}
    GROUP BY cat.nome_categoria
    ORDER BY total DESC;
    """,
    parametros
)
dados_categoria = cursor.fetchall()
mostrar_grafico_barras("Chamados por Categoria", dados_categoria)

cursor.execute(
    f"""
    SELECT s.nome_setor, COUNT(*) AS total
    {query_base}
    GROUP BY s.nome_setor
    ORDER BY total DESC;
    """,
    parametros
)
dados_setor = cursor.fetchall()
mostrar_grafico_barras("Chamados por Setor", dados_setor)

cursor.execute(
    f"""
    SELECT c.prioridade, COUNT(*) AS total
    {query_base}
    GROUP BY c.prioridade
    ORDER BY total DESC;
    """,
    parametros
)
dados_prioridade = cursor.fetchall()
mostrar_grafico_barras("Chamados por Prioridade", dados_prioridade)

st.subheader("Últimos Chamados")

cursor.execute(
    f"""
    SELECT
        c.id_chamado,
        c.titulo,
        c.status,
        c.prioridade,
        s.nome_setor,
        cat.nome_categoria,
        t.nome_tecnico,
        c.data_abertura
    {query_base}
    ORDER BY c.data_abertura DESC
    LIMIT 20;
    """,
    parametros
)

dados_chamados = cursor.fetchall()

html_tabela = """
<table style="width:100%; border-collapse: collapse;">
    <thead>
        <tr>
            <th style="text-align:left; padding:8px; border-bottom:1px solid #444;">ID</th>
            <th style="text-align:left; padding:8px; border-bottom:1px solid #444;">Título</th>
            <th style="text-align:left; padding:8px; border-bottom:1px solid #444;">Status</th>
            <th style="text-align:left; padding:8px; border-bottom:1px solid #444;">Prioridade</th>
            <th style="text-align:left; padding:8px; border-bottom:1px solid #444;">Setor</th>
            <th style="text-align:left; padding:8px; border-bottom:1px solid #444;">Categoria</th>
            <th style="text-align:left; padding:8px; border-bottom:1px solid #444;">Técnico</th>
            <th style="text-align:left; padding:8px; border-bottom:1px solid #444;">Data abertura</th>
        </tr>
    </thead>
    <tbody>
"""

for linha in dados_chamados:
    html_tabela += f"""
        <tr>
            <td style="padding:8px; border-bottom:1px solid #333;">{linha[0]}</td>
            <td style="padding:8px; border-bottom:1px solid #333;">{linha[1]}</td>
            <td style="padding:8px; border-bottom:1px solid #333;">{linha[2]}</td>
            <td style="padding:8px; border-bottom:1px solid #333;">{linha[3]}</td>
            <td style="padding:8px; border-bottom:1px solid #333;">{linha[4]}</td>
            <td style="padding:8px; border-bottom:1px solid #333;">{linha[5]}</td>
            <td style="padding:8px; border-bottom:1px solid #333;">{linha[6]}</td>
            <td style="padding:8px; border-bottom:1px solid #333;">{linha[7]}</td>
        </tr>
    """

html_tabela += """
    </tbody>
</table>
"""

st.markdown(html_tabela, unsafe_allow_html=True)

cursor.close()
conexao.close()
