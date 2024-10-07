import os
import pymongo
import boto3
import json

# Configuración de la base de datos MongoDB desde variables de entorno
mongo_config = {
    'host': os.environ.get('MONGO_URI'),  # Cambia con la IP y el puerto de tu servidor MongoDB
    'database': os.environ.get('MONGO_DATABASE')          # Cambia con el nombre de tu base de datos
}

# Conexión a la base de datos MongoDB
client = pymongo.MongoClient(mongo_config['host'])
db = client[mongo_config['database']]

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
