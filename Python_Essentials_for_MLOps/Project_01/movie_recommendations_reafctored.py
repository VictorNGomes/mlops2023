import requests
import zipfile
import pandas as pd
import os
import logging
import pandas as pd
import re
import numpy as np
from IPython.display import display
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Configuração do logging
import logging
log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s")

# Configuração do logging
log_file = 'recommendation.log'
log_handler = logging.FileHandler(log_file)
log_handler.setFormatter(log_formatter)
logger = logging.getLogger()
logger.addHandler(log_handler)
logger.setLevel(logging.INFO)


# URL do arquivo ZIP
zip_url = "https://files.grouplens.org/datasets/movielens/ml-25m.zip"

# Nome dos arquivos CSV que você deseja extrair
csv_files = ["movies.csv", "ratings.csv"]

# Diretório onde você deseja salvar os arquivos CSV extraídos
output_directory = "./movielens_data/"

# Função para fazer o download e extrair os arquivos CSV
def create_output_directory(output_directory):
    try:
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
            logging.info(f"Diretório '{output_directory}' criado com sucesso.")
        else:
            logging.info(f"Diretório '{output_directory}' já existe.")

        return True

    except Exception as e:
        logging.error(f"Erro ao criar o diretório de saída: {str(e)}")
        return False

# Função para fazer o download do arquivo ZIP
def download_zip(zip_url, output_directory):
    try:
        response = requests.get(zip_url)
        with open(os.path.join(output_directory, "movielens_data.zip"), "wb") as zip_file:
            zip_file.write(response.content)
        logging.info("Download do arquivo ZIP concluído com sucesso.")
        return True

    except Exception as e:
        logging.error(f"Erro ao fazer o download do arquivo ZIP: {str(e)}")
        return False

# Função para extrair arquivos CSV do ZIP
def extract_csv_files(output_directory):
    try:
        with zipfile.ZipFile(os.path.join(output_directory, "movielens_data.zip"), "r") as zip_ref:
            zip_ref.extractall(output_directory)
        logging.info("Arquivos CSV extraídos com sucesso.")
        return True

    except Exception as e:
        logging.error(f"Erro ao extrair arquivos CSV do ZIP: {str(e)}")
        return False

# Função para carregar os arquivos CSV em DataFrames
def load_data(csv_files, output_directory):
    try:
        data = {}
        for file_name in csv_files:
            file_path = os.path.join(output_directory+"/ml-25m", file_name)
            data[file_name.split(".")[0]] = pd.read_csv(file_path)
        logging.info("Dados carregados com sucesso.")
        return data

    except Exception as e:
        logging.error(f"Erro ao carregar os dados CSV: {str(e)}")
        return None

# Função principal que chama as etapas
def download_and_extract_data(zip_url, csv_files, output_directory):
    if create_output_directory(output_directory):
        if download_zip(zip_url, output_directory):
            if extract_csv_files(output_directory):
                return load_data(csv_files, output_directory)
    
    return None

def clean_title(title):
    title = re.sub("[^a-zA-Z0-9 ]", "", title)
    return title

# Chama a função para baixar e extrair os dados
data = download_and_extract_data(zip_url, csv_files, output_directory)

try:
    if data:
        movies = data["movies"]
        ratings = data["ratings"]
        movies["clean_title"] = movies["title"].apply(clean_title) 
        vectorizer = TfidfVectorizer(ngram_range=(1,2))
        tfidf = vectorizer.fit_transform(movies["clean_title"])

        # Agora você pode usar os DataFrames movies_df e ratings_df para trabalhar com os dados.
        # Por exemplo, você pode imprimir as primeiras linhas de cada DataFrame:

        print("Primeiras linhas do DataFrame 'movies':")
        print(movies.head())

        print("\nPrimeiras linhas do DataFrame 'ratings':")
        print(ratings.head())
        
except Exception as e:
    logging.error(f"Erro ao carregar os dados: {str(e)}")

# Função para limpar o título


# Função para realizar a pesquisa com base no título
def search(title):
    try:
        title = clean_title(title)
        query_vec = vectorizer.transform([title])
        similarity = cosine_similarity(query_vec, tfidf).flatten()
        indices = np.argpartition(similarity, -5)[-5:]
        results = movies.iloc[indices].iloc[::-1]
        return results
    except Exception as e:
        logging.error(f"Erro na pesquisa: {str(e)}")
        return pd.DataFrame()

# Função para encontrar filmes similares
def find_similar_movies(movie_id):
    try:
        similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()
        similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]
        similar_user_recs = similar_user_recs.value_counts() / len(similar_users)

        similar_user_recs = similar_user_recs[similar_user_recs > 0.10]
        all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] > 4)]
        all_user_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())
        rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
        rec_percentages.columns = ["similar", "all"]

        rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
        rec_percentages = rec_percentages.sort_values("score", ascending=False)
        return rec_percentages.head(10).merge(movies, left_index=True, right_on="movieId")[["score", "title", "genres"]]
    except Exception as e:
        logging.error(f"Erro ao encontrar filmes similares: {str(e)}")
        return pd.DataFrame()




"""movie_input = widgets.Text(
    value='Toy Story',
    description='Movie Title:',
    disabled=False
)
movie_list = widgets.Output()

def on_type(data):
    with movie_list:
        movie_list.clear_output()
        title = data["new"]
        if len(title) > 5:
            results = search(title)
            if not results.empty:
                display(results)

movie_input.observe(on_type, names='value')

display(movie_input, movie_list)

movie_name_input = widgets.Text(
    value='Toy Story',
    description='Movie Title:',
    disabled=False
)
recommendation_list = widgets.Output()

def on_type_recommendation(data):
    with recommendation_list:
        recommendation_list.clear_output()
        title = data["new"]
        if len(title) > 5:
            results = search(title)
            if not results.empty:
                movie_id = results.iloc[0]["movieId"]
                recommendations = find_similar_movies(movie_id)
                if not recommendations.empty:
                    display(recommendations)

movie_name_input.observe(on_type_recommendation, names='value')

display(movie_name_input, recommendation_list)"""

def on_type():
    
    title = "Toy Story "
    if len(title) > 5:
        results = search(title)
        if not results.empty:
            print(results)

on_type()