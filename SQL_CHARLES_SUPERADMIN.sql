-- SQL PARA CREAR CHARLES JÉLVEZ COMO SUPERADMIN
-- Proyecto: Sistema de Cámaras UFRO
-- Ejecutar en base de datos PostgreSQL de Railway

-- SQL para crear Charles Jélvez como SUPERADMIN
-- Ejecutar en la base de datos PostgreSQL de Railway

-- Opción 1: INSERT con ON CONFLICT (recomendado)
INSERT INTO usuario (
    username, 
    password_hash, 
    rol, 
    activo, 
    email, 
    nombre_completo, 
    created_at
) VALUES (
    'charles.jelvez',
    '$2b$12$LKGWq7tCl.qLV8JZKUZ5VOH4BFY8o8J8HFVvNJZJX4k4PUZ2KrnGG',
    'superadmin',
    true,
    'charles.jelvez@ufro.cl',
    'Charles Jélvez',
    NOW()
) ON CONFLICT (username) 
DO UPDATE SET
    password_hash = EXCLUDED.password_hash,
    rol = EXCLUDED.rol,
    activo = EXCLUDED.activo,
    email = EXCLUDED.email,
    nombre_completo = EXCLUDED.nombre_completo;

-- Verificar que el usuario se creó/actualizó correctamente
SELECT 
    username,
    rol,
    activo,
    email,
    nombre_completo,
    created_at
FROM usuario 
WHERE username = 'charles.jelvez';