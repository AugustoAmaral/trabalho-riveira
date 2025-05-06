import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2  # OpenCV para implementação do filtro de Gabor
import glob

# Constantes
PASTA_ENTRADA = "./saida/"  # Pasta de entrada (saída do exercício anterior)
PASTA_SAIDA = "./saida/"  # Pasta de saída (mesma pasta)

def verificar_arquivos():
    """
    Verifica se existem arquivos em escala de cinza na pasta saida.
    Se não existirem, verifica se há arquivos na pasta entrada.
    """
    # Procura por arquivos com _cinza no nome
    arquivos_cinza = glob.glob(os.path.join(PASTA_ENTRADA, "*_cinza.*"))
    
    if len(arquivos_cinza) > 0:
        return True, arquivos_cinza
    
    # Se não encontrou arquivos em escala de cinza, verifica a pasta entrada
    if os.path.exists("./entrada"):
        arquivos_entrada = glob.glob("./entrada/*.*")
        if len(arquivos_entrada) > 0:
            return False, "entrada"
    
    return False, None

def aplicar_fft(imagem):
    """
    Aplica a Transformada de Fourier e realiza melhorias na imagem.
    
    Parâmetros:
    - imagem: array NumPy da imagem em escala de cinza
    
    Retorna:
    - imagem_melhorada: imagem após aplicação da FFT e filtragem
    - espectro_original: espectro de frequência original para visualização
    - espectro_filtrado: espectro de frequência após filtragem para visualização
    """
    # Aplicar a transformada de Fourier
    f_transform = np.fft.fft2(imagem)
    f_shift = np.fft.fftshift(f_transform)
    
    # Guardar o espectro original para visualização
    espectro_original = 20 * np.log(np.abs(f_shift) + 1)
    
    # Obter as dimensões da imagem
    linhas, colunas = imagem.shape
    centro_linha, centro_coluna = linhas // 2, colunas // 2
    
    # Criar um filtro passa-alta (destacar bordas)
    # Usar um filtro Butterworth para transição mais suave
    n = 2  # Ordem do filtro
    d0 = 30  # Frequência de corte
    
    y, x = np.ogrid[:linhas, :colunas]
    distancia = np.sqrt((y - centro_linha) ** 2 + (x - centro_coluna) ** 2)
    mascara = 1 / (1 + (d0 / (distancia + 0.0001)) ** (2 * n))
    
    # Aplicar o filtro
    f_shift_filtrado = f_shift * mascara
    
    # Guardar o espectro filtrado para visualização
    espectro_filtrado = 20 * np.log(np.abs(f_shift_filtrado) + 1)
    
    # Inverter a transformada para obter a imagem melhorada
    f_ishift = np.fft.ifftshift(f_shift_filtrado)
    img_back = np.fft.ifft2(f_ishift)
    img_back = np.abs(img_back)
    
    # Normalizar a imagem de volta para o intervalo [0, 255]
    imagem_melhorada = np.uint8(255 * (img_back - np.min(img_back)) / (np.max(img_back) - np.min(img_back)))
    
    return imagem_melhorada, espectro_original, espectro_filtrado

def aplicar_gabor(imagem):
    """
    Aplica filtros de Gabor na imagem para destacar texturas e bordas em várias orientações.
    
    Parâmetros:
    - imagem: array NumPy da imagem em escala de cinza
    
    Retorna:
    - imagem_melhorada: imagem após aplicação e combinação de filtros Gabor
    - filtros_individuais: lista de imagens resultantes de cada filtro individual
    """
    # Parâmetros para os filtros de Gabor
    ksize = 31  # Tamanho do kernel
    sigma = 5.0  # Desvio padrão
    theta_values = np.arange(0, np.pi, np.pi / 4)  # 4 orientações diferentes
    lambd = 10.0  # Comprimento de onda
    gamma = 0.5  # Relação de aspecto
    psi = 0  # Deslocamento de fase
    
    # Lista para armazenar os resultados de cada filtro
    filtros_individuais = []
    
    # Aplicar filtros Gabor com diferentes orientações
    for theta in theta_values:
        # Criar o kernel do filtro Gabor
        kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma, psi, ktype=cv2.CV_32F)
        
        # Normalizar o kernel
        kernel /= 1.5 * kernel.sum()
        
        # Aplicar o filtro
        filtrado = cv2.filter2D(imagem, cv2.CV_8UC3, kernel)
        
        # Armazenar o resultado
        filtros_individuais.append(filtrado)
    
    # Combinar os resultados dos diferentes filtros (média ponderada)
    # Usar float64 para os cálculos intermediários para evitar erros de casting
    imagem_melhorada = np.zeros_like(imagem, dtype=np.float64)
    pesos = [1.0, 1.2, 1.0, 1.2]  # Pesos diferentes para cada orientação
    
    for i, filtro in enumerate(filtros_individuais):
        imagem_melhorada += pesos[i] * filtro
    
    # Normalizar a imagem resultante
    imagem_melhorada = np.clip(imagem_melhorada / sum(pesos), 0, 255).astype(np.uint8)
    
    return imagem_melhorada, filtros_individuais

def processar_imagem(caminho_imagem):
    """
    Processa uma imagem aplicando FFT e filtros de Gabor.
    """
    # Carrega a imagem em escala de cinza
    imagem = np.array(Image.open(caminho_imagem))
    
    # Extrai o nome base do arquivo
    nome_arquivo = os.path.basename(caminho_imagem)
    base_nome = nome_arquivo.replace("_cinza", "")
    
    # Aplica a FFT
    print(f"Aplicando FFT em {nome_arquivo}...")
    imagem_fft, espectro_original, espectro_filtrado = aplicar_fft(imagem)
    
    # Aplica os filtros de Gabor
    print(f"Aplicando filtros de Gabor em {nome_arquivo}...")
    imagem_gabor, filtros_gabor_individuais = aplicar_gabor(imagem)
    
    # Salva os resultados
    Image.fromarray(imagem_fft).save(os.path.join(PASTA_SAIDA, f"{base_nome}_fft.png"))
    Image.fromarray(imagem_gabor).save(os.path.join(PASTA_SAIDA, f"{base_nome}_gabor.png"))
    
    # Visualiza e salva a comparação
    plt.figure(figsize=(20, 10))
    
    # Imagem original
    plt.subplot(231)
    plt.title('Original (Escala de Cinza)')
    plt.imshow(imagem, cmap='gray')
    plt.axis('off')
    
    # Espectro de frequência original
    plt.subplot(232)
    plt.title('Espectro de Frequência Original')
    plt.imshow(espectro_original, cmap='viridis')
    plt.axis('off')
    
    # Espectro de frequência filtrado
    plt.subplot(233)
    plt.title('Espectro de Frequência Filtrado')
    plt.imshow(espectro_filtrado, cmap='viridis')
    plt.axis('off')
    
    # Imagem após FFT
    plt.subplot(234)
    plt.title('Resultado FFT')
    plt.imshow(imagem_fft, cmap='gray')
    plt.axis('off')
    
    # Imagem após Gabor
    plt.subplot(235)
    plt.title('Resultado Gabor')
    plt.imshow(imagem_gabor, cmap='gray')
    plt.axis('off')
    
    # Diferença entre FFT e Gabor
    plt.subplot(236)
    plt.title('Diferença (FFT - Gabor)')
    diferenca = np.abs(imagem_fft.astype(np.int16) - imagem_gabor.astype(np.int16)).astype(np.uint8)
    plt.imshow(diferenca, cmap='hot')
    plt.axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(PASTA_SAIDA, f"{base_nome}_comparacao_metodos.png"))
    plt.close()
    
    # Visualiza e salva os filtros de Gabor individuais
    n_filtros = len(filtros_gabor_individuais)
    fig, axs = plt.subplots(1, n_filtros, figsize=(15, 5))
    for i, filtro in enumerate(filtros_gabor_individuais):
        axs[i].imshow(filtro, cmap='gray')
        axs[i].set_title(f'Orientação {i+1}')
        axs[i].axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(PASTA_SAIDA, f"{base_nome}_gabor_orientacoes.png"))
    plt.close()
    
    return base_nome

def main():
    print("Iniciando melhorias de imagem com FFT e Gabor...")
    
    # Verifica arquivos existentes
    tem_arquivos, resultado = verificar_arquivos()
    
    if not tem_arquivos:
        if resultado == "entrada":
            print("\nNão foram encontradas imagens em escala de cinza na pasta 'saida'.")
            print("Foram detectadas imagens na pasta 'entrada'.")
            print("Por favor, execute o programa 'exercicio1.py' primeiro para gerar as imagens em escala de cinza.")
        else:
            print("\nNão foram encontradas imagens em escala de cinza na pasta 'saida'.")
            print("Não foram detectadas imagens na pasta 'entrada'.")
            print("Por favor, adicione algumas imagens na pasta 'entrada' e execute o programa 'exercicio1.py' primeiro.")
        
        return
    
    print(f"Encontradas {len(resultado)} imagens em escala de cinza para processar.")
    
    # Processa cada imagem
    for i, imagem in enumerate(resultado):
        print(f"\nProcessando imagem {i+1}/{len(resultado)}: {os.path.basename(imagem)}")
        base_nome = processar_imagem(imagem)
        print(f"Imagem {base_nome} processada com sucesso!")
    
    print("\nProcessamento concluído! Todas as imagens foram processadas com FFT e Gabor.")
    print("Os resultados foram salvos na pasta 'saida' com os sufixos '_fft.png' e '_gabor.png'.")
    print("Também foram geradas imagens de comparação com o sufixo '_comparacao_metodos.png'.")

if __name__ == "__main__":
    main()