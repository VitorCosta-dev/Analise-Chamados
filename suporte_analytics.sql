-- Projeto: Suporte Analytics
-- Banco sugerido: suporte_analytics
-- Execute este script dentro do banco suporte_analytics no PostgreSQL.

CREATE TABLE IF NOT EXISTS setor (
    id_setor SERIAL PRIMARY KEY,
    nome_setor VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS categoria (
    id_categoria SERIAL PRIMARY KEY,
    nome_categoria VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS tecnico (
    id_tecnico SERIAL PRIMARY KEY,
    nome_tecnico VARCHAR(100) NOT NULL UNIQUE,
    nivel_tecnico VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS chamado (
    id_chamado SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descricao TEXT,
    data_abertura TIMESTAMP NOT NULL,
    data_fechamento TIMESTAMP,
    prioridade VARCHAR(20) NOT NULL,
    status VARCHAR(30) NOT NULL,
    id_setor INTEGER NOT NULL REFERENCES setor(id_setor),
    id_tecnico INTEGER REFERENCES tecnico(id_tecnico),
    id_categoria INTEGER NOT NULL REFERENCES categoria(id_categoria),
    CONSTRAINT chk_chamado_prioridade
        CHECK (prioridade IN ('BAIXA', 'MEDIA', 'ALTA', 'CRITICA')),
    CONSTRAINT chk_chamado_status
        CHECK (status IN ('ABERTO', 'EM_ANDAMENTO', 'RESOLVIDO', 'CANCELADO')),
    CONSTRAINT chk_chamado_data_fechamento
        CHECK (data_fechamento IS NULL OR data_fechamento >= data_abertura)
);

INSERT INTO setor (id_setor, nome_setor) VALUES
    (1, 'Financeiro'),
    (2, 'Comercial'),
    (3, 'RH'),
    (4, 'Operacoes'),
    (5, 'Logistica'),
    (6, 'Administrativo')
ON CONFLICT (id_setor) DO UPDATE
SET nome_setor = EXCLUDED.nome_setor;

INSERT INTO categoria (id_categoria, nome_categoria) VALUES
    (1, 'Hardware'),
    (2, 'Software'),
    (3, 'Rede'),
    (4, 'Acesso'),
    (5, 'Sistema'),
    (6, 'Impressora')
ON CONFLICT (id_categoria) DO UPDATE
SET nome_categoria = EXCLUDED.nome_categoria;

INSERT INTO tecnico (id_tecnico, nome_tecnico, nivel_tecnico) VALUES
    (1, 'Vitor', 'Junior'),
    (2, 'Ana', 'Pleno'),
    (3, 'Bruno', 'Senior')
ON CONFLICT (id_tecnico) DO UPDATE
SET
    nome_tecnico = EXCLUDED.nome_tecnico,
    nivel_tecnico = EXCLUDED.nivel_tecnico;

SELECT setval('setor_id_setor_seq', (SELECT MAX(id_setor) FROM setor));
SELECT setval('categoria_id_categoria_seq', (SELECT MAX(id_categoria) FROM categoria));
SELECT setval('tecnico_id_tecnico_seq', (SELECT MAX(id_tecnico) FROM tecnico));

CREATE INDEX IF NOT EXISTS idx_chamado_status
    ON chamado(status);

CREATE INDEX IF NOT EXISTS idx_chamado_prioridade
    ON chamado(prioridade);

CREATE INDEX IF NOT EXISTS idx_chamado_data_abertura
    ON chamado(data_abertura);

CREATE OR REPLACE VIEW vw_chamados_completos AS
SELECT
    c.id_chamado,
    c.titulo,
    c.descricao,
    c.data_abertura,
    c.data_fechamento,
    ROUND(
        EXTRACT(EPOCH FROM (c.data_fechamento - c.data_abertura)) / 3600,
        2
    ) AS tempo_resolucao_horas,
    c.prioridade,
    c.status,
    s.nome_setor,
    cat.nome_categoria,
    t.nome_tecnico,
    t.nivel_tecnico
FROM chamado c
JOIN setor s
    ON c.id_setor = s.id_setor
JOIN categoria cat
    ON c.id_categoria = cat.id_categoria
LEFT JOIN tecnico t
    ON c.id_tecnico = t.id_tecnico;

CREATE OR REPLACE VIEW vw_indicadores_chamados AS
SELECT
    COUNT(*) AS total_chamados,
    COUNT(*) FILTER (WHERE status = 'RESOLVIDO') AS chamados_resolvidos,
    COUNT(*) FILTER (WHERE status = 'ABERTO') AS chamados_abertos,
    COUNT(*) FILTER (WHERE status = 'EM_ANDAMENTO') AS chamados_em_andamento,
    COUNT(*) FILTER (WHERE prioridade = 'CRITICA') AS chamados_criticos,
    ROUND(
        AVG(EXTRACT(EPOCH FROM (data_fechamento - data_abertura)) / 3600)
        FILTER (WHERE data_fechamento IS NOT NULL),
        2
    ) AS tempo_medio_resolucao_horas
FROM chamado;

SELECT *
FROM vw_chamados_completos
LIMIT 10;
