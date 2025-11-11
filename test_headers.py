#!/usr/bin/env python3
"""
Script para testar a remoção de cabeçalhos duplicados
"""
import pandas as pd
from app import extract_tables_from_pdf, remove_duplicate_headers

# Exemplo de teste com dados simulados
def test_header_removal():
    # Simula dados com cabeçalhos duplicados
    test_data = {
        'Item': ['0001', 'Item', '0002', 'Item', '0003'],
        'Descrição': ['Produto A', 'Descrição', 'Produto B', 'Descrição', 'Produto C'],
        'Unid.': ['UN', 'Unid.', 'KG', 'Unid.', 'M'],
        'Quant.': ['10', 'Quant.', '5', 'Quant.', '20'],
        'Vlr. Unit.': ['15.50', 'Vlr. Unit.', '30.00', 'Vlr. Unit.', '8.75'],
        'Vlr. Total': ['155.00', 'Vlr. Total', '150.00', 'Vlr. Total', '175.00']
    }
    
    df = pd.DataFrame(test_data)
    column_names = ['Item', 'Descrição', 'Unid.', 'Quant.', 'Vlr. Unit.', 'Vlr. Total']
    
    print("=== TESTE DE REMOÇÃO DE CABEÇALHOS ===")
    print("DataFrame original:")
    print(df)
    print(f"Linhas originais: {len(df)}")
    
    cleaned_df = remove_duplicate_headers(df, column_names)
    
    print("\nDataFrame limpo:")
    print(cleaned_df)
    print(f"Linhas finais: {len(cleaned_df)}")

if __name__ == "__main__":
    test_header_removal()