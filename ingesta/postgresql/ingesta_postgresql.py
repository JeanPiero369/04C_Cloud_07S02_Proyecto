import os
import psycopg2
import boto3
import pandas as pd

# Configuración de la base de datos PostgreSQL desde variables de entorno
db_config = {
    'host': os.environ.get('POSTGRES_HOST'),
    'port': int(os.environ.get('POSTGRES_PORT')),
    'user': os.environ.get('POSTGRES_USER'),
    'password': os.environ.get('POSTGRES_PASSWORD'),
    'dbname': os.environ.get('POSTGRES_DB')
}

# Conexión a la base de datos PostgreSQL
connection = psycopg2.connect(**db_config)
cursor = connection.cursor()

# Función para extraer datos y guardarlos en CSV
def export_to_csv(query, filename):
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    # Convertir a DataFrame sin modificar los datos
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(filename, index=False, header=False)  # No incluir encabezado
    print(f"Exported {filename}")

# Consultas para cada tabla
queries = {
    'Persona': "SELECT * FROM Persona;",
    'Cliente': "SELECT * FROM Cliente;",
    'Especialidad': "SELECT * FROM Especialidad;",
    'Agente': "SELECT * FROM Agente;"
}

# Exportar cada tabla a un archivo CSV
for table_name, query in queries.items():
    export_to_csv(query, f"{table_name}.csv")

# Subir archivos CSV a S3
nombreBucket = os.environ.get('S3_BUCKET', 'nombre_por_defecto_bucket')  # Cambia esto al nombre de tu bucket de S3
s3 = boto3.client('s3')

for table_name in queries.keys():
    ficheroUpload = f"{table_name}.csv"
    # Especificar la ruta en el bucket
    s3.upload_file(ficheroUpload, nombreBucket, f"{table_name}/{ficheroUpload}")
    print(f"Uploaded {ficheroUpload} to S3 under {table_name}/")

# Cierre de la conexión
cursor.close()
connection.close()
