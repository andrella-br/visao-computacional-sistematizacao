# Proposta — Fase 1: Definição e Dados

**Disciplina:** Visão Computacional e Reconhecimento de Padrões
**Integrante:** 1 (individual)

## Problema

Em canteiros de obra, o não uso de Equipamentos de Proteção Individual (EPI) — capacete e colete de segurança — é uma das principais causas de acidentes de trabalho. A fiscalização manual é cara, lenta e não escala para grandes obras ou múltiplas câmeras. Este projeto constrói um sistema de visão computacional que (1) **detecta** o uso ou ausência de EPIs em imagens de canteiro de obra e (2) **segmenta** as pessoas presentes na cena, demonstrando o funcionamento em vídeo.

## Classes-alvo

**Detecção (10 classes):** `Hardhat`, `NO-Hardhat`, `Safety Vest`, `NO-Safety Vest`, `Mask`, `NO-Mask`, `Person`, `Safety Cone`, `machinery`, `vehicle`.

**Segmentação (1 classe):** `person` (silhueta completa da pessoa).

## Fonte dos dados

- **Detecção:** *Construction Site Safety* (Roboflow Universe, espelhado no Kaggle por `snehilsanyal`), licença **CC BY 4.0**. Dataset completo com 2.801 imagens anotadas em formato YOLO; usamos um subconjunto de **350 imagens**, selecionado por amostragem estratificada (seed fixa = 42) que garante presença mínima de todas as 10 classes.
- **Segmentação:** subconjunto do **COCO 2017** (conjunto de validação), categoria `person`, que já possui máscaras de instância prontas. Usamos **300 imagens** (de 2.693 elegíveis), seed = 42.
- Ambos os datasets são públicos, citados com fonte e licença em `reports/eda-fase1.md`, e splits de treino/validação/teste (70/20/10) foram gerados com seed fixa e reprodutível (`src/data/make_splits.py`).

## Ferramenta de anotação/uso

Nenhuma anotação manual foi necessária nesta fase: ambos os datasets já vêm anotados (bounding boxes YOLO para EPIs; máscaras poligonais COCO para pessoas). Caso a Fase 3 exija refinamento das máscaras, a ferramenta prevista é o **Roboflow (Smart Polygon, assistido por SAM)**, que reduz o esforço manual de anotação para um integrante trabalhando sozinho.

## Por que essa escolha

- É o cenário citado como exemplo no próprio enunciado da disciplina.
- Combina uma fonte de detecção robusta e bem licenciada com uma fonte de segmentação padrão-ouro (COCO), citável e amplamente usada na literatura, sem custo de anotação manual.
- O volume do subconjunto (350 e 300 imagens) atende ao mínimo de 300 imagens exigido, mantendo o treino leve o suficiente para rodar em Colab por um único integrante.
