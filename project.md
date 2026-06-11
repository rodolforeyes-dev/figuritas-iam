# ROLE

Actúa como un desarrollador Full Stack senior especializado en Python, FastAPI y aplicaciones web simples orientadas a usuarios no técnicos.

Debes diseñar e implementar una aplicación web extremadamente simple para facilitar el intercambio de figuritas de un álbum escolar del Mundial.

La prioridad principal es la facilidad de uso, por encima de la complejidad técnica.

---

# TASK

Desarrollar una aplicación web que permita a los padres registrar las figuritas repetidas de sus hijos y que el sistema encuentre automáticamente posibles intercambios entre las familias participantes.

La aplicación debe:

1. Permitir registrar participantes.
2. Permitir registrar figuritas repetidas.
3. Detectar automáticamente coincidencias.
4. Mostrar posibles intercambios de forma clara.
5. Permitir buscar rápidamente una figurita específica.
6. Requerir la menor cantidad posible de acciones por parte de los usuarios.

El objetivo es evitar que los padres deban publicar listas manuales en grupos de WhatsApp.

---

# CONTEXT

## Escenario

La aplicación será utilizada por familias del:

IAM Instituto Agropecuario de Monte

Características del álbum:

* 204 figuritas numeradas del 1 al 204.
* Aproximadamente 150 alumnos participantes.
* Cada alumno recibe figuritas periódicamente.
* Se generan muchas repetidas.
* Actualmente los intercambios se organizan manualmente mediante grupos de WhatsApp.

Se busca una solución simple, rápida y accesible desde celular.

---

## Requisitos funcionales

### Registro de participante

Solicitar únicamente:

* Nombre y apellido del padre/madre/tutor.
* Nombre y apellido del alumno.
* Salita del alumno.

Ejemplo:

Padre/Madre:
Juan Pérez

Alumno:
Tomás Pérez

Salita:
Sala Blanca

La lista de salitas debe poder configurarse fácilmente.

Ejemplo:

* Sala Blanca
* Sala Verde
* Sala Roja

No implementar autenticación compleja.

Para el MVP basta con:

* Nombre del responsable.
* Nombre del alumno.
* Salita.

Opcionalmente generar un código único para futuras ediciones.

---

### Gestión de figuritas repetidas

La pantalla principal debe mostrar las 204 figuritas.

Representarlas mediante una grilla visual amigable.

Ejemplo:

1 2 3 4 5
6 7 8 9 10
...

Cada figurita debe poder marcarse o desmarcarse con un toque.

Estados:

* Gris = no registrada.
* Verde = figurita repetida disponible para intercambio.

El usuario solo registrará las figuritas repetidas.

No pedir que cargue todas las faltantes para evitar complejidad y abandono de uso.

---

### Búsqueda rápida de figuritas

Incluir una sección destacada llamada:

"Busco esta figurita"

El usuario ingresa un número.

Ejemplo:

87

Al presionar buscar, el sistema debe mostrar inmediatamente quién tiene esa figurita repetida.

Resultado esperado:

Figurita 87 disponible en:

* María González (Alumno: Mateo González - Sala Verde)
* Carlos López (Alumno: Sofía López - Sala Blanca)

Ordenar resultados por fecha de actualización más reciente.

---

### Motor de coincidencias

Generar una sección llamada:

"Posibles intercambios"

El sistema debe detectar coincidencias entre usuarios.

Ejemplo:

Juan Pérez tiene repetidas:
12, 45, 89

María González tiene repetidas:
5, 12, 77

Resultado:

Coincidencia encontrada:
Ambos poseen figuritas que podrían intercambiar.

Para el MVP no es necesario implementar optimización avanzada ni cadenas de intercambio.

Las coincidencias simples son suficientes.

---

### Vista por figurita

Permitir consultar cualquier figurita del álbum.

Ejemplo:

Figurita 45

Mostrar:

* Cantidad de usuarios que la poseen repetida.
* Quiénes la tienen.
* Alumno asociado.
* Salita correspondiente.

---

### Panel general

Crear una vista administrativa simple con:

* Cantidad total de participantes.
* Cantidad total de figuritas registradas.
* Figuritas más repetidas.
* Figuritas menos registradas.
* Figuritas sin registros.
* Últimas actualizaciones realizadas.
* Participantes por salita.

---

## Requisitos técnicos

### Backend

Utilizar:

* Python 3.12
* FastAPI

---

### Frontend

Preferentemente:

* HTML
* CSS
* JavaScript Vanilla

o

* HTMX

Evitar frameworks pesados.

Priorizar simplicidad y rapidez.

---

### Persistencia

NO utilizar base de datos para el MVP.

Utilizar archivos JSON.

Ejemplo:

data/participants.json

La aplicación debe:

* Crear archivos automáticamente.
* Guardar cambios automáticamente.
* Recuperar datos al reiniciar.

---

### Cantidad de figuritas repetidas

El sistema debe permitir registrar múltiples copias de una misma figurita.

Ejemplo:

Figurita 15 → Cantidad: 4
Figurita 87 → Cantidad: 3
Figurita 102 → Cantidad: 2

La interfaz debe ser simple y rápida.

Opciones aceptables:

* Un selector + y - para aumentar o disminuir la cantidad.
* Un campo numérico junto a cada figurita.
* Un clic para agregar y clics adicionales para incrementar la cantidad.

No limitar la cantidad de copias de una figurita.

---

### Búsquedas

Cuando un usuario busque una figurita, el sistema debe mostrar también la cantidad disponible.

Ejemplo:

Figurita 87 disponible en:

* María González (Alumno: Mateo González - Sala Verde) → 3 unidades
* Carlos López (Alumno: Sofía López - Sala Blanca) → 1 unidad

---

### Modelo de datos

Utilizar un diccionario donde la clave sea el número de figurita y el valor la cantidad disponible.

Ejemplo:

```json
{
  "id": "abc123",
  "responsable": "Juan Pérez",
  "alumno": "Tomás Pérez",
  "salita": "Sala Blanca",
  "figuritas_repetidas": {
    "15": 4,
    "87": 3,
    "102": 2
  },
  "fecha_actualizacion": "2026-06-11T10:30:00"
}
```

---

### Intercambios

Cuando se concrete un intercambio, el sistema deberá permitir descontar unidades del stock registrado.

Ejemplo:

Antes:

Figurita 87 = 3 unidades

Después de entregar una:

Figurita 87 = 2 unidades

---

### Estadísticas

Las estadísticas deben considerar cantidades reales y no solamente la existencia de una figurita.

Ejemplo:

Si 10 familias tienen la figurita 87 y cada una tiene 3 copias, el sistema debe contabilizar 30 unidades disponibles.

```
```
### Datos de contacto

Durante el registro solicitar:

* Nombre y apellido del padre/madre/tutor.
* Número de teléfono celular.
* Nombre y apellido del alumno.
* Salita.

Ejemplo:

Responsable:
Juan Pérez

Teléfono:
2226-123456

Alumno:
Tomás Pérez

Salita:
Sala Blanca

---

### Privacidad

Los datos de contacto solo deben mostrarse cuando un usuario consulta una figurita disponible.

No es necesario mostrar un listado completo de participantes.

---

### Resultado de búsqueda

Cuando un usuario busque una figurita, el sistema debe mostrar:

* Nombre del responsable.
* Nombre del alumno.
* Salita.
* Cantidad disponible.
* Teléfono de contacto.

Ejemplo:

Figurita 87 disponible en:

María González
Alumno: Mateo González
Sala: Verde
Cantidad: 3
Teléfono: 2226-555123

---

Carlos López
Alumno: Sofía López
Sala: Blanca
Cantidad: 1
Teléfono: 2226-888777

---

### Enlace rápido de contacto

Si el sistema detecta un número de celular válido, generar automáticamente un botón:

"Contactar"

Que abra:

https://wa.me/NUMERO

Ejemplo:

https://wa.me/5492226123456

El sistema no debe enviar mensajes automáticamente.

Solo debe facilitar el contacto entre las familias.


## Registro de participante

Solicitar únicamente:

* Nombre y apellido del padre/madre/tutor.
* Número de teléfono celular.
* Nombre y apellido del alumno.
* Salita.

Ejemplo:

Responsable:
Juan Pérez

Teléfono:
2226-123456

Alumno:
Tomás Pérez

Salita:
Sala Blanca

La lista de salitas debe poder configurarse fácilmente.

Ejemplo:

* Sala Blanca
* Sala Verde
* Sala Roja

No implementar autenticación compleja.

Para el MVP basta con:

* Nombre del responsable.
* Teléfono.
* Nombre del alumno.
* Salita.

Opcionalmente generar un código único para futuras ediciones.

---

## Gestión de figuritas repetidas

El álbum contiene 204 figuritas numeradas del 1 al 204.

La pantalla principal debe mostrar las 204 figuritas mediante una grilla visual amigable.

Ejemplo:

1 2 3 4 5
6 7 8 9 10
...

Cada figurita debe permitir registrar cantidad disponible.

No solamente indicar si la posee o no.

Ejemplos:

Figurita 15 → Cantidad: 4

Figurita 87 → Cantidad: 3

Figurita 102 → Cantidad: 2

Estados sugeridos:

* Gris = sin unidades registradas.
* Verde = una o más unidades disponibles.

La interfaz debe ser extremadamente simple.

Opciones aceptables:

* Botones + y -.
* Campo numérico.
* Toques sucesivos que incrementen la cantidad.

El usuario solo registrará figuritas repetidas.

No solicitar figuritas faltantes para minimizar la carga de datos.

---

## Pantalla inicial

La aplicación debe mostrar únicamente dos acciones principales:

### Buscar figurita

### Registrar mis figuritas

El objetivo es que cualquier padre pueda utilizar la aplicación en menos de 10 segundos.

---

## Búsqueda rápida de figuritas

Incluir una sección destacada llamada:

"Busco esta figurita"

El usuario ingresa un número entre 1 y 204.

Ejemplo:

87

Al presionar Buscar, el sistema debe mostrar inmediatamente quién posee esa figurita disponible.

Resultado esperado:

Figurita 87 disponible en:

María González
Alumno: Mateo González
Sala: Verde
Cantidad disponible: 3
Teléfono: 2226-555123

[Contactar]

---

Carlos López
Alumno: Sofía López
Sala: Blanca
Cantidad disponible: 1
Teléfono: 2226-888777

---

## Datos de contacto


Los datos de contacto solo deben mostrarse cuando un usuario consulta una figurita disponible.

No mostrar un listado general de teléfonos ni participantes.

---

## Enlace rápido de contacto

Cuando exista un teléfono válido, generar automáticamente un botón:

"Contactar"

Que abra:

https://wa.me/NUMERO

Ejemplo:

https://wa.me/5492226123456

La aplicación no debe enviar mensajes automáticamente.

Simplemente facilitar el contacto entre familias.

---

## Motor de coincidencias

Generar una sección llamada:

"Posibles intercambios"

El sistema debe detectar coincidencias simples entre participantes que posean figuritas repetidas.

No es necesario implementar optimización avanzada ni cadenas de intercambio para el MVP.

---

## Vista por figurita

Permitir consultar cualquier figurita del álbum.

Mostrar:

* Número de figurita.
* Cantidad total de unidades registradas.
* Cantidad de participantes que la poseen.
* Listado de responsables.
* Nombre del alumno.
* Salita.
* Cantidad disponible por participante.

---

## Estadísticas

Las estadísticas deben considerar cantidades reales.

Ejemplo:

Si 10 familias registraron la figurita 87 y cada una tiene 3 unidades:

Total disponible = 30 unidades

Mostrar:

* Participantes registrados.
* Figuritas más repetidas.
* Figuritas menos registradas.
* Figuritas sin registros.
* Cantidad total de figuritas cargadas.
* Participantes por salita.
* Últimas actualizaciones.

---

## Modelo de datos sugerido

```json
{
  "id": "abc123",
  "responsable": "Juan Pérez",
  "telefono": "2226123456",
  "alumno": "Tomás Pérez",
  "salita": "Sala Blanca",
  "figuritas_repetidas": {
    "15": 4,
    "87": 3,
    "102": 2
  },
  "fecha_actualizacion": "2026-06-11T10:30:00"
}
```

---

## Diseño visual

La aplicación será utilizada por familias del:

IAM Instituto Agropecuario de Monte

Debe incluir:

* Diseño responsive.
* Compatibilidad con Android e iPhone.
* Botones grandes.
* Tipografía legible.
* Colores amigables.
* Estética inspirada en álbumes de figuritas y fútbol.

La prioridad absoluta es la simplicidad de uso desde el celular.

---

## Objetivo principal

Permitir que cualquier familia pueda:

1. Registrar sus figuritas repetidas en menos de un minuto.
2. Buscar una figurita en menos de 10 segundos.
3. Encontrar quién la tiene disponible.
4. Contactar a esa familia directamente.
5. Coordinar el intercambio fuera de la aplicación.


### Modelo de datos sugerido

```json
{
  "id": "abc123",
  "responsable": "Juan Pérez",
  "alumno": "Tomás Pérez",
  "salita": "Sala Blanca",
  "figuritas_repetidas": [12, 45, 89],
  "fecha_actualizacion": "2026-06-11T10:30:00"
}
```

---

## Diseño UX

El usuario promedio tiene conocimientos técnicos nulos.

La interfaz debe:

* Funcionar perfectamente desde celular.
* Tener botones grandes.
* Tener números fáciles de tocar.
* Tener navegación simple.
* Minimizar la cantidad de clics.
* Permitir registrar figuritas repetidas en menos de un minuto.

La experiencia debe sentirse similar a marcar casillas en una planilla visual.

---

## Diseño visual

Inspiración:

* Álbum de figuritas.
* Mundial de fútbol.
* Diseño amigable para familias.

Incluir:

* Logo o encabezado con el nombre:
  "IAM Instituto Agropecuario de Monte"
* Diseño responsive.
* Colores agradables.
* Compatibilidad con Android e iPhone.

---

## Extras deseables

Si el tiempo lo permite:

* Exportar participantes a CSV.
* Filtrar participantes por salita.
* Compartir enlace directo a una figurita buscada.
* Generar ranking de figuritas más difíciles de conseguir.

---

## Entregables

Generar:

1. Estructura completa del proyecto.
2. Backend FastAPI.
3. Modelos de datos.
4. Persistencia JSON.
5. Pantallas HTML.
6. CSS responsive.
7. Motor de búsqueda de figuritas.
8. Motor de coincidencias.
9. Datos de prueba.
10. Instrucciones de instalación.
11. Código listo para ejecutar con:

uvicorn main:app --reload

El resultado debe ser un MVP funcional, simple de mantener, fácil de desplegar y preparado para crecer en futuras versiones.

###repositorio
https://github.com/rodolforeyes-dev/figuritas-iam.git
