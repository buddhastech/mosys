CREATE DATABASE MOCIS;
USE MOCIS;
DROP DATABASE MOCIS;
INSERT INTO tipo_de_usuarios (nombre_del_tipo) VALUES ("Administrador");
INSERT INTO usuarios (usuario_cedula_pkey,
nombre,
apellido_paterno,
apellido_materno,
correo,
telefono,
contraseña,
estado) VALUES ("702660191",
"Diego",
"Duarte",
"Fernández",
"diegoduarte8343@gmail.com",
"64832448",
"slipknot83",
1);

SELECT * FROM usuarios;
