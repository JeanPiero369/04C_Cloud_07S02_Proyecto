import pandas as pd
from faker import Faker
import random
import os

# Inicializar Faker
fake = Faker()

personas = []
especialidades = [
    {"id_especialidad": 1, "nombre_especialidad": "Ventas Directas"},
    {"id_especialidad": 2, "nombre_especialidad": "Ventas en línea"},
    {"id_especialidad": 3, "nombre_especialidad": "Marketing"},
    {"id_especialidad": 4, "nombre_especialidad": "Atención al Cliente"},
    {"id_especialidad": 5, "nombre_especialidad": "Corporativos"},
    {"id_especialidad": 6, "nombre_especialidad": "Reclamaciones"},
]
clientes = []
agentes = []
TipoSeguro = [
    "ROBO",
    "INCENDIO",
    "AUTOMOVIL",
    "HOGAR",
    "LAPTOP",
    "SALUD",
    "VIDA",
    "VIAJE",
    "MOTOCICLETA",
    "DESEMPLEO"
]
Polizas = []
Seguros = []
# Listas para almacenar los datos generados
Bienes = []

def dates():
    date1, date2 = fake.date(), fake.date()
    while(date1 > date2):
        date1, date2 = fake.date(), fake.date()
    return date1, date2

# Función para guardar datos en CSV
def guardar_csv(datos, columnas, nombre_archivo):
    df = pd.DataFrame(datos, columns=columnas)
    df.to_csv(f'data/generated_data/{nombre_archivo}', index=False)


# Generar datos de personas
def generate_data_clientes():
    for _ in range(1, 10001):
        persona = {
            "id_persona": _,
            "nombre": fake.first_name(),
            "apellido": fake.last_name(),
            "email": fake.email(),
            "telefono": fake.phone_number(),
        }
        personas.append(persona)

    for _ in range(1, 8001):
        cliente = {
            "id_persona": _,
            "direccion": fake.address().replace("\n", " "),  # Reemplazar salto de línea
            "DNI": random.randint(10000000, 99999999),
        }
        clientes.append(cliente)

    for _ in range(8001, 10001):
        agente = {
            "id_persona": _,
            "direccion_oficina": fake.address().replace("\n", " "),  # Reemplazar salto de línea
            "id_especialidad": random.randint(1,6)
        }
        agentes.append(agente)

    # Guardar datos en CSV
    guardar_csv(personas, ["id_persona", "nombre", "apellido", "email", "telefono", "edad", "direccion"], 'persona_generated.csv')
    guardar_csv(especialidades, ["id_especialidad", "nombre_especialidad"], 'especialidades_generated.csv')
    guardar_csv(clientes, ["id_persona", "direccion", "DNI"], 'clientes_generated.csv')
    guardar_csv(agentes, ["id_persona", "direccion_oficina", "id_especialidad"], 'agentes_generated.csv')

def generate_data_seguro():
    for _ in range(1, 8001):  # 8000 clientes, uno por cliente
        poliza = {
            "idPoliza": _,
            "idCliente": _,  # Cada cliente tiene una única póliza
            "idAgente": random.randint(8001, 10001),
            "fechaInicio": fake.date(),
            "fechaFin": fake.date(),
            "prima": random.randint(250, 2000)
        }
        Polizas.append(poliza)

    # Aseguramos que cada póliza tenga al menos un seguro
    for poliza in Polizas:
        num_seguros = random.randint(1, 5)  # Número de seguros por póliza (mínimo 1)
        for _ in range(num_seguros):
            tipo = random.choice(TipoSeguro)
            seguro = {
                "idSeguro": len(Seguros) + 1,  # Incrementar el ID del seguro
                "nombreSeguro": f"Seguro de {tipo}",
                "descripcion": f"El presente Seguro es un seguro de tipo {tipo} para el cliente {poliza['idCliente']} con agente a cargo {poliza['idAgente']}",
                "tipo": tipo,
                "idPoliza": poliza["idPoliza"],  # Vincular el seguro a la póliza
                "monto": random.randint(40, 250)
            }
            Seguros.append(seguro)

    # Guardar datos en CSV
    guardar_csv(Polizas, ["idPoliza", "idCliente", "idAgente", "fechaInicio", "fechaFin", "prima"], 'polizas_generated.csv')
    guardar_csv(Seguros, ["idSeguro", "nombreSeguro", "descripcion", "tipo", "idPoliza", "monto"], 'seguros_generated.csv')

def generate_data_bienes():
    # Aseguramos que cada seguro tenga al menos un bien y posiblemente más
    for seguro in Seguros:
        num_bienes = random.randint(1, 3)  # Cada seguro tiene al menos un bien, pero puede tener hasta 3
        for _ in range(num_bienes):
            tipo = random.choice(["Auto", "Casa", "Laptop"])
            bien = {
                "id": len(Bienes) + 1,  # Incrementar el ID del bien
                "ID_cliente": seguro["idPoliza"],  # Asignar cliente basado en la póliza asociada
                "ID_seguro": seguro["idSeguro"],  # Vincular el bien con el seguro correspondiente
                "tipoBien": tipo,  # Especificar el tipo de bien
                "valor": None  # Campo común para el valor
            }

            # Propiedades específicas según el tipo de bien
            if tipo == "Auto":
                bien.update({
                    "placa": fake.license_plate(),
                    "marca": random.choice(["Toyota", "Nissan", "Hyundai", "Kia", "Chevrolet", "Suzuki", "Mazda", "Ford", "Volkswagen", "Mercedes Benz"]),
                    "valor": random.randint(14000, 100000)  # Valor del auto
                })
            elif tipo == "Casa":
                bien.update({
                    "fechaCompra": fake.date(),
                    "cochera": random.choice([True, False]),
                    "valor": random.randint(50000, 500000)  # Valor de la casa
                })
            elif tipo == "Laptop":
                bien.update({
                    "marca": random.choice(["Dell", "HP", "Lenovo", "Apple", "Acer", "Asus", "MSI"]),
                    "modelo": fake.random_int(min=2017, max=2021),
                    "valor": random.randint(3000, 12000)  # Valor de la laptop
                })

            Bienes.append(bien)

    # Guardar datos en CSV
    guardar_csv(Bienes, ["id", "ID_cliente", "ID_seguro", "tipoBien", "placa", "marca", "valor", "fechaCompra", "cochera", "modelo"], 'bienes_generated.csv')

def generate_all_data():
    # Crear carpeta para guardar los datos generados dentro de 'data'
    os.makedirs('data/generated_data', exist_ok=True)

    # Generar datos de clientes, seguros y bienes
    generate_data_clientes()
    generate_data_seguro()
    generate_data_bienes()