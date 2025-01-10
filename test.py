import mysql.connector

# Datos de conexión a la base de datos
host = "localhost"
user = "root"
password = ""
database = "sgi"

try:
    # Conectar a la base de datos
    cnx = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )

    # Crear un cursor
    cursor = cnx.cursor()

    # Parámetro para la consulta
    nombre_usuario = "JoseDaza" 

    # Ejecutar la consulta
    cursor.execute("SELECT a.user AS nombre_usuario, r.nombre_rol, p.nombre_permiso, p.archivo "
                   "FROM acceso AS a "
                   "JOIN roles AS r ON a.roles_fk = r.id_rol "
                   "JOIN permiso_rol AS pr ON r.id_rol = pr.rol_fk "
                   "JOIN permisos AS p ON p.id_permisos = pr.permiso_fk "
                   "WHERE a.user = %s AND p.nombre_permiso NOT LIKE 'GESTION%'", (nombre_usuario,))

    # Obtener los resultados
    resultados = cursor.fetchall()

    # Imprimir los resultados (opcional)
    for resultado in resultados:
        print(resultado)

except mysql.connector.Error as error:
    print(f"Error al conectar a MySQL: {error}")

finally:
    # Cerrar la conexión
    if cnx:
        cnx.close()