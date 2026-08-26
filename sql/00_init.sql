-- Fase 0 / subpasso 1.1 — inicialização do banco
-- SRC do projeto: SIRGAS 2000 / UTM 23S (EPSG:31983). Ver CLAUDE.md.

CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

CREATE SCHEMA IF NOT EXISTS bruto;      -- carga direta das fontes (ANA, MapBiomas, IBGE, SNIRH, IBAMA)
CREATE SCHEMA IF NOT EXISTS analitico;  -- modelo estrela, reaproveitado no Power BI na Fase 7

COMMENT ON SCHEMA bruto IS 'Dados carregados diretamente das fontes, sem transformação de modelo.';
COMMENT ON SCHEMA analitico IS 'Modelo estrela (fatos e dimensões) para análise em SQL e consumo no Power BI.';
