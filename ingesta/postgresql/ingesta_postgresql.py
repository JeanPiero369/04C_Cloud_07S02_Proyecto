import psycopg2
import boto3
import pandas as pd

# Configuración de la base de datos PostgreSQL
db_config = {
    'host': '18.206.168.84',  # Cambia esto con tu host de la base de datos
    'port': 5432,              # Cambia esto con el puerto de tu base de datos (por defecto 5432)
    'user': 'tu_usuario',      # Cambia esto con tu usuario de la base de datos
    'password': 'tu_contraseña',  # Cambia esto con tu contraseña de la base de datos
    'database': 'universidad'  # Cambia esto con el nombre de tu base de datos
}

# Conexión a la base de datos PostgreSQL
connection = psycopg2.connect(**db_config)
cursor = connection.cursor()

# Consulta de los datos
query = "SELECT * FROM alumnos;"  # Cambia 'alumnos' por el nombre de la tabla que deseas consultar
cursor.execute(query)

# Carga de datos en un DataFrame de pandas
data = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
df = pd.DataFrame(data, columns=columns)

# Guardar el DataFrame en un archivo CSV
ficheroUpload = "data_postgresql.csv"
df.to_csv(ficheroUpload, index=False)

# Subir a S3
nombreBucket = "04c-cloud-05s03-ingesta-from-database"
s3 = boto3.client('s3')
response = s3.upload_file(ficheroUpload, nombreBucket, ficheroUpload)

print("Ingesta desde PostgreSQL completada")

# Cierre de la conexión
cursor.close()
connection.close()
