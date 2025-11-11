#!/usr/bin/env python3
"""
Script para testar a consolidação de linhas quebradas
"""
import pandas as pd
from app import consolidate_broken_rows

def test_broken_lines_consolidation():
    # Simula dados com linhas quebradas
    test_data = {
        'Item': ['0249', '', '0250', '0251', '', '0252'],
        'Descrição': [
            'Grampeador UN',
            'Controle de Pressão da Mola Corpo em Aço',  # Linha quebrada
            'GRAMPEADOR UN',
            'Grampeador UN',
            'GRAMPOS DE 10G/8 MM, EMAÇO GALVANIZADO',  # Linha quebrada
            'GRAMPEADOR UN'
        ],
        'Unid.': ['', '', 'UN', 'UN', '', 'UN'],
        'Quant.': ['420', '', '25', '30', '', '8'],
        'Vlr. Unit.': ['36.47', '', '61.47', '149.68', '', '117.83'],
        'Vlr. Total': ['15317.40', '', '1536.75', '4490.40', '', '942.64']
    }
    
    df = pd.DataFrame(test_data)
    column_names = ['Item', 'Descrição', 'Unid.', 'Quant.', 'Vlr. Unit.', 'Vlr. Total']
    
    print("=== TESTE DE CONSOLIDAÇÃO DE LINHAS QUEBRADAS ===")
    print("DataFrame original:")
    for i, row in df.iterrows():
        print(f"  {i}: {list(row.values)}")
    
    print(f"Linhas originais: {len(df)}")
    
    consolidated_df = consolidate_broken_rows(df, column_names)
    
    print("\nDataFrame consolidado:")
    for i, row in consolidated_df.iterrows():
        print(f"  {i}: {list(row.values)}")
    
    print(f"Linhas finais: {len(consolidated_df)}")

if __name__ == "__main__":
    test_broken_lines_consolidation()