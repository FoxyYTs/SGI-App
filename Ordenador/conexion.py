import mysql.connector

def conectar():  # Nombre más descriptivo
    try:
        mydb = mysql.connector.connect(
            host="172.22.85.242",
            user="root",
            passwd="",
            database="sgi"
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None  # Importante retornar None en caso de error