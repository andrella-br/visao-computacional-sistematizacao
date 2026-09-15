## MODIFIED Requirements

### Requirement: Relatório de conformidade
O projeto SHALL gerar um relatório (arquivo **Parquet** com os eventos brutos + Markdown com resumo) mostrando, por classe de violação: número de eventos, tempo total de violação e percentual do vídeo com violação, além da lista dos eventos individuais.

#### Scenario: Resumo por classe é auditável
- **WHEN** alguém abre o relatório de conformidade
- **THEN** encontra quantos eventos de `NO-Hardhat`, `NO-Mask` e `NO-Safety Vest` ocorreram, o tempo total de cada um, e os timestamps de início/fim de cada evento individual

#### Scenario: Dados brutos são lidos como Parquet
- **WHEN** alguém carrega os dados brutos de eventos de violação em pandas ou outra ferramenta compatível
- **THEN** lê `reports/violacoes-epi.parquet` (não um `.csv`), com colunas tipadas (`classe`, `inicio_s`, `fim_s`, `duracao_s`, `confianca_media`)
