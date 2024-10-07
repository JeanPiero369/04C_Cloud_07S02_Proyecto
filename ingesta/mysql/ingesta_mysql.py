import os
import mysql.connector
import boto3
import pandas as pd

# Configuración de la base de datos MySQL desde variables de entorno
db_config = {
    'host': os.environ.get('MYSQL_HOST'),
    'port': int(os.environ.get('MYSQL_PORT')),
    'user': os.environ.get('MYSQL_USER'),
    'password': os.environ.get('MYSQL_PASSWORD'),
    'database': os.environ.get('MYSQL_DATABASE')
}

# Conexión a la base de datos MySQL
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Función para extraer datos y guardarlos en CSV
def export_to_csv(query, filename):
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    
    # Excluir el primer campo (encabezado)
    if len(columns) > 0:
        columns = columns[1:]  # Excluir el primer encabezado
        data = [row[1:] for row in data]  # Excluir el primer campo de cada fila

    df = pd.DataFrame(data, columns=columns)
    df.to_csv(filename, index=False)
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
