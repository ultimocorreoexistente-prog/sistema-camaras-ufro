#!/usr/bin/env python3
"""
Generador de SQL para crear usuario Charles Jélvez como SUPERADMIN
Versión sin dependencias externas
"""

def main():
    print("=" * 60)
    print("🚀 GENERADOR SQL - CHARLES JÉLVEZ SUPERADMIN")
    print("=" * 60)
    
    # Hash pre-computado para 'charles123' (bcrypt)
    password_hash = "$2b$12$LKGWq7tCl.qLV8JZKUZ5VOH4BFY8o8J8HFVvNJZJX4k4PUZ2KrnGG"
    
    print("📋 INFORMACIÓN DEL USUARIO:")
    print("   Username: charles.jelvez")
    print("   Password: charles123")
    print("   Rol: superadmin")
    print("   Email: charles.jelvez@ufro.cl")
    print("   Nombre: Charles Jélvez")
    
    print("\n💾 SQL PARA EJECUTAR EN RAILWAY POSTGRESQL:")
    print("=" * 60)
    
    sql_script = f"""-- SQL para crear Charles Jélvez como SUPERADMIN
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
    '{password_hash}',
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
WHERE username = 'charles.jelvez';"""
    
    print(sql_script)
    
    print("\n" + "=" * 60)
    print("🎯 PASOS PARA EJECUTAR:")
    print("1. Ir a https://railway.app/dashboard")
    print("2. Seleccionar proyecto 'gestion-camaras-ufro'")
    print("3. Ir a la sección 'Database'")
    print("4. Hacer click en 'Connect' o abrir psql")
    print("5. Copiar y ejecutar el SQL de arriba")
    print("6. Verificar que el SELECT muestre el usuario")
    
    print("\n🔐 CREDENCIALES FINALES:")
    print("   URL: https://gestion-camaras-ufro.up.railway.app/")
    print("   Usuario: charles.jelvez")
    print("   Contraseña: charles123")
    print("   Rol: superadmin")
    
    # Guardar en archivo
    filename = '/workspace/sistema-camaras-flask/SQL_CHARLES_SUPERADMIN.sql'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("-- SQL PARA CREAR CHARLES JÉLVEZ COMO SUPERADMIN\n")
        f.write("-- Proyecto: Sistema de Cámaras UFRO\n")
        f.write("-- Ejecutar en base de datos PostgreSQL de Railway\n\n")
        f.write(sql_script)
    
    print(f"\n💾 SQL guardado en: {filename}")
    print("\n✅ ¡SQL listo para ejecutar!")

if __name__ == "__main__":
    main()