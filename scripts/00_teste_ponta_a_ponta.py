"""
Teste ponta a ponta da Fase 0: aquisição (IBGE) -> transformação (SIRGAS2000/UTM23S)
-> carga no PostGIS (schema bruto).

Usa a malha municipal do Rio de Janeiro (API de malhas territoriais do IBGE) como
carga de validação — não é a malha final do projeto (essa vem na Fase 1 com as
sub-bacias ottocodificadas da ANA).
"""
import os

import geopandas as gpd
import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

IBGE_MALHA_URL = (
    "https://servicodados.ibge.gov.br/api/v3/malhas/estados/33"
    "?intrarregiao=municipio&formato=application/vnd.geo+json"
)
EPSG_IBGE = 4674  # SIRGAS 2000 geográfico, padrão de saída da API do IBGE
EPSG_PROJETO = 31983  # SIRGAS 2000 / UTM 23S, SRC único do projeto (ver CLAUDE.md)

load_dotenv()


def main() -> None:
    print(f"Baixando malha municipal (RJ) do IBGE...")
    resp = requests.get(IBGE_MALHA_URL, timeout=30)
    resp.raise_for_status()
    gdf = gpd.GeoDataFrame.from_features(resp.json()["features"], crs=EPSG_IBGE)
    print(f"  {len(gdf)} municípios recebidos")

    gdf = gdf.to_crs(epsg=EPSG_PROJETO)
    gdf = gdf.rename(columns={"codarea": "cd_mun"})

    url = (
        f"postgresql+psycopg2://{os.environ['POSTGRES_USER']}:"
        f"{os.environ['POSTGRES_PASSWORD']}@{os.environ.get('POSTGRES_HOST', 'localhost')}:"
        f"{os.environ.get('POSTGRES_PORT', 5432)}/{os.environ['POSTGRES_DB']}"
    )
    engine = create_engine(url)

    print("Gravando em bruto.ibge_malha_municipal_teste...")
    gdf.to_postgis(
        "ibge_malha_municipal_teste",
        engine,
        schema="bruto",
        if_exists="replace",
        index=False,
    )

    with engine.connect() as conn:
        count = conn.execute(
            text("SELECT count(*) FROM bruto.ibge_malha_municipal_teste")
        ).scalar()
        srid = conn.execute(
            text(
                "SELECT Find_SRID('bruto', 'ibge_malha_municipal_teste', 'geometry')"
            )
        ).scalar()

    print(f"Linhas na tabela: {count}")
    print(f"SRID da geometria: {srid} (esperado {EPSG_PROJETO})")
    assert count == len(gdf), "contagem de linhas divergente entre GeoDataFrame e PostGIS"
    assert srid == EPSG_PROJETO, "SRID gravado diferente do SRC único do projeto"
    print("Teste ponta a ponta OK: IBGE -> Python -> PostGIS (bruto.*)")


if __name__ == "__main__":
    main()
