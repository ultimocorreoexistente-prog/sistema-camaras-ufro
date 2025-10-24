-- ====================================================================================
-- SQL PARA CREAR CHARLES JÉLVEZ COMO SUPERADMIN EN RAILWAY POSTGRESQL
-- Proyecto: Sistema de Cámaras UFRO
-- Instrucciones: Ejecutar en la consola de Railway PostgreSQL
-- ====================================================================================

-- INSTRUCCIONES PARA CHARLES JÉLVEZ:
-- 1. Ve a Railway dashboard → Proyecto "gestion-camaras-ufro" → Database
-- 2. Click en "Connect" → "Postgres CLI" 
-- 3. Copia y pega cada comando de abajo uno por uno
-- 4. Confirma que veas los mensajes de éxito
-- ====================================================================================

-- CÓDIGO SQL LISTO PARA EJECUTAR (copia y pega en la consola de Railway):
-- ====================================================================================

-- PASO 1: Crear Charles como SUPERADMIN (INSERT con ON CONFLICT para actualizar si ya existe)
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

-- PASO 2: Verificar que Charles se creó correctamente
SELECT 
    username,
    rol,
    activo,
    email,
    nombre_completo,
    created_at
FROM usuario 
WHERE username = 'charles.jelvez';

-- ====================================================================================
-- CREDENCIALES PARA CHARLES JÉLVEZ:
-- Usuario: charles.jelvez
-- Contraseña: charles123
-- URL: https://gestion-camaras-ufro.up.railway.app/
-- Rol: SUPERADMIN (acceso completo a todas las funciones)
-- ====================================================================================