# API con Django REST Framework

Para levantar el proyecto dentro de un entorno cerrado únicamente necesita tener instalado docker en su equipo.

Teniendo el repositorio clonado y estando posicionado en la raiz del proyecto crearemos la imagen de docker:
> docker build -t drf .

Con la imagen creada procedemos a crear el contenedor:
> docker run -d -p 8000:8000 --name drf drf

Esto nos dejará un contenedor levantado, si queremos acceder al mismo podemos hacerlo con el comando:
> docker exec -ti drf bash

Si desea ejecutarlo sin docker necesitará instalar las versiones indicadas en el fichero requirements.py y ejecutar el comando runserver:
> pip3 install -r requirements.txt

> python3 drf/manage.py runserver 8000

# Ejecutar tests

Una vez dentro del contenedor podemos lanzar los tests unitarios con el siguiente comando:
> python3 /opt/drf/drf/manage.py test hotels

Esto ejecuta los tests ubicados en el directorio '/opt/drf/drf/hotels/tests/'.

# Características del proyecto
Cuenta con endpoints para los cuatro modelos de la app hotels (Hotel, Room, Rate e Inventory) que permiten la creación, modificación, elimitación y obtención de los objetos de la base de datos.

Además de los endpoints relacionados directamente con el modelo, tenemos un endpoint availability que nos permite conocer si hay habitaciones libres y a qué precios, dados el código de hotel y las fechas de entrada y salida.
En la consulta de este endpoint se tendrá en cuenta que las habitaciones estén libres todos los días desde la fecha de entrada hasta la de salida.

Toda todos estos endpoints se pueden ver en detalle en la url: http://127.0.0.1:8000/swagger/

Este proyecto está Dockerizado, cuenta con test unitarios para las funcionalidades principales de endpoints, se ha implementado la posibilidad de utilizar OAuth2 en las peticiones a la API y también se ha documentado con Swagger.

Se han adjuntado unos fixtures para poblar mínimamente la base de datos y poder probar todas las funcionalidades de manera inmediata.
En estos fixtures se incluyen dos usuarios con sus contraseñas:
* admin / 123456: Usuario administrador
* api_user / MXcwUnvjKGFUz2ma: Usuario api preparado para utilizar con OAuth2

Los datos para utilizar OAuth2 con el usuario api_user se pueden encontrar en: /admin/oauth2_provider/application/1/change/

# Posibles extras
A continuación listamos una serie de posibles mejoras a realizar:
* Mejora de la dockerización, incluyendo un volumen que apunte a la raíz del código, que nos permitiría una edición cómoda y directa sobre el código sin necesidad de rehacer la imagen.
* Cambiar la base de datos (a PostgreSQL por ejemplo), esto se incluiría en la Dockerización haciendo uso de docker-compose.
* Inclusión de los modelos en la vista de admin de Django.
* Añadir traducciones
* Separación de settings para desarrollo y producción.
