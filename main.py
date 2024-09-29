from fastapi import FastAPI
import mysql.connector
import schemas  # Asegúrate de tener schemas para Cliente y Agente

app = FastAPI()

host_name = "3.210.219.55"
port_number = "8005"
user_name = "root"
password_db = "utec"
database_name = "Aseguradora"  

# Get echo test for load balancer's health check
@app.get("/")
def get_echo_test():
    return {"message": "Echo Test OK"}

# ----- Operaciones CRUD para Clientes -----

# Get all clients
@app.get("/clientes")
def get_clientes():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM cliente")
    result = cursor.fetchall()
    cursor.close()
    mydb.close()
    return {"clientes": result}

# Get a client by ID
@app.get("/clientes/{id_cliente}")
def get_cliente(id_cliente: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM cliente WHERE id_cliente = {id_cliente}")
    result = cursor.fetchone()
    cursor.close()
    mydb.close()
    return {"cliente": result}

# Add a new client
@app.post("/clientes")
def add_cliente(cliente: schemas.Cliente):  # Asegúrate de tener el esquema de Cliente en schemas.py
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    sql = "INSERT INTO cliente (nombre, apellido, email, telefono, direccion, DNI) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (cliente.nombre, cliente.apellido, cliente.email, cliente.telefono, cliente.direccion, cliente.DNI)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": "Cliente added successfully"}

# Modify a client
@app.put("/clientes/{id_cliente}")
def update_cliente(id_cliente: int, cliente: schemas.Cliente):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    sql = "UPDATE cliente SET nombre=%s, apellido=%s, email=%s, telefono=%s, direccion=%s, DNI=%s WHERE id_cliente=%s"
    val = (cliente.nombre, cliente.apellido, cliente.email, cliente.telefono, cliente.direccion, cliente.DNI, id_cliente)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": "Cliente updated successfully"}

# Delete a client by ID
@app.delete("/clientes/{id_cliente}")
def delete_cliente(id_cliente: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"DELETE FROM cliente WHERE id_cliente = {id_cliente}")
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": "Cliente deleted successfully"}

# ----- Operaciones CRUD para Agentes -----

# Get all agents
@app.get("/agentes")
def get_agentes():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM agente")
    result = cursor.fetchall()
    cursor.close()
    mydb.close()
    return {"agentes": result}

# Get an agent by ID
@app.get("/agentes/{id_agente}")
def get_agente(id_agente: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM agente WHERE id_agente = {id_agente}")
    result = cursor.fetchone()
    cursor.close()
    mydb.close()
    return {"agente": result}

# Add a new agent
@app.post("/agentes")
def add_agente(agente: schemas.Agente):  # Asegúrate de tener el esquema de Agente en schemas.py
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    sql = "INSERT INTO agente (nombre, apellido, email, telefono, direccion_oficina, codigo_registro, especialidad) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = (agente.nombre, agente.apellido, agente.email, agente.telefono, agente.direccion_oficina, agente.codigo_registro, agente.especialidad)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": "Agente added successfully"}

# Modify an agent
@app.put("/agentes/{id_agente}")
def update_agente(id_agente: int, agente: schemas.Agente):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    sql = "UPDATE agente SET nombre=%s, apellido=%s, email=%s, telefono=%s, direccion_oficina=%s, codigo_registro=%s, especialidad=%s WHERE id_agente=%s"
    val = (agente.nombre, agente.apellido, agente.email, agente.telefono, agente.direccion_oficina, agente.codigo_registro, agente.especialidad, id_agente)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": "Agente updated successfully"}

# Delete an agent by ID
@app.delete("/agentes/{id_agente}")
def delete_agente(id_agente: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"DELETE FROM agente WHERE id_agente = {id_agente}")
    mydb.commit()
    cursor.close()
    mydb.close()
    return {"message": "Agente deleted successfully"}
