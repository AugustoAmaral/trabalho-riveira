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

## Modos de Execução

### 1. Modo Treino Automático (NOVO!)
- MediaPipe detecta e conta dedos automaticamente
- Pressione ESPAÇO para salvar todas as mãos detectadas
- Gera dataset rapidamente sem entrada manual
- Mostra landmarks da mão para verificação visual

### 2. Modo Normal
- Usa modelo treinado para classificação
- Permite captura manual com seleção de região
- Mostra detecções em tempo real

## Como Usar

### Gerando Dataset Rapidamente:

1. Execute e escolha modo 2:
   ```bash
   python3 main.py
   > Escolha (1 ou 2): 2
   ```

2. Posicione suas mãos mostrando diferentes números de dedos

3. Pressione ESPAÇO quando a detecção estiver correta
   - Salva automaticamente com a contagem do MediaPipe
   - Pode ter múltiplas mãos no frame

4. Gere 50-100 imagens em poucos minutos!

### Treinando o Modelo:

1. Execute novamente e escolha modo 1
2. O sistema perguntará se deseja treinar com as imagens
3. Responda 's' para treinar

## Controles

### Modo Treino Automático:
- **ESPAÇO**: Salvar todas as detecções atuais
- **M**: Modo correção manual - permite corrigir a contagem antes de salvar
- **ESC**: Sair

### Modo Normal:
- **ESPAÇO**: Captura manual (selecionar com mouse)
- **ESC**: Sair

## Indicadores Visuais

- **Retângulo Amarelo**: Detecção MediaPipe (modo treino)
- **Retângulo Laranja**: Mão detectada sem classificação
- **Retângulo Verde**: Mão com classificação do modelo
- **Landmarks**: Pontos da mão (modo treino)

## Dicas

- No modo treino, verifique se a contagem está correta antes de salvar
- Varie posições, ângulos e distâncias
- O MediaPipe é muito preciso, mas verifique visualmente
- Com 10-20 capturas (ESPAÇO) você já tem um bom dataset