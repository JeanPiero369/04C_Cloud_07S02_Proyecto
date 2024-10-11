FROM python:3.10

# Establece el directorio de trabajo
WORKDIR /programas/ingesta

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de tu proyecto al contenedor
COPY . .

# Comando para ejecutar tu script
CMD [ "python3", "./ingesta_postgresql.py" ]
