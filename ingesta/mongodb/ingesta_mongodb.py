import os
from pymongo import MongoClient
import boto3
import json

# Conexión a la base de datos MongoDB
#  Obtener la URI de MongoDB y el nombre de la base de datos de las variables de entorno
mongo_host = os.environ.get("MONGODB_HOST")  # Cambia a tu host de MongoDB
mongo_port = os.environ.get("MONGODB_PORT")       # Cambia a tu puerto de MongoDB
mongo_db = os.environ.get("MONGODB_DATABASE")  # Cambia a tu base de datos MongoDB

# Crear la URI de conexión
mongo_uri = f"mongodb://{mongo_host}:{mongo_port}/"

client = MongoClient(mongo_uri)
db = client[mongo_db]  # Nombre de la base de datos
collection = db[mongo_db]

# Obtener todas las colecciones en la base de datos
collections = db.list_collection_names()

# Configuración de S3 desde variables de entorno
nombreBucket = os.environ.get('S3_BUCKET', '04c-cloud-05s03-ingesta-from-database')
s3 = boto3.client('s3')

for collection_name in collections:
    collection = db[collection_name]
    # Consulta de los datos
    data = list(collection.find())  # Consulta todos los documentos de la colección

    # Guardar los datos en un archivo JSON
    json_filename = f"{collection_name}.json"
    with open(json_filename, 'w') as json_file:
        json.dump(data, json_file, default=str)  # Se utiliza default=str para tipos de datos no serializables
    
    # Subir el archivo JSON a S3
    s3.upload_file(json_filename, nombreBucket, f"{collection_name}/{json_filename}")
    print(f"Uploaded {json_filename} to S3 under {collection_name}/")

# Cierre de la conexión
client.close()
