"""
Testes unitários para as funções de processamento de dados do app.py
"""
import pytest
import pandas as pd
import sys
import os

# Adicionar o diretório raiz ao path para importar o módulo app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import consolidate_broken_rows, remove_duplicate_headers


class TestConsolidateBrokenRows:
    """
    Testes para a função consolidate_broken_rows.
    """
    
    def test_consolidate_empty_dataframe(self, empty_dataframe, column_names):
        """
        Testa se a função lida corretamente com DataFrame vazio.
        """
        result = consolidate_broken_rows(empty_dataframe, column_names)
        assert result.empty
        assert len(result) == 0
    
    def test_consolidate_normal_rows(self, sample_dataframe, column_names):
        """
        Testa se linhas normais (sem quebras) são mantidas inalteradas.
        """
        # Criar DataFrame sem linhas quebradas
        df = pd.DataFrame({
            'Item': ['001', '002', '003'],
            'Descrição': ['Produto A', 'Produto B', 'Produto C'],
            'Quantidade': [10, 20, 30],
            'Valor': [100.0, 200.0, 300.0]
        })
        
        result = consolidate_broken_rows(df, column_names)
        
        assert len(result) == 3
        assert result['Item'].tolist() == ['001', '002', '003']
        assert result['Descrição'].tolist() == ['Produto A', 'Produto B', 'Produto C']
    
    def test_consolidate_broken_rows(self, dataframe_with_broken_rows, column_names):
        """
        Testa a consolidação de linhas quebradas.
        """
        result = consolidate_broken_rows(dataframe_with_broken_rows, column_names)
        
        # Deve ter menos linhas que o original
        assert len(result) < len(dataframe_with_broken_rows)
        
        # A primeira linha deve ter a descrição consolidada
        expected_desc = "Produto com nome muito longo que foi quebrado"
        assert expected_desc in result.iloc[0]['Descrição']
        
        # A segunda linha deve ter descrição consolidada
        expected_desc2 = "Produto B segunda linha"
        assert expected_desc2 in result.iloc[1]['Descrição']
    
    def test_consolidate_preserves_columns(self, dataframe_with_broken_rows, column_names):
        """
        Testa se todas as colunas são preservadas após consolidação.
        """
        result = consolidate_broken_rows(dataframe_with_broken_rows, column_names)
        
        assert list(result.columns) == list(dataframe_with_broken_rows.columns)
    
    def test_consolidate_handles_nan_values(self, column_names):
        """
        Testa o tratamento de valores NaN durante consolidação.
        """
        df = pd.DataFrame({
            'Item': ['001', None, '002'],
            'Descrição': ['Produto A', 'continuação', 'Produto B'],
            'Quantidade': [10, None, 20],
            'Valor': [100.0, None, 200.0]
        })
        
        result = consolidate_broken_rows(df, column_names)
        
        # Deve consolidar corretamente mesmo com valores None
        assert len(result) <= len(df)
        assert not result.empty
    
    def test_consolidate_performance_large_dataset(self, large_dataframe, column_names):
        """
        Testa performance com dataset grande.
        """
        # Este teste verifica se a função não trava com muitos dados
        result = consolidate_broken_rows(large_dataframe, column_names)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) <= len(large_dataframe)


class TestRemoveDuplicateHeaders:
    """
    Testes para a função remove_duplicate_headers.
    """
    
    def test_remove_empty_dataframe(self, empty_dataframe, column_names):
        """
        Testa se a função lida corretamente com DataFrame vazio.
        """
        result = remove_duplicate_headers(empty_dataframe, column_names)
        assert result.empty
        assert len(result) == 0
    
    def test_remove_no_duplicates(self, sample_dataframe, column_names):
        """
        Testa DataFrame sem cabeçalhos duplicados.
        """
        result = remove_duplicate_headers(sample_dataframe, column_names)
        
        # Deve manter o mesmo tamanho se não há duplicatas
        assert len(result) == len(sample_dataframe)
    
    def test_remove_duplicate_headers(self, dataframe_with_duplicates, column_names):
        """
        Testa a remoção de cabeçalhos duplicados.
        """
        result = remove_duplicate_headers(dataframe_with_duplicates, column_names)
        
        # Deve ter menos linhas que o original
        assert len(result) < len(dataframe_with_duplicates)
        
        # Não deve conter linhas com 'Item', 'Descrição' como dados
        item_values = result['Item'].astype(str).tolist()
        assert 'Item' not in item_values
        
        desc_values = result['Descrição'].astype(str).tolist()
        assert 'Descrição' not in desc_values
    
    def test_remove_preserves_data_rows(self, dataframe_with_duplicates, column_names):
        """
        Testa se as linhas de dados válidas são preservadas.
        """
        result = remove_duplicate_headers(dataframe_with_duplicates, column_names)
        
        # Deve preservar as linhas de dados válidas
        valid_items = ['001', '002', '003']
        result_items = result['Item'].tolist()
        
        for item in valid_items:
            assert item in result_items
    
    def test_remove_handles_case_insensitive(self, column_names):
        """
        Testa se a remoção é case-insensitive.
        """
        df = pd.DataFrame({
            'Item': ['ITEM', '001', 'item', '002'],
            'Descrição': ['DESCRIÇÃO', 'Produto A', 'descrição', 'Produto B'],
            'Quantidade': ['QUANTIDADE', '10', 'quantidade', '20'],
            'Valor': ['VALOR', '100.0', 'valor', '200.0']
        })
        
        result = remove_duplicate_headers(df, column_names)
        
        # Deve remover tanto 'ITEM' quanto 'item'
        assert len(result) == 2
        assert '001' in result['Item'].values
        assert '002' in result['Item'].values
    
    def test_remove_multiple_header_patterns(self, column_names):
        """
        Testa remoção de diferentes padrões de cabeçalho.
        """
        df = pd.DataFrame({
            'Item': ['Item', '001', 'Código', '002', 'Produto'],
            'Descrição': ['Descrição', 'Prod A', 'Nome', 'Prod B', 'Desc'],
            'Quantidade': ['Qtd', '10', 'Quant', '20', 'Unidades'],
            'Valor': ['Valor', '100', 'Preço', '200', 'Total']
        })
        
        result = remove_duplicate_headers(df, column_names)
        
        # Deve manter apenas as linhas de dados válidas
        expected_items = ['001', '002']
        result_items = result['Item'].tolist()
        
        for item in expected_items:
            assert item in result_items


class TestFunctionsIntegration:
    """
    Testes de integração entre funções.
    """
    
    def test_consolidate_then_remove_headers(self, column_names):
        """
        Testa o fluxo completo: consolidar linhas + remover headers.
        """
        # DataFrame com linhas quebradas E cabeçalhos duplicados
        df = pd.DataFrame({
            'Item': ['Item', '001', 'nan', 'Item', '002'],
            'Descrição': ['Descrição', 'Produto longo', 'continuação', 'Descrição', 'Produto B'],
            'Quantidade': ['Quantidade', '10', '', 'Quantidade', '20'],
            'Valor': ['Valor', '100.0', '', 'Valor', '200.0']
        })
        
        # Primeiro consolida linhas quebradas
        consolidated = consolidate_broken_rows(df, column_names)
        
        # Depois remove cabeçalhos duplicados
        final_result = remove_duplicate_headers(consolidated, column_names)
        
        # Verifica resultado final
        assert len(final_result) == 2  # Apenas 2 produtos válidos
        
        # Verifica se consolidação funcionou
        assert 'Produto longo continuação' in final_result.iloc[0]['Descrição']
        
        # Verifica se remoção de headers funcionou
        assert 'Item' not in final_result['Item'].values
        assert 'Descrição' not in final_result['Descrição'].values


# Testes com pytest.mark para categorização
@pytest.mark.unit
def test_functions_exist():
    """
    Verifica se todas as funções principais existem e são chamáveis.
    """
    assert callable(consolidate_broken_rows)
    assert callable(remove_duplicate_headers)


@pytest.mark.unit
def test_functions_return_dataframe():
    """
    Verifica se as funções retornam DataFrame.
    """
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    columns = ['A', 'B']
    
    result1 = consolidate_broken_rows(df, columns)
    result2 = remove_duplicate_headers(df, columns)
    
    assert isinstance(result1, pd.DataFrame)
    assert isinstance(result2, pd.DataFrame)