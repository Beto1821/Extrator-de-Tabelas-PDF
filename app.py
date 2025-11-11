import tabula
import pandas as pd
import os

try:
    import camelot
    CAMELOT_AVAILABLE = True
except ImportError:
    CAMELOT_AVAILABLE = False
    print("Camelot não disponível. Usando apenas Tabula.")


def consolidate_broken_rows(df: pd.DataFrame, column_names: list[str]):
    """
    Consolida linhas quebradas onde o texto da descrição foi 
    dividido em múltiplas linhas.
    """
    if df.empty:
        return df
    
    print(f"Consolidando linhas quebradas... DataFrame original: {df.shape}")
    
    consolidated_rows = []
    i = 0
    
    while i < len(df):
        current_row = df.iloc[i].copy()
        
        # Verifica se a linha atual tem um código de item (primeira coluna)
        item_code = str(current_row.iloc[0]).strip()
        
        # Se tem código de item e não está vazio, é uma linha principal
        if item_code and item_code != 'nan' and len(item_code) >= 3:
            # Verifica as próximas linhas para possíveis continuações
            j = i + 1
            
            while j < len(df):
                next_row = df.iloc[j]
                next_item_code = str(next_row.iloc[0]).strip()
                
                # Se a próxima linha não tem código de item (ou é vazia/nan),
                # pode ser uma continuação da descrição
                if not next_item_code or next_item_code == 'nan' or len(next_item_code) < 3:
                    # Verifica se há texto na segunda coluna (descrição)
                    continuation_text = str(next_row.iloc[1]).strip()
                    
                    if continuation_text and continuation_text != 'nan':
                        # Consolida o texto na descrição da linha principal
                        current_desc = str(current_row.iloc[1]).strip()
                        if current_desc == 'nan':
                            current_desc = ''
                        
                        current_row.iloc[1] = f"{current_desc} {continuation_text}".strip()
                        print(f"Linha {j} consolidada na linha {i}: {continuation_text[:50]}...")
                        j += 1
                    else:
                        break
                else:
                    # Se a próxima linha tem código de item, para a consolidação
                    break
            
            consolidated_rows.append(current_row)
            i = j  # Pula para a próxima linha não processada
        else:
            # Se não é uma linha principal válida, pode ser continuação órfã
            # Tenta anexar à linha anterior se possível
            if consolidated_rows:
                continuation_text = str(current_row.iloc[1]).strip()
                if continuation_text and continuation_text != 'nan':
                    last_row = consolidated_rows[-1]
                    current_desc = str(last_row.iloc[1]).strip()
                    last_row.iloc[1] = f"{current_desc} {continuation_text}".strip()
                    print(f"Linha órfã {i} anexada: {continuation_text[:50]}...")
            i += 1
    
    if consolidated_rows:
        result_df = pd.DataFrame(consolidated_rows, columns=df.columns)
        result_df.reset_index(drop=True, inplace=True)
        print(f"Consolidação concluída: {len(df)} → {len(result_df)} linhas")
        return result_df
    else:
        return df


def remove_duplicate_headers(df: pd.DataFrame, column_names: list[str]):
    """
    Remove cabeçalhos duplicados que aparecem no meio dos dados.
    Detecta linhas que contêm 'Item', 'Descrição', 'Unid.', etc.
    """
    if df.empty:
        return df
    
    print(f"Removendo cabeçalhos duplicados... DataFrame original: {df.shape}")
    
    # Identifica linhas que são cabeçalhos duplicados
    rows_to_remove = []
    
    for idx, row in df.iterrows():
        # Converte todos os valores da linha para string
        row_str = ' '.join([str(val) for val in row.values if pd.notna(val)])
        
        # Lista de palavras-chave dos cabeçalhos (flexível)
        header_keywords = ['Item', 'Descrição', 'Unid.', 'Quant.', 
                          'Vlr. Unit.', 'Vlr. Total', 'Quantidade', 
                          'Valor', 'Código', 'Nome', 'Preço', 'Total',
                          'Qtd', 'Desc', 'ITEM', 'DESCRIÇÃO', 'item',
                          'descrição', 'quantidade', 'valor']
        
        # Conta quantas palavras-chave do cabeçalho estão presentes
        keyword_count = sum(1 for keyword in header_keywords 
                          if keyword.lower() in row_str.lower())
        
        # Se encontrar 2 ou mais palavras-chave, considera cabeçalho
        if keyword_count >= 2:
            rows_to_remove.append(idx)
            print(f"Linha {idx} removida (cabeçalho): {row_str[:100]}...")
    
    # Remove as linhas identificadas como cabeçalhos
    if rows_to_remove:
        cleaned_df = df.drop(rows_to_remove).copy()
        print(f"Removidas {len(rows_to_remove)} linhas de cabeçalho")
    else:
        cleaned_df = df.copy()
        print("Nenhum cabeçalho duplicado encontrado")
    
    # Remove linhas completamente vazias
    before_empty = cleaned_df.shape[0]
    cleaned_df = cleaned_df.dropna(how='all')
    after_empty = cleaned_df.shape[0]
    
    if before_empty != after_empty:
        print(f"Removidas {before_empty - after_empty} linhas vazias")
    
    # Reset do índice
    cleaned_df.reset_index(drop=True, inplace=True)
    
    print(f"DataFrame final: {cleaned_df.shape}")
    return cleaned_df


def extract_tables_from_pdf(pdf_path: str, column_names: list[str]):
    """
    Extrai tabelas de um PDF e retorna como DataFrame.
    Remove cabeçalhos duplicados automaticamente.
    """
    if not os.path.exists(pdf_path):
        print(f"Erro: Arquivo {pdf_path} não existe.")
        empty_df = pd.DataFrame(columns=column_names)
        return empty_df

    print(f"📄 Extraindo tabelas de: {pdf_path}")
    
    # Método 1: Camelot
    if CAMELOT_AVAILABLE:
        try:
            print("🔍 Método 1: Tentando com Camelot (lattice)...")
            tables = camelot.read_pdf(pdf_path, pages='all', flavor='lattice')
            
            if len(tables) == 0:
                print("🔍 Tentando Camelot (stream)...")
                tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream')
            
            if len(tables) > 0:
                print(f"✅ Camelot: {len(tables)} tabela(s) encontrada(s)")
                
                all_dfs = []
                for i, table in enumerate(tables):
                    df = table.df
                    df = df.dropna(how='all')
                    
                    if df.shape[1] == len(column_names):
                        df.columns = column_names
                        all_dfs.append(df)

                if all_dfs:
                    result_df = pd.concat(all_dfs, ignore_index=True)
                    result_df = result_df.dropna(how='all')
                    
                    # Remove cabeçalhos duplicados
                    result_df = remove_duplicate_headers(result_df, column_names)
                    
                    # Consolida linhas quebradas
                    result_df = consolidate_broken_rows(result_df, column_names)
                    
                    print(f"✅ Camelot: {result_df.shape[0]} linhas finais")
                    return result_df
                    
        except Exception as e:
            print(f"Erro Camelot: {e}")

    # Método 2: Tabula
    try:
        print("🔍 Método 2: Tentando com Tabula...")
        
        configs = [
            {'pages': 'all', 'multiple_tables': True, 'stream': True},
            {'pages': 'all', 'multiple_tables': True, 'lattice': True},
        ]
        
        for i, config in enumerate(configs):
            try:
                tables = tabula.read_pdf(pdf_path, **config)
                
                if tables:
                    print(f"✅ Config {i+1}: {len(tables)} tabela(s)")
                    
                    correct_tables = []
                    for table in tables:
                        table = table.dropna(how='all')
                        
                        if table.shape[1] == len(column_names):
                            table.columns = column_names
                            correct_tables.append(table)
                    
                    if correct_tables:
                        result_df = pd.concat(correct_tables, ignore_index=True)
                        result_df = result_df.dropna(how='all')
                        
                        # Remove cabeçalhos duplicados
                        result_df = remove_duplicate_headers(result_df, column_names)
                        
                        # Consolida linhas quebradas
                        result_df = consolidate_broken_rows(result_df, column_names)
                        
                        print(f"✅ Tabula: {result_df.shape[0]} linhas finais")
                        return result_df
                        
            except Exception as config_error:
                print(f"Config {i+1} erro: {config_error}")

    except Exception as e:
        print(f"Erro Tabula: {e}")

    # Debug
    print("Analisando estrutura do PDF...")
    try:
        tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True, stream=True)
        
        for i, table in enumerate(tables):
            print(f"Tabela {i+1}: {table.shape}")
            print(f"Colunas: {list(table.columns)}")
            print(table.head(2))
            print("-" * 30)
            
    except Exception as debug_error:
        print(f"Debug erro: {debug_error}")
    
    # Sempre retornar DataFrame, mesmo que vazio
    print("❌ Nenhuma tabela encontrada. Retornando DataFrame vazio.")
    empty_df = pd.DataFrame(columns=column_names)
    return empty_df


def format_excel(dataframe: pd.DataFrame, excel_path: str):
    """Salva DataFrame em Excel."""
    try:
        dataframe.to_excel(excel_path, index=False)
        print(f"Salvo: {excel_path}")
    except Exception as e:
        print(f"Erro salvamento: {e}")


def main():
    """Função principal."""
    print("=== Extrator de Tabelas PDF ===")
    
    pdf_path = input("Caminho do PDF: ").strip()
    cols = input("Colunas (separadas por vírgula): ").strip()
    column_names = [name.strip() for name in cols.split(",")]

    df_table = extract_tables_from_pdf(pdf_path, column_names)

    if not df_table.empty:
        name_base = os.path.splitext(os.path.basename(pdf_path))[0]
        excel_output = f"{name_base}_extracted.xlsx"
        format_excel(df_table, excel_output)
    else:
        print("❌ Extração falhou")


if __name__ == "__main__":
    main()