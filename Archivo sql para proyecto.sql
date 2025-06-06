CREATE DATABASE IF NOT EXISTS gestion;

USE gestion;

CREATE TABLE IF NOT EXISTS rol (
    id_rol INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    contrasena VARCHAR(64),
    id_rol INT,
    FOREIGN KEY (id_rol) REFERENCES rol(id_rol)
);

CREATE TABLE IF NOT EXISTS pedido (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    descripcion TEXT,
    estado ENUM('Pendiente', 'Despachado') DEFAULT 'Pendiente',
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

CREATE TABLE IF NOT EXISTS movimiento (
    id_movimiento INT AUTO_INCREMENT PRIMARY KEY,
    id_pedido INT,
    tipo ENUM('Ingreso','Despacho'),
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido)
);

INSERT INTO rol (nombre) VALUES ('admin'), ('usuario')
ON DUPLICATE KEY UPDATE nombre = nombre;

INSERT INTO usuario (nombre, email, contrasena, id_rol)
VALUES 
  ('Admin', 'admin@abc.com', SHA2('admin123', 256), (SELECT id_rol FROM rol WHERE nombre = 'admin')),
  ('Juan', 'juan@abc.com', SHA2('user123', 256), (SELECT id_rol FROM rol WHERE nombre = 'usuario'))
ON DUPLICATE KEY UPDATE email = email;