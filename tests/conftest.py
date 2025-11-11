"""
Configuração global para todos os testes do projeto.
Define fixtures reutilizáveis e configurações compartilhadas.
"""
import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path
from faker import Faker
from unittest.mock import Mock, MagicMock

# Configurar faker para dados consistentes
fake = Faker(['pt_BR'])
Faker.seed(42)


@pytest.fixture
def sample_dataframe():
    """
    Fixture que retorna um DataFrame de exemplo para testes.
    """
    return pd.DataFrame({
        'Item': ['001', '002', '003', 'nan', '004'],
        'Descrição': ['Produto A', 'Produto B', 'Produto C', 'continuação', 'Produto D'],
        'Quantidade': [10, 20, 30, None, 40],
        'Valor': [100.0, 200.0, 300.0, None, 400.0]
    })


@pytest.fixture
def dataframe_with_duplicates():
    """
    DataFrame com cabeçalhos duplicados para testar remoção.
    """
    data = {
        'Item': ['Item', '001', '002', 'Item', '003'],
        'Descrição': ['Descrição', 'Produto A', 'Produto B', 'Descrição', 'Produto C'],
        'Quantidade': ['Quantidade', '10', '20', 'Quantidade', '30'],
        'Valor': ['Valor', '100.0', '200.0', 'Valor', '300.0']
    }
    return pd.DataFrame(data)


@pytest.fixture
def dataframe_with_broken_rows():
    """
    DataFrame com linhas quebradas para testar consolidação.
    """
    return pd.DataFrame({
        'Item': ['001', 'nan', '002', 'nan', '003'],
        'Descrição': ['Produto com nome muito', 'longo que foi quebrado', 'Produto B', 'segunda linha', 'Produto C'],
        'Quantidade': [10, None, 20, None, 30],
        'Valor': [100.0, None, 200.0, None, 300.0]
    })


@pytest.fixture
def empty_dataframe():
    """
    DataFrame vazio para testes de edge cases.
    """
    return pd.DataFrame()


@pytest.fixture
def large_dataframe():
    """
    DataFrame grande para testes de performance.
    """
    fake = Faker()
    Faker.seed(42)
    
    data = {
        'Item': [f'{i:03d}' for i in range(1, 1001)],
        'Descrição': [fake.text(max_nb_chars=50) for _ in range(1000)],
        'Quantidade': [fake.random_int(1, 100) for _ in range(1000)],
        'Valor': [fake.pyfloat(left_digits=3, right_digits=2, positive=True) for _ in range(1000)]
    }
    return pd.DataFrame(data)


@pytest.fixture
def temp_pdf_file():
    """
    Cria um arquivo PDF temporário para testes.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        # Criar um PDF simples (seria melhor ter um PDF real para testes)
        tmp.write(b'%PDF-1.4\n%Test PDF content\nendobj\n%%EOF')
        tmp.flush()
        yield tmp.name
    os.unlink(tmp.name)


@pytest.fixture
def mock_camelot_tables():
    """
    Mock das tabelas retornadas pelo Camelot.
    """
    mock_table = Mock()
    mock_table.df = pd.DataFrame({
        'Item': ['001', '002', '003'],
        'Descrição': ['Produto A', 'Produto B', 'Produto C'],
        'Quantidade': ['10', '20', '30'],
        'Valor': ['100.0', '200.0', '300.0']
    })
    
    mock_tables = [mock_table]
    return mock_tables


@pytest.fixture
def mock_tabula_tables():
    """
    Mock das tabelas retornadas pelo Tabula.
    """
    return [pd.DataFrame({
        'Item': ['001', '002', '003'],
        'Descrição': ['Produto A', 'Produto B', 'Produto C'],
        'Quantidade': [10, 20, 30],
        'Valor': [100.0, 200.0, 300.0]
    })]


@pytest.fixture
def column_names():
    """
    Lista de nomes de colunas padrão para testes.
    """
    return ['Item', 'Descrição', 'Quantidade', 'Valor']


@pytest.fixture
def test_data_dir():
    """
    Diretório para arquivos de teste.
    """
    return Path(__file__).parent / "fixtures"


# Configurações do pytest
def pytest_configure(config):
    """
    Configurações globais do pytest.
    """
    config.addinivalue_line(
        "markers", "unit: marca testes unitários"
    )
    config.addinivalue_line(
        "markers", "integration: marca testes de integração"
    )
    config.addinivalue_line(
        "markers", "performance: marca testes de performance"
    )
    config.addinivalue_line(
        "markers", "ui: marca testes de interface"
    )


def pytest_collection_modifyitems(config, items):
    """
    Adiciona marcadores automáticos baseados na localização dos testes.
    """
    for item in items:
        # Adicionar marcadores baseados no path do teste
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)