
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import uuid

import conexion


def encriptar_clave(clave):
    contrasena_md5 = hashlib.md5(clave.encode()).hexdigest()
    arr2 = list(contrasena_md5)
    pass_encriptada = ""

    for i in range(len(contrasena_md5)):
        pass_encriptada += arr2[i] + "y" + str(i * 3)

    return pass_encriptada

def generar_token_pass(correo):
    mydb = conexion.conectar()
    mycursor = mydb.cursor()

    token = genera_token()
    sql = "UPDATE acceso SET request_password='1', token_password = %s WHERE email = %s"
    val = (token, correo)
    mycursor.execute(sql, val)
    mydb.commit()

    mycursor.close()
    mydb.close()

    return token

def genera_token():
  unique_id = str(uuid.uuid4())
  random_int = random.randint(0, 1000)  # Agrega un número aleatorio para mayor aleatoriedad
  combined_string = unique_id + str(random_int)
  hash_object = hashlib.md5(combined_string.encode())
  token = hash_object.hexdigest()
  return token

def get_valor(campo, campo_where, valor):
    mydb = conexion.conectar()
    mycursor = mydb.cursor()

    sql = "SELECT {} FROM acceso WHERE {} = %s".format(campo, campo_where)
    mycursor.execute(sql, (valor,))
    resultado = mycursor.fetchone()
    mycursor.close()
    mydb.close()

    if resultado:
        return resultado[0]
    else:
        return None
    


def enviar_correo(email, user, asunto, cuerpo):

    mensaje = MIMEMultipart()
    mensaje["From"] = "Laboratorio Integrado <bludu360@gmail.com>"
    mensaje["To"] = f"{user} <{email}>"
    mensaje["Subject"] = asunto
    mensaje["Date"] = "17 Oct 2024 16:41"  # Puedes personalizar la fecha
    mensaje["X-Mailer"] = "my-python-program"  # Puedes agregar un encabezado personalizado

    # Agregar el cuerpo del mensaje
    cuerpo_html = f"""
    <html>
    <body>
    <p>{cuerpo}</p>
    </body>
    </html>
    """
    mensaje.attach(MIMEText(cuerpo_html, "html"))

    mensaje["X-Gm-Labels"] = "Important"  # Marcar como importante en Gmail
    mensaje["Disposition-Notification-To"] = "bludu360@gmail.com"  # Solicitar notificación de entrega

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("bludu360@gmail.com", "valzuafuphnupqhj")
        server.sendmail("Laboratorio Integrado <bludu360@gmail.com>", email, mensaje.as_string())
