import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Constantes para os diretórios
PASTA_ENTRADA = "./entrada/"  # Pasta atual
PASTA_SAIDA = "./saida/"  # Pasta de saída

def calcular_limiar_otsu(histograma, total_pixels):
    """
    Implementação do algoritmo de Otsu para encontrar o limiar ótimo.
    """
    # Peso acumulado
    peso_soma = 0
    # Soma acumulada
    soma = 0
    # Valor máximo para variância entre classes
    variancia_max = 0
    # Limiar ótimo
    limiar = 0
    
    # Valores possíveis de intensidade (0-255)
    for i in range(256):
        # Peso da classe 1 (pixels com valor menor ou igual a i)
        peso_1 = peso_soma
        # Peso da classe 2 (pixels com valor maior que i)
        peso_2 = total_pixels - peso_1
        
        # Se uma das classes está vazia, continua para o próximo i
        if peso_1 == 0 or peso_2 == 0:
            peso_soma += histograma[i]
            soma += i * histograma[i]
            continue
        
        # Média da classe 1
        media_1 = soma / peso_1 if peso_1 > 0 else 0
        # Média da classe 2
        media_2 = (soma_total - soma) / peso_2 if peso_2 > 0 else 0
        
        # Variância entre classes
        variancia = peso_1 * peso_2 * ((media_1 - media_2) ** 2)
        
        # Atualiza o limiar se a variância atual é maior
        if variancia > variancia_max:
            variancia_max = variancia
            limiar = i
        
        # Atualiza o peso e a soma para o próximo i
        peso_soma += histograma[i]
        soma += i * histograma[i]
    
    return limiar

def processar_imagem(caminho_imagem, pasta_saida):
    """
    Processa uma imagem: converte para escala de cinza e aplica binarização de Otsu.
    """
    # Carrega a imagem
    imagem = Image.open(caminho_imagem)
    
    # Converte para escala de cinza
    imagem_cinza = imagem.convert('L')
    
    # Converte para numpy array para processamento
    img_array = np.array(imagem_cinza)
    
    # Calcula o histograma
    histograma = np.zeros(256, dtype=int)
    altura, largura = img_array.shape
    total_pixels = altura * largura
    
    for y in range(altura):
        for x in range(largura):
            histograma[img_array[y, x]] += 1
    
    # Cálculo de soma total para Otsu
    global soma_total
    soma_total = 0
    for i in range(256):
        soma_total += i * histograma[i]
    
    # Calcula o limiar usando o algoritmo de Otsu
    limiar = calcular_limiar_otsu(histograma, total_pixels)
    
    # Aplica binarização usando o limiar calculado
    imagem_binaria = np.zeros_like(img_array)
    for y in range(altura):
        for x in range(largura):
            if img_array[y, x] > limiar:
                imagem_binaria[y, x] = 255
            else:
                imagem_binaria[y, x] = 0
    
    # Obtém o nome do arquivo sem o caminho completo
    nome_arquivo = os.path.basename(caminho_imagem)
    base_nome, extensao = os.path.splitext(nome_arquivo)
    
    # Salva as imagens processadas
    Image.fromarray(img_array).save(os.path.join(pasta_saida, f"{base_nome}_cinza{extensao}"))
    Image.fromarray(imagem_binaria).save(os.path.join(pasta_saida, f"{base_nome}_binaria{extensao}"))
    
    # Opcional: visualização dos resultados
    plt.figure(figsize=(15, 5))
    plt.subplot(131)
    plt.title('Original')
    plt.imshow(imagem)
    
    plt.subplot(132)
    plt.title('Escala de Cinza')
    plt.imshow(img_array, cmap='gray')
    
    plt.subplot(133)
    plt.title(f'Binária (Otsu, limiar={limiar})')
    plt.imshow(imagem_binaria, cmap='gray')
    
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_saida, f"{base_nome}_comparacao.png"))
    plt.close()

def main():
    print("Iniciando processamento de imagens...")
    
    # Cria a pasta de saída se não existir
    if not os.path.exists(PASTA_SAIDA):
        os.makedirs(PASTA_SAIDA)
        print(f"Pasta de saída criada: {PASTA_SAIDA}")
    
    # Lista todos os arquivos na pasta
    arquivos = os.listdir(PASTA_ENTRADA)
    
    # Filtra apenas arquivos JPG e PNG
    extensoes_validas = ['.jpg', '.jpeg', '.png']
    imagens = [arquivo for arquivo in arquivos if os.path.isfile(os.path.join(PASTA_ENTRADA, arquivo)) and 
                os.path.splitext(arquivo.lower())[1] in extensoes_validas]
    
    print(f"Encontradas {len(imagens)} imagens para processar.")
    
    # Processa cada imagem
    for i, imagem in enumerate(imagens):
        caminho_completo = os.path.join(PASTA_ENTRADA, imagem)
        print(f"Processando imagem {i+1}/{len(imagens)}: {imagem}")
        processar_imagem(caminho_completo, PASTA_SAIDA)
    
    print("Processamento concluído! Todas as imagens foram salvas na pasta 'output'.")

if __name__ == "__main__":
    main()