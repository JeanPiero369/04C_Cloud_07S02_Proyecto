import mysql.connector
import psycopg2
from pymongo import MongoClient
import pandas as pd
import os 

# ================== Cargar datos en MySQL ==================
def load_data_mysql():
    try:
        # Conexión a MySQL
        connection = mysql.connector.connect(
            host=os.environ.get('MYSQL_HOST'),
            port=int(os.environ.get('MYSQL_PORT')),
            user=os.environ.get('MYSQL_USER'),  # Cambia esto a tu usuario de MySQL
            password=os.environ.get('MYSQL_PASSWORD'),  # Cambia esto a tu contraseña de MySQL
            database=os.environ.get('MYSQL_DATABASE')
        )
        cursor = connection.cursor()

        # Habilitar el uso de archivos locales en MySQL
        cursor.execute("SET GLOBAL local_infile = 1;")

        # Cargar datos de personas
        query_personas = """
        LOAD DATA LOCAL INFILE './data/generated_data/persona_generated.csv'
        INTO TABLE Persona
        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 ROWS
        (id_persona, nombre, apellido, email, telefono);
        """
        cursor.execute(query_personas)

        # Cargar datos de especialidades
        query_especialidades = """
        LOAD DATA LOCAL INFILE './data/generated_data/especialidades_generated.csv'
        INTO TABLE Especialidad
        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 ROWS
        (id_especialidad, nombre_especialidad);
        """
        cursor.execute(query_especialidades)

        # Cargar datos de clientes
        query_clientes = """
        LOAD DATA LOCAL INFILE './data/generated_data/clientes_generated.csv'
        INTO TABLE Cliente
        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 ROWS
        (id_persona, direccion, DNI);
        """
        cursor.execute(query_clientes)

        # Cargar datos de agentes
        query_agentes = """
        LOAD DATA LOCAL INFILE './data/generated_data/agentes_generated.csv'
        INTO TABLE Agente
        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        IGNORE 1 ROWS
        (id_persona, direccion_oficina, id_especialidad);
        """
        cursor.execute(query_agentes)

        connection.commit()
        print("Datos cargados correctamente en las tablas de MySQL.")
    except Exception as e:
        print(f"Error al cargar datos en MySQL: {e}")
    finally:
        cursor.close()
        connection.close()

# ================== Cargar datos en PostgreSQL ==================
def load_data_seguros_postgresql():
    try:
        connection = psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST'),
            port=int(os.environ.get('POSTGRES_PORT')),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            database=os.environ.get('POSTGRES_DB')
        )

        cursor = connection.cursor()

        # Cargar polizas
        polizas_df = pd.read_csv('./data/generated_data/polizas_generated.csv')
        for _, row in polizas_df.iterrows():
            cursor.execute(
                "INSERT INTO polizas (idPoliza, idCliente, idAgente, fechaInicio, fechaFin, prima) VALUES (%s, %s, %s, %s, %s, %s)",
                (row['idPoliza'], row['idCliente'], row['idAgente'], row['fechaInicio'], row['fechaFin'], row['prima'])
            )

        # Cargar seguros
        seguros_df = pd.read_csv('./data/generated_data/seguros_generated.csv')
        for _, row in seguros_df.iterrows():
            cursor.execute(
                "INSERT INTO seguros (idSeguro, nombreSeguro, descripcion, tipoSeguro, idPoliza, monto) VALUES (%s, %s, %s, %s, %s, %s)",
                (row['idSeguro'], row['nombreSeguro'], row['descripcion'], row['tipo'], row['idPoliza'], row['monto'])
            )

        connection.commit()
        print("Datos cargados correctamente en las tablas 'polizas' y 'seguros' de PostgreSQL.")
    except Exception as e:
        print(f"Error al cargar datos en PostgreSQL: {e}")
    finally:
        cursor.close()
        connection.close()

# ================== Cargar datos en MongoDB ==================
def load_data_bienes_mongodb():
    try:
        # Conexión a MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client['bienes']  # Cambia esto a tu base de datos de MongoDB
        bienes_collection = db['bienes']  # Cambia esto a tu colección de MongoDB

        # Cargar el CSV en pandas
        bienes_df = pd.read_csv('./data/generated_data/bienes_generated.csv')

        # Convertir el DataFrame a un diccionario para inserción en MongoDB
        bienes_dict = bienes_df.to_dict("records")

        # Inserción masiva en MongoDB
        bienes_collection.insert_many(bienes_dict)
        print(f"{len(bienes_dict)} registros insertados en MongoDB.")
    except Exception as e:
        print(f"Error al cargar datos en MongoDB: {e}")

# ================== Ejecutar todas las funciones de carga ==================
def cargar_todos_los_datos():
    load_data_mysql()  # Cargar datos en MySQL
    load_data_seguros_postgresql()  # Cargar datos en PostgreSQL
    #load_data_bienes_mongodb()  # Cargar datos en MongoDB