import mysql.connector
import psycopg2
from pymongo import MongoClient
import os

# ================== Crear tablas en MySQL ==================
def create_mysql_tables():
    connection = None
    cursor = None
    try:
        # Conexión a MySQL
        connection = mysql.connector.connect(
            host=os.environ.get('MYSQL_HOST'),
            port=int(os.environ.get('MYSQL_PORT')),
            user=os.environ.get('MYSQL_USER'),  # Cambia esto a tu usuario de MySQL
            password=os.environ.get('MYSQL_PASSWORD'),  # Cambia esto a tu contraseña de MySQL
            allow_local_infile=True  
        )
        cursor = connection.cursor()

        database_name = os.environ.get('MYSQL_DATABASE')  # Cambia esto al nombre de la base de datos que deseas crear
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")

        # Ahora puedes conectarte a la base de datos recién creada
        connection.database = database_name

        # Crear las tablas en MySQL
        queries = [
            """
            CREATE TABLE IF NOT EXISTS Persona (
                id_persona INT(11) NOT NULL AUTO_INCREMENT,
                nombre VARCHAR(100) NOT NULL,
                apellido VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                telefono VARCHAR(20) NOT NULL,
                PRIMARY KEY (id_persona)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS Cliente (
                id_persona INT(11) NOT NULL,
                direccion VARCHAR(255) NOT NULL,
                DNI VARCHAR(20) NOT NULL,
                PRIMARY KEY (id_persona),
                FOREIGN KEY (id_persona) REFERENCES Persona(id_persona) ON DELETE CASCADE
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS Especialidad (
                id_especialidad INT(11) NOT NULL AUTO_INCREMENT,
                nombre_especialidad VARCHAR(100) NOT NULL,
                PRIMARY KEY (id_especialidad)
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS Agente (
                id_persona INT(11) NOT NULL,
                direccion_oficina VARCHAR(255) NOT NULL,
                id_especialidad INT(11) NOT NULL,
                PRIMARY KEY (id_persona),
                FOREIGN KEY (id_persona) REFERENCES Persona(id_persona) ON DELETE CASCADE,
                FOREIGN KEY (id_especialidad) REFERENCES Especialidad(id_especialidad) ON DELETE RESTRICT
            );
            """
        ]

        for query in queries:
            cursor.execute(query)

        connection.commit()
        print("Tablas creadas correctamente en MySQL.")
    except Exception as e:
        print(f"Error al crear tablas en MySQL: {e}")
    finally:
        cursor.close()
        connection.close()

# ================== Crear tablas en PostgreSQL ==================
def create_postgresql_tables():
    try:
        # Conexión al servidor de PostgreSQL
        connection = psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST'),
            port=int(os.environ.get('POSTGRES_PORT')),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD')
        )
        cursor = connection.cursor()
        connection.autocommit = True 

        # Obtener el nombre de la base de datos de las variables de entorno
        database_name = os.environ.get('POSTGRES_DB')  # Nombre predeterminado si no se proporciona

        # Eliminar la base de datos si ya existe
        cursor.execute(f"DROP DATABASE IF EXISTS {database_name};")
        print(f"Base de datos '{database_name}' eliminada (si existía).")

        # Crear la base de datos
        cursor.execute(f"CREATE DATABASE {database_name};")
        print(f"Base de datos '{database_name}' creada correctamente.")

        cursor.close()
        connection.close()

        # Conectarse a la base de datos recién creada
        connection = psycopg2.connect(
            host=os.environ.get('POSTGRES_HOST'),
            port=int(os.environ.get('POSTGRES_PORT')),
            user=os.environ.get('POSTGRES_USER'),
            password=os.environ.get('POSTGRES_PASSWORD'),
            database=database_name  # Conectarse a la nueva base de datos
        )
        cursor = connection.cursor()

        # Crear tablas en PostgreSQL
        queries = [
            """
            CREATE TABLE IF NOT EXISTS polizas (
                idPoliza SERIAL PRIMARY KEY,
                idCliente BIGINT NOT NULL,
                idAgente BIGINT NOT NULL,
                fechaInicio DATE NOT NULL,
                fechaFin DATE NOT NULL,
                prima DECIMAL NOT NULL
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS seguros (
                idSeguro SERIAL PRIMARY KEY,
                nombreSeguro VARCHAR(255) NOT NULL,
                descripcion TEXT,
                tipoSeguro VARCHAR(100),
                idPoliza BIGINT REFERENCES polizas(idPoliza),
                monto DECIMAL NOT NULL
            );
            """
        ]

        for query in queries:
            cursor.execute(query)

        connection.commit()
        print("Tablas creadas correctamente en PostgreSQL.")
    except Exception as e:
        print(f"Error al crear tablas en PostgreSQL: {e}")
    finally:
        cursor.close()
        connection.close()

# ================== Crear base de datos en MongoDB ==================
def create_mongodb_database():
    try:
        #  Obtener la URI de MongoDB y el nombre de la base de datos de las variables de entorno
        mongo_host = os.environ.get("MONGODB_HOST")  # Cambia a tu host de MongoDB
        mongo_port = os.environ.get("MONGODB_PORT")       # Cambia a tu puerto de MongoDB
        mongo_db = os.environ.get("MONGODB_DATABASE")  # Cambia a tu base de datos MongoDB

        # Crear la URI de conexión
        mongo_uri = f"mongodb://{mongo_host}:{mongo_port}/"

        client = MongoClient(mongo_uri)

        # Verificar si la base de datos 'bienes' existe y eliminarla si es así
        if mongo_db in client.list_database_names():
            client.drop_database(mongo_db)
            print("Base de datos 'bienes' eliminada correctamente.")

        # Crear la base de datos y la colección nuevamente
        db = client[mongo_db]  # Crea una base de datos llamada 'bienes'
        collection = db[mongo_db]  # Crea una colección llamada 'bienes'
        collection.insert_one({"mensaje": "conexion exitosa"})
        print("Base de datos y colección 'bienes' creadas en MongoDB.")

    except Exception as e:
        print(f"Error al crear la base de datos en MongoDB: {e}")
    finally:
        client.close()

# ================== Ejecutar todas las funciones ==================
def crear_todas_las_tablas():
    create_mysql_tables()  # Crear tablas en MySQL
    create_postgresql_tables()  # Crear tablas en PostgreSQL
    create_mongodb_database()  # Crear base de datos en MongoDB