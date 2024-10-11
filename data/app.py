from create_tables import crear_todas_las_tablas
from data import generate_all_data
from load_data import cargar_todos_los_datos


def main():
    # 1. Crear las tablas en MySQL, PostgreSQL y MongoDB
    crear_todas_las_tablas()

    # 2. Generar los datos
    generate_all_data()

    #3. Cargar los datos
    cargar_todos_los_datos()

if __name__ == "__main__":
    main()