# Contexto do projeto — Bacia do Rio Guandu

## O que é isto
Projeto-portfólio de análise ambiental, com prazo de ~10 semanas, cujo objetivo é
demonstrar domínio de ArcGIS Pro, PostGIS, Python geoespacial, Power BI e licenciamento
ambiental para vagas de analista ambiental pleno / geoprocessamento no Rio de Janeiro.

**Pergunta de pesquisa:** como a mudança de uso e cobertura do solo na bacia do Guandu
entre 1990 e 2024 se relaciona com a qualidade da água bruta captada — e quais sub-bacias
deveriam ser prioridade de restauração e fiscalização?

## Entregáveis
1. Pipeline reprodutível (aquisição → banco → análise) neste repositório
2. Três pranchas cartográficas em ArcGIS Pro (mudança de uso, pressões, priorização)
3. Painel Power BI com indicadores por sub-bacia
4. Relatório técnico de 6–10 páginas em formato de consultoria

## Fases
| Fase | Escopo | Prazo | Status |
|---|---|---|---|
| 0 | Preparação de ambiente | 3 dias | em andamento |
| 1 | Recorte e base cartográfica (ANA ottocodificada, 8–15 sub-bacias) | sem. 1–2 | |
| 2 | Uso do solo no GEE (MapBiomas, cortes 1990/2000/2010/2024) | sem. 3–4 | |
| 3 | Modelagem estrela e carga no PostGIS | sem. 5 | |
| 4 | Análise espacial em SQL + Mann-Kendall | sem. 6 | |
| 5 | Camada regulatória e índice de priorização | sem. 7 | |
| 6 | Cartografia em ArcGIS Pro (trial de 21 dias começa aqui) | sem. 8 | |
| 7 | Painel Power BI | sem. 9 | |
| 8 | Relatório e empacotamento | sem. 10 | |

## Convenções técnicas
- **SRC único:** SIRGAS 2000 / UTM 23S (EPSG:31983). Área e distância nunca em geográficas.
- **Banco:** PostGIS em Docker. Schema `bruto` para carga direta, `analitico` para o
  modelo estrela — o mesmo modelo é reaproveitado no Power BI na Fase 7.
- **Carga sempre por script**, nunca manual. O valor do projeto é ser reproduzível.
- **Análise espacial em SQL** dentro do banco; Python só para aquisição e estatística.
- Credenciais em `.env` (fora do versionamento). Nada de segredo em commit.
- Commit e push ao fim de cada fase, com o README crescendo junto.

## Fora de escopo (decisão deliberada)
Machine learning, classificação supervisionada própria (usar MapBiomas pronto),
modelagem hidrológica, aplicação web. Cada um adiciona ~1 mês e nenhum requisito de vaga.

## Riscos conhecidos
- Dados do INEA podem estar em PDF ou indisponíveis → substituir por outorgas do SNIRH e
  licenciamento do IBAMA, e declarar a limitação no relatório.
- ID do asset MapBiomas muda a cada coleção — verificar a coleção corrente antes da Fase 2.
- O trial do ArcGIS Pro só pode ser ativado na Fase 6. Antes disso, verificar licença
  educacional/alumni da UFV.

## Estado atual
Fase 0 concluída até o esqueleto do repositório. Pendentes: subir o contêiner, rodar
`sql/00_init.sql`, criar o venv, autenticar no GEE e fazer o teste ponta a ponta com a
malha municipal do IBGE.
