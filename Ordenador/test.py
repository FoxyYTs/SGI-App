import mysql.connector
import conexion

def register(entry_correo, entry_usuario, entry_clave, entry_con_clave):
    nombre = "Ejemplo"
    ubicacion = 1
    unidad_medida = 1

    try:
        mydb = conexion.conectar()
        mycursor = mydb.cursor()

        sql = """INSERT INTO implemento 
                (nombre_implemento, ubicacion_fk, und_medida_fk) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        
        val = (nombre, ubicacion, unidad_medida)
        mycursor.execute(sql, val)
        mydb.commit()


    except mysql.connector.Error as err:
        print("Error de conexión:", err)
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
