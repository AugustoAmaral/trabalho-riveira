"""
Módulo para processamento de imagens RGB e em escala de cinza.

Este módulo contém funções para processar imagens aplicando filtros
de frequência tanto em imagens coloridas quanto em escala de cinza.
"""

import numpy as np
from PIL import Image
from filtros import criar_filtro_passa_baixa, criar_filtro_passa_alta, aplicar_filtro_frequencia


def processar_imagem_rgb(caminho_imagem, frequencia_corte_baixa, frequencia_corte_alta):
    """
    Processa uma imagem RGB aplicando filtros de frequência.
    
    Parâmetros:
    - caminho_imagem: caminho para o arquivo de imagem
    - frequencia_corte_baixa: frequência de corte para o filtro passa-baixa
    - frequencia_corte_alta: frequência de corte para o filtro passa-alta
    
    Retorna:
    - dict: dicionário com todos os resultados do processamento
    """
    # Carrega a imagem RGB
    imagem_rgb = Image.open(caminho_imagem)
    imagem_rgb_array = np.array(imagem_rgb)
    
    # Converte para escala de cinza se necessário
    if len(imagem_rgb_array.shape) == 3:
        imagem_cinza = imagem_rgb.convert('L')
        imagem_cinza_array = np.array(imagem_cinza)
    else:
        imagem_cinza_array = imagem_rgb_array
    
    # Criar filtros
    forma = imagem_cinza_array.shape
    filtro_passa_baixa = criar_filtro_passa_baixa(forma, frequencia_corte_baixa)
    filtro_passa_alta = criar_filtro_passa_alta(forma, frequencia_corte_alta)
    
    # Aplicar filtros
    img_passa_baixa, espectro_orig_pb, espectro_filt_pb = aplicar_filtro_frequencia(imagem_cinza_array, filtro_passa_baixa)
    img_passa_alta, espectro_orig_pa, espectro_filt_pa = aplicar_filtro_frequencia(imagem_cinza_array, filtro_passa_alta)
    
    return {
        'original_rgb': imagem_rgb_array,
        'original_cinza': imagem_cinza_array,
        'passa_baixa': img_passa_baixa,
        'passa_alta': img_passa_alta,
        'espectro_original_pb': espectro_orig_pb,
        'espectro_filtrado_pb': espectro_filt_pb,
        'espectro_original_pa': espectro_orig_pa,
        'espectro_filtrado_pa': espectro_filt_pa,
        'filtro_pb': filtro_passa_baixa,
        'filtro_pa': filtro_passa_alta
    }


def processar_imagem_cinza(caminho_imagem, frequencia_corte_baixa, frequencia_corte_alta):
    """
    Processa uma imagem em escala de cinza aplicando filtros de frequência.
    
    Parâmetros:
    - caminho_imagem: caminho para o arquivo de imagem
    - frequencia_corte_baixa: frequência de corte para o filtro passa-baixa
    - frequencia_corte_alta: frequência de corte para o filtro passa-alta
    
    Retorna:
    - dict: dicionário com todos os resultados do processamento
    """
    # Carrega a imagem em escala de cinza
    imagem_cinza = Image.open(caminho_imagem)
    imagem_cinza_array = np.array(imagem_cinza)
    
    # Criar filtros
    forma = imagem_cinza_array.shape
    filtro_passa_baixa = criar_filtro_passa_baixa(forma, frequencia_corte_baixa)
    filtro_passa_alta = criar_filtro_passa_alta(forma, frequencia_corte_alta)
    
    # Aplicar filtros
    img_passa_baixa, espectro_orig_pb, espectro_filt_pb = aplicar_filtro_frequencia(imagem_cinza_array, filtro_passa_baixa)
    img_passa_alta, espectro_orig_pa, espectro_filt_pa = aplicar_filtro_frequencia(imagem_cinza_array, filtro_passa_alta)
    
    return {
        'original_cinza': imagem_cinza_array,
        'passa_baixa': img_passa_baixa,
        'passa_alta': img_passa_alta,
        'espectro_original_pb': espectro_orig_pb,
        'espectro_filtrado_pb': espectro_filt_pb,
        'espectro_original_pa': espectro_orig_pa,
        'espectro_filtrado_pa': espectro_filt_pa,
        'filtro_pb': filtro_passa_baixa,
        'filtro_pa': filtro_passa_alta
    }
