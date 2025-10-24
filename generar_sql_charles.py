#!/usr/bin/env python3
"""
Script simplificado para crear usuario Charles Jélvez como SUPERADMIN
Usa la aplicación Flask directamente para crear el usuario
"""

import os
import sys
import hashlib

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_password_hash(password):
    """Crear hash de contraseña usando Werkzeug"""
    # Simular el hash de Flask/Werkzeug
    import werkzeug.security
    return werkzeug.security.generate_password_hash(password)

def main():
    print("=" * 60)
    print("🚀 CREACIÓN DE USUARIO CHARLES JÉLVEZ - SUPERADMIN")
    print("=" * 60)
    
    # Crear hash de la contraseña
    password_hash = create_password_hash('charles123')
    print(f"✅ Hash de contraseña generado")
    
    # Información del usuario Charles
    charles_data = {
        'username': 'charles.jelvez',
        'password_hash': password_hash,
        'rol': 'superadmin',
        'activo': True,
        'email': 'charles.jelvez@ufro.cl',
        'nombre_completo': 'Charles Jélvez'
    }
    
    print("\n📋 DATOS DEL USUARIO:")
    for key, value in charles_data.items():
        print(f"   {key}: {value}")
    
    print("\n💾 SQL GENERADO PARA EJECUTAR EN RAILWAY:")
    print("=" * 60)
    
    sql_script = f"""
-- Crear/Actualizar usuario Charles Jélvez como SUPERADMIN
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

-- Verificar resultado
SELECT username, rol, activo, email, nombre_completo 
FROM usuario 
WHERE username = 'charles.jelvez';
"""
    
    print(sql_script)
    
    print("\n🎯 INSTRUCCIONES PARA EJECUTAR:")
    print("1. Acceder al dashboard de Railway")
    print("2. Ir a la sección Database")
    print("3. Abrir psql o la interfaz de consultas")
    print("4. Ejecutar el SQL mostrado arriba")
    print("5. Verificar que el usuario se creó correctamente")
    
    print("\n🔐 CREDENCIALES FINALES:")
    print("   Usuario: charles.jelvez")
    print("   Contraseña: charles123")
    print("   Rol: superadmin")
    print("   URL: https://gestion-camaras-ufro.up.railway.app/")
    
    # Guardar SQL en archivo
    with open('/workspace/sistema-camaras-flask/charles_superadmin_sql_final.sql', 'w') as f:
        f.write("-- SQL FINAL PARA CREAR CHARLES JÉLVEZ COMO SUPERADMIN\n")
        f.write("-- Ejecutar en la base de datos PostgreSQL de Railway\n\n")
        f.write(sql_script)
    
    print(f"\n💾 SQL guardado en: charles_superadmin_sql_final.sql")

if __name__ == "__main__":
    main()