# 🚀 Deploy no Render - Extrator de Tabelas PDF

## 📋 Pré-requisitos

1. ✅ Conta no [Render](https://render.com)
2. ✅ Repositório Git com o código (GitHub/GitLab)
3. ✅ Arquivos de configuração (já criados)

## 🔧 Arquivos de Configuração Criados

- ✅ `render.yaml` - Configuração automática do Render
- ✅ `Dockerfile` - Container Docker (alternativo)
- ✅ `.streamlit/config.toml` - Configurações do Streamlit
- ✅ `start.sh` - Script de inicialização
- ✅ `requirements.txt` - Dependências com versões específicas

## 🚀 Passo a Passo para Deploy

### Opção 1: Deploy Automático (Recomendado)

1. **Fazer Push do código**:
   ```bash
   git add .
   git commit -m "Preparado para deploy no Render"
   git push origin main
   ```

2. **No painel do Render**:
   - Clique em "New +"
   - Escolha "Web Service"
   - Conecte seu repositório GitHub
   - Selecione o repositório "Extrator-de-Tabelas-PDF"

3. **Configurações no Render**:
   - **Name**: `extrator-tabelas-pdf`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app_ui.py --server.port $PORT --server.address 0.0.0.0`
   - **Instance Type**: `Starter` (gratuito)

### Opção 2: Docker Deploy

Se escolher Docker:
- **Build Command**: `docker build -t extractor .`
- **Start Command**: `docker run -p $PORT:8501 extractor`

## 🌍 Variáveis de Ambiente

No painel do Render, adicione:
- `PYTHON_VERSION`: `3.9.18`
- `PORT`: (Render define automaticamente)

## 🔍 Troubleshooting

### Problemas Comuns:

1. **Erro de dependências**:
   - Verifique se todas as dependências estão no `requirements.txt`
   - Teste localmente com: `pip install -r requirements.txt`

2. **Erro de porta**:
   - O Render define a porta via `$PORT`
   - Use sempre `--server.port $PORT`

3. **Timeout de build**:
   - O build pode demorar devido ao `camelot-py`
   - É normal levar 5-10 minutos

4. **Erro de ghostscript**:
   - Já incluído no `requirements.txt`
   - Necessário para o `camelot-py`

## 📊 Monitoramento

Após o deploy:
- ✅ URL estará disponível no painel do Render
- ✅ Logs visíveis em tempo real
- ✅ Deploy automático a cada push

## 🎯 Resultado Esperado

- 🌐 **URL pública**: `https://extrator-tabelas-pdf.onrender.com`
- 📱 **Interface completa**: Com imagem do pumper e funcionalidades
- 🚀 **Funcional**: Extração de tabelas, consolidação e download

---

**⚡ Deploy em produção pronto!**