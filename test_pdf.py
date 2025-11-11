#!/usr/bin/env python3
"""
Script de teste para extrair tabelas do PDF anexado
"""
import os
import sys
from app import extract_tables_from_pdf


def main():
    # Colunas esperadas baseadas na imagem do PDF
    column_names = ['Item', 'Descrição', 'Unid.', 'Quant.', 'Vlr. Unit.', 'Vlr. Total']
    
    print("=== TESTE DE EXTRAÇÃO DE TABELA PDF ===")
    print(f"Colunas esperadas: {column_names}")
    
    # Solicita o caminho do PDF
    pdf_path = input("Digite o caminho completo do arquivo PDF: ").strip().strip('"')
    
    if not os.path.exists(pdf_path):
        print(f"ERRO: Arquivo não encontrado: {pdf_path}")
        return
    
    print(f"\nProcessando: {pdf_path}")
    print("-" * 60)
    
    # Tenta extrair as tabelas
    df = extract_tables_from_pdf(pdf_path, column_names)
    
    if df is not None and not df.empty:
        print(f"\n✅ SUCESSO! Tabela extraída com {df.shape[0]} linhas e {df.shape[1]} colunas")
        print("\nPrimeiras 5 linhas:")
        print(df.head())
        
        # Salva em Excel
        output_file = f"{os.path.splitext(pdf_path)[0]}_extracted.xlsx"
        df.to_excel(output_file, index=False)
        print(f"\n💾 Arquivo salvo como: {output_file}")
        
    else:
        print("\n❌ FALHA: Não foi possível extrair a tabela")


if __name__ == "__main__":
    main()