# object-tracking Specification

## Purpose

Rastreia objetos entre quadros do vídeo (ByteTrack), atribuindo identidade persistente para contar violações de EPI de forma mais precisa que a heurística de agrupamento por tempo — item de bônus do enunciado.

## Requirements

### Requirement: Rastreamento com IDs persistentes
O projeto SHALL rodar o detector com um rastreador (ByteTrack, embutido no Ultralytics) sobre o vídeo do cenário, atribuindo um ID persistente a cada objeto detectado entre quadros consecutivos, e salvar um vídeo anotado mostrando esses IDs.

#### Scenario: Objeto mantém o mesmo ID entre quadros
- **WHEN** o mesmo objeto (ex. uma pessoa sem colete) aparece em múltiplos quadros consecutivos do vídeo
- **THEN** o vídeo anotado mostra o mesmo ID de rastreamento para esse objeto ao longo dos quadros em que ele é visível

### Requirement: Contagem de violações únicas deduplicadas
O projeto SHALL contar, por classe de violação (`NO-Hardhat`, `NO-Mask`, `NO-Safety Vest`), quantos objetos rastreados distintos (tracks únicos) tiveram essa classe como dominante, e comparar essa contagem com os eventos brutos agrupados por tempo (Fase 4).

#### Scenario: Contagem por rastreamento difere da contagem por tempo
- **WHEN** alguém compara o número de eventos por tempo com o número de tracks únicos para a mesma classe
- **THEN** encontra ambos os números documentados lado a lado, evidenciando que o agrupamento por tempo pode super ou subestimar o número real de violações distintas
