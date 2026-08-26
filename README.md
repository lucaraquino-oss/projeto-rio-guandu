# Bacia do Rio Guandu — análise de uso do solo e qualidade da água

Projeto-portfólio de análise ambiental. Ver [CLAUDE.md](CLAUDE.md) para o contexto
completo (pergunta de pesquisa, fases, convenções técnicas e riscos).

## Setup (Fase 0)

Pré-requisitos: Docker Engine + Docker Compose plugin.

```bash
cp .env.example .env   # ajuste a senha antes de subir o contêiner
docker compose up -d
docker compose exec postgis psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT postgis_full_version();"
```

O `sql/00_init.sql` é executado automaticamente na primeira inicialização do
volume (via `docker-entrypoint-initdb.d`) e cria a extensão PostGIS e os
schemas `bruto` e `analitico`.

### Ambiente Python

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/earthengine authenticate   # login Google, uma vez só
```

O Earth Engine exige um projeto GCP registrado (ver `EE_PROJECT` no `.env`).
Registro gratuito para uso acadêmico/não-comercial em
[code.earthengine.google.com/register](https://code.earthengine.google.com/register).

Teste ponta a ponta (IBGE → Python → PostGIS):

```bash
.venv/bin/python scripts/00_teste_ponta_a_ponta.py
```

## Estrutura

- `sql/` — scripts de inicialização e modelagem do banco.
- `scripts/` — aquisição de dados e utilitários Python.
- `docs/` — notas técnicas e relatório.

## Status

Ver tabela de fases em [CLAUDE.md](CLAUDE.md).
