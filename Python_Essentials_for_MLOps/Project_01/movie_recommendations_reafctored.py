import pandas as pd
import re
import logging
import unittest
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ipywidgets as widgets
from IPython.display import display



if __name__ == "__main__":
   

    # Function to search for movies
    def search(title):
        title = clean_title(title)
        query_vec = vectorizer.transform([title])
        similarity = cosine_similarity(query_vec, tfidf).flatten()
        indices = np.argpartition(similarity, -5)[-5:]
        results = movies.iloc[indices].iloc[::-1]
        return results

    # Function to find similar movies
    def find_similar_movies(movie_id):
        similar_users = ratings[(ratings["movieId"] == movie_id) & (ratings["rating"] > 4)]["userId"].unique()
        similar_user_recs = ratings[(ratings["userId"].isin(similar_users)) & (ratings["rating"] > 4)]["movieId"]
        similar_user_recs = similar_user_recs.value_counts() / len(similar_users)

        similar_user_recs = similar_user_recs[similar_user_recs > .10]
        all_users = ratings[(ratings["movieId"].isin(similar_user_recs.index)) & (ratings["rating"] > 4)]
        all_user_recs = all_users["movieId"].value_counts() / len(all_users["userId"].unique())
        rec_percentages = pd.concat([similar_user_recs, all_user_recs], axis=1)
        rec_percentages.columns = ["similar", "all"]

        rec_percentages["score"] = rec_percentages["similar"] / rec_percentages["all"]
        rec_percentages = rec_percentages.sort_values("score", ascending=False)
        return rec_percentages.head(10).merge(movies, left_index=True, right_on="movieId")[["score", "title", "genres"]]

    import ipywidgets as widgets
    from IPython.display import display

     # Load movies data
    movies = load_movies_data("./ml-25m/movies.csv")
    
    # Load ratings data
    ratings = pd.read_csv("./ml-25m/ratings.csv")

    movie_input = widgets.Text(
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
                display(search(title))
        

    movie_input.observe(on_type, names='value')

    display(movie_input, movie_list)

    movie_id = 89745

    movie_name_input = widgets.Text(
        value='Toy Story',
        description='Movie Title:',
        disabled=False
    )
    recommendation_list = widgets.Output()

    def on_type(data):
        with recommendation_list:
            recommendation_list.clear_output()
            title = data["new"]
            if len(title) > 5:
                results = search(title)
                movie_id = results.iloc[0]["movieId"]
                display(find_similar_movies(movie_id))

    movie_name_input.observe(on_type, names='value')

    display(movie_name_input, recommendation_list)
