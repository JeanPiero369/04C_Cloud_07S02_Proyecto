from enum import Enum
from fastapi import FastAPI, HTTPException
import httpx
from typing import List, Optional, Union
from pydantic import BaseModel, Field, validator
from datetime import date
import os

app = FastAPI()

# Configuración de URLs de microservicios
CLIENTE_API_URL = os.getenv("CLIENTE_API_URL", "http://cliente-api:8000")
BIENES_API_URL = os.getenv("BIENES_API_URL", "http://bienes-api:3000")
POLIZA_API_URL = os.getenv("POLIZA_API_URL", "http://poliza-api:8080")

# Modelos Pydantic para validación de datos
class Cliente(BaseModel):
    id_persona: Optional[int] = None
    nombre: str
    apellido: str
    email: str
    telefono: str
    direccion: str
    DNI: str

class Agente(BaseModel):
    id_persona: Optional[int] = None
    nombre: str
    apellido: str
    email: str
    telefono: str
    direccion_oficina: str
    id_especialidad: int

class Especialidad(BaseModel):
    id_especialidad: Optional[int] = None
    nombre: str

class BienBase(BaseModel):
    id: Optional[int] = None
    ID_cliente: int
    ID_seguro: int
    tipoBien: str

class Auto(BienBase):
    tipoBien: str = "Auto"
    placa: str
    marca: str
    fechaCompra: date
    valor: float

class Casa(BienBase):
    tipoBien: str = "Casa"
    fechaCompra: date
    cochera: bool
    valor: float

class Laptop(BienBase):
    tipoBien: str = "Laptop"
    fechaCompra: date
    marca: str
    modelo: str
    valor: float

Bien = Union[Auto, Casa, Laptop]

class TipoSeguros(str, Enum):
    ROBO = "ROBO"
    INCENDIO = "INCENDIO"
    AUTOMOVIL = "AUTOMOVIL"
    HOGAR = "HOGAR"
    LAPTOP = "LAPTOP"
    SALUD = "SALUD"
    VIDA = "VIDA"
    VIAJE = "VIAJE"
    MOTOCICLETA = "MOTOCICLETA"
    DESEMPLEO = "DESEMPLEO"


class Seguro(BaseModel):
    nombreSeguro: str
    descripcion: str
    tipoSeguro: TipoSeguros
    monto: float

    @validator('tipoSeguro')
    def tipo_seguro_valido(cls, v):
        if v not in TipoSeguros:
            raise ValueError(f'Tipo de seguro no válido. Debe ser uno de: {", ".join([t.value for t in TipoSeguros])}')
        return v

class Poliza(BaseModel):
    idCliente: int
    idAgente: int
    fechaInicio: str
    fechaFin: str
    prima: float

@app.get("/")
async def read_root():
    return {"message": "Orquestador de Servicios de Seguros"}
    
# Endpoints para Clientes
@app.get("/clientes")
async def obtener_todos_clientes():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CLIENTE_API_URL}/clientes")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener los clientes")
        return response.json()
    
# Endpoints para Clientes
@app.post("/clientes")
async def crear_cliente(cliente: Cliente):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{CLIENTE_API_URL}/clientes", json=cliente.dict())
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al crear el cliente")
        return response.json()

@app.get("/clientes/{cliente_id}")
async def obtener_cliente(cliente_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CLIENTE_API_URL}/clientes/{cliente_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Cliente no encontrado")
        return response.json()
    
@app.put("/clientes/{cliente_id}")
async def actualizar_cliente(cliente_id: int, cliente: Cliente):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{CLIENTE_API_URL}/clientes/{cliente_id}", json=cliente.dict())
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al actualizar el cliente")
        return response.json()
    
@app.delete("/clientes/{cliente_id}")
async def eliminar_cliente(cliente_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{CLIENTE_API_URL}/clientes/{cliente_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al eliminar el cliente")
        return {"message": "Cliente eliminado con éxito"}

# Endpoints para Agentes
@app.get("/agentes")
async def obtener_todos_agentes():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CLIENTE_API_URL}/agentes")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener los agentes")
        return response.json()

@app.post("/agentes")
async def crear_agente(agente: Agente):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{CLIENTE_API_URL}/agentes", json=agente.dict())
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al crear el agente")
        return response.json()

@app.get("/agentes/{agente_id}")
async def obtener_agente(agente_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CLIENTE_API_URL}/agentes/{agente_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Agente no encontrado")
        return response.json()
    
@app.put("/agentes/{agente_id}")
async def actualizar_agente(agente_id: int, agente: Agente):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{CLIENTE_API_URL}/agentes/{agente_id}", json=agente.dict())
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al actualizar el agente")
        return response.json()

@app.delete("/agentes/{agente_id}")
async def eliminar_agente(agente_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{CLIENTE_API_URL}/agentes/{agente_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al eliminar el agente")
        return {"message": "Agente eliminado con éxito"}
    
# Endpoints para Especialidades
@app.get("/especialidades")
async def obtener_todas_especialidades():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{CLIENTE_API_URL}/especialidades")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener las especialidades")
        return response.json()

@app.post("/especialidades")
async def crear_especialidad(especialidad: Especialidad):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{CLIENTE_API_URL}/especialidades", json=especialidad.dict())
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al crear la especialidad")
        return response.json()

@app.put("/especialidades/{especialidad_id}")
async def actualizar_especialidad(especialidad_id: int, especialidad: Especialidad):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{CLIENTE_API_URL}/especialidades/{especialidad_id}", json=especialidad.dict())
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al actualizar la especialidad")
        return response.json()

@app.delete("/especialidades/{especialidad_id}")
async def eliminar_especialidad(especialidad_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{CLIENTE_API_URL}/especialidades/{especialidad_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al eliminar la especialidad")
        return {"message": "Especialidad eliminada con éxito"}

# Endpoints para Bienes
@app.post("/bienes")
async def crear_bien(bien: Bien):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BIENES_API_URL}/bienes", json=bien.dict(exclude_none=True))
        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail="Error al crear el bien")
        return response.json()

@app.get("/bienes/{bien_id}")
async def obtener_bien(bien_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BIENES_API_URL}/bienes/{bien_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Bien no encontrado")
        return response.json()

@app.put("/bienes/{bien_id}")
async def actualizar_bien(bien_id: int, bien: Bien):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{BIENES_API_URL}/bienes/{bien_id}", json=bien.dict(exclude_none=True))
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al actualizar el bien")
        return response.json()

@app.delete("/bienes/{bien_id}")
async def eliminar_bien(bien_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BIENES_API_URL}/bienes/{bien_id}")
        if response.status_code != 204:
            raise HTTPException(status_code=response.status_code, detail="Error al eliminar el bien")
        return {"message": "Bien eliminado con éxito"}

@app.get("/bienes/autos")
async def obtener_autos():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BIENES_API_URL}/bienes/autos")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener autos")
        return response.json()

@app.get("/bienes/casas")
async def obtener_casas():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BIENES_API_URL}/bienes/casas")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener casas")
        return response.json()

@app.get("/bienes/laptops")
async def obtener_laptops():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BIENES_API_URL}/bienes/laptops")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener laptops")
        return response.json()

@app.get("/bienes/all")
async def obtener_todos_bienes():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BIENES_API_URL}/bienes/all")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener todos los bienes")
        return response.json()

@app.get("/check_api")
async def verificar_api():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BIENES_API_URL}/check_api")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al verificar la API")
        return response.json()

# Endpoints para Pólizas
@app.get("/polizas")
async def get_all_polizas():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{POLIZA_API_URL}/api/polizas")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener las pólizas")
        return response.json()

@app.get("/polizas/{id}")
async def get_poliza_by_id(id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{POLIZA_API_URL}/api/polizas/{id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Póliza no encontrada")
        elif response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener la póliza")
        return response.json()

@app.post("/polizas")
async def create_poliza(poliza: Poliza):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{POLIZA_API_URL}/api/polizas", json=poliza.dict())
        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail="Error al crear la póliza")
        return response.json()

@app.put("/polizas/{id}")
async def update_poliza(id: int, poliza: Poliza):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{POLIZA_API_URL}/api/polizas/{id}", json=poliza.dict())
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Póliza no encontrada")
        elif response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al actualizar la póliza")
        return response.json()

@app.delete("/polizas/{id}")
async def delete_poliza(id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{POLIZA_API_URL}/api/polizas/{id}")
        if response.status_code != 204:
            raise HTTPException(status_code=response.status_code, detail="Error al eliminar la póliza")
        return {"detail": "Póliza eliminada con éxito"}

@app.get("/polizas/cliente/{idCliente}")
async def get_polizas_by_cliente(idCliente: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{POLIZA_API_URL}/api/polizas/cliente/{idCliente}")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener las pólizas del cliente")
        return response.json()

# Endpoints para Seguros
@app.get("/seguros")
async def get_all_seguros():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{POLIZA_API_URL}/api/seguros")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener los seguros")
        return response.json()

@app.get("/seguros/{id}")
async def get_seguro_by_id(id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{POLIZA_API_URL}/api/seguros/{id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Seguro no encontrado")
        elif response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al obtener el seguro")
        return response.json()

@app.post("/seguros")
async def create_seguro(seguro: Seguro):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{POLIZA_API_URL}/api/seguros", json=seguro.dict())
        if response.status_code != 201:
            raise HTTPException(status_code=response.status_code, detail="Error al crear el seguro")
        return response.json()

@app.put("/seguros/{id}")
async def update_seguro(id: int, seguro: Seguro):
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{POLIZA_API_URL}/api/seguros/{id}", json=seguro.dict())
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Seguro no encontrado")
        elif response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error al actualizar el seguro")
        return response.json()

@app.delete("/seguros/{id}")
async def delete_seguro(id: int):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{POLIZA_API_URL}/api/seguros/{id}")
        if response.status_code != 204:
            raise HTTPException(status_code=response.status_code, detail="Error al eliminar el seguro")
        return {"detail": "Seguro eliminado con éxito"}

# Operación compuesta para crear una póliza completa
@app.post("/crear-poliza-completa")
async def crear_poliza_completa(cliente_id: int, agente_id: int, bienes: List[Bien], seguros: List[Seguro], poliza: Poliza):
    async with httpx.AsyncClient() as client:
        # Verificar si el cliente y el agente existen
        cliente_response = await client.get(f"{CLIENTE_API_URL}/clientes/{cliente_id}")
        agente_response = await client.get(f"{CLIENTE_API_URL}/agentes/{agente_id}")
        if cliente_response.status_code != 200 or agente_response.status_code != 200:
            raise HTTPException(status_code=404, detail="Cliente o agente no encontrado")
        
        # Crear la póliza
        poliza.idCliente = cliente_id
        poliza.idAgente = agente_id
        poliza_response = await client.post(f"{POLIZA_API_URL}/api/polizas", json=poliza.dict())
        if poliza_response.status_code != 201:
            raise HTTPException(status_code=500, detail="Error al crear la póliza")
        
        poliza_creada = poliza_response.json()
        
        # Crear seguros y asociarlos a la póliza
        seguros_creados = []
        for seguro in seguros:
            seguro_data = seguro.dict()
            seguro_data["poliza"] = {"id": poliza_creada["id"]}
            seguro_response = await client.post(f"{POLIZA_API_URL}/api/seguros", json=seguro_data)
            if seguro_response.status_code != 201:
                raise HTTPException(status_code=500, detail="Error al crear un seguro")
            seguros_creados.append(seguro_response.json())
        
        # Crear los bienes y asociarlos con los seguros
        bienes_creados = []
        for bien, seguro_creado in zip(bienes, seguros_creados):
            bien_data = bien.dict(exclude_none=True)
            bien_data["ID_cliente"] = cliente_id
            bien_data["ID_seguro"] = seguro_creado["idSeguro"]
            bien_response = await client.post(f"{BIENES_API_URL}/bienes", json=bien_data)
            if bien_response.status_code != 201:
                raise HTTPException(status_code=500, detail="Error al crear un bien")
            bienes_creados.append(bien_response.json())
        
        return {
            "poliza": poliza_creada,
            "bienes": bienes_creados,
            "seguros": seguros_creados
        }


# Operación para obtener un resumen del cliente
@app.get("/resumen-cliente/{cliente_id}")
async def resumen_cliente(cliente_id: int):
    async with httpx.AsyncClient() as client:
        # Obtener información del cliente
        cliente_response = await client.get(f"{CLIENTE_API_URL}/clientes/{cliente_id}")
        if cliente_response.status_code != 200:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        cliente = cliente_response.json()
        
        # Obtener póliza del cliente
        polizas_response = await client.get(f"{POLIZA_API_URL}/api/polizas/cliente/{cliente_id}")
        if polizas_response.status_code != 200:
            polizas = []
        else:
            polizas = polizas_response.json()
        
        # Obtener bienes del cliente
        bienes_response = await client.get(f"{BIENES_API_URL}/bienes", params={"ID_cliente": cliente_id})
        if bienes_response.status_code != 200:
            bienes = []
        else:
            bienes = bienes_response.json()
        
        return {
            "cliente": cliente,
            "polizas": polizas,
            "bienes": bienes
        }
    
@app.post("/crear-seguro")
async def crear_seguro(seguro: Seguro):
    async with httpx.AsyncClient() as client:
        seguro_response = await client.post(f"{POLIZA_API_URL}/api/seguros", json=seguro.dict())
        if seguro_response.status_code != 201:
            raise HTTPException(status_code=500, detail="Error al crear el seguro")
        
        seguro_creado = seguro_response.json()
        
        return {
            "mensaje": "Seguro creado exitosamente",
            "seguro": seguro_creado
        }

@app.post("/añadir-seguro-a-poliza/{poliza_id}/{seguro_id}")
async def añadir_seguro_a_poliza(poliza_id: int, seguro_id: int):
    async with httpx.AsyncClient() as client:
        # Verificar si la póliza existe
        poliza_response = await client.get(f"{POLIZA_API_URL}/api/polizas/{poliza_id}")
        if poliza_response.status_code != 200:
            raise HTTPException(status_code=404, detail="Póliza no encontrada")
        
        # Verificar si el seguro existe
        seguro_response = await client.get(f"{POLIZA_API_URL}/api/seguros/{seguro_id}")
        if seguro_response.status_code != 200:
            raise HTTPException(status_code=404, detail="Seguro no encontrado")
        
        # Asociar el seguro a la póliza
        seguro_data = seguro_response.json()
        seguro_data["poliza"] = {"id": poliza_id}
        update_response = await client.put(f"{POLIZA_API_URL}/api/seguros/{seguro_id}", json=seguro_data)
        if update_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error al asociar el seguro a la póliza")
        
        return {
            "mensaje": "Seguro añadido exitosamente a la póliza",
            "seguro_actualizado": update_response.json()
        }
