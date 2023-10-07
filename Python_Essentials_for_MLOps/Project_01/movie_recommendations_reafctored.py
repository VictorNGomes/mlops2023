"""
O módulo 'zipfile' permite trabalhar com arquivos compactados no formato ZIP.
Ele fornece classes e métodos para criar, ler, escrever e extrair arquivos ZIP.
"""
import zipfile
import os
import logging
import re
import requests
import pandas as pd

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s")

# Configuração do logging
LOG_FILE = 'recommendation.log'
log_handler = logging.FileHandler(LOG_FILE)
log_handler.setFormatter(log_formatter)
logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)


# URL do arquivo ZIP
ZIP_URL = "https://files.grouplens.org/datasets/movielens/ml-25m.zip"

# Nome dos arquivos CSV que você deseja extrair
csv_files = ["movies.csv", "ratings.csv"]

# Diretório onde você deseja salvar os arquivos CSV extraídos
OUTPUT_DIRECTORY = "./movielens_data/"

vectorizer = TfidfVectorizer(ngram_range=(1,2))

# Função para fazer o download e extrair os arquivos CSV
def create_output_directory(output_directory):
    """
    Cria o diretório de saída se ele não existir.

    Args:
        output_directory (str): O caminho para o diretório de saída.

    Returns:
        bool: True se o diretório foi criado com sucesso ou já existia, False em caso de erro.
    """
    try:
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
            logging.info("Diretório '%s' criado com sucesso.",output_directory)
        else:
            logging.info("Diretório '%s' já existe.",output_directory)

        return True

    except OSError as err:
        logging.error("Erro ao criar o diretório de saída: %s",err)
        return False

# Função para fazer o download do arquivo ZIP
def download_zip(zip_url, output_directory):
    """
    Faz o download do arquivo ZIP se ele não existir no diretório de saída.

    Args:
        zip_url (str): A URL do arquivo ZIP a ser baixado.
        output_directory (str): O caminho para o diretório de saída.

    Returns:
        bool: True se o download foi bem-sucedido ou o arquivo já existe, False em caso de erro.
    """
    zip_file_path = os.path.join(output_directory, "movielens_data.zip")

    # Verifica se o arquivo ZIP já existe no diretório de saída
    if os.path.exists(zip_file_path):
        logging.info("O arquivo ZIP já existe. Não é necessário fazer o download novamente.")
        return True

    try:
        response = requests.get(zip_url,timeout=10)
        with open(zip_file_path, "wb") as zip_file:
            zip_file.write(response.content)
        logging.info("Download do arquivo ZIP concluído com sucesso.")
        return True

    except FileNotFoundError as err:
        logging.error("Erro ao fazer o download do arquivo ZIP: %s",err)
        return False

# Função para extrair arquivos CSV do ZIP
def extract_csv_files(output_directory):
    """
    Extrai arquivos CSV do arquivo ZIP.

    Args:
        output_directory (str): O caminho para o diretório de saída.

    Returns:
        bool: True se a extração foi bem-sucedida, False em caso de erro.
    """
    try:
        with zipfile.ZipFile(os.path.join(output_directory, "movielens_data.zip"), "r") as zip_ref:
            zip_ref.extractall(output_directory)
        logging.info("Arquivos CSV extraídos com sucesso.")
        return True

    except FileExistsError as err:
        logging.error("Erro ao extrair arquivos CSV do ZIP: %s",err)
        return False

# Função para carregar os arquivos CSV em DataFrames
def load_data(csv_path, output_directory):
    """
    Carrega os arquivos CSV em DataFrames do pandas.

    Args:
        csv_files (list): Lista de nomes de arquivos CSV.
        output_directory (str): O caminho para o diretório de saída.

    Returns:
        dict: Um dicionário contendo DataFrames com os dados carregados.
    """
    try:
        data = {}
        for file_name in csv_path:
            file_path = os.path.join(output_directory+"/ml-25m", file_name)
            data[file_name.split(".", maxsplit=1)[0]] = pd.read_csv(file_path)
        logging.info("Dados carregados com sucesso.")
        return data

    except FileExistsError as err:
        logging.error("Erro ao carregar os dados CSV: %s",err)
        return None

# Função principal que chama as etapas
def download_and_extract_data(zip_url, csv_files, output_directory):
    """
    Função principal que baixa, extrai e carrega os dados.

    Args:
        zip_url (str): A URL do arquivo ZIP a ser baixado.
        csv_files (list): Lista de nomes de arquivos CSV.
        output_directory (str): O caminho para o diretório de saída.

    Returns:
        dict: Um dicionário contendo DataFrames com os dados carregados.
    """
    if create_output_directory(output_directory):
        if download_zip(zip_url, output_directory):
            if extract_csv_files(output_directory):
                return load_data(csv_path=csv_files, output_directory=output_directory)

    return None

def clean_title(title):
    """
    Limpa o título do filme removendo caracteres especiais.

    Args:
        title (str): O título do filme.

    Returns:
        str: O título limpo.
    """
    title = re.sub("[^a-zA-Z0-9 ]", "", title)
    return title

# Chama a função para baixar e extrair os dados
data = download_and_extract_data(ZIP_URL, csv_files, OUTPUT_DIRECTORY)


try:
    if data:
        movies = data["movies"]
        ratings = data["ratings"]
        movies["clean_title"] = movies["title"].apply(clean_title)


except Exception as err:
    logging.error("Erro ao carregar os dados: %s",err)

def vectorized_data():
    """
    Realiza a vetorização dos títulos de filmes.

    Returns:
        scipy.sparse.csr_matrix: A matriz de recursos TF-IDF dos títulos de filmes.
    """
    try:
        movies["clean_title"] = movies["title"].apply(clean_title)
        logging.info("Título limpo")
        tfidf = vectorizer.fit_transform(movies["clean_title"])
        logging.info("Títulos vetorizados")

        return tfidf
    except Exception as err:
        logging.error("Erro na limpeza do título e vetorização dos dados: %s",err)
        return None




# Função para realizar a pesquisa com base no título
def search(title):
    """
    Realiza a pesquisa de filmes com base no título.

    Args:
        title (str): O título do filme a ser pesquisado.

    Returns:
        pd.DataFrame: Um DataFrame contendo os resultados da pesquisa.
    """
    try:
        title = clean_title(title)
        tfidf = vectorized_data()
        query_vec = vectorizer.transform([title])
        similarity = cosine_similarity(query_vec, tfidf).flatten()
        indices = np.argpartition(similarity, -5)[-5:]
        results = movies.iloc[indices].iloc[::-1]
        return results
    except AssertionError as err:
        logging.error("Erro na pesquisa: %s",err)
        return pd.DataFrame()

# Função para encontrar filmes similares
def find_similar_movies(movie_id):
    """
    Encontra filmes similares com base no ID do filme.

    Args:
        movie_id (int): O ID do filme.

    Returns:
        pd.DataFrame: Um DataFrame contendo os filmes similares encontrados.
    """
    try:
        similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]\
        ["userId"].unique()
        similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & \
                                    (ratings["rating"] > 4)]["movieId"]
        similar_user_recs = similar_user_recs.value_counts() / len(similar_users)

        similar_user_recs = similar_user_recs[similar_user_recs > 0.10]
        all_users = ratings[(ratings["movieId"].\
                             isin(similar_user_recs.index)) & (ratings["rating"] > 4)]
        all_user_recs = all_users["movieId"].value_counts() / \
            len(all_users["userId"].unique())
        rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
        rec_percentages.columns = ["similar", "all"]

        rec_percentages["score"] = \
            rec_percentages["similar"] / rec_percentages["all"]
        rec_percentages = rec_percentages.sort_values("score", ascending=False)
        return rec_percentages.head(10)\
            .merge(movies, left_index=True, right_on="movieId")[["score", "title", "genres"]]
    except Exception as err:
        logging.error("Erro ao encontrar filmes similares: %s",err)
        return pd.DataFrame()


def on_type_recommendation():
    """
    Função para realizar uma pesquisa e recomendar filmes com base no título "Toy Story".
    """
    title = "Toy Story"
    if len(title) > 5:
        results = search(title)
        if not results.empty:
            movie_id = results.iloc[0]["movieId"]
            recommendations = find_similar_movies(movie_id)
            if not recommendations.empty:
                print(recommendations)

on_type_recommendation()
