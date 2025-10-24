-- ============================================================
-- SCRIPT SQL DIRECTO PARA CREAR CHARLES JÉLVEZ COMO SUPERADMIN
-- ============================================================
-- Ejecutar directamente en la base de datos PostgreSQL de Railway
-- URL: https://gestion-camaras-ufro.up.railway.app/
-- Este script crea el usuario sin depender del deploy de Flask

-- Verificar si Charles ya existe
DO $$
DECLARE
    user_exists boolean;
BEGIN
    -- Verificar si existe el usuario
    SELECT EXISTS(SELECT 1 FROM usuario WHERE username = 'charles.jelvez') INTO user_exists;
    
    IF user_exists THEN
        -- Si existe, actualizar rol y contraseña
        UPDATE usuario 
        SET 
            password_hash = '$2b$12$LKGWq7tCl.qLV8JZKUZ5VOH4BFY8o8J8HFVvNJZJX4k4PUZ2KrnGG', -- hash de 'charles123'
            rol = 'superadmin',
            activo = true,
            email = 'charles.jelvez@ufro.cl',
            nombre_completo = 'Charles Jélvez'
        WHERE username = 'charles.jelvez';
        
        RAISE NOTICE 'Usuario Charles actualizado como SUPERADMIN';
    ELSE
        -- Si no existe, crear nuevo usuario
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
            '$2b$12$LKGWq7tCl.qLV8JZKUZ5VOH4BFY8o8J8HFVvNJZJX4k4PUZ2KrnGG', -- hash de 'charles123'
            'superadmin',
            true,
            'charles.jelvez@ufro.cl',
            'Charles Jélvez',
            NOW()
        );
        
        RAISE NOTICE 'Usuario Charles Jélvez creado como SUPERADMIN';
    END IF;
END
$$;

-- Verificar el resultado
SELECT 
    username,
    rol,
    activo,
    email,
    nombre_completo,
    created_at
FROM usuario 
WHERE username = 'charles.jelvez';

-- ============================================================
-- CREDENCIALES PARA LOGIN:
-- Usuario: charles.jelvez
-- Contraseña: charles123
-- Rol: superadmin
-- ============================================================