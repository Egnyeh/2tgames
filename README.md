2tGamesCafe

Documento de requisitos del sistema

Introducción

Propósitos del documento:
Este documento tiene como objetivo definir los requisitos de la aplicación y web empresarial de 2tGames.


Alcance del sistema

El sistema permitirá al usuario realizar compras, consultar las diferentes cartas de bebida y los eventos los cuales se organizarán.


Descripción general

El sistema permitirá al dueño del bar gestionar la tienda online y realizar cambios en la aplicación y la pagina web.
Podrá modificar, añadir y eliminar productos de la tienda online.
En la aplicación habrá un espacio habilitado para que los clientes reserven tanto mesas, como futuros juegos que vayan a poner en venta.

Requisitos no funcionales
• RNF1: El sistema debe constar de tres partes:
    Aplicación web (frontend).
    Aplicación móvil (Android/iOS).
    Backend con API REST y base de datos.

• RNF2: El backend debe estar implementado con un framework moderno (ej. FastAPI, Spring Boot, o Node.js/Express).

• RNF3: El frontend web debe ser responsive y fácil de usar.

• RNF4: La app móvil debe ser intuitiva y con tiempos de carga bajos.

• RNF5: La base de datos debe garantizar integridad y consistencia en las transacciones de compra.

• RNF6: El sistema debe proteger la información sensible de los usuarios (datos personales y bancarios) cumpliendo con estándares de seguridad.

• RNF7: El sistema debe ser escalable para soportar múltiples usuarios concurrentes.

• RNF8: El backend y la base de datos deben poder desplegarse en contenedores Docker.

• RNF9: Todas las funcionalidades críticas deben contar con pruebas unitarias y de integración.

• RNF10: El sistema debe estar disponible al menos el 95% del tiempo (alta disponibilidad).


Requisitos funcionales
• RF1: El sistema debe permitir el registro de usuarios mediante correo electrónico y contraseña.

• RF2: El sistema debe permitir a los usuarios iniciar sesión con sus credenciales.

• RF3: Los usuarios podrán ver el catálogo de productos (sobres y cartas).

• RF4: El usuario podrá añadir productos al carrito de compra.

• RF5: El sistema debe permitir realizar el pago de los productos seleccionados.

• RF6: El sistema debe guardar en la base de datos las compras realizadas por cada usuario.

• RF7: Los usuarios podrán ver el historial de sus compras.

• RF8: El administrador podrá añadir, editar o eliminar productos de la tienda.

• RF9: El administrador podrá gestionar usuarios (activar, desactivar, modificar datos).

• RF10: El sistema enviará confirmaciones de compra al usuario (por ejemplo, por correo electrónico o en la app).


Requisitos de interfaz

La interfaz gráfica de usuario será desarrollada con Jetpack Compose, el framework par la creación de interfaces para aplicaciones Android.


Requisitos del sistema
La aplicación de Android será desarrollada para teléfonos móviles de Android con una versión de Android 12 o superior (API 31). Se usará Kotlin y, como ya se ha comentado Jetpack Compose.

La parte del backend usará FastAPI, en su última versión disponible en el momento del desarrollo de la aplicación.

En cuanto al motor de base de datos, el lado del backen, será MySQL, en su última versión. Tendrás que usar el ORM SQLModel que está basado en SQLAlchemy, usa Pydantic y está bien integrado con FastAPI.

Por último, el backend deberá ser desplegado por medio de contenedores Docker (al menos dos contenedores: uno para FastAPY y otro para MySQL).



Criterios de aceptación

El sistema será aceptado si:
• Todos los requisitos funcionales han sido implementados y probados.
• Se ha documentado la aplicación.
• Se han realizado pruebas de usabilidad con al menos 5 clientes.
• El dueño ha revisado y aprobado los informes generados, realizando pruebas durante dos semanas de la aplicación.
