Pós-graduação · Visão Computacional e Reconhecimento de Padrões
🎯 Sistematização — Sistema de Visão Computacional para Detecção e Segmentação
Atividade prática em grupo · Aprendizagem Baseada em Projetos · Prof. Romes Heriberto
📌 O desafio: Visão Computacional em Campo
Empresas brasileiras — da construção civil ao agronegócio — usam visão computacional para enxergar em escala aquilo que nenhuma equipe humana conseguiria monitorar. Nesta Sistematização, seu grupo vai assumir o papel de um time de engenharia de IA contratado para resolver um problema real: construir, de ponta a ponta, um sistema que detecta e segmenta objetos em imagens e demonstra o funcionamento em vídeo.

Cada grupo escolhe um cenário (ou propõe o seu, mediante aprovação do professor):

🦺 Segurança do Trabalho
Detecção de EPIs (capacete, colete) e segmentação de pessoas em canteiros de obra.	🐂 Agronegócio
Detecção e segmentação de gado, frutas ou pragas para contagem e monitoramento.	🏙️ Cidades Inteligentes
Buracos em vias, vagas de estacionamento ou análise de tráfego urbano.
🛒 Varejo
Detecção e segmentação de produtos em prateleiras (auditoria de gôndola).	💡 Cenário livre
Qualquer problema real de detecção + segmentação, mediante aprovação prévia do professor na Fase 1.
✅ Requisitos técnicos mínimos (todos os grupos)
Dataset: mínimo de 300 imagens anotadas do domínio escolhido. Pode ser público (Roboflow Universe, Kaggle, subconjunto do COCO) com a fonte citada, ou anotado pelo grupo (CVAT, Label Studio ou Roboflow). Dividir em treino / validação / teste.
Detecção de objetos: fine-tuning de um detector moderno — YOLO (Ultralytics) ou Faster R-CNN (torchvision).
Segmentação: segmentação de instâncias (YOLO-seg ou Mask R-CNN) ou semântica (DeepLab / U-Net) no mesmo domínio.
Avaliação: mAP@0.5 e mAP@0.5:0.95, IoU, precisão/recall, matriz de confusão e análise qualitativa de erros (exemplos comentados de falsos positivos e falsos negativos).
Vídeo: inferência do sistema em um vídeo real do cenário (mínimo 30 segundos).
⭐ Bônus (até +0,5 ponto extra, limitado à nota máxima): rastreamento de objetos no vídeo (ByteTrack ou DeepSORT) ou demo interativa publicada (Gradio / Hugging Face Spaces).
🗺️ Roadmap do projeto 
FASE 1 · 
Definição e dados. Formar o grupo, escolher o cenário e o dataset. Fazer a análise exploratória das imagens (quantidade por classe, resolução, condições de luz, desbalanceamento). Entregar proposta de 1 página: problema, classes-alvo, fonte dos dados e ferramenta de anotação.

FASE 2 · 
Baseline de detecção. Preparar os dados (formato YOLO ou COCO, splits fixos com seed). Fazer o fine-tuning do detector no Colab (GPU), registrar curvas de treino e obter as primeiras métricas no conjunto de validação. Documentar hiperparâmetros (épocas, tamanho de imagem, batch, augmentation).

FASE 3 · 
Segmentação. Treinar (ou adaptar) o modelo de segmentação no mesmo domínio. Comparar visualmente caixas × máscaras: o que a segmentação revela que a detecção não mostra? Ajustar o dataset/anotações se necessário.

FASE 4 · 
Avaliação e vídeo. Rodar a avaliação completa no conjunto de teste (nunca visto no treino): mAP, IoU, precisão/recall, matriz de confusão. Montar a análise de erros com exemplos comentados. Executar a inferência no vídeo do cenário e gravar o resultado.

FASE 5 ·
Entrega e apresentação. Finalizar o relatório técnico, organizar o repositório (README com instruções de reprodução), gravar o vídeo-pitch e submeter tudo no Moodle.

🧰 Ferramentas sugeridas
Google Colab (GPU) · PyTorch / torchvision · Ultralytics YOLO · OpenCV · CVAT / Label Studio / Roboflow (anotação) · supervision (visualização) · GitHub.

📦 Como será a entrega
Grupos: 1 a 5 integrantes. Todos os membros submetem pelo AVA, identificando todos os componente no README.
Item 1 — Relatório técnico README (PDF ou MD, 6–10 páginas): problema e cenário · dataset e EDA · metodologia (modelos e hiperparâmetros) · resultados com métricas · análise de erros · limitações e próximos passos.
Item 2 — Repositório GitHub: código organizado + README com instruções de reprodução e link do dataset.
Item 3 — Notebook Colab executável: com as células de treino, avaliação e inferência (saídas visíveis).
Item 4 — Vídeo-pitch (5–8 min): YouTube não listado ou Google Drive, com participação de todos os integrantes, demonstrando o sistema funcionando (incluindo o vídeo com inferência).
Prazo final: ⚠️ Conforme Cronograma
Integridade acadêmica: datasets e códigos de terceiros devem ser citados. O uso de IA generativa como apoio é permitido e deve ser declarado no relatório (onde e como foi usada). Entregas em atraso não serão aceitas, exceto casos avaliados pela coordenação.
📊 Barema de avaliação (100%)
Critério	O que será avaliado	Peso
1. Problema e dataset	Clareza do cenário, qualidade e origem dos dados, EDA e splits corretos.	10%
2. Detecção de objetos	Pipeline funcional, fine-tuning correto, desempenho e documentação dos hiperparâmetros.	25%
3. Segmentação	Implementação correta (instâncias ou semântica), qualidade das máscaras e comparação com a detecção.	20%
4. Avaliação e análise crítica	mAP, IoU, precisão/recall, matriz de confusão e análise de erros no conjunto de teste.	20%
5. Aplicação em vídeo	Inferência demonstrada em vídeo real do cenário (≥ 30 s).	10%
6. Relatório e repositório	Documentação, organização, reprodutibilidade e citação de fontes.	10%
7. Vídeo-pitch	Clareza, domínio técnico do grupo e participação de todos os integrantes.	5%
Total	100%
Dúvidas? Utilize o fórum Fale com o Professor. Bom projeto! 🚀 — Prof. Romes Heriberto