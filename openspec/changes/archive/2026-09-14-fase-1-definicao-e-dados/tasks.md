## 1. Aquisição dos dados

- [x] 1.1 Baixar o dataset completo "Construction Site Safety" (Roboflow/Kaggle, CC BY 4.0) temporariamente, selecionar por amostragem estratificada um subconjunto de ~300-400 imagens que preserve todas as 10 classes, salvar apenas o subconjunto em `data/raw/construction-site-safety/` e verificar que todas as classes aparecem no subconjunto
- [x] 1.2 Baixar um subconjunto do COCO (categoria `person`, com máscaras) de volume equivalente (~300 imagens) para `data/raw/coco-person/`, e verificar que cada imagem baixada tem anotação de máscara de `person`
- [x] 1.3 Documentar em `docs/` (ou seção do README) a fonte, licença e contagem de imagens de cada dataset baixado

## 2. Splits reprodutíveis

- [x] 2.1 Definir e documentar uma seed fixa de split (treino/validação/teste) e aplicá-la ao dataset de detecção, verificando que rodar novamente com a mesma seed reproduz os mesmos splits
- [x] 2.2 Aplicar a mesma seed ao subconjunto do COCO usado para segmentação e verificar a reprodutibilidade da mesma forma

## 3. Análise exploratória (EDA)

- [x] 3.1 Calcular e registrar a contagem de instâncias por classe do **subconjunto** de detecção selecionado (`Hardhat`, `NO-Hardhat`, `Safety Vest`, `NO-Safety Vest`, `Mask`, `NO-Mask`, `Person`, `Safety Cone`, `machinery`, `vehicle`) e salvar o resultado (tabela/gráfico) em `reports/figures/`
- [x] 3.2 Registrar resolução das imagens e observações sobre condições de iluminação (amostragem visual) para o subconjunto de detecção
- [x] 3.3 Identificar e documentar o desbalanceamento entre classes no subconjunto (ex. proporção `Hardhat` vs `NO-Hardhat`), destacando classes sub-representadas mesmo após a amostragem estratificada

## 4. Documentação e proposta

- [x] 4.1 Escrever a proposta de 1 página (`docs/proposta-fase1.md`): problema, classes-alvo, fonte dos dados, ferramenta/estratégia de anotação, e verificar que cobre todos os itens exigidos pelo enunciado
- [x] 4.2 Atualizar `README.md` para declarar o cenário "Segurança do Trabalho" no lugar de "a definir", incluindo as classes-alvo
- [x] 4.3 Atualizar `docs/roadmap.md` (Fase 1) marcando o cenário e o dataset como definidos

## 5. Validação final

- [x] 5.1 Rodar `openspec validate fase-1-definicao-e-dados --strict` e confirmar que a mudança passa sem erros
- [x] 5.2 Revisar manualmente que nenhuma decisão de arquitetura/hiperparâmetro de modelo foi tomada nesta mudança (fica para a Fase 2 e Fase 3)
