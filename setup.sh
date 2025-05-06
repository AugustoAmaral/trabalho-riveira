#!/bin/bash

# setup.sh
# Script para configurar o ambiente virtual Python e instalar as dependências necessárias

echo "Configurando ambiente para processamento de imagens..."

# Verifica se o Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "Erro: Python 3 não encontrado. Por favor, instale o Python 3 e tente novamente."
    echo "Visite https://www.python.org/downloads/ para baixar e instalar."
    exit 1
fi

# Verifica se o módulo venv está disponível
python3 -c "import venv" &> /dev/null
if [ $? -ne 0 ]; then
    echo "Módulo venv do Python não está disponível. Tentando instalar..."
    
    # Tentativa de instalação do venv baseado no sistema operacional
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y python3-venv
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3-venv
        else
            echo "Não foi possível determinar o gerenciador de pacotes. Instale python3-venv manualmente."
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "No macOS, o módulo venv já deveria estar incluído no Python 3."
        echo "Verifique sua instalação do Python ou reinstale-o a partir de https://www.python.org/downloads/"
        exit 1
    else
        echo "Sistema operacional não reconhecido. Instale o módulo venv manualmente."
        exit 1
    fi
fi

# Nome do ambiente virtual
VENV_DIR="venv"

# Cria o ambiente virtual
echo "Criando ambiente virtual Python..."
python3 -m venv $VENV_DIR

# Verifica se o ambiente virtual foi criado com sucesso
if [ ! -d "$VENV_DIR" ]; then
    echo "Erro: Não foi possível criar o ambiente virtual. Verifique as permissões da pasta."
    exit 1
fi

echo "Ambiente virtual criado com sucesso!"

# Ativa o ambiente virtual
echo "Ativando ambiente virtual..."
source "$VENV_DIR/bin/activate" || {
    echo "Erro: Não foi possível ativar o ambiente virtual."
    exit 1
}

# Atualiza pip no ambiente virtual
echo "Atualizando pip..."
pip install --upgrade pip

# Lista de pacotes necessários
pacotes=("numpy" "pillow" "matplotlib")

# Instala cada pacote no ambiente virtual
echo "Instalando dependências necessárias..."
for pacote in "${pacotes[@]}"; do
    echo "Instalando $pacote..."
    pip install "$pacote"
    
    # Verifica se a instalação foi bem-sucedida
    if [ $? -eq 0 ]; then
        echo "$pacote instalado com sucesso!"
    else
        echo "Erro ao instalar $pacote. Verifique sua conexão com a internet e tente novamente."
        exit 1
    fi
done

# Cria a pasta de saída para as imagens processadas se não existir
OUTPUT_DIR="output"
if [ ! -d "$OUTPUT_DIR" ]; then
    echo "Criando pasta de saída '$OUTPUT_DIR'..."
    mkdir -p "$OUTPUT_DIR"
fi

echo ""
echo "=========================================================="
echo "Configuração concluída com sucesso!"
echo "Para utilizar o ambiente configurado:"
echo ""
echo "1. Ative o ambiente virtual com o comando:"
echo "   source $VENV_DIR/bin/activate"
echo ""
echo "2. Execute o programa de processamento de imagens:"
echo "   python3 exercicio1.py"
echo ""
echo "3. Quando terminar, desative o ambiente virtual:"
echo "   deactivate"
echo "=========================================================="

# Desativa o ambiente virtual ao final do script
deactivate