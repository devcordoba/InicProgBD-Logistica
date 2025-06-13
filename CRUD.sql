-- Crear (Dar de alta un usuario)
INSERT INTO Usuarios (nombre, email, contrasena, id_rol)
VALUES ('Lucía Ramos', 'lucia@example.com', SHA2('clave123', 256), 2);

-- Leer (Ver todos los usuarios)
SELECT u.id_usuario, u.nombre, u.email, r.nombre AS rol
FROM Usuarios u
JOIN Roles r ON u.id_rol = r.id_rol;

-- Actualizar (Cambiar nombre a usuario)
UPDATE Usuarios SET nombre = 'Lucía R.' WHERE id_usuario = 1;

-- Actualizar (Cambiar rol a usuario)
UPDATE Usuarios SET id_rol = 1 WHERE id_usuario = 1;

-- Eliminar (Borrar un usuario)
DELETE FROM Usuarios WHERE id_usuario = 1;