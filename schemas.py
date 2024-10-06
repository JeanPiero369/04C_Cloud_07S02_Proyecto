from pydantic import BaseModel
from typing import Optional

# Esquema para Persona (base común entre Cliente y Agente)
class Persona(BaseModel):
    id_persona: Optional[int]=None # Asignado automáticamente por la base de datos
    nombre: str
    apellido: str
    email: str
    telefono: str

# Esquema para Cliente, heredando de Persona
class Cliente(Persona):
    direccion: str
    DNI: str

# Esquema para Especialidad
class Especialidad(BaseModel):
    id_especialidad: Optional[int]  # Asignado automáticamente por la base de datos
    nombre_especialidad: str

# Esquema para Agente, heredando de Persona
class Agente(Persona):
    direccion_oficina: str
    codigo_registro: str
    especialidad: Especialidad  # Relación con la especialidad
