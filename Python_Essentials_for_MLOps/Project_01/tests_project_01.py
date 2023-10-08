import os
import pytest
import zipfile
from unittest import mock
from movie_recommendations_reafctored import clean_title, create_output_directory, download_zip, extract_csv_files, load_data

# Função para criar um diretório temporário para testes
@pytest.fixture
def temp_directory(tmpdir):
    return str(tmpdir.mkdir("test_dir"))

# Teste para a função clean_title
def test_clean_title():
    dirty_title = "Movie_Title! With_Special Characters..."
    cleaned_title = clean_title(dirty_title)
    assert cleaned_title == "MovieTitle WithSpecial Characters"

# Teste para a função create_output_directory
def test_create_output_directory(temp_directory):
    output_directory = os.path.join(temp_directory, "output")
    
    # Verifica se o diretório é criado com sucesso
    assert create_output_directory(output_directory) == True
    assert os.path.exists(output_directory) == True
    
    # Verifica se o diretório já existe
    assert create_output_directory(output_directory) == True

# Teste para a função download_zip
def test_download_zip(temp_directory):
    output_directory = temp_directory
    zip_url = "https://example.com/test.zip"
    
    # Mock para simular o download
    with mock.patch('requests.get') as mock_get:
        mock_response = mock.Mock()
        mock_response.content = b'Test data'
        mock_get.return_value = mock_response
        
        # Verifica se o download é bem-sucedido
        assert download_zip(zip_url, output_directory) == True
        zip_file_path = os.path.join(output_directory, "movielens_data.zip")
        assert os.path.exists(zip_file_path) == True

# Teste para a função extract_csv_files
def test_extract_csv_files(temp_directory):
    output_directory = temp_directory
    
    # Cria um arquivo ZIP temporário
    zip_file_path = os.path.join(output_directory, "movielens_data.zip")
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        zipf.write(__file__, "testfile.txt")
    
    # Verifica se a extração é bem-sucedida
    assert extract_csv_files(output_directory) == True



if __name__ == '__main__':
    pytest.main()
