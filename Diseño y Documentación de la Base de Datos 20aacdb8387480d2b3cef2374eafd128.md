# Diseño y Documentación de la Base de Datos

## Entidades Principales

Tras analizar el sistema, se identifican las siguientes entidades clave:

- **Usuario**: representa a los individuos que interactúan con el sistema.
- **Rol**: determina los permisos y el nivel de acceso del usuario.
- **Pedido**: solicitud generada por un usuario.
- **Movimiento**: registro de eventos asociados a un pedido (ingreso, despacho).

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

### *Pedidos*

- `id_pedido`: Identificador del pedido.
- `id_usuario`: Usuario que realiza el pedido.
- `fecha`: Fecha y hora de creación.
- `estado`: Estado actual (`Pendiente`, `Despachado`).
- `descripcion`: Detalles del pedido.

### *Movimientos*

- `id_movimiento`: Identificador del evento.
- `id_pedido`: Pedido relacionado.
- `tipo`: Tipo de movimiento (`Ingreso`, `Despacho`).
- `fecha`: Momento en que ocurre el evento.

## Relaciones Entre Entidades

- **Usuario ↔ Rol**: relación de uno a muchos (1 Rol puede ser asignado a varios Usuarios).
- **Usuario ↔ Pedido**: un Usuario puede generar múltiples Pedidos (relación 1:N).
- **Pedido ↔ Movimiento**: cada Pedido puede registrar varios Movimientos (relación 1:N).

## Normalización

El modelo fue normalizado hasta **Tercera Forma Normal (3FN)** para evitar redundancias y dependencias innecesarias:

- Todos los atributos son atómicos (1FN).
- Se eliminaron dependencias parciales (2FN).
- Se eliminaron dependencias transitivas, separando responsabilidades conceptuales en distintas tablas (3FN).

## Diagrama Modelo Entidad Relación

![Diagrama Modelo Relacional](diagrams/DiagramaModeloRelacional.drawio.svg)

## Modelo Relacional

```sql
CREATE TABLE Roles (
    id_rol INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE Usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    contrasena CHAR(64) NOT NULL,
    id_rol INT NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES Roles(id_rol)
);

CREATE TABLE Pedidos (
    id_pedido INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('Pendiente', 'Despachado') DEFAULT 'Pendiente',
    descripcion TEXT,
    FOREIGN KEY (id_usuario) REFERENCES Usuarios(id_usuario)
);

CREATE TABLE Movimientos (
    id_movimiento INT PRIMARY KEY AUTO_INCREMENT,
    id_pedido INT NOT NULL,
    tipo ENUM('Ingreso', 'Despacho') NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_pedido) REFERENCES Pedidos(id_pedido)
);
```

## Diagrama Entidad Relacion

![Diagrama Entidad-Relación](diagrams/DiagramaER.drawio.svg)

## Consideraciones de Diseño

- **Roles en tabla separada**: mejora la escalabilidad y evita errores de tipeo o inconsistencias.
- **Contraseñas hasheadas**: se aplica SHA-256 antes del almacenamiento.
- **Estados y tipos controlados con ENUM**: garantiza integridad en campos críticos.
- **Movimientos sin ID de usuario**: no se incluye, ya que no se requería en la lógica original; puede agregarse si se desea mayor trazabilidad.

## CRUD de Usuario en SQL

### *Crear*

```sql
INSERT INTO Usuarios (nombre, email, contrasena, id_rol)
VALUES ('Lucía Ramos', 'lucia@example.com', SHA2('clave123', 256), 2);

```

### *Leer*

```sql
SELECT u.id_usuario, u.nombre, u.email, r.nombre AS rol
FROM Usuarios u
JOIN Roles r ON u.id_rol = r.id_rol;
```

### *Actualizar Nombre*

```sql
UPDATE Usuarios
SET nombre = 'Lucía R.'
WHERE id_usuario = 1;
```

### *Cambiar Contraseña*

```sql
UPDATE Usuarios
SET contrasena = SHA2('nuevaclave', 256)
WHERE id_usuario = 1;
```

### *Cambiar Rol*

```sql
UPDATE Usuarios
SET id_rol = 1
WHERE id_usuario = 1;
```

### *Eliminar*

```sql
DELETE FROM Usuarios
WHERE id_usuario = 1;
```

## Script Completo – Creación de Base de Datos

```sql
CREATE DATABASE IF NOT EXISTS sistema_pedidos;
USE sistema_pedidos;

CREATE TABLE Roles (
    id_rol INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE Usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    contrasena CHAR(64) NOT NULL,
    id_rol INT NOT NULL,
    FOREIGN KEY (id_rol) REFERENCES Rol(id_rol)
);

CREATE TABLE Pedidos (
    id_pedido INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('Pendiente', 'Despachado') DEFAULT 'Pendiente',
    descripcion TEXT,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

CREATE TABLE Movimientos (
    id_movimiento INT PRIMARY KEY AUTO_INCREMENT,
    id_pedido INT NOT NULL,
    tipo ENUM('Ingreso', 'Despacho') NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_pedido) REFERENCES Pedido(id_pedido)
);

-- Carga inicial de roles
INSERT INTO roles (nombre) VALUES ('admin'), ('usuario')
ON DUPLICATE KEY UPDATE nombre = nombre;

-- Carga inicial de usuarios
INSERT INTO usuarios (nombre, email, contrasena, id_rol)
VALUES 
  ('Admin', 'admin@abc.com', SHA2('admin123', 256), (SELECT id_rol FROM roles WHERE nombre = 'admin')),
  ('Juan', 'juan@abc.com', SHA2('user123', 256), (SELECT id_rol FROM roles WHERE nombre = 'usuario'))
ON DUPLICATE KEY UPDATE email = email;
```