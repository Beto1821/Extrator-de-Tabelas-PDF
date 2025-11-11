"""
Testes unitários para a função extract_tables_from_pdf usando mocks.
"""
import pytest
import pandas as pd
import sys
import os
from unittest.mock import patch, Mock, MagicMock

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import extract_tables_from_pdf


class TestExtractTablesFromPDF:
    """
    Testes para a função extract_tables_from_pdf.
    """
    
    @patch('app.camelot')
    def test_extract_with_camelot_success(self, mock_camelot, temp_pdf_file, 
                                          mock_camelot_tables, column_names):
        """
        Testa extração bem-sucedida usando Camelot.
        """
        # Configurar mock do camelot
        mock_camelot.read_pdf.return_value = mock_camelot_tables
        
        result = extract_tables_from_pdf(temp_pdf_file, column_names)
        
        # Verificações
        assert isinstance(result, pd.DataFrame)
        assert not result.empty
        assert len(result.columns) == len(column_names)
        mock_camelot.read_pdf.assert_called_once()
    
    @patch('app.tabula')
    @patch('app.CAMELOT_AVAILABLE', False)
    def test_extract_with_tabula_fallback(self, mock_tabula, temp_pdf_file,
                                          mock_tabula_tables, column_names):
        """
        Testa fallback para Tabula quando Camelot não disponível.
        """
        # Configurar mock do tabula
        mock_tabula.read_pdf.return_value = mock_tabula_tables
        
        result = extract_tables_from_pdf(temp_pdf_file, column_names)
        
        # Verificações
        assert isinstance(result, pd.DataFrame)
        assert not result.empty
        mock_tabula.read_pdf.assert_called_once()
    
    @patch('app.camelot')
    @patch('app.tabula')
    def test_extract_camelot_fails_tabula_succeeds(self, mock_tabula, 
                                                   mock_camelot, temp_pdf_file,
                                                   mock_tabula_tables, 
                                                   column_names):
        """
        Testa fallback quando Camelot falha e Tabula funciona.
        """
        # Camelot falha
        mock_camelot.read_pdf.side_effect = Exception("Camelot error")
        
        # Tabula funciona
        mock_tabula.read_pdf.return_value = mock_tabula_tables
        
        result = extract_tables_from_pdf(temp_pdf_file, column_names)
        
        # Verificações
        assert isinstance(result, pd.DataFrame)
        assert not result.empty
        mock_camelot.read_pdf.assert_called_once()
        mock_tabula.read_pdf.assert_called_once()
    
    @patch('app.camelot')
    @patch('app.tabula')
    def test_extract_both_methods_fail(self, mock_tabula, mock_camelot,
                                       temp_pdf_file, column_names):
        """
        Testa quando ambos os métodos falham.
        """
        # Ambos falham
        mock_camelot.read_pdf.side_effect = Exception("Camelot error")
        mock_tabula.read_pdf.side_effect = Exception("Tabula error")
        
        result = extract_tables_from_pdf(temp_pdf_file, column_names)
        
        # Deve retornar DataFrame vazio
        assert isinstance(result, pd.DataFrame)
        assert result.empty
    
    def test_extract_invalid_file_path(self, column_names):
        """
        Testa com caminho de arquivo inválido.
        """
        invalid_path = "/path/that/does/not/exist.pdf"
        
        result = extract_tables_from_pdf(invalid_path, column_names)
        
        # Deve retornar DataFrame vazio
        assert isinstance(result, pd.DataFrame)
        assert result.empty
    
    @patch('app.camelot')
    def test_extract_with_custom_columns(self, mock_camelot, temp_pdf_file,
                                         mock_camelot_tables):
        """
        Testa com nomes de colunas personalizados.
        """
        custom_columns = ['Código', 'Nome', 'Qtd', 'Preço']
        mock_camelot.read_pdf.return_value = mock_camelot_tables
        
        result = extract_tables_from_pdf(temp_pdf_file, custom_columns)
        
        assert list(result.columns) == custom_columns
    
    @patch('app.camelot')
    def test_extract_empty_tables(self, mock_camelot, temp_pdf_file,
                                  column_names):
        """
        Testa quando Camelot retorna tabelas vazias.
        """
        # Mock retorna lista vazia
        mock_camelot.read_pdf.return_value = []
        
        result = extract_tables_from_pdf(temp_pdf_file, column_names)
        
        # Deve retornar DataFrame vazio
        assert isinstance(result, pd.DataFrame)
        assert result.empty
    
    @patch('app.camelot')
    @patch('app.consolidate_broken_rows')
    @patch('app.remove_duplicate_headers')
    def test_extract_calls_processing_functions(self, mock_remove_headers,
                                                mock_consolidate, mock_camelot,
                                                temp_pdf_file, 
                                                mock_camelot_tables,
                                                column_names):
        """
        Verifica se as funções de processamento são chamadas.
        """
        mock_camelot.read_pdf.return_value = mock_camelot_tables
        mock_remove_headers.return_value = mock_camelot_tables[0].df
        mock_consolidate.return_value = mock_camelot_tables[0].df
        
        extract_tables_from_pdf(temp_pdf_file, column_names)
        
        # Verifica se as funções foram chamadas
        mock_remove_headers.assert_called_once()
        mock_consolidate.assert_called_once()


@pytest.mark.unit 
class TestExtractTablesIntegration:
    """
    Testes de integração para extract_tables_from_pdf.
    """
    
    @patch('app.camelot')
    def test_full_pipeline_with_processing(self, mock_camelot, temp_pdf_file):
        """
        Testa o pipeline completo com dados que precisam de processamento.
        """
        # Criar dados que simulam extração real com problemas
        mock_table = Mock()
        mock_table.df = pd.DataFrame({
            'Item': ['Item', '001', 'nan', '002', 'Item', '003'],
            'Descrição': ['Descrição', 'Produto A muito', 'longo', 'Produto B', 
                         'Descrição', 'Produto C'],
            'Quantidade': ['Qtd', '10', '', '20', 'Qtd', '30'],
            'Valor': ['Valor', '100.0', '', '200.0', 'Valor', '300.0']
        })
        
        mock_camelot.read_pdf.return_value = [mock_table]
        
        column_names = ['Item', 'Descrição', 'Quantidade', 'Valor']
        result = extract_tables_from_pdf(temp_pdf_file, column_names)
        
        # Verificações do resultado final
        assert isinstance(result, pd.DataFrame)
        assert not result.empty
        
        # Verifica se headers duplicados foram removidos
        assert 'Item' not in result['Item'].values
        
        # Verifica se consolidação aconteceu
        first_desc = result.iloc[0]['Descrição']
        assert 'Produto A muito longo' in first_desc
    
    def test_extract_with_real_column_names(self, temp_pdf_file):
        """
        Testa com nomes de colunas típicos de um PDF real.
        """
        realistic_columns = [
            'Código do Item',
            'Descrição do Produto', 
            'Unidade de Medida',
            'Quantidade',
            'Valor Unitário',
            'Valor Total'
        ]
        
        result = extract_tables_from_pdf(temp_pdf_file, realistic_columns)
        
        # Deve retornar DataFrame com as colunas corretas
        assert isinstance(result, pd.DataFrame)
        # Com arquivo de teste simples, deve retornar vazio
        if not result.empty:
            assert list(result.columns) == realistic_columns