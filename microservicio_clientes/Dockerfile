# Usa una imagen base de Python
FROM python:3-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /programas/api-aseguradora

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias desde el archivo requirements.txt
RUN pip3 install -r requirements.txt

# Copia todos los archivos de la aplicación al contenedor
COPY . .

# Comando por defecto para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
