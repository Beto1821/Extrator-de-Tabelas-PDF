"""
Testes de performance para funções críticas usando pytest-benchmark.
"""
import pytest
import pandas as pd
import sys
import os
from faker import Faker

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import consolidate_broken_rows, remove_duplicate_headers


@pytest.fixture
def performance_dataframe():
    """
    DataFrame grande para testes de performance.
    """
    fake = Faker()
    Faker.seed(42)
    
    # Criar DataFrame com 5000 linhas
    size = 5000
    data = {
        'Item': [f'{i:04d}' if i % 10 != 0 else 'nan' for i in range(size)],
        'Descrição': [fake.text(max_nb_chars=100) for _ in range(size)],
        'Quantidade': [fake.random_int(1, 1000) if i % 10 != 0 else None 
                      for i in range(size)],
        'Valor': [fake.pyfloat(left_digits=4, right_digits=2, positive=True)
                 if i % 10 != 0 else None for i in range(size)]
    }
    return pd.DataFrame(data)


@pytest.fixture  
def dataframe_with_many_duplicates():
    """
    DataFrame com muitos cabeçalhos duplicados para teste de performance.
    """
    fake = Faker()
    Faker.seed(42)
    
    data = []
    for i in range(1000):
        # A cada 50 linhas, inserir um cabeçalho duplicado
        if i % 50 == 0:
            data.append(['Item', 'Descrição', 'Quantidade', 'Valor'])
        else:
            data.append([
                f'{i:04d}',
                fake.company(),
                fake.random_int(1, 100),
                fake.pyfloat(left_digits=3, right_digits=2, positive=True)
            ])
    
    return pd.DataFrame(data, columns=['Item', 'Descrição', 'Quantidade', 'Valor'])


@pytest.mark.performance
class TestPerformance:
    """
    Testes de performance para funções críticas.
    """
    
    def test_consolidate_performance_small(self, benchmark, sample_dataframe):
        """
        Benchmark para consolidação com DataFrame pequeno.
        """
        columns = ['Item', 'Descrição', 'Quantidade', 'Valor']
        
        result = benchmark(consolidate_broken_rows, sample_dataframe, columns)
        
        assert isinstance(result, pd.DataFrame)
    
    def test_consolidate_performance_large(self, benchmark, performance_dataframe):
        """
        Benchmark para consolidação com DataFrame grande (5000 linhas).
        """
        columns = ['Item', 'Descrição', 'Quantidade', 'Valor']
        
        result = benchmark(consolidate_broken_rows, performance_dataframe, columns)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) <= len(performance_dataframe)
    
    def test_remove_headers_performance_small(self, benchmark, sample_dataframe):
        """
        Benchmark para remoção de headers com DataFrame pequeno.
        """
        columns = ['Item', 'Descrição', 'Quantidade', 'Valor']
        
        result = benchmark(remove_duplicate_headers, sample_dataframe, columns)
        
        assert isinstance(result, pd.DataFrame)
    
    def test_remove_headers_performance_many_duplicates(self, benchmark, 
                                                        dataframe_with_many_duplicates):
        """
        Benchmark para remoção com muitos headers duplicados.
        """
        columns = ['Item', 'Descrição', 'Quantidade', 'Valor']
        
        result = benchmark(remove_duplicate_headers, dataframe_with_many_duplicates, columns)
        
        assert isinstance(result, pd.DataFrame)
        # Deve ter removido os headers duplicados
        assert len(result) < len(dataframe_with_many_duplicates)
    
    def test_full_pipeline_performance(self, benchmark, performance_dataframe):
        """
        Benchmark do pipeline completo: consolidar + remover headers.
        """
        columns = ['Item', 'Descrição', 'Quantidade', 'Valor']
        
        def full_pipeline(df, cols):
            consolidated = consolidate_broken_rows(df, cols)
            return remove_duplicate_headers(consolidated, cols)
        
        result = benchmark(full_pipeline, performance_dataframe, columns)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) <= len(performance_dataframe)
    
    @pytest.mark.slow
    def test_memory_usage_large_dataset(self, performance_dataframe):
        """
        Teste de uso de memória com dataset grande.
        """
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        # Memória antes
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        columns = ['Item', 'Descrição', 'Quantidade', 'Valor']
        
        # Processar dados
        consolidated = consolidate_broken_rows(performance_dataframe, columns)
        result = remove_duplicate_headers(consolidated, columns)
        
        # Memória depois
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        
        memory_increase = memory_after - memory_before
        
        # Verificar que não houve vazamento excessivo (limite arbitrário: 100MB)
        assert memory_increase < 100
        assert isinstance(result, pd.DataFrame)
    
    def test_consolidate_complexity(self, benchmark):
        """
        Testa a complexidade da função de consolidação com diferentes tamanhos.
        """
        def create_test_data(size):
            return pd.DataFrame({
                'Item': [f'{i:04d}' if i % 3 != 0 else 'nan' for i in range(size)],
                'Descrição': [f'Produto {i}' if i % 3 != 0 else f'cont {i}' 
                             for i in range(size)],
                'Quantidade': [i if i % 3 != 0 else None for i in range(size)],
                'Valor': [i * 10.0 if i % 3 != 0 else None for i in range(size)]
            })
        
        columns = ['Item', 'Descrição', 'Quantidade', 'Valor']
        
        # Testar com 1000 linhas
        test_data = create_test_data(1000)
        result = benchmark(consolidate_broken_rows, test_data, columns)
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) <= len(test_data)


@pytest.mark.benchmark
def test_pandas_operations_performance(benchmark):
    """
    Benchmark das operações pandas utilizadas internamente.
    """
    # Simular operações pandas típicas usadas no app
    fake = Faker()
    Faker.seed(42)
    
    df = pd.DataFrame({
        'A': [fake.word() for _ in range(10000)],
        'B': [fake.sentence() for _ in range(10000)],
        'C': [fake.random_int(1, 1000) for _ in range(10000)]
    })
    
    def pandas_operations(dataframe):
        # Simular operações típicas
        result = dataframe.copy()
        result = result[result['A'].notna()]
        result = result.reset_index(drop=True)
        result['D'] = result['A'] + ' ' + result['B']
        return result
    
    result = benchmark(pandas_operations, df)
    assert len(result) <= len(df)


# Configurações específicas para testes de performance
@pytest.fixture(autouse=True)
def performance_config():
    """
    Configurações automáticas para testes de performance.
    """
    # Configurar pandas para melhor performance em testes
    pd.set_option('mode.chained_assignment', None)
    yield
    # Restaurar configurações padrão
    pd.reset_option('mode.chained_assignment')


class TestPerformanceRegression:
    """
    Testes para detectar regressões de performance.
    """
    
    @pytest.mark.performance
    def test_consolidate_time_limit(self, performance_dataframe):
        """
        Verifica se consolidação não ultrapassa tempo limite.
        """
        import time
        
        columns = ['Item', 'Descrição', 'Quantidade', 'Valor']
        
        start_time = time.time()
        result = consolidate_broken_rows(performance_dataframe, columns)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Limite de 5 segundos para 5000 linhas
        assert execution_time < 5.0
        assert isinstance(result, pd.DataFrame)
    
    @pytest.mark.performance
    def test_remove_headers_time_limit(self, dataframe_with_many_duplicates):
        """
        Verifica se remoção de headers não ultrapassa tempo limite.
        """
        import time
        
        columns = ['Item', 'Descrição', 'Quantidade', 'Valor']
        
        start_time = time.time()
        result = remove_duplicate_headers(dataframe_with_many_duplicates, columns)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        # Limite de 2 segundos para 1000 linhas com duplicatas
        assert execution_time < 2.0
        assert isinstance(result, pd.DataFrame)