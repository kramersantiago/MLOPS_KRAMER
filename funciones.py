# Importar librerias necesarias
import pandas as pd
import numpy as np
import ast
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import warnings
warnings.filterwarnings("ignore")

# Cargar las bases de datos
df_user_items = pd.read_parquet('Data/df_user_items.parquet')

df_user_reviews = pd.read_parquet('Data/df_user_reviews.parquet')

df_steam_games = pd.read_parquet('Data/df_steam_games.parquet')

df_games_specs = pd.read_parquet('Data/df_games_specs.parquet')

# -------------------------------------------------------------------------- Funcion developer --------------------------------------------------------------------- 


# Función para obtener el año
def release_year(release_date):
    try:
        return pd.to_datetime(release_date).year
    except (TypeError, ValueError):
        return None


df_steam_games = df_steam_games.rename(columns={'id': 'item_id'})

# Aplicar la función a la columna "release_date" y crear una nueva columna "release_year"
df_steam_games['release_year'] = df_steam_games['release_date'].apply(release_year).astype(pd.Int32Dtype(), errors='ignore')

def developer(desarrollador):
    # Filtrar el DataFrame para obtener solo las filas relacionadas con el developer
    df_developer = df_steam_games[df_steam_games['developer'] == desarrollador]

    # Calcula la cantidad de items por año
    items_per_year = df_developer.groupby(df_developer['release_date'].dt.year)['item_id'].count()
    items_per_year = items_per_year.astype(int)

    # Calcula la cantidad de items gratis por año
    free_items = df_developer[df_developer['price'] == 0].groupby(df_developer['release_date'].dt.year)['item_id'].count()

    # Calcula el porcentaje de items gratis por año
    free_content = (free_items.all() / items_per_year * 100).fillna(0).astype(int)
    
    # Formatea los años en el resultado
    items_per_year = {year: count for year, count in items_per_year.items()}
    free_content = {year: f"{value}%" for year, value in free_content.items()}
    
    result = {
        'Cantidad por año': f"{items_per_year}",
        'Porcentaje gratis por año': f"{free_content}"
    }
    
    return result

# -------------------------------------------------------------------------- Funcion userdata --------------------------------------------------------------------- 


df_user_items['item_id'] = df_user_items['item_id'].astype(pd.Int32Dtype())
df_user_reviews['item_id'] = df_user_reviews['item_id'].astype(pd.Int32Dtype())
df_steam_games['item_id'] = df_steam_games['item_id'].dropna().astype(pd.Int32Dtype())

def userdata(user_id):
    user_id = str(user_id)
    # Filtrar el DataFrame "user_items" para obtener solo las filas relacionadas con el usuario
    user = df_user_items[df_user_items['user_id'] == user_id]

    # Verificar si el usuario se encuentra en el DataFrame
    if user.empty:
        return pd.DataFrame()

    # Unir "user_items" con "steam_games" para obtener la información de precios
    df_items_merged = user.merge(df_steam_games, on='item_id', how='inner')

    # Calcular la cantidad de dinero gastado por el usuario
    spent_money = df_items_merged['price'].sum()
    spent_money = f"${spent_money:.2f} USD"

    # Unir "user_items" con "user_reviews" para obtener la información de recomendación
    df_reviews_merged = pd.merge(user, df_user_reviews, on='item_id', how='inner')

    # Calcular la cantidad de items y el porcentaje de recomendación en base a "recommend"
    items = len(df_reviews_merged)
    recommend_percentage = df_reviews_merged[df_reviews_merged['user_id_x'] == user_id]['recommend'].mean() * 100

    # Crear un DataFrame con los resultados
    resultados = {
        'Usuario': user_id,
        'Dinero gastado': spent_money,
        '% de recomendacion': recommend_percentage.round(2),
        'Cantidad de items': items,
    }

    return resultados

# -------------------------------------------------------------------------- Funcion UserForGenre --------------------------------------------------------------------- 


df_playtime = df_user_items[['user_id', 'item_id', 'playtime_forever']]

# Crear un DF que contenga las columas "item_id", "genres" y "release_year" y convertir las cadenas de valores en  "genres" a strings
df_genres = df_steam_games[['item_id', 'genres', 'release_year']]

def parse_genres(x):
    try:
        return ast.literal_eval(x) if pd.notna(x) else None
    except (SyntaxError, ValueError):
        return None

df_genres['genres'] = df_genres['genres'].apply(parse_genres)
df_genres = df_genres.explode('genres')

# Unir los DF
df_genres_playtime = df_genres.merge(df_playtime, on='item_id', how='right')

# Crear un DF que contenga las columnas "item_id", "genres" y "release_year" y convertir las cadenas de valores en  "genres" a strings
df_genres = df_steam_games[['item_id', 'genres', 'release_year']]

def safe_literal_eval(x):
    try:
        return ast.literal_eval(x)
    except (SyntaxError, ValueError):
        return None

df_genres = df_genres.explode('genres')

df_playtime = df_user_items[['user_id', 'item_id', 'playtime_forever']]

# Unir los DF
df_genres_playtime = df_genres.merge(df_playtime, on='item_id', how='right')

def UserForGenre(genero):

    # Eliminar filas donde el user_id sea un valor nulo
    df = df_genres_playtime.dropna(subset=['user_id'])

    # Filtrar los juegos por el genero dado
    genre = df[df['genres'] == genero]

    # Encontrar al usuario con mas horas jugadas en el genero dado
    user_most_hours = genre.loc[genre['playtime_forever'].idxmax()]['user_id']
    print(user_most_hours)
    # Filtrar el DataFrame para obtener solo las filas relacionadas con el usuario que acumula más horas
    df_user_most_hours = genre.groupby('release_year')['playtime_forever'].sum().reset_index()

    # DF que acumula las horas jugadas por año de lanzamiento
    playtime_years = df_user_most_hours[['release_year', 'playtime_forever']]

    result = {
        'Usuario con mas horas jugadas para el genero dado': user_most_hours,
        'Horas jugadas': [{'Año': int(row['release_year']), 'Horas': int(row['playtime_forever'])} for _, row in playtime_years.iterrows()]
    }
    
    return result

# -------------------------------------------------------------------------- Funcion best_developer_year --------------------------------------------------------------------- 

# Crear un DF que cuente la cantidad de reviews positivas hechas por los usuarios a la desarrolladora
df_merged_reviews = pd.merge(df_user_reviews, df_steam_games, on='item_id', how='left')
df_merged_reviews = df_merged_reviews.loc[(df_merged_reviews['recommend'] == False) & (df_merged_reviews['sentiment_analysis'] == 0), ['release_year', 'developer']]
df_merged_reviews = df_merged_reviews.groupby(['release_year', 'developer']).size().reset_index(name='reviews')
df_merged_reviews = df_merged_reviews.sort_values(by=['release_year', 'reviews'], ascending=[False, False])
df_merged_reviews = df_merged_reviews.groupby('release_year').head(3)

def best_developer_year(year):
    # Filtrar el DF para obtener las filas relacionadas con el año dado
    top_3 = df_merged_reviews[df_merged_reviews['release_year'] == year]

    # Devolver los resultados de las 3 desarrolladoras con mas reviews positivas
    result = [
        {"Puesto 1": top_3.iloc[0]['developer']},
        {"Puesto 2": top_3.iloc[1]['developer']},
        {"Puesto 3": top_3.iloc[2]['developer']}
        ]
    
    return result
df_reviews = df_user_reviews [['sentiment_label', 'item_id']]

df_developer = df_steam_games[['developer', 'item_id']]

df_reviews_analysis = df_developer.merge(df_reviews, on= 'item_id', how= 'right')

# -------------------------------------------------------------------------- Funcion developer_reviews_analysis --------------------------------------------------------------------- 

def developer_reviews_analysis(desarrolladora):
    # Filtrar el DataFrame df_merged_reviews para las reseñas del desarrollador proporcionado.
    developer_reviews = df_reviews_analysis[df_reviews_analysis['developer'] == desarrolladora]

    # Utilizar la función groupby para agrupar por 'sentiment_analysis' y contar el número de registros.
    sentiment_counts = developer_reviews.groupby('sentiment_label').size().reset_index(name='count')

    # Crear un diccionario con el nombre del desarrollador como clave y una lista con la cantidad de reseñas positivas y negativas.
    result = {
        desarrolladora: [
            f"Negative = {sentiment_counts.loc[sentiment_counts['sentiment_label'] == 0, 'count'].values[0]}",
            f"Positive = {sentiment_counts.loc[sentiment_counts['sentiment_label'] == 2, 'count'].values[0]}"
        ]
    }

    return result

# -------------------------------------------------------------------------- Funcion recomendacion_juego --------------------------------------------------------------------- 


def recomendacion_juego(item_id):
    item_id = str(item_id)
    
    # Filtrar el DF en base al "item_id"
    df = df_games_specs[df_games_specs['item_id'] == item_id]
    
    # Devolver la lista de "recommends"
    result = df['recommends'].iloc[0]
    
    # Asegurarse de que result sea una lista plana
    if isinstance(result, np.ndarray):
        result = result.tolist()
    elif not isinstance(result, list):
        result = [result]
 
    return result