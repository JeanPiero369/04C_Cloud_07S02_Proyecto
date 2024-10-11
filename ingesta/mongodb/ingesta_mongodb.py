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

# Configuración de S3 desde variables de entorno
nombreBucket = os.environ.get('S3_BUCKET', '04c-cloud-05s03-ingesta-from-database')
s3 = boto3.client('s3')

# Consulta de todos los documentos de la colección
data = list(collection.find())  # Consulta todos los documentos de la colección

# Guardar los datos en un archivo JSON, con un documento por línea
json_filename = f"{mongo_db}.json"
with open(json_filename, 'w') as json_file:
    for idx, document in enumerate(data):
        if idx == 0:  # Omitir el primer documento
            continue
        json_file.write(json.dumps(document, default=str) + "\n")  # Escribe cada documento como una línea JSON

# Subir el archivo JSON a S3
s3.upload_file(json_filename, nombreBucket, f"{mongo_db}/{json_filename}")

# Cierre de la conexión
client.close()
