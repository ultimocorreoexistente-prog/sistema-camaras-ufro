"""Script para limpiar todas las tablas de la base de datos Railway antes de migrar"""
import psycopg2
import os

# URL de conexión a Railway
DATABASE_URL = "postgresql://postgres:WMQxvzTQsdkiAUOqfMgXmzgAHqxDkwRJ@tramway.proxy.rlwy.net:34726/railway"

print("=== LIMPIANDO BASE DE DATOS RAILWAY ===")
print("\n⚠️  ADVERTENCIA: Se eliminarán TODOS los datos de las tablas\n")

try:
    # Conectar a la base de datos
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Lista de tablas en orden de dependencias (primero las que tienen FK)
    tablas = [
        'falla',
        'mantenimiento',
        'camara',
        'puerto_switch',
        'switch',
        'nvr_dvr',
        'fuente_poder',
        'ups',
        'gabinete',
        'catalogo_tipo_falla',
        'equipo_tecnico',
        'ubicacion',
        'usuario'
    ]
    
    print("Eliminando datos de las tablas...\n")
    
    # Deshabilitar temporalmente las restricciones de FK
    cur.execute("SET session_replication_role = 'replica';")
    
    for tabla in tablas:
        try:
            cur.execute(f"TRUNCATE TABLE {tabla} CASCADE;")
            print(f"   ✓ Tabla '{tabla}' limpiada")
        except Exception as e:
            print(f"   ⚠ Tabla '{tabla}': {str(e)}")
    
    # Rehabilitar restricciones de FK
    cur.execute("SET session_replication_role = 'origin';")
    
    # Confirmar cambios
    conn.commit()
    
    print("\n✅ Base de datos limpiada exitosamente")
    print("   → Todas las tablas están vacías y listas para la migración\n")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    if conn:
        conn.rollback()
