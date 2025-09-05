import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import uuid

# Importa mysql.connector para manejar errores específicos si es necesario
import mysql.connector

class Funciones:
    # Estos métodos no necesitan la instancia de la clase (self)
    @staticmethod
    def encriptar_clave(clave):
        # Esta es una implementación básica; para producción se recomienda bcrypt o argon2.
        contrasena_md5 = hashlib.md5(clave.encode()).hexdigest()
        arr2 = list(contrasena_md5)
        pass_encriptada = ""

        for i in range(len(contrasena_md5)):
            pass_encriptada += arr2[i] + "y" + str(i * 3)

        return pass_encriptada

    @staticmethod
    def genera_token():
        unique_id = str(uuid.uuid4())
        random_int = random.randint(0, 1000)
        combined_string = unique_id + str(random_int)
        hash_object = hashlib.md5(combined_string.encode())
        token = hash_object.hexdigest()
        return token

    # Este método ahora recibe la conexión como argumento
    def generar_token_pass(self, conexion, correo):
        mycursor = conexion.cursor()
        
        token = self.genera_token()
        
        sql = "UPDATE acceso SET request_password='1', token_password = %s WHERE email = %s"
        val = (token, correo)
        try:
            mycursor.execute(sql, val)
            conexion.commit()
            return token
        except mysql.connector.Error as err:
            print(f"Error al generar token: {err}")
            return None
        finally:
            mycursor.close()

    # Este método ahora recibe la conexión y usa placeholders seguros
    def get_valor(self, conexion, campo, campo_where, valor):
        mycursor = conexion.cursor()
        
        sql = "SELECT {} FROM acceso WHERE {} = %s".format(campo, campo_where)
        
        try:
            mycursor.execute(sql, (valor,))
            resultado = mycursor.fetchone()
            if resultado:
                return resultado[0]
            else:
                return None
        except mysql.connector.Error as err:
            print(f"Error al obtener valor: {err}")
            return None
        finally:
            mycursor.close()

    @staticmethod
    def enviar_correo(email, user, asunto, cuerpo):
        mensaje = MIMEMultipart()
        mensaje["From"] = "Laboratorio Integrado <bludu360@gmail.com>"
        mensaje["To"] = f"{user} <{email}>"
        mensaje["Subject"] = asunto
        mensaje["Date"] = "17 Oct 2024 16:41"
        mensaje["X-Mailer"] = "my-python-program"
        cuerpo_html = f"""
        <html>
        <body>
        <p>{cuerpo}</p>
        </body>
        </html>
        """
        mensaje.attach(MIMEText(cuerpo_html, "html"))
        mensaje["X-Gm-Labels"] = "Important"
        mensaje["Disposition-Notification-To"] = "bludu360@gmail.com"

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login("bludu360@gmail.com", "valzuafuphnupqhj")
                server.sendmail("Laboratorio Integrado <bludu360@gmail.com>", email, mensaje.as_string())
        except Exception as e:
            print(f"Error al enviar correo: {e}")