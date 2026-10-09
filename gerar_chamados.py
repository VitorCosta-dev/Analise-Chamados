import random
import os
from datetime import datetime, timedelta

import pg8000.dbapi
from dotenv import load_dotenv

load_dotenv()

conexao = pg8000.dbapi.connect(
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_NAME", "suporte_analytics"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD"),
    port=int(os.getenv("DB_PORT", "5432"))
)

cursor = conexao.cursor()

titulos = {
    1: [
        "Computador nao liga",
        "Troca de monitor",
        "Teclado com defeito",
        "Mouse nao funciona"
    ],
    2: [
        "Erro ao abrir sistema",
        "Programa travando",
        "Atualizacao de software",
        "Instalacao de aplicativo"
    ],
    3: [
        "Internet lenta",
        "Sem conexao de rede",
        "Falha no Wi-Fi",
        "Problema de acesso a pasta de rede"
    ],
    4: [
        "Reset de senha",
        "Usuario bloqueado",
        "Permissao de acesso",
        "Criacao de usuario"
    ],
    5: [
        "Erro no sistema interno",
        "Tela com falha no sistema",
        "Sistema indisponivel",
        "Lentidao no sistema"
    ],
    6: [
        "Impressora nao imprime",
        "Troca de toner",
        "Impressora offline",
        "Fila de impressao travada"
    ]
}

prioridades = ["BAIXA", "MEDIA", "ALTA", "CRITICA"]
status_opcoes = ["ABERTO", "EM_ANDAMENTO", "RESOLVIDO", "CANCELADO"]

for i in range(200):
    id_categoria = random.randint(1, 6)
    id_setor = random.randint(1, 6)
    id_tecnico = random.randint(1, 3)

    titulo = random.choice(titulos[id_categoria])
    descricao = f"Chamado gerado para analise de suporte: {titulo}."

    data_abertura = datetime.now() - timedelta(days=random.randint(0, 180), hours=random.randint(0, 23))
    status = random.choices(
        status_opcoes,
        weights=[15, 20, 55, 10],
        k=1
    )[0]

    if status in ["RESOLVIDO", "CANCELADO"]:
        data_fechamento = data_abertura + timedelta(hours=random.randint(1, 96))
    else:
        data_fechamento = None

    prioridade = random.choices(
        prioridades,
        weights=[35, 35, 20, 10],
        k=1
    )[0]

    cursor.execute("""
        INSERT INTO chamado (
            titulo,
            descricao,
            data_abertura,
            data_fechamento,
            prioridade,
            status,
            id_setor,
            id_tecnico,
            id_categoria
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        titulo,
        descricao,
        data_abertura,
        data_fechamento,
        prioridade,
        status,
        id_setor,
        id_tecnico,
        id_categoria
    ))

conexao.commit()

cursor.close()
conexao.close()

print("200 chamados inseridos com sucesso!")
