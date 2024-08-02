# Descripción del Proyecto: Control de Gastos
Este proyecto es una aplicación web de Control de Gastos diseñada para ayudar a los usuarios a gestionar sus finanzas personales.
La aplicación permite a los usuarios registrar ingresos y egresos, categorizarlos, y generar métricas en tiempo real 
para un mejor análisis y comprensión de sus hábitos financieros.

# Características Principales
* **Registro de Usuarios:** Los usuarios pueden registrarse, iniciar sesión y gestionar sus propias cuentas de manera segura.
* **Gestión de Ingresos y Egresos:** Permite a los usuarios registrar y categorizar sus ingresos y egresos.
* **Filtrado por Categoría y Fecha:** Los usuarios pueden filtrar los registros por categorías y meses específicos.
* **Visualización de Datos:** Ofrece gráficos interactivos y métricas en tiempo real para visualizar los datos financieros.
* **Seguridad y Privacidad:** Cada usuario puede ver y gestionar únicamente sus propios datos.

# Tecnologías Utilizadas
* **Backend:** Django
* **Frontend:** HTML, CSS, JavaScript
* **Base de Datos:** SQLite (puede ser cambiada a PostgreSQL, MySQL, etc.)
* **Autenticación:** Sistema de autenticación de Django
* **Visualización de Datos:** Matplotlib, Django Charts

# Estructura del Proyecto
El proyecto está modularizado en varias aplicaciones para mantener un código limpio y organizado:

* **home:** Página de inicio y gestión de la autenticación de usuarios.
* **ahorro:** Gestión de ahorros.
* **egreso:** Gestión de egresos.
* **ingreso:** Gestión de ingresos.
* **metricas:** Generación de métricas y gráficos en tiempo real.
