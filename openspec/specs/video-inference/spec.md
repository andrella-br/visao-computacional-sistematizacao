# video-inference Specification

## Purpose

Demonstra o sistema de visão computacional funcionando em um vídeo real do cenário de segurança do trabalho, atendendo ao requisito de "Aplicação em vídeo" da Fase 4 do roadmap.

## Requirements

### Requirement: Inferência em vídeo real do cenário
O projeto SHALL rodar o detector e o segmentador treinados sobre o vídeo real do cenário (`video/input/video_final_canteiro_obra.mp4`, ≥30 segundos), salvando as saídas anotadas (caixas e máscaras) em `video/output/`.

#### Scenario: Vídeo anotado demonstra o sistema funcionando
- **WHEN** alguém assiste ao vídeo anotado gerado
- **THEN** vê as caixas de EPI (detector) e/ou as máscaras de pessoa (segmentador) sobrepostas nos quadros do vídeo real do canteiro de obra, com confiança das detecções visível

#### Scenario: Vídeo de saída é reprodutível
- **WHEN** o script de inferência em vídeo é executado novamente
- **THEN** gera a mesma saída anotada a partir dos mesmos pesos e do mesmo vídeo de entrada, sem exigir passos manuais adicionais
