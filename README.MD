
# 📊 Extrator de Tabelas PDF

Aplicativo para extrair tabelas de arquivos PDF e convertê-las para Excel de forma automatizada.

## 🚀 Funcionalidades

- ✅ **Múltiplos métodos de extração**: Usa Camelot e Tabula para máxima compatibilidade
- ✅ **Interface amigável**: Interface web com Streamlit
- ✅ **Configuração flexível**: Defina os nomes das colunas da tabela
- ✅ **Exportação para Excel**: Salva os resultados em formato .xlsx
- ✅ **Debug automático**: Mostra informações detalhadas sobre tabelas encontradas

## 📋 Instalação

1. **Clone ou baixe os arquivos**

2. **Instale as dependências:**
```bash
pip3 install -r requirements.txt
```

3. **Execute o aplicativo:**
```bash
python3 -m streamlit run app_ui.py
```

## 💡 Como usar

### Interface Web (Recomendado)

1. Execute `python3 -m streamlit run app_ui.py`
2. Acesse http://localhost:8501 no navegador
3. Faça upload do arquivo PDF
4. Informe o número de colunas esperado na tabela
5. Digite o nome de cada coluna
6. Clique em "Extrair Tabelas"
7. Baixe o arquivo Excel gerado

### Linha de Comando

```bash
python3 app.py
```

## 📝 Exemplo de uso

Para o PDF anexado (Planilha de Preço Estimado), use:

- **Número de colunas**: 6
- **Nomes das colunas**:
  - Item
  - Descrição
  - Unid.
  - Quant.
  - Vlr. Unit.
  - Vlr. Total

## 🔧 Dependências

- `streamlit`: Interface web
- `pandas`: Manipulação de dados
- `tabula-py`: Extração de tabelas (método principal)
- `camelot-py[cv]`: Extração avançada de tabelas
- `openpyxl`: Geração de arquivos Excel
- `xlsxwriter`: Formatação de Excel

## 🛠️ Melhorias implementadas

1. **Múltiplos métodos de extração**: Camelot + Tabula para maior compatibilidade
2. **Configurações automáticas**: Testa diferentes parâmetros automaticamente
3. **🆕 Remoção de cabeçalhos duplicados**: Remove automaticamente cabeçalhos que se repetem em cada página
4. **Debug detalhado**: Mostra estrutura das tabelas encontradas para troubleshooting
5. **Tratamento de erros**: Recuperação graceful quando um método falha
6. **Interface melhorada**: Streamlit com upload de arquivos

### ✨ Novas Funcionalidades:

#### 🧹 Limpeza Inteligente de Dados
- ✅ **Remoção de Cabeçalhos Duplicados**: Remove cabeçalhos repetidos em cada página
- ✅ **🆕 Consolidação de Linhas Quebradas**: Junta descrições longas que foram quebradas em múltiplas linhas
- ✅ **Preservação de Dados**: Não perde informações importantes durante a limpeza
- ✅ **Logs detalhados**: Mostra exatamente o que foi processado

#### 🎨 Interface Visual Melhorada
- ✅ **🛢️ Imagem personalizada**: Logo do pumper.png na aba, barra lateral e área central
- ✅ **Design profissional**: Cores e estilos personalizados
- ✅ **Instruções visuais**: Guia completo na tela inicial
- ✅ **Barra de progresso**: Acompanhe o processo com porcentagem em tempo real
- ✅ **Validações inteligentes**: Alertas quando PDF não é carregado ou campos vazios
- ✅ **Estatísticas do resultado**: Métricas dos dados extraídos
- ✅ **Mensagens informativas**: Dicas de troubleshooting e ajuda

## 🐛 Troubleshooting

**Problema**: "Nenhuma tabela encontrada"

**Soluções**:
1. Verifique se o PDF contém tabelas com bordas visíveis
2. Confirme se o número de colunas está correto
3. Verifique os logs no terminal para mais detalhes
4. Teste com diferentes configurações (o app faz isso automaticamente)

**Problema**: "Tabela com número incorreto de colunas"

**Soluções**:
1. Conte as colunas manualmente no PDF
2. Verifique se há colunas vazias ou mescladas
3. Analise o output de debug para ver a estrutura real

## 📞 Suporte

Se ainda houver problemas:
1. Verifique os logs detalhados no terminal
2. Teste primeiro com um PDF mais simples
3. Considere usar ferramentas de OCR se o PDF for digitalizado

## 🎯 Status

✅ **Funcionando**: Interface web Streamlit
✅ **Funcionando**: Extração com múltiplos métodos
✅ **Funcionando**: Exportação para Excel
✅ **Funcionando**: Debug e análise de estrutura