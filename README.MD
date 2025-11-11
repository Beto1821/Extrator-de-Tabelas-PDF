# 🚀 Extrator de Tabelas de PDF

<p align="center"><img src="public/pumper.png" width="200"></p>

Uma ferramenta de uso pessoal para extrair tabelas de arquivos PDF de forma rápida e convertê-las para o formato Excel.

## Descrição

Este projeto é uma aplicação web simples construída para facilitar a extração de dados tabulares de documentos PDF. A interface permite que o usuário faça o upload de um arquivo, especifique o número e os nomes das colunas da tabela desejada e, com um clique, extraia os dados e faça o download de um arquivo Excel formatado.

Foi desenvolvida para agilizar tarefas do dia a dia que envolvem a cópia manual de informações de PDFs para planilhas.

**Este projeto é de código aberto, totalmente gratuito e não possui fins lucrativos.**

![Screenshot da Aplicação](https://i.imgur.com/V234d9k.png)
## Ferramentas Utilizadas

*   **Front-end:** [Streamlit](https://streamlit.io/)
*   **Extração de PDF:** [Tabula-py](https://github.com/chezou/tabula-py)
*   **Manipulação de Dados:** [Pandas](https://pandas.pydata.org/)
*   **Geração de Excel:** [XlsxWriter](https://xlsxwriter.readthedocs.io/)

## Como Executar Localmente

Siga os passos abaixo para configurar e executar o projeto em sua máquina.

### 1. Pré-requisitos

*   **Python 3.8+**
*   **Java:** A biblioteca `tabula-py` depende do Java. Para verificar se você tem o Java instalado, abra o terminal e execute:
    ```bash
    java -version
    ```
    Se o comando não for encontrado, você precisará instalar o Java.

### 2. Instalação

1.  **Clone o repositório** (ou simplesmente baixe os arquivos para uma pasta em seu computador).

2.  **Crie um ambiente virtual** (recomendado para isolar as dependências do projeto):
    ```bash
    python -m venv .venv
    ```

3.  **Ative o ambiente virtual:**
    *   No Windows: `.\.venv\Scripts\activate`
    *   No macOS/Linux: `source .venv/bin/activate`

4.  **Instale as dependências** a partir do arquivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Execução

Com o ambiente virtual ativado e as dependências instaladas, execute o seguinte comando no terminal:

```bash
streamlit run app_ui.py
```

A aplicação será aberta automaticamente em uma nova aba do seu navegador, pronta para uso!