from pydantic import BaseModel

# Esquema para Cliente
class Cliente(BaseModel):
    nombre: str
    apellido: str
    email: str
    telefono: str
    direccion: str
    DNI: str

# Esquema para Agente
class Agente(BaseModel):
    nombre: str
    apellido: str
    email: str
    telefono: str
    direccion_oficina: str
    codigo_registro: str
    especialidad: str
