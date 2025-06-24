"""
Módulo para criação e aplicação de filtros de frequência ideais.

Este módulo contém funções para criar filtros passa-baixa e passa-alta
e aplicar transformadas de Fourier em imagens.
"""

import numpy as np


def criar_filtro_passa_baixa(forma, frequencia_corte):
    """
    Cria um filtro passa-baixa ideal (circular) no domínio da frequência.
    
    Parâmetros:
    - forma: tupla com as dimensões da imagem (linhas, colunas)
    - frequencia_corte: raio do filtro em pixels
    
    Retorna:
    - mascara: array 2D com o filtro (1 dentro do raio, 0 fora)
    """
    linhas, colunas = forma
    centro_linha, centro_coluna = linhas // 2, colunas // 2
    
    # Grade de coordenadas
    y, x = np.ogrid[:linhas, :colunas]
    
    # Distância do centro
    distancia = np.sqrt((y - centro_linha) ** 2 + (x - centro_coluna) ** 2)
    
    # Criar máscara circular (1 dentro do raio, 0 fora)
    mascara = np.zeros((linhas, colunas))
    mascara[distancia <= frequencia_corte] = 1
    
    return mascara


def criar_filtro_passa_alta(forma, frequencia_corte):
    """
    Cria um filtro passa-alta ideal (circular) no domínio da frequência.
    
    Parâmetros:
    - forma: tupla com as dimensões da imagem (linhas, colunas)
    - frequencia_corte: raio do filtro em pixels
    
    Retorna:
    - mascara_passa_alta: array 2D com o filtro (0 dentro do raio, 1 fora)
    """
    mascara_passa_baixa = criar_filtro_passa_baixa(forma, frequencia_corte)
    mascara_passa_alta = 1 - mascara_passa_baixa
    
    return mascara_passa_alta


def aplicar_filtro_frequencia(imagem, mascara_filtro):
    """
    Aplica um filtro no domínio da frequência usando transformada de Fourier.
    
    Parâmetros:
    - imagem: array 2D da imagem em escala de cinza
    - mascara_filtro: array 2D com o filtro a ser aplicado
    
    Retorna:
    - imagem_filtrada: imagem filtrada normalizada para [0, 255]
    - espectro_original: espectro de frequência original (para visualização)
    - espectro_filtrado: espectro de frequência filtrado (para visualização)
    """
    # Aplicar a transformada de Fourier
    f_shift = np.fft.fftshift(np.fft.fft2(imagem))
    
    # Guardar o espectro original para visualização
    espectro_original = 20 * np.log(np.abs(f_shift) + 1)
    
    # Aplicar o filtro
    f_shift_filtrado = f_shift * mascara_filtro
    
    # Guardar o espectro filtrado para visualização
    espectro_filtrado = 20 * np.log(np.abs(f_shift_filtrado) + 1)
    
    # Inverter a transformada para obter a imagem filtrada
    img_back = np.fft.ifft2(np.fft.ifftshift(f_shift_filtrado))
    img_back = np.abs(img_back)
    
    # Normalizar a imagem de volta para o intervalo [0, 255]
    imagem_filtrada = np.uint8(255 * (img_back - np.min(img_back)) / (np.max(img_back) - np.min(img_back)))
    
    return imagem_filtrada, espectro_original, espectro_filtrado
