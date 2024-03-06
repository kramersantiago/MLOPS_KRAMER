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

**1. Data Engineering: ETL**

- australian_user_reviews.json: Se llevó a cabo su ETL en el archivo de Jupyter Notebook ETL_user_reviews para posteriormente exportarlo en un archivo parquet con el fin de reducir el tamaño del archivo final: df_user_reviews.parquet.
- australian_users_items.json: Se llevó su ETL en el Jupyter Notebook ETL_user_items y luego se exportó al archivo parquet df_user_items.parquet.
- output_steam_games.json: El proceso de ETL se ve reflejado en el Jupyter Notebook ETL_steam_games y finalmente se exportó al archivo df_steam_games.parquet.
<br/>

**1.1. Feature Engineering**

Se creó la columna "sentiment_analysis" aplicando análisis de sentimiento con NLP con la siguiente escala: toma el valor '0' si es malo, '1' si es neutral o si la reseña no está escrita y '2' si es positivo.

<br/>

**2. API**

Se utilizó el framework FastAPI para crear la API y finalmente se la deployó utilizando Render. Este puede ser accedido en este [enlace](https://mlops-kramer.onrender.com/docs)
