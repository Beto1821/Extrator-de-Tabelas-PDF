# 🚀 Extrator de Tabelas de PDF

<p align="center"><img src="public/pumper.png" width="200"></p>

Uma ferramenta profissional para extrair tabelas de arquivos PDF de forma rápida e convertê-las para o formato Excel, com **Dark Mode** completo e **framework de testes robusto**.

## ✨ Funcionalidades

### 🔍 **Extração Inteligente de PDFs**
- Extração automática usando **Camelot** e **Tabula** como fallback
- Processamento inteligente: remoção de headers duplicados e consolidação de linhas quebradas
- Configuração flexível de colunas com nomes personalizados
- Suporte para PDFs complexos com múltiplas tabelas

### 🌙 **Dark Mode Completo**
- Toggle dinâmico na sidebar (🌙 Dark Mode / ☀️ Light Mode)
- CSS otimizado para reduzir cansaço visual
- Persistência do tema durante toda a sessão
- Interface responsiva e moderna

### 🧪 **Framework de Testes Profissional**
- **46 testes automatizados** (100% de aprovação)
- **Cobertura de código** de 78% no núcleo da aplicação
- **Benchmarks de performance** integrados
- **Relatórios HTML** visuais e detalhados

### 💾 **Exportação e Interface**
- Conversão direta para Excel com formatação
- Barra de progresso em tempo real
- Upload drag-and-drop intuitivo
- Preview dos dados extraídos

**Este projeto é de código aberto, totalmente gratuito e não possui fins lucrativos.**

![Screenshot da Aplicação](https://i.imgur.com/V234d9k.png)

## 🛠️ Tecnologias Utilizadas

### **Core**
- **Front-end:** [Streamlit](https://streamlit.io/) - Interface web moderna
- **Extração PDF:** [Camelot-py](https://camelot-py.readthedocs.io/) + [Tabula-py](https://github.com/chezou/tabula-py)
- **Processamento:** [Pandas](https://pandas.pydata.org/) - Manipulação de dados
- **Exportação:** [XlsxWriter](https://xlsxwriter.readthedocs.io/) - Geração de Excel

### **Testes e Qualidade**
- **pytest** - Framework de testes principal
- **pytest-cov** - Cobertura de código
- **pytest-benchmark** - Medição de performance  
- **pytest-mock** - Mocking profissional
- **pytest-html** - Relatórios visuais
- **faker** - Dados de teste realistas
- **hypothesis** - Testes baseados em propriedades

## 🚀 Como Executar Localmente

### 📋 **Pré-requisitos**

- **Python 3.8+**
- **Java:** Necessário para `tabula-py`. Verifique com:
  ```bash
  java -version
  ```

### ⚡ **Instalação Rápida**

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/Beto1821/Extrator-de-Tabelas-PDF.git
   cd Extrator-de-Tabelas-PDF
   ```

2. **Configure o ambiente:**
   ```bash
   python -m venv .venv
   # Windows: .\.venv\Scripts\activate
   # macOS/Linux: source .venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação:**
   ```bash
   streamlit run app_ui.py
   ```

🌐 **Acesse:** http://localhost:8501

---

## 🧪 Framework de Testes

### 📊 **Visão Geral dos Testes**

O projeto possui um **framework de testes profissional** com cobertura abrangente:

- ✅ **46 testes automatizados** (100% aprovação)
- ✅ **25 testes unitários** cobrindo funções críticas
- ✅ **11 testes de integração** validando pipelines completos  
- ✅ **10 testes de performance** com benchmarks detalhados
- ✅ **Cobertura de 78%** no código principal
- ✅ **Relatórios HTML** visuais e interativos

### 🗂️ **Estrutura de Testes**

```
tests/
├── unit/           # Testes unitários das funções
├── integration/    # Testes end-to-end do pipeline
├── performance/    # Benchmarks de performance
├── conftest.py     # Fixtures compartilhadas
└── reports/        # Relatórios HTML gerados
```

### 🎯 **Como Executar os Testes**

#### **Teste Completo (Recomendado):**
```bash
pytest tests/ -v --cov=app --cov-report=html --html=tests/reports/test_report.html
```
*Executa todos os testes com cobertura e relatório HTML*

#### **Testes por Categoria:**
```bash
# Apenas testes unitários (rápido)
pytest tests/unit/ -v

# Apenas testes de integração
pytest tests/integration/ -v

# Apenas benchmarks de performance
pytest tests/performance/ --benchmark-only

# Testes em paralelo (mais rápido)
pytest tests/ -n auto
```

#### **Relatórios de Cobertura:**
```bash
# Relatório no terminal
pytest tests/ --cov=app --cov-report=term

# Relatório HTML detalhado
pytest tests/ --cov=app --cov-report=html
# Visualizar em: htmlcov/index.html
```

### ⚡ **Benchmarks de Performance**

Os testes medem automaticamente a performance das operações:

- **Operações rápidas**: ~3.728 ops/sec (remoção de headers)
- **Operações pandas**: ~600 ops/sec (manipulação de dados)
- **Pipeline completo**: ~2 ops/sec (PDF → Excel)

### 🎨 **Relatórios Visuais**

Após executar os testes, você terá acesso a:

1. **Relatório HTML de Testes**: `tests/reports/test_report.html`
2. **Relatório de Cobertura**: `htmlcov/index.html`
3. **Benchmarks no Terminal**: Estatísticas detalhadas de performance

### 🔧 **Ferramentas de Teste Instaladas**

- **pytest** - Framework principal
- **pytest-cov** - Cobertura de código
- **pytest-benchmark** - Medição de performance
- **pytest-html** - Relatórios visuais
- **pytest-mock** - Mocking profissional
- **pytest-xdist** - Execução paralela
- **faker** - Dados de teste realistas  
- **hypothesis** - Testes baseados em propriedades
- **psutil** - Monitoramento de memória

### 💡 **Exemplos de Uso dos Testes**

```bash
# Desenvolvimento: executar testes durante codificação
pytest tests/unit/ -x --tb=short

# CI/CD: executar com cobertura mínima
pytest tests/ --cov=app --cov-fail-under=70

# Performance: verificar se não há regressão
pytest tests/performance/ --benchmark-compare

# Debugging: executar teste específico
pytest tests/unit/test_data_processing.py::test_consolidate_broken_rows -v
```

### 📈 **Benefícios do Framework de Testes**

- **🛡️ Detecção Precoce**: Bugs capturados antes da produção
- **🔄 Refatoração Segura**: Mudanças validadas automaticamente  
- **📊 Monitoramento**: Performance acompanhada continuamente
- **📋 Documentação**: Testes servem como documentação viva
- **🚀 Confiança**: Deploy seguro com validação completa

---

## 🌙 Como Usar o Dark Mode

1. **Ativar**: Clique em "🌙 Dark Mode" na sidebar
2. **Desativar**: Clique em "☀️ Light Mode" na sidebar  
3. **Persistência**: Tema mantido durante toda a sessão

---

## 📁 Estrutura do Projeto

```
app_raspagem_pdf/
├── app.py              # Lógica de extração PDF
├── app_ui.py           # Interface Streamlit
├── requirements.txt    # Dependências
├── pyproject.toml     # Configuração pytest
├── tests/             # Framework de testes
│   ├── unit/          # Testes unitários
│   ├── integration/   # Testes integração  
│   ├── performance/   # Benchmarks
│   └── conftest.py    # Fixtures
├── htmlcov/           # Relatórios cobertura
└── temp_files/        # Arquivos temporários
```

---

## 🎯 Como Usar a Aplicação

### 📄 **Upload e Configuração**
1. Acesse http://localhost:8501 
2. Escolha o tema (🌙 Dark Mode / ☀️ Light Mode)
3. Faça upload do arquivo PDF
4. Configure o número de colunas esperadas
5. Defina os nomes das colunas (opcional)

### ⚙️ **Processamento Automático**
- A aplicação tenta **Camelot** primeiro (mais preciso)
- Fallback para **Tabula** se necessário
- Remove headers duplicados automaticamente  
- Consolida linhas quebradas
- Valida e limpa os dados

### 📊 **Resultados**
- Preview dos dados extraídos
- Download automático do Excel
- Feedback visual do progresso
- Tratamento de erros amigável

---

## 🤝 Contribuindo

### 🐛 **Reportar Bugs**
1. Execute os testes: `pytest tests/ -v`
2. Inclua logs e versões no issue
3. Descreva os passos para reproduzir

### 🔧 **Desenvolvimento** 
```bash
# Setup completo para desenvolvimento
git clone https://github.com/Beto1821/Extrator-de-Tabelas-PDF.git
cd Extrator-de-Tabelas-PDF
python -m venv .venv
source .venv/bin/activate  # ou .\.venv\Scripts\activate no Windows
pip install -r requirements.txt

# Executar testes durante desenvolvimento
pytest tests/unit/ -x --tb=short

# Verificar cobertura
pytest tests/ --cov=app --cov-report=term
```

### ✅ **Pull Request Checklist**
- [ ] Todos os testes passando: `pytest tests/`
- [ ] Cobertura mantida acima de 70%
- [ ] Código formatado: `black . && flake8 .`
- [ ] Funcionalidade testada manualmente
- [ ] README atualizado se necessário

---

## 📊 Status do Projeto

- ✅ **Extração PDF**: Camelot + Tabula implementado
- ✅ **Interface**: Streamlit com Dark Mode
- ✅ **Testes**: Framework completo (46 testes)
- ✅ **Performance**: Benchmarks integrados  
- ✅ **Cobertura**: 78% no código principal
- ✅ **Relatórios**: HTML automático
- ⏳ **CI/CD**: Em planejamento
- ⏳ **Docker**: Em planejamento

---

## 📜 Licença

Este projeto é **open-source** e **gratuito**. Desenvolvido sem fins lucrativos para a comunidade.

---

## 💡 Suporte

- 🐛 **Issues**: [GitHub Issues](https://github.com/Beto1821/Extrator-de-Tabelas-PDF/issues)
- 📧 **Email**: Para questões técnicas específicas
- 📖 **Documentação**: Este README + código comentado

---

**Desenvolvido com ❤️ para facilitar extração de dados PDF**