import os
from processamento import processar_imagem_rgb, processar_imagem_cinza
from visualizacao import salvar_resultados
from utils import verificar_arquivos, criar_pasta_se_nao_existir, obter_nome_base_arquivo

# ===== CONSTANTES DA APLICAÇÃO =====
# Diretórios
PASTA_ENTRADA = "./entrada/"  # Pasta de entrada (imagens originais)
PASTA_SAIDA_CINZA = "./saida/"  # Pasta com imagens em escala de cinza do exercício 1
PASTA_SAIDA = "./saida/"  # Pasta de saída

# Parâmetros dos filtros
FREQUENCIA_CORTE_BAIXA = 30  # Raio do filtro passa-baixa (em pixels)
FREQUENCIA_CORTE_ALTA = 20   # Raio do filtro passa-alta (em pixels)

# Extensões de arquivo válidas
EXTENSOES_VALIDAS = ['.jpg', '.jpeg', '.png']

# Parâmetros de visualização
CMAP_CINZA = 'gray'
CMAP_ESPECTRO = 'viridis'
FIGSIZE_RGB = (20, 15)
FIGSIZE_CINZA = (15, 15)

def main():
    print("Iniciando aplicação de filtros de frequência ideais (passa-baixa e passa-alta)...")
    print(f"Frequência de corte passa-baixa: {FREQUENCIA_CORTE_BAIXA} pixels")
    print(f"Frequência de corte passa-alta: {FREQUENCIA_CORTE_ALTA} pixels")
    
    # Cria a pasta de saída se não existir
    pasta_criada = criar_pasta_se_nao_existir(PASTA_SAIDA)
    if pasta_criada:
        print(f"Pasta de saída criada: {PASTA_SAIDA}")
    
    # Verifica arquivos disponíveis
    imagens_rgb, imagens_cinza = verificar_arquivos(PASTA_ENTRADA, PASTA_SAIDA_CINZA, EXTENSOES_VALIDAS)
    
    print(f"\nEncontradas {len(imagens_rgb)} imagens RGB na pasta entrada.")
    print(f"Encontradas {len(imagens_cinza)} imagens em escala de cinza na pasta saida.")
    
    if len(imagens_rgb) == 0 and len(imagens_cinza) == 0:
        print("\nNenhuma imagem encontrada para processar!")
        print("Por favor, adicione imagens na pasta 'entrada' ou execute os exercícios 1 e 2 primeiro.")
        return
    
    # Processar imagens RGB
    if len(imagens_rgb) > 0:
        print(f"\nProcessando {len(imagens_rgb)} imagens RGB...")
        for i, caminho_imagem in enumerate(imagens_rgb):
            nome_base = obter_nome_base_arquivo(caminho_imagem)
            
            print(f"Processando imagem RGB {i+1}/{len(imagens_rgb)}: {os.path.basename(caminho_imagem)}")
            resultados = processar_imagem_rgb(caminho_imagem, FREQUENCIA_CORTE_BAIXA, FREQUENCIA_CORTE_ALTA)
            salvar_resultados(resultados, nome_base, 'rgb', PASTA_SAIDA, 
                             CMAP_CINZA, CMAP_ESPECTRO, FIGSIZE_RGB, FIGSIZE_CINZA)
            print(f"Imagem RGB {nome_base} processada com sucesso!")
    
    # Processar imagens em escala de cinza
    if len(imagens_cinza) > 0:
        print(f"\nProcessando {len(imagens_cinza)} imagens em escala de cinza...")
        for i, caminho_imagem in enumerate(imagens_cinza):
            nome_base = obter_nome_base_arquivo(caminho_imagem, "_cinza")
            
            print(f"Processando imagem cinza {i+1}/{len(imagens_cinza)}: {os.path.basename(caminho_imagem)}")
            resultados = processar_imagem_cinza(caminho_imagem, FREQUENCIA_CORTE_BAIXA, FREQUENCIA_CORTE_ALTA)
            salvar_resultados(resultados, nome_base, 'cinza', PASTA_SAIDA, 
                             CMAP_CINZA, CMAP_ESPECTRO, FIGSIZE_RGB, FIGSIZE_CINZA)
            print(f"Imagem cinza {nome_base} processada com sucesso!")
    
    print("\nProcessamento concluído!")
    print("Filtros ideais aplicados:")
    print("- Passa-baixa: remove ruídos e suaviza a imagem (corte abrupto)")
    print("- Passa-alta: destaca bordas e detalhes finos (corte abrupto)")
    print("As imagens filtradas e visualizações foram salvas na pasta 'saida'.")
    print("\nNota: Filtros ideais podem causar artefatos de ringing devido ao corte abrupto.")

if __name__ == "__main__":
    main()