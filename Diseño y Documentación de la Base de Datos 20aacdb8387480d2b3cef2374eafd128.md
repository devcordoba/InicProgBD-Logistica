# Diseño y Documentación de la Base de Datos

## Entidades Principales

Tras analizar el sistema, se identifican las siguientes entidades clave:

- **Usuario**: representa a los individuos que interactúan con el sistema.
- **Rol**: determina los permisos y el nivel de acceso del usuario.
- **Comision**: solicitud generada por un usuario.

## Atributos de Cada Entidad

### *Usuarios*

- `id_usuario`: Identificador único.
- `nombre`: Nombre completo del usuario.
- `email`: Dirección de correo (única).
- `contrasena`: Hash de la contraseña (SHA-256).
- `id_rol`: Referencia al rol asignado.

### *Roles*

- `id_rol`: Clave primaria.
- `nombre`: Nombre del rol (ej. `admin`, `usuario`).

### *Comisiones*

- `id_comision`: Identificador de la comisión.
- `id_usuario`: Usuario que realiza la comisión.
- `fecha`: Fecha y hora de creación.
- `estado`: Estado actual (`Pendiente`, `Despachado`).
- `descripcion`: Detalles.

## Relaciones Entre Entidades

- **Usuario ↔ Rol**  
  Relación de **uno a muchos**.  
  Cada *Rol* puede estar asociado a varios *Usuarios*, pero cada *Usuario* tiene asignado solo un *Rol*.  
  _(Representación: `Usuarios }o--|| Roles`)_

- **Usuario ↔ Comisión**  
  Relación de **uno a muchos**.  
  Un *Usuario* puede registrar múltiples *Comisiones*, pero cada *Comisión* pertenece a un único *Usuario*.  
  _(Representación: `Usuarios ||--o{ Comisiones`)_

## Normalización

El modelo fue normalizado hasta **Tercera Forma Normal (3FN)** para evitar redundancias y dependencias innecesarias:

- Todos los atributos son atómicos (1FN).
- Se eliminaron dependencias parciales (2FN).
- Se eliminaron dependencias transitivas, separando responsabilidades conceptuales en distintas tablas (3FN).

## Modelo Relacional

![Diagrama Modelo Relacional](diagrams/Diagrama-relacional.png)


## Diagrama DER

![Diagrama Entidad-Relación](diagrams/DiagramaEntidadRelacion.drawio.jpeg)

## Consideraciones de Diseño

- **Roles en tabla separada**: mejora la escalabilidad y evita errores de tipeo o inconsistencias.
- **Contraseñas hasheadas**: se aplica SHA-256 antes del almacenamiento.
- **Estados y tipos controlados con ENUM**: garantiza integridad en campos críticos.
- **Movimientos sin ID de usuario**: no se incluye, ya que no se requería en la lógica original; puede agregarse si se desea mayor trazabilidad.

## Diagrama de clases


![Diagrama de clases](diagrams/diagrama-clases.png)