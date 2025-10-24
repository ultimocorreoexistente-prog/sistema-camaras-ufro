#!/usr/bin/env python3
"""
Generar hash correcto con Werkzeug y actualizar Charles Jélvez
"""

import psycopg2
from werkzeug.security import generate_password_hash

def generar_hash_werkzeug():
    """Generar hash usando el mismo método que la aplicación"""
    password = "charles123"
    hash_werkzeug = generate_password_hash(password, method='pbkdf2:sha256')
    print(f"🔐 Password: {password}")
    print(f"🔑 Hash Werkzeug: {hash_werkzeug}")
    return hash_werkzeug

def conectar_y_actualizar(hash_correcto):
    """Conectar a BD y actualizar hash de Charles"""
    DATABASE_URL = "postgresql://postgres:WMQxvzTQsdkiAUOqfMgXmzgAHqxDkwRJ@tramway.proxy.rlwy.net:34726/railway"
    
    try:
        print("🔌 Conectando a la base de datos...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Obtener hash actual de Charles
        cursor.execute("SELECT username, password_hash FROM usuario WHERE username = 'charles.jelvez';")
        charles = cursor.fetchone()
        
        if charles:
            username, hash_actual = charles
            print(f"📊 Hash actual de {username}:")
            print(f"   {hash_actual}")
            
            # Actualizar con hash de Werkzeug
            cursor.execute("""
                UPDATE usuario 
                SET password_hash = %s 
                WHERE username = %s;
            """, (hash_correcto, username))
            
            conn.commit()
            print("✅ Hash actualizado exitosamente")
            
            # Verificar cambio
            cursor.execute("SELECT username, password_hash FROM usuario WHERE username = %s;", (username,))
            charles_nuevo = cursor.fetchone()
            
            if charles_nuevo:
                username_nuevo, hash_nuevo = charles_nuevo
                print(f"✅ Hash confirmado:")
                print(f"   {hash_nuevo}")
                
        else:
            print("❌ Usuario Charles no encontrado")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

def main():
    print("🔧 CORRECCIÓN DE HASH CHARLES - WERkzeug")
    print("=" * 50)
    
    # Generar hash correcto con Werkzeug
    hash_correcto = generar_hash_werkzeug()
    
    print("\n" + "=" * 50)
    print("🔄 Actualizando en base de datos...")
    
    # Actualizar en base de datos
    conectar_y_actualizar(hash_correcto)
    
    print("\n✅ Proceso completado")
    print("\n🔑 CREDENCIALES ACTUALIZADAS:")
    print("   Usuario: charles.jelvez")
    print("   Contraseña: charles123")
    print("   Hash: Werkzeug (compatible con aplicación)")

if __name__ == "__main__":
    main()