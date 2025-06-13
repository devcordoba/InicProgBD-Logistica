CREATE DATABASE IF NOT EXISTS sistema_comisions;
USE sistema_comisions;

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

CREATE TABLE Comisiones (
    id_comision INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('Pendiente', 'Despachado') DEFAULT 'Pendiente',
    descripcion TEXT,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
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