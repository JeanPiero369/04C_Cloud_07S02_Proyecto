# Sistema de Gestión de Pólizas - Arquitectura Backend

Este proyecto es un sistema web desarrollado en **Flask** para gestionar pólizas, clientes, agentes y especialidades. Utiliza diversas tecnologías de backend para gestionar la ingesta y almacenamiento de datos en múltiples bases de datos y servicios en la nube.

## Descripción del Proyecto

El sistema permite:

- Registrar y mostrar **clientes**, **agentes** y **pólizas**.
- Asociar **clientes** a pólizas, asignar **agentes** y gestionar **especialidades**.
- Administrar las interacciones y la ingesta de datos a través de bases de datos relacionales y NoSQL.

La solución emplea contenedores **Docker** para desplegar servicios en **Amazon EC2**, y se apoya en servicios de **AWS** como **S3**, **Athena** y **Glue** para el procesamiento y análisis de datos.

### Funcionalidades:

1. **Clientes**: Registro y consulta de clientes.
2. **Agentes**: Registro y consulta de agentes.
3. **Pólizas**: Registro y consulta de pólizas.
4. **Especialidades**: Administración de las especialidades de los agentes.
5. **Ingesta de datos**: Importación y sincronización de datos en distintas bases de datos.

## Tecnologías Utilizadas

- **Flask**: Framework para el desarrollo de la aplicación web.
- **MySQL**, **PostgreSQL**, **MongoDB**: Bases de datos para almacenar diferentes tipos de información.
- **Docker**: Contenedores para desplegar las bases de datos y servicios de ingesta.
- **Amazon EC2**: Máquinas virtuales para ejecutar contenedores Docker.
- **AWS S3**: Almacenamiento de datos en la nube.
- **AWS Glue**: Servicio de ETL (Extract, Transform, Load) para procesar los datos.
- **AWS Athena**: Herramienta de análisis de datos almacenados en S3.

## Estructura del Proyecto

El proyecto tiene las siguientes rutas y páginas:

1. **/clientes**:
    - Registro de nuevos clientes vía JSON o formulario.
    - Lista de clientes registrados.
2. **/agentes**:
    - Registro de nuevos agentes vía JSON o formulario.
    - Lista de agentes registrados.
3. **/polizas**:
    - Registro de nuevas pólizas (asociadas a clientes y agentes).
    - Lista de pólizas registradas.
4. **/especialidades**:
    - Gestión de especialidades de agentes.

### Flujo de Ingesta de Datos

1. **Bases de Datos (EC2 MV Base de Datos)**
   - **MySQL**: Base de datos `BD_clientes` para gestionar la información de clientes.
   - **PostgreSQL**: Base de datos `BD_polizas` para almacenar datos de pólizas.
   - **MongoDB**: Base de datos `BD_bienes` para gestionar información relacionada con bienes asegurados.

2. **Contenedores Docker en EC2 MV Ingesta**:
   - Scripts de ingesta (`ingesta_mysql.py`, `ingesta_postgresql.py`, `ingesta_mongodb.py`) ejecutados en contenedores Docker para sincronizar los datos en AWS S3.
   
3. **Almacenamiento en AWS**:
   - Los datos de cada base de datos son enviados a buckets de **Amazon S3**:
     - `04c-cloud-07502-proyecto-mysql`
     - `04c-cloud-07502-proyecto-postgresql`
     - `04c-cloud-07502-proyecto-mongodb`

4. **Procesamiento y Análisis de Datos**:
   - **AWS Glue**: Servicio que ejecuta el proceso ETL para los datos almacenados en S3.
   - **Amazon Athena**: Realiza consultas y análisis sobre los datos transformados.


