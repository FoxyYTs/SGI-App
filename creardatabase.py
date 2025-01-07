import conexion

mydb = conexion.conectar()

try:
    mycursor = mydb.cursor()

    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS `acceso` (
            `user` varchar(15) NOT NULL,
            `email` varchar(255) NOT NULL,
            `pass` varchar(255) NOT NULL,
            `request_password` enum('0','1') NOT NULL DEFAULT '0',
            `token_password` varchar(200) NOT NULL,
            `roles_fk` int(11) DEFAULT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)
    mycursor.execute("""
        CREATE TABLE `area` (
            `id_area` int(11) NOT NULL,
            `nombre_area` varchar(45) DEFAULT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)
    
    mydb.commit() # Guardar los cambios en la base de datos
    print("Tabla 'acceso' creada (o ya existente).")

except:
    print(f"Error al ejecutar la consulta")
finally: # Cerrar la conexión siempre
    if mydb:
        mycursor.close()
        mydb.close()