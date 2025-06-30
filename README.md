# Sistema de Reconhecimento de Mãos

Sistema modular para detecção de mãos e contagem de dedos usando MediaPipe para detecção e um classificador customizado para contagem.

## Instalação

```bash
pip3 install -r requirements.txt
```

## Estrutura do Projeto

```
.
├── main.py              # Ponto de entrada
├── data_handler.py      # Gerencia dataset
├── model_trainer.py     # Treina/carrega modelo de classificação
├── hand_detector.py     # Detecta mãos usando MediaPipe
├── capture_manager.py   # Interface de captura
└── hand_dataset/        # Diretório de imagens
    ├── 0_fingers/
    ├── 1_fingers/
    ├── 2_fingers/
    ├── 3_fingers/
    ├── 4_fingers/
    └── 5_fingers/
```

## Como Funciona

1. **Detecção**: MediaPipe detecta mãos com alta precisão
2. **Classificação**: Modelo customizado conta os dedos nas regiões detectadas
3. **Treinamento**: Você treina apenas o classificador de dedos (muito mais simples)

## Como Usar

1. **Primeira execução**:
   ```bash
   python3 main.py
   ```
   - O sistema já detectará mãos (retângulos laranjas)
   - Mas não contará dedos até treinar

2. **Capturar imagens para treinamento**:
   - Pressione ESPAÇO quando uma mão estiver visível
   - Clique e arraste para selecionar a mão
   - Digite o número de dedos levantados (0-5)

3. **Treinar o classificador**:
   - Com ~30-50 imagens já funciona bem
   - O programa perguntará se deseja treinar
   - Após treinar, verá retângulos verdes com contagem

## Controles

- **ESPAÇO**: Capturar frame para treinamento
- **ESC**: Sair do programa
- **Mouse**: Selecionar região da mão (durante captura)

## Dicas para Melhor Desempenho

- O MediaPipe já detecta mãos muito bem
- Foque em capturar diferentes posições de dedos
- 5-10 exemplos por número de dedos já é suficiente
- Varie ângulos e distâncias

## Indicadores Visuais

- **Retângulo Laranja**: Mão detectada (sem classificação)
- **Retângulo Verde**: Mão detectada com contagem de dedos
- **Porcentagem**: Confiança da classificação