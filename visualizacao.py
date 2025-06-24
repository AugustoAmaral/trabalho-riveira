"""
Módulo para visualização e salvamento de resultados.

Este módulo contém funções para salvar imagens filtradas e criar
visualizações completas dos resultados do processamento.
"""

import os
import matplotlib.pyplot as plt
from PIL import Image


def salvar_resultados(resultados, nome_base, tipo_processamento, pasta_saida, 
                     cmap_cinza='gray', cmap_espectro='viridis', 
                     figsize_rgb=(20, 15), figsize_cinza=(15, 15)):
    """
    Salva os resultados do processamento.
    
    Parâmetros:
    - resultados: dicionário com os resultados do processamento
    - nome_base: nome base do arquivo
    - tipo_processamento: 'rgb' ou 'cinza'
    - pasta_saida: pasta onde salvar os resultados
    - cmap_cinza: colormap para imagens em escala de cinza
    - cmap_espectro: colormap para espectros de frequência
    - figsize_rgb: tamanho da figura para imagens RGB
    - figsize_cinza: tamanho da figura para imagens em escala de cinza
    """
    # Salvar imagens filtradas
    Image.fromarray(resultados['passa_baixa']).save(
        os.path.join(pasta_saida, f"{nome_base}_{tipo_processamento}_passa_baixa.png")
    )
    Image.fromarray(resultados['passa_alta']).save(
        os.path.join(pasta_saida, f"{nome_base}_{tipo_processamento}_passa_alta.png")
    )
    
    # Criar visualização completa
    if tipo_processamento == 'rgb':
        _criar_visualizacao_rgb(resultados, nome_base, pasta_saida, 
                               cmap_cinza, cmap_espectro, figsize_rgb)
    else:  # tipo_processamento == 'cinza'
        _criar_visualizacao_cinza(resultados, nome_base, pasta_saida, 
                                 cmap_cinza, cmap_espectro, figsize_cinza)


def _criar_visualizacao_rgb(resultados, nome_base, pasta_saida, 
                           cmap_cinza, cmap_espectro, figsize_rgb):
    """
    Cria visualização completa para imagens RGB.
    """
    fig, axes = plt.subplots(3, 4, figsize=figsize_rgb)
    
    # Linha 1: Imagens originais e filtradas
    axes[0, 0].imshow(resultados['original_rgb'])
    axes[0, 0].set_title('Original (RGB)')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(resultados['original_cinza'], cmap=cmap_cinza)
    axes[0, 1].set_title('Original (Escala de Cinza)')
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(resultados['passa_baixa'], cmap=cmap_cinza)
    axes[0, 2].set_title('Filtro Passa-Baixa')
    axes[0, 2].axis('off')
    
    axes[0, 3].imshow(resultados['passa_alta'], cmap=cmap_cinza)
    axes[0, 3].set_title('Filtro Passa-Alta')
    axes[0, 3].axis('off')
    
    # Linha 2: Espectros de frequência para passa-baixa
    axes[1, 0].imshow(resultados['espectro_original_pb'], cmap=cmap_espectro)
    axes[1, 0].set_title('Espectro Original')
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(resultados['filtro_pb'], cmap=cmap_cinza)
    axes[1, 1].set_title('Filtro Passa-Baixa')
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(resultados['espectro_filtrado_pb'], cmap=cmap_espectro)
    axes[1, 2].set_title('Espectro Filtrado (PB)')
    axes[1, 2].axis('off')
    
    axes[1, 3].imshow(resultados['passa_baixa'], cmap=cmap_cinza)
    axes[1, 3].set_title('Resultado Passa-Baixa')
    axes[1, 3].axis('off')
    
    # Linha 3: Espectros de frequência para passa-alta
    axes[2, 0].imshow(resultados['espectro_original_pa'], cmap=cmap_espectro)
    axes[2, 0].set_title('Espectro Original')
    axes[2, 0].axis('off')
    
    axes[2, 1].imshow(resultados['filtro_pa'], cmap=cmap_cinza)
    axes[2, 1].set_title('Filtro Passa-Alta')
    axes[2, 1].axis('off')
    
    axes[2, 2].imshow(resultados['espectro_filtrado_pa'], cmap=cmap_espectro)
    axes[2, 2].set_title('Espectro Filtrado (PA)')
    axes[2, 2].axis('off')
    
    axes[2, 3].imshow(resultados['passa_alta'], cmap=cmap_cinza)
    axes[2, 3].set_title('Resultado Passa-Alta')
    axes[2, 3].axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_saida, f"{nome_base}_rgb_filtros_frequencia.png"))
    plt.close()


def _criar_visualizacao_cinza(resultados, nome_base, pasta_saida, 
                             cmap_cinza, cmap_espectro, figsize_cinza):
    """
    Cria visualização completa para imagens em escala de cinza.
    """
    fig, axes = plt.subplots(3, 3, figsize=figsize_cinza)
    
    # Linha 1: Imagens originais e filtradas
    axes[0, 0].imshow(resultados['original_cinza'], cmap=cmap_cinza)
    axes[0, 0].set_title('Original (Escala de Cinza)')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(resultados['passa_baixa'], cmap=cmap_cinza)
    axes[0, 1].set_title('Filtro Passa-Baixa')
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(resultados['passa_alta'], cmap=cmap_cinza)
    axes[0, 2].set_title('Filtro Passa-Alta')
    axes[0, 2].axis('off')
    
    # Linha 2: Filtros e espectros para passa-baixa
    axes[1, 0].imshow(resultados['filtro_pb'], cmap=cmap_cinza)
    axes[1, 0].set_title('Filtro Passa-Baixa')
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(resultados['espectro_original_pb'], cmap=cmap_espectro)
    axes[1, 1].set_title('Espectro Original')
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(resultados['espectro_filtrado_pb'], cmap=cmap_espectro)
    axes[1, 2].set_title('Espectro Filtrado (PB)')
    axes[1, 2].axis('off')
    
    # Linha 3: Filtros e espectros para passa-alta
    axes[2, 0].imshow(resultados['filtro_pa'], cmap=cmap_cinza)
    axes[2, 0].set_title('Filtro Passa-Alta')
    axes[2, 0].axis('off')
    
    axes[2, 1].imshow(resultados['espectro_original_pa'], cmap=cmap_espectro)
    axes[2, 1].set_title('Espectro Original')
    axes[2, 1].axis('off')
    
    axes[2, 2].imshow(resultados['espectro_filtrado_pa'], cmap=cmap_espectro)
    axes[2, 2].set_title('Espectro Filtrado (PA)')
    axes[2, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_saida, f"{nome_base}_cinza_filtros_frequencia.png"))
    plt.close()
