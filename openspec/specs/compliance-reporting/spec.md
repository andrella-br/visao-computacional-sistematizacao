# compliance-reporting Specification

## Purpose

Transforma as detecções de EPI do vídeo em um relatório de auditoria de segurança, mostrando quando e por quanto tempo cada violação (ausência de EPI) ocorreu — uma aplicação prática do sistema de detecção além da demonstração visual em vídeo.

## Requirements

### Requirement: Detecção de violações por quadro
O projeto SHALL rodar o detector da Fase 2 sobre o vídeo do cenário, quadro a quadro, registrando toda detecção das classes de violação (`NO-Hardhat`, `NO-Mask`, `NO-Safety Vest`) com o timestamp do quadro e a confiança da detecção.

#### Scenario: Violação é registrada com timestamp
- **WHEN** um quadro do vídeo contém uma detecção de `NO-Safety Vest` com confiança acima do limiar
- **THEN** o timestamp (em segundos) desse quadro e a confiança da detecção ficam registrados nos dados brutos

### Requirement: Agrupamento em eventos de violação
O projeto SHALL agrupar detecções consecutivas da mesma classe de violação em "eventos" (um intervalo de início/fim), em vez de listar cada quadro individualmente.

#### Scenario: Detecções consecutivas viram um único evento
- **WHEN** a mesma classe de violação é detectada em quadros consecutivos (sem lacuna maior que um limiar curto)
- **THEN** essas detecções são agregadas em um único evento, com timestamp de início, fim, duração e confiança média — não como linhas separadas por quadro

### Requirement: Relatório de conformidade
O projeto SHALL gerar um relatório (arquivo **Parquet** com os eventos brutos + Markdown com resumo) mostrando, por classe de violação: número de eventos, tempo total de violação e percentual do vídeo com violação, além da lista dos eventos individuais.

#### Scenario: Resumo por classe é auditável
- **WHEN** alguém abre o relatório de conformidade
- **THEN** encontra quantos eventos de `NO-Hardhat`, `NO-Mask` e `NO-Safety Vest` ocorreram, o tempo total de cada um, e os timestamps de início/fim de cada evento individual

#### Scenario: Dados brutos são lidos como Parquet
- **WHEN** alguém carrega os dados brutos de eventos de violação em pandas ou outra ferramenta compatível
- **THEN** lê `reports/violacoes-epi.parquet` (não um `.csv`), com colunas tipadas (`classe`, `inicio_s`, `fim_s`, `duracao_s`, `confianca_media`)
