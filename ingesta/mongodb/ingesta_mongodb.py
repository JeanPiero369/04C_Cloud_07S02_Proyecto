import pymongo
import boto3
import pandas as pd

# Configuración de la base de datos MongoDB
mongo_config = {
    'host': 'mongodb://18.206.168.84:27017/',  # Cambia con la IP y el puerto de tu servidor MongoDB
    'database': 'universidad',                 # Cambia con el nombre de tu base de datos
    'collection': 'alumnos'                    # Cambia con el nombre de la colección
}

# Conexión a la base de datos MongoDB
client = pymongo.MongoClient(mongo_config['host'])
db = client[mongo_config['database']]
collection = db[mongo_config['collection']]

# Consulta de los datos
data = list(collection.find())  # Consulta todos los documentos de la colección

# Carga de datos en un DataFrame de pandas
df = pd.DataFrame(data)

# Guardar el DataFrame en un archivo CSV
ficheroUpload = "data_mongodb.csv"
df.to_csv(ficheroUpload, index=False)

# Subir a S3
nombreBucket = "04c-cloud-05s03-ingesta-from-database"
s3 = boto3.client('s3')
response = s3.upload_file(ficheroUpload, nombreBucket, ficheroUpload)

print("Ingesta desde MongoDB completada")

# Cierre de la conexión
client.close()
