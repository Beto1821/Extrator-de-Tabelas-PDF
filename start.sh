#!/bin/bash

# Script de inicialização para Render
echo "🚀 Iniciando Extrator de Tabelas PDF..."

# Criar diretório temporário se não existir
mkdir -p temp_files

# Iniciar aplicação Streamlit
streamlit run app_ui.py --server.port ${PORT:-8501} --server.address 0.0.0.0 --server.headless true