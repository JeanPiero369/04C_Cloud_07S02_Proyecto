from fastapi import FastAPI, HTTPException
import mysql.connector
import schemas  # Ensure you have schemas defined for Cliente and Agente

app = FastAPI()

# Database configuration
host_name = "3.210.219.55"
port_number = "8005"
user_name = "root"
password_db = "utec"
database_name = "Aseguradora"

# Health check endpoint
@app.get("/")
def get_echo_test():
    return {"message": "Echo Test OK"}

# ----- CRUD Operations for Clientes -----
# Obtener todos los clientes con sus detalles de Persona
@app.get("/clientes", response_model=List[Cliente])
def get_clientes():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.*, p.nombre, p.apellido, p.email, p.telefono
        FROM Cliente c
        JOIN Persona p ON c.id_persona = p.id_persona
    """)
    result = cursor.fetchall()
    cursor.close()
    mydb.close()
    return {"clientes": result}

# Obtener un cliente por ID con detalles de Persona
@app.get("/clientes/{id_cliente}", response_model=Cliente)
def get_cliente(id_cliente: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.*, p.nombre, p.apellido, p.email, p.telefono
        FROM Cliente c
        JOIN Persona p ON c.id_persona = p.id_persona
        WHERE c.id_persona = %s
    """, (id_cliente,))
    result = cursor.fetchone()
    cursor.close()
    mydb.close()
    if result:
        return {"cliente": result}
    raise HTTPException(status_code=404, detail="Cliente not found")

# Agregar un nuevo cliente y crear la entrada correspondiente en Persona
@app.post("/clientes", response_model=Cliente)
def add_cliente(cliente: Cliente):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    
    # Insertar en Persona primero
    sql_persona = "INSERT INTO Persona (nombre, apellido, email, telefono) VALUES (%s, %s, %s, %s)"
    val_persona = (cliente.nombre, cliente.apellido, cliente.email, cliente.telefono)
    cursor.execute(sql_persona, val_persona)
    id_persona = cursor.lastrowid  # Obtener el ID de la nueva Persona

    # Ahora insertar en Cliente
    sql_cliente = "INSERT INTO Cliente (id_persona, direccion, DNI) VALUES (%s, %s, %s)"
    val_cliente = (id_persona, cliente.direccion, cliente.DNI)
    cursor.execute(sql_cliente, val_cliente)
    mydb.commit()

    cliente.id_persona = id_persona  # Asignar el ID al objeto cliente
    cursor.close()
    mydb.close()
    return cliente

# Modificar un cliente (y actualizar la información de Persona)
@app.put("/clientes/{id_cliente}", response_model=Cliente)
def update_cliente(id_cliente: int, cliente: Cliente):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()

    # Actualizar información de Persona
    sql_persona = "UPDATE Persona SET nombre=%s, apellido=%s, email=%s, telefono=%s WHERE id_persona=%s"
    cursor.execute(sql_persona, (cliente.nombre, cliente.apellido, cliente.email, cliente.telefono, id_cliente))

    # Actualizar información de Cliente
    sql_cliente = "UPDATE Cliente SET direccion=%s, DNI=%s WHERE id_persona=%s"
    cursor.execute(sql_cliente, (cliente.direccion, cliente.DNI, id_cliente))
    
    mydb.commit()
    cursor.close()
    mydb.close()
    return cliente

# Eliminar un cliente por ID (también elimina la correspondiente Persona)
@app.delete("/clientes/{id_cliente}")
def delete_cliente(id_cliente: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    
    # Primero eliminar de Cliente
    cursor.execute("DELETE FROM Cliente WHERE id_persona = %s", (id_cliente,))
    # Ahora eliminar de Persona
    cursor.execute("DELETE FROM Persona WHERE id_persona = %s", (id_cliente,))
    
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": "Cliente deleted successfully"}

# ----- CRUD Operations for Agentes -----

# Obtener todos los agentes con sus detalles de Persona
@app.get("/agentes", response_model=List[Agente])
def get_agentes():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.*, p.nombre, p.apellido, p.email, p.telefono
        FROM Agente a
        JOIN Persona p ON a.id_persona = p.id_persona
    """)
    result = cursor.fetchall()
    cursor.close()
    mydb.close()
    return {"agentes": result}

# Agregar un nuevo agente y crear la entrada correspondiente en Persona
@app.post("/agentes", response_model=Agente)
def add_agente(agente: Agente):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    
    # Insertar en Persona primero
    sql_persona = "INSERT INTO Persona (nombre, apellido, email, telefono) VALUES (%s, %s, %s, %s)"
    val_persona = (agente.nombre, agente.apellido, agente.email, agente.telefono)
    cursor.execute(sql_persona, val_persona)
    id_persona = cursor.lastrowid  # Obtener el ID de la nueva Persona

    # Ahora insertar en Agente
    sql_agente = "INSERT INTO Agente (id_persona, direccion_oficina, id_especialidad) VALUES (%s, %s, %s)"
    val_agente = (id_persona, agente.direccion_oficina, agente.id_especialidad)
    cursor.execute(sql_agente, val_agente)
    mydb.commit()

    agente.id_persona = id_persona  # Asignar el ID al objeto agente
    cursor.close()
    mydb.close()
    return agente

# Modificar un agente (y actualizar la información de Persona)
@app.put("/agentes/{id_agente}", response_model=Agente)
def update_agente(id_agente: int, agente: Agente):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()

    # Actualizar información de Persona
    sql_persona = "UPDATE Persona SET nombre=%s, apellido=%s, email=%s, telefono=%s WHERE id_persona=%s"
    cursor.execute(sql_persona, (agente.nombre, agente.apellido, agente.email, agente.telefono, id_agente))

    # Actualizar información de Agente
    sql_agente = "UPDATE Agente SET direccion_oficina=%s, id_especialidad=%s WHERE id_persona=%s"
    cursor.execute(sql_agente, (agente.direccion_oficina, agente.id_especialidad, id_agente))
    
    mydb.commit()
    cursor.close()
    mydb.close()
    return agente

# Eliminar un agente por ID (también elimina la correspondiente Persona)
@app.delete("/agentes/{id_agente}")
def delete_agente(id_agente: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    
    # Primero eliminar de Agente
    cursor.execute("DELETE FROM Agente WHERE id_persona = %s", (id_agente,))
    # Ahora eliminar de Persona
    cursor.execute("DELETE FROM Persona WHERE id_persona = %s", (id_agente,))
    
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": "Agente deleted successfully"}

# ----- CRUD Operations for Especialidades -----

# Obtener todas las especialidades
@app.get("/especialidades", response_model=List[Especialidad])
def get_especialidades():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Especialidad")
    result = cursor.fetchall()
    cursor.close()
    mydb.close()
    return {"especialidades": result}

# Agregar una nueva especialidad
@app.post("/especialidades", response_model=Especialidad)
def add_especialidad(especialidad: Especialidad):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    sql = "INSERT INTO Especialidad (nombre) VALUES (%s)"
    val = (especialidad.nombre,)
    cursor.execute(sql, val)
    mydb.commit()
    especialidad.id_especialidad = cursor.lastrowid  # Asignar el ID al objeto especialidad
    cursor.close()
    mydb.close()
    return especialidad

# Modificar una especialidad
@app.put("/especialidades/{id_especialidad}", response_model=Especialidad)
def update_especialidad(id_especialidad: int, especialidad: Especialidad):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    sql = "UPDATE Especialidad SET nombre=%s WHERE id_especialidad=%s"
    cursor.execute(sql, (especialidad.nombre, id_especialidad))
    mydb.commit()
    cursor.close()
    mydb.close()
    return especialidad

# Eliminar una especialidad por ID
@app.delete("/especialidades/{id_especialidad}")
def delete_especialidad(id_especialidad: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM Especialidad WHERE id_especialidad = %s", (id_especialidad,))
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": "Especialidad deleted successfully"}

