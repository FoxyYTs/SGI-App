# SGI LAB MANAGER - Aplicación Web

![Banner del Proyecto SGI LAB MANAGER Web](https://github.com/FoxyYTs/imgs/blob/main/imageweb.png?raw=true)
*Coloca aquí una imagen representativa de tu aplicación web en funcionamiento.*

## 📄 Descripción General

**SGI LAB MANAGER** es un sistema integral de gestión de inventarios diseñado para el laboratorio del Politécnico Colombiano Jaime Isaza Cadavid, sede regional Oriente. Esta aplicación web es el componente central del sistema, proporcionando una interfaz accesible y completa para la administración eficiente de insumos, sustancias y equipos del laboratorio.

Su objetivo principal es optimizar la administración de recursos, mejorar la precisión del inventario y aumentar la seguridad en las prácticas de laboratorio, digitalizando procesos que antes se realizaban manualmente.

## ✨ Características Principales

* **Gestión de Inventario:** Registro detallado, clasificación, entrada, salida y seguimiento de implementos y sustancias.
* **Control de Stock:** Administración de niveles de stock, alertas para mínimos y máximos.
* **Gestión de Usuarios y Permisos:** Control de acceso basado en roles para diferentes perfiles (laboratoristas, monitores, administradores).
* **Consulta y Búsqueda Avanzada:** Herramientas para localizar rápidamente cualquier elemento en el inventario.
* **Generación de Reportes:** Creación de informes personalizables sobre uso, movimientos, stock y estado del inventario.
* **Información de Seguridad:** Acceso directo a fichas técnicas y de seguridad de sustancias.
* **Gestión Documental:** Posibilidad de adjuntar manuales de uso y otra documentación relevante a cada elemento.

## 🚀 Tecnologías Utilizadas

Este proyecto web está construido con las siguientes tecnologías:

* **Front-End:**
    * `HTML`
    * `CSS`
    * `JavaScript`
* **Back-End:**
    * `PHP` (Lenguaje principal del servidor)
* **Base de Datos:**
    * `MySQL`

### Plan de Migración Futura

Actualmente, se está planificando y evaluando la migración de este componente web a **Django (Python)** para aprovechar sus funcionalidades y escalar el proyecto, lo que permitirá una arquitectura más robusta y modular.

## ⚙️ Configuración y Ejecución Local

Para configurar y ejecutar la aplicación web SGI LAB MANAGER en tu entorno local, sigue estos pasos:

1.  **Clonar el Repositorio:**
    ```bash
    git clone [https://github.com/FoxyYTs/SGI.git](https://github.com/FoxyYTs/SGI.git)
    cd SGI
    ```
2.  **Configurar la Base de Datos:**
    * Crea una base de datos MySQL (ej. `sgi_lab_db`).
    * **Importa el esquema:** Si tienes un archivo `.sql` con el esquema de la base de datos (por ejemplo, `database_schema.sql`), impórtalo en tu nueva base de datos.
        ```bash
        # Ejemplo: mysql -u tu_usuario -p sgi_lab_db < database_schema.sql
        ```
    * **Configurar Conexión:** Edita el archivo de configuración de la base de datos en el proyecto (ej. `includes/db_config.php` o similar, busca el archivo donde se definen las credenciales de conexión) y actualiza los parámetros (`DB_HOST`, `DB_USER`, `DB_PASS`, `DB_NAME`) con los de tu entorno local.
3.  **Servidor Web:**
    * Asegúrate de tener un servidor web local (como Apache con XAMPP/WAMP/MAMP o Nginx) con soporte para PHP.
    * Coloca los archivos del proyecto en el directorio raíz de tu servidor web (ej. `htdocs` para XAMPP/WAMP, `www` para MAMP, o configura un Virtual Host).
4.  **Acceso a la Aplicación:**
    * Abre tu navegador web y navega a la URL local donde desplegaste el proyecto (ej. `http://localhost/SGI` o la URL de tu Virtual Host).

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Si deseas colaborar con este proyecto, por favor, sigue el flujo estándar de GitHub:

1.  Haz un "fork" de este repositorio.
2.  Crea una nueva rama para tu funcionalidad o corrección (`git checkout -b feature/nombre-funcionalidad` o `fix/nombre-bug`).
3.  Realiza tus cambios, asegurándote de seguir las convenciones de codificación existentes.
4.  Haz "commit" de tus cambios con un mensaje claro y descriptivo (`git commit -m 'feat: Añade [descripción de la funcionalidad]'`).
5.  Empuja la rama a tu "fork" (`git push origin feature/nombre-funcionalidad`).
6.  Abre un "Pull Request" (PR) a la rama `main` de este repositorio, explicando claramente los cambios realizados y por qué son necesarios.

## 👨‍💻 Desarrollador Principal

* **José Andrés Daza Gallego**
    * [GitHub](https://github.com/FoxyYTs)
    * [LinkedIn](https://www.linkedin.com/in/jose-andres-daza-gallego/)
    * [Portafolio](https://foxyyts.github.io/gitprofile/)

## 📜 Licencia

Este proyecto está bajo la licencia [Nombre de la Licencia, ej., MIT License]. Consulta el archivo [LICENSE](LICENSE) para más detalles.
