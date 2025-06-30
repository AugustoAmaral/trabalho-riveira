# Sistema de Reconhecimento de Mãos

## Instalação

```bash
pip3 install -r requirements.txt
```

## Estrutura do Projeto

```
.
├── main.py              # Ponto de entrada
├── data_handler.py      # Gerencia dataset
├── model_trainer.py     # Treina/carrega modelo
├── hand_detector.py     # Detecta mãos no frame
├── capture_manager.py   # Interface de captura
└── hand_dataset/        # Diretório de imagens
    ├── 0_fingers/
    ├── 1_fingers/
    ├── 2_fingers/
    ├── 3_fingers/
    ├── 4_fingers/
    └── 5_fingers/
```

## Como Usar

1. **Primeira execução**:
   ```bash
   python3 main.py
   ```

2. **Capturar imagens para treinamento**:
   - Pressione ESPAÇO para congelar o frame
   - Clique e arraste para selecionar a mão
   - Digite o número de dedos levantados (0-5)
   - A imagem será salva automaticamente

3. **Treinar o modelo**:
   - Após coletar ~50-100 imagens
   - O programa perguntará se deseja treinar
   - Responda 's' para treinar com as imagens existentes

4. **Visualização em tempo real**:
   - Após treinar, o programa detectará mãos automaticamente
   - Mostrará retângulos verdes com contagem de dedos

## Controles

- **ESPAÇO**: Capturar frame para treinamento
- **ESC**: Sair do programa
- **Mouse**: Selecionar região da mão (durante captura)

## Dicas

- Capture imagens com diferentes iluminações
- Varie a distância e ângulo da mão
- Inclua diferentes tons de pele se possível
- Mínimo recomendado: 10 imagens por número de dedos