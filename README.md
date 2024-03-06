MLOps: Proyecto Individual 1
=============

### Descripción del Proyecto

Logros Destacados
En el marco de este proyecto, se ha logrado la creación exitosa de un Producto Mínimo Viable (MVP), introduciendo una API implementada en una infraestructura en la nube y la aplicación de un modelo de **Machine Learning**. La iniciativa, que simula las responsabilidades combinadas de un **Ingeniero de MLOps**, fusiona habilidades de **Ingeniería de Datos** y **Ciencia de Datos** para satisfacer las necesidades de la plataforma multinacional de videojuegos, Steam.

Enfoque Estratégico
El enfoque estratégico se centró en realizar un análisis de sentimientos sobre los comentarios de los usuarios de juegos, además de proporcionar recomendaciones de juegos a partir del nombre de un juego y/o los gustos específicos de un usuario.

Caso de Negocio Real
El proyecto se basó en el desarrollo de un caso de negocio real, aprovechando conjuntos de datos públicos de la industria de videojuegos para lograr un análisis significativo.

<br/>

**Datos**

Se nos asignaron 3 archivos JSON los cuáles fueron utilizados para este proyecto:
- australian_user_reviews.json: este archivo contiene las reviews de los usuarios sobre juegos.
- australian_users_items.json: este archivo contiene información de los usuarios, como la cantidad de horas jugadas y los artículos en su posesión..
- output_steam_games.json: este archivo contiene información de los juegos disponibles en Steam, tales como su nombre, género, etc.

<br/>

### 1. Data Engineering: ETL

- australian_user_reviews.json: Se llevó a cabo su ETL en el archivo de Jupyter Notebook ETL_user_reviews para posteriormente exportarlo en un archivo parquet con el fin de reducir el tamaño del archivo final: df_user_reviews.parquet.
- australian_users_items.json: Se llevó su ETL en el Jupyter Notebook ETL_user_items y luego se exportó al archivo parquet df_user_items.parquet.
- output_steam_games.json: El proceso de ETL se ve reflejado en el Jupyter Notebook ETL_steam_games y finalmente se exportó al archivo df_steam_games.parquet.
<br/>

**1.1. Feature Engineering**

Se creó la columna "sentiment_analysis" aplicando análisis de sentimiento con NLP con la siguiente escala: toma el valor '0' si es malo, '1' si es neutral o si la reseña no está escrita y '2' si es positivo.

<br/>

### 2. API

Se utilizó el framework FastAPI para crear la API y finalmente se la deployó utilizando Render. Este puede ser accedido en este [enlace](https://mlops-kramer.onrender.com/docs). Esta misma cuenta con 6 endpoints los cuales se detallan a continuación:
- Endpoint developer(developer): Devuelve la cantidad de items y porcentaje de contenido gratuito por año según la empresa desarrolladora.
- Endpoint userdata(user_id): Devuelve la cantidad de dinero gastado por el usuario, el porcentaje de recomendación en base a la columna "recommend" y la cantidad de items.
- Endpoint userforgenre(genero): Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.
- Endpoint bestdeveloperyear(year): Devuelve el top 3 de desarrolladores con juegos más recomendados por usuarios para el año dado.
- Endpoint developerreviewsanalysis(developer): Devuelve un diccionario con el nombre del desarrollador ingresado como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.
- Endpoint recomendacionjuego(item_id): Ingresando el item_id, se devuelve una lista con 5 juegos recomendados similares al ingresado.

<br/>

### EDA

Se realizó un EDA con el fin de ver patrones en los datos que ayuden a la hora de realizar el modelo de Machine Learning para el sistema de recomendación de videojuegos.

<br/>

### 4. Modelo de Machine Learning

Se creó un modelo de ML el cual consiste en un sistema de recomendación ítem-ítem que recibe el item_id y devuelve 5 videojuegos similares al ingresado en base a la **similitud del coseno**. Utilicé la librería Scikit-Learn para el modelo, utilziando un CountVectorizer() para transformar los datos de la columna "specs" la cual contiene especificaciones de cada videojuego en vectores para calcular la similitud entre entos videojuegos.


