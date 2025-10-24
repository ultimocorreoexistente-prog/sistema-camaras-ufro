-- SISTEMA COMPLETO DE USUARIOS Y ROLES
-- Generación: 2025-10-24 22:25:37
-- Correos actualizados a @ufrontera.cl

-- Limpiar tabla de usuarios completamente
TRUNCATE TABLE usuario RESTART IDENTITY CASCADE;

-- Crear usuarios con roles y permisos
INSERT INTO usuario (username, password_hash, rol, nombre_completo, email, activo, fecha_creacion)
VALUES ('charles.jelvez', 'pbkdf2:sha256:1000000$7d6451a5d0ffff3352524132761f2024$75d1a09870f58e7bca3701574b065345da26bd6c49a0ea3b2b5f925ac4fe521f', 'superadmin', 'Charles Jélvez', 'charles.jelvez@ufrontera.cl', true, NOW());

INSERT INTO usuario (username, password_hash, rol, nombre_completo, email, activo, fecha_creacion)
VALUES ('admin', 'pbkdf2:sha256:1000000$84dd50328b5686e330934dc62963303a$462b026a7a49a85cd3551934a3177895c172e9987a5391ab5c99740885ed7a21', 'admin', 'Administrador Principal', 'admin@ufrontera.cl', true, NOW());

INSERT INTO usuario (username, password_hash, rol, nombre_completo, email, activo, fecha_creacion)
VALUES ('supervisor', 'pbkdf2:sha256:1000000$c27c81b541d3a1dcb4688ee40c2c6bff$fb3d7cf30a77425be1468e849c8241248121b5fcd56f809501afe4505ee2f9e0', 'supervisor', 'Supervisor General', 'supervisor@ufrontera.cl', true, NOW());

INSERT INTO usuario (username, password_hash, rol, nombre_completo, email, activo, fecha_creacion)
VALUES ('tecnico1', 'pbkdf2:sha256:1000000$74b68275edf4c5b327111d74c5efbe31$db4486b0844ce6df4750bf5c966c3309b25f47d035da6cf3f035da57af65607d', 'tecnico', 'Técnico Principal', 'tecnico@ufrontera.cl', true, NOW());

INSERT INTO usuario (username, password_hash, rol, nombre_completo, email, activo, fecha_creacion)
VALUES ('visualizador', 'pbkdf2:sha256:1000000$e3c67d501499dda6b44431b2c3992f0a$e62efa69faa8174c8c76657c30e48bb34013a08c4f8631a51b9505e749c3b873', 'visualizador', 'Visualizador', 'visualizador@ufrontera.cl', true, NOW());

-- Verificar usuarios creados
SELECT username, rol, nombre_completo, email, activo FROM usuario ORDER BY rol, username;