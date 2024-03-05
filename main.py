from fastapi import FastAPI
import funciones
from funciones import *

app = FastAPI()
# http://127.0.0.1:8000

#ruta_parquet = os.environ.get("archivos_parquet")
df_games_specs = pd.read_parquet('Data/df_games_specs.parquet')
# ---------------------------- Funcion developer ---------------------------- 

@app.get(path='/developer',
          description=""" 
    <html>
        <body style="background-color: #000000;">
            <h1 style="color: ffff00;">INSTRUCCIONES</h1>
            <h3 style="color: ffff00; font-family: 'Trebuchet MS';">
                1. Haga clic en "Try it out".<br>
                2. Ingrese el desarrollador en el cuadro debajo de "description".<br>
                3. Cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora.<br>
                4. Sugerencia de usuarios: Valve, Ubisoft, Rockstar Games.<br>
                5. Para cambiar de usuario, copie y pegue de las sugerencias y presione Execute nuevamente.
            </h3>         
        </body>
    </html>
    """,
         tags=["Consultas developer"])

def developer(desarrollador: str):
    result = funciones.developer(desarrollador)
    return result

# ---------------------------- Funcion userdata ---------------------------- 

@app.get(path = '/userdata',
          description=""" 
    <html>
        <body>
            <h1>INSTRUCCIONES</h1>
            <h3>
                1. Haga clic en "Try it out".<br>
                2. Ingrese el usuario en el cuadro debajo de "description".<br>
                3. Observe el dinero gastado por el usuario, el porcentaje de recomendación y la cantidad de items que tiene el mismo.<br>
                4. Sugerencia de usuarios: BrainsAccount, 76561197970982479, AVATAR715, tarjla.<br>
                5. Para cambiar de usuario, copie y pegue de las sugerencias y presione Execute nuevamente.
            </h3>         
        </body>
    </html>
    """,
         tags=["Consultas de userdata"])

def userdata(user_id: str):
    result = funciones.userdata(user_id)
    return result

# ---------------------------- Funcion UserForGenre ---------------------------- 

@app.get(path='/UserForGenre',
          description=""" 
    <html>
        <body style="background-color: #000000;">
            <h1 style="color: ffff00;">INSTRUCCIONES</h1>
            <h3 style="color: ffff00; font-family: 'Trebuchet MS';">
                1. Haga clic en "Try it out".<br>
                2. Ingrese el usuario en el cuadro debajo de "description".<br>
                3. El usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.<br>
                4. Sugerencia de usuarios: Action, Strategy, Simulation, Racing.<br>
                5. Para cambiar de usuario, copie y pegue de las sugerencias y presione Execute nuevamente.
            </h3>         
        </body>
    </html>
    """,
         tags=["Consultas UserForGenre"])

def UserForGenre(genero: str):
    result = funciones.UserForGenre(genero)
    return result

# ---------------------------- Funcion best_developer_year ---------------------------- 

@app.get(path='/best_developer_year',
          description=""" 
    <html>
        <body style="background-color: #000000;">
            <h1 style="color: ffff00;">INSTRUCCIONES</h1>
            <h3 style="color: ffff00; font-family: 'Trebuchet MS';">
                1. Haga clic en "Try it out".<br>
                2. Ingrese el desarrollador en el cuadro debajo de "description".<br>
                3. Devuelve el top 3 de desarrolladores con juegos MÁS recomendados por usuarios para el año dado<br>
                4. Ingrese un año para obtener el resultado.<br>
                5. Para cambiar de desarrollador, copie y pegue de las sugerencias y presione Execute nuevamente.
            </h3>         
        </body>
    </html>
    """,
         tags=["Consultas best_developer_year"])

def best_developer_year(year: int):
    result = funciones.best_developer_year(year)
    return result

# ---------------------------- Funcion developer_reviews_analysis ---------------------------- 

@app.get(path='/developer_reviews_analysis',
          description=""" 
    <html>
        <body style="background-color: #000000;">
            <h1 style="color: ffff00;">INSTRUCCIONES</h1>
            <h3 style="color: ffff00; font-family: 'Trebuchet MS';">
                1. Haga clic en "Try it out".<br>
                2. Ingrese el desarrollador en el cuadro debajo de "description".<br>
                3. Según el desarrollador, se devuelve un diccionario con el nombre del desarrollador como llave<br>
                   y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados<br> 
                   con un análisis de sentimiento como valor positivo o negativo.<br>
                4. Sugerencia de usuarios: Valve, Ubisoft, Rockstar Games.<br>
                5. Para cambiar de desarrollador, copie y pegue de las sugerencias y presione Execute nuevamente.
            </h3>         
        </body>
    </html>
    """,
         tags=["Consultas developer_reviews_analysis"])

def developer_reviews_analysis(desarrolladora: str):
    result = funciones.developer_reviews_analysis(desarrolladora)
    return result

# ---------------------------- Funcion recomendacion_juego ---------------------------- 

@app.get(path='/recomendacion_juego',
          description=""" 
    <html>
        <body style="background-color: #000000;">
            <h1 style="color: ffff00;">INSTRUCCIONES</h1>
            <h3 style="color: ffff00; font-family: 'Trebuchet MS';">
                1. Haga clic en "Try it out".<br>
                2. Ingrese el desarrollador en el cuadro debajo de "description".<br>
                3. Ingresando el id de producto, deberíamos recibir una lista con 5 juegos recomendados similares al ingresado.<br>
                4. Sugerencia de id de producto: 761140, 643980, 670290.<br>
                5. Para cambiar de juego, copie y pegue de las sugerencias y presione Execute nuevamente.
            </h3>         
        </body>
    </html>
    """,
         tags=["Consultas recomendacion_juego"])

def recomendacion_juego(item_id: str):
    result = funciones.recomendacion_juego(item_id)
    return {'result': result}