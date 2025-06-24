"""
Módulo de utilitários para manipulação de arquivos e diretórios.

Este módulo contém funções auxiliares para verificação de arquivos,
validação de extensões e outras operações de sistema.
"""

import os
import glob


def verificar_arquivos(pasta_entrada, pasta_saida_cinza, extensoes_validas):
    """
    Verifica quais arquivos estão disponíveis para processamento.
    
    Parâmetros:
    - pasta_entrada: pasta onde procurar imagens RGB
    - pasta_saida_cinza: pasta onde procurar imagens em escala de cinza
    - extensoes_validas: lista de extensões de arquivo válidas
    
    Retorna:
    - tupla: (lista de imagens RGB, lista de imagens em escala de cinza)
    """
    # Verificar imagens RGB na pasta entrada
    imagens_rgb = []
    
    if os.path.exists(pasta_entrada):
        arquivos_entrada = os.listdir(pasta_entrada)
        imagens_rgb = [
            os.path.join(pasta_entrada, arquivo) 
            for arquivo in arquivos_entrada 
            if os.path.isfile(os.path.join(pasta_entrada, arquivo)) and 
               os.path.splitext(arquivo.lower())[1] in extensoes_validas
        ]
    
    # Verificar imagens em escala de cinza na pasta saida
    imagens_cinza = []
    if os.path.exists(pasta_saida_cinza):
        imagens_cinza = glob.glob(os.path.join(pasta_saida_cinza, "*_cinza.*"))
    
    return imagens_rgb, imagens_cinza


def criar_pasta_se_nao_existir(pasta):
    """
    Cria uma pasta se ela não existir.
    
    Parâmetros:
    - pasta: caminho da pasta a ser criada
    
    Retorna:
    - bool: True se a pasta foi criada, False se já existia
    """
    if not os.path.exists(pasta):
        os.makedirs(pasta)
        return True
    return False


def obter_nome_base_arquivo(caminho_arquivo, remover_sufixo=None):
    """
    Obtém o nome base de um arquivo (sem extensão e opcionalmente sem sufixo).
    
    Parâmetros:
    - caminho_arquivo: caminho completo do arquivo
    - remover_sufixo: sufixo a ser removido do nome (ex: "_cinza")
    
    Retorna:
    - str: nome base do arquivo
    """
    nome_arquivo = os.path.basename(caminho_arquivo)
    nome_base = os.path.splitext(nome_arquivo)[0]
    
    if remover_sufixo and nome_base.endswith(remover_sufixo):
        nome_base = nome_base.replace(remover_sufixo, "")
    
    return nome_base
