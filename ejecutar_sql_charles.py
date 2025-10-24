#!/usr/bin/env python3
"""
Script para ejecutar SQL directo y crear usuario Charles Jélvez como SUPERADMIN
Este script se conecta directamente a la base de datos PostgreSQL de Railway
"""

import psycopg2
import os
import sys

def get_railway_db_url():
    """Obtiene la URL de la base de datos Railway desde las variables de entorno"""
    
    # Railway typically provides DATABASE_URL
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        # Buscar variables alternativas comunes en Railway
        for var in ['PGDATABASE', 'POSTGRES_URL', 'DATABASE_CONNECTION']:
            if var in os.environ:
                database_url = os.environ[var]
                break
    
    if not database_url:
        print("❌ ERROR: No se encontró URL de base de datos en variables de entorno")
        print("Variables disponibles:")
        for key, value in os.environ.items():
            if 'DATABASE' in key.upper() or 'PG' in key.upper() or 'RAILWAY' in key.upper():
                print(f"  {key}: {value[:50]}...")
        return None
    
    print(f"✅ URL de base de datos encontrada: {database_url[:50]}...")
    return database_url

def create_charles_superadmin():
    """Conecta a la base de datos y crea/actualiza usuario Charles como SUPERADMIN"""
    
    # Obtener URL de base de datos
    db_url = get_railway_db_url()
    if not db_url:
        return False
    
    # SQL para crear/actualizar usuario Charles
    sql_script = """
    -- Verificar si Charles ya existe y crear/actualizar
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
                password_hash = '$2b$12$LKGWq7tCl.qLV8JZKUZ5VOH4BFY8o8J8HFVvNJZJX4k4PUZ2KrnGG',
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
                '$2b$12$LKGWq7tCl.qLV8JZKUZ5VOH4BFY8o8J8HFVvNJZJX4k4PUZ2KrnGG',
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
    """
    
    try:
        # Conectar a la base de datos
        print("🔌 Conectando a la base de datos Railway...")
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        print("📝 Ejecutando script SQL...")
        cursor.execute(sql_script)
        
        # Obtener resultados
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        
        # Confirmar cambios
        conn.commit()
        print("✅ Cambios confirmados en la base de datos")
        
        # Mostrar resultado
        print("\n📊 RESULTADO:")
        print("-" * 50)
        if results:
            for row in results:
                for i, col_name in enumerate(column_names):
                    print(f"{col_name}: {row[i]}")
                print("-" * 30)
        else:
            print("❌ No se encontraron resultados")
        
        # Cerrar conexión
        cursor.close()
        conn.close()
        
        print("\n🎉 ¡Usuario Charles Jélvez configurado como SUPERADMIN!")
        print("📋 CREDENCIALES:")
        print("   Usuario: charles.jelvez")
        print("   Contraseña: charles123")
        print("   Rol: superadmin")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR al conectar/ejecutar SQL: {str(e)}")
        return False

def test_login():
    """Prueba el login con las credenciales de Charles"""
    print("\n🧪 PROBANDO LOGIN...")
    
    # Crear instancia temporal de la app para probar login
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        from app import app, Usuario, db
        
        with app.app_context():
            # Buscar usuario Charles
            charles = Usuario.query.filter_by(username='charles.jelvez').first()
            
            if charles:
                print(f"✅ Usuario encontrado: {charles.username}")
                print(f"   Rol: {charles.rol}")
                print(f"   Activo: {charles.activo}")
                
                # Probar contraseña
                if charles.check_password('charles123'):
                    print("✅ Contraseña correcta")
                    print("🎉 LOGIN EXITOSO - Charles puede acceder al sistema")
                else:
                    print("❌ Contraseña incorrecta")
            else:
                print("❌ Usuario Charles no encontrado en la base de datos")
                
    except Exception as e:
        print(f"❌ Error al probar login: {str(e)}")

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 EJECUTOR SQL DIRECTO - CHARLES JÉLVEZ SUPERADMIN")
    print("=" * 60)
    
    # Crear usuario Charles
    success = create_charles_superadmin()
    
    if success:
        # Probar login si es posible
        test_login()
        
        print("\n🔗 PRÓXIMOS PASOS:")
        print("1. Acceder a https://gestion-camaras-ufro.up.railway.app/")
        print("2. Hacer login con:")
        print("   Usuario: charles.jelvez")
        print("   Contraseña: charles123")
        print("3. Verificar acceso como SUPERADMIN")
    else:
        print("\n❌ No se pudo completar la configuración")
        print("💡 Revisa las variables de entorno de la base de datos")