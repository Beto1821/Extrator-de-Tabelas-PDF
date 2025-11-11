"""
Testes de integração para o fluxo completo de extração de PDF.
"""
import pytest
import pandas as pd
import tempfile
import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import extract_tables_from_pdf
from app_ui import to_excel


@pytest.mark.integration
class TestPDFExtractionIntegration:
    """
    Testes de integração para extração completa de PDF.
    """
    
    def test_pdf_to_excel_pipeline(self, temp_pdf_file):
        """
        Testa o pipeline completo: PDF -> DataFrame -> Excel.
        """
        columns = ['Item', 'Descrição', 'Quantidade', 'Valor']
        
        # Extrair dados do PDF
        df = extract_tables_from_pdf(temp_pdf_file, columns)
        
        # Converter para Excel
        if not df.empty:
            excel_data = to_excel(df)
            assert isinstance(excel_data, bytes)
            assert len(excel_data) > 0
        else:
            # Com arquivo de teste vazio, DataFrame será vazio
            assert isinstance(df, pd.DataFrame)
            assert len(df) == 0
    
    def test_end_to_end_with_real_data(self):
        """
        Testa com dados que simulam um PDF real.
        """
        # Simular dados extraídos de PDF real
        raw_data = pd.DataFrame({
            'Col1': ['Item', '001', 'nan', '002', 'Item', '003', 'nan'],
            'Col2': ['Descrição', 'Produto A muito longo', 
                    'que foi quebrado', 'Produto B', 'Descrição',
                    'Produto C com nome', 'também longo'],
            'Col3': ['Qtd', '10', '', '20', 'Qtd', '30', ''],
            'Col4': ['Valor', '100.50', '', '200.75', 'Valor', '300.25', '']
        })
        
        columns = ['Item', 'Descrição', 'Quantidade', 'Valor']
        
        # Simular processamento completo
        from app import consolidate_broken_rows, remove_duplicate_headers
        
        # Renomear colunas
        raw_data.columns = columns
        
        # Remover headers duplicados
        clean_data = remove_duplicate_headers(raw_data, columns)
        
        # Consolidar linhas quebradas
        final_data = consolidate_broken_rows(clean_data, columns)
        
        # Verificações
        assert isinstance(final_data, pd.DataFrame)
        assert not final_data.empty
        
        # Deve ter consolidado as descrições
        descriptions = final_data['Descrição'].tolist()
        assert any('Produto A muito longo que foi quebrado' in desc 
                  for desc in descriptions)
        
        # Não deve ter headers como dados
        items = final_data['Item'].astype(str).tolist()
        assert 'Item' not in items
        
        # Converter para Excel
        excel_data = to_excel(final_data)
        assert isinstance(excel_data, bytes)
        assert len(excel_data) > 0
    
    def test_error_handling_integration(self):
        """
        Testa tratamento de erros no fluxo completo.
        """
        columns = ['Item', 'Descrição', 'Quantidade', 'Valor']
        
        # Arquivo inexistente
        result = extract_tables_from_pdf('arquivo_inexistente.pdf', columns)
        assert isinstance(result, pd.DataFrame)
        assert result.empty
        
        # Tentar converter DataFrame vazio para Excel
        excel_data = to_excel(result)
        assert isinstance(excel_data, bytes)
        # Excel vazio ainda tem alguns bytes de estrutura
        assert len(excel_data) > 0
    
    def test_large_data_integration(self, large_dataframe):
        """
        Testa integração com dataset grande.
        """
        columns = ['Item', 'Descrição', 'Quantidade', 'Valor']
        
        # Simular processamento completo com dados grandes
        from app import consolidate_broken_rows, remove_duplicate_headers
        
        # Processar dados
        processed_data = remove_duplicate_headers(large_dataframe, columns)
        final_data = consolidate_broken_rows(processed_data, columns)
        
        # Converter para Excel
        excel_data = to_excel(final_data)
        
        # Verificações
        assert isinstance(final_data, pd.DataFrame)
        assert isinstance(excel_data, bytes)
        assert len(excel_data) > 1000  # Excel com dados deve ser maior


@pytest.mark.integration
class TestUIIntegration:
    """
    Testes de integração para funções da interface.
    """
    
    def test_to_excel_function(self, sample_dataframe):
        """
        Testa a função to_excel isoladamente.
        """
        excel_data = to_excel(sample_dataframe)
        
        assert isinstance(excel_data, bytes)
        assert len(excel_data) > 0
        
        # Verificar se é um arquivo Excel válido (começa com assinatura Excel)
        # Excel files começam com PK (ZIP signature)
        assert excel_data[:2] == b'PK'
    
    def test_to_excel_with_unicode(self):
        """
        Testa conversão para Excel com caracteres Unicode.
        """
        df_unicode = pd.DataFrame({
            'Produto': ['Açúcar', 'Café', 'Pão'],
            'Descrição': ['Açúcar cristal', 'Café torrado', 'Pão francês'],
            'Preço': [5.50, 12.80, 0.75]
        })
        
        excel_data = to_excel(df_unicode)
        
        assert isinstance(excel_data, bytes)
        assert len(excel_data) > 0
    
    def test_to_excel_empty_dataframe(self, empty_dataframe):
        """
        Testa conversão de DataFrame vazio para Excel.
        """
        excel_data = to_excel(empty_dataframe)
        
        assert isinstance(excel_data, bytes)
        assert len(excel_data) > 0  # Excel vazio ainda tem estrutura


@pytest.mark.integration
class TestFileHandling:
    """
    Testes de integração para manipulação de arquivos.
    """
    
    def test_temp_file_cleanup(self):
        """
        Testa se arquivos temporários são limpos corretamente.
        """
        import tempfile
        import os
        
        # Criar arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
            df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
            excel_data = to_excel(df)
            tmp.write(excel_data)
            tmp.flush()
            
            temp_path = tmp.name
            
            # Verificar se arquivo foi criado
            assert os.path.exists(temp_path)
            
            # Ler arquivo de volta
            df_read = pd.read_excel(temp_path)
            assert len(df_read) == 3
            
        # Limpar
        os.unlink(temp_path)
        assert not os.path.exists(temp_path)
    
    def test_concurrent_processing(self):
        """
        Testa processamento concorrente de múltiplos DataFrames.
        """
        import concurrent.futures
        from app import consolidate_broken_rows
        
        def process_dataframe(i):
            df = pd.DataFrame({
                'Item': [f'{j:03d}' for j in range(i*100, (i+1)*100)],
                'Desc': [f'Product {j}' for j in range(i*100, (i+1)*100)],
                'Qty': [j for j in range(i*100, (i+1)*100)],
                'Price': [j*10.0 for j in range(i*100, (i+1)*100)]
            })
            columns = ['Item', 'Desc', 'Qty', 'Price']
            return consolidate_broken_rows(df, columns)
        
        # Processar 5 DataFrames concorrentemente
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(process_dataframe, i) for i in range(5)]
            results = [future.result() for future in futures]
        
        # Verificar resultados
        for result in results:
            assert isinstance(result, pd.DataFrame)
            assert len(result) == 100


@pytest.mark.integration
@pytest.mark.slow
class TestPerformanceIntegration:
    """
    Testes de integração focados em performance.
    """
    
    def test_memory_usage_pipeline(self):
        """
        Testa uso de memória no pipeline completo.
        """
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Criar dados grandes
        large_df = pd.DataFrame({
            'Item': [f'{i:04d}' for i in range(10000)],
            'Desc': [f'Product {i} with long description' for i in range(10000)],
            'Qty': list(range(10000)),
            'Price': [i * 1.5 for i in range(10000)]
        })
        
        columns = ['Item', 'Desc', 'Qty', 'Price']
        
        # Pipeline completo
        from app import consolidate_broken_rows, remove_duplicate_headers
        
        processed = remove_duplicate_headers(large_df, columns)
        final = consolidate_broken_rows(processed, columns)
        excel_data = to_excel(final)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Não deve aumentar mais que 200MB
        assert memory_increase < 200
        assert isinstance(excel_data, bytes)
    
    def test_processing_time_pipeline(self, large_dataframe):
        """
        Testa tempo de processamento do pipeline completo.
        """
        import time
        
        columns = ['Item', 'Descrição', 'Quantidade', 'Valor']
        
        start_time = time.time()
        
        # Pipeline completo
        from app import consolidate_broken_rows, remove_duplicate_headers
        
        processed = remove_duplicate_headers(large_dataframe, columns)
        final = consolidate_broken_rows(processed, columns)
        excel_data = to_excel(final)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Não deve levar mais que 10 segundos para 1000 linhas
        assert processing_time < 10.0
        assert isinstance(excel_data, bytes)
        assert len(excel_data) > 0