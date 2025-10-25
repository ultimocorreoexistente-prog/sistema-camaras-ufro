import os
import psycopg2
from psycopg2 import sql

# Obtener DATABASE_URL de las variables de entorno
database_url = os.environ.get('DATABASE_URL')

if not database_url:
    print("ERROR: DATABASE_URL no está configurada")
    print("Para Railway, puedes obtener la URL desde: https://railway.app → tu proyecto → PostgreSQL → Connect")
    exit(1)

# Leer el script de migración
with open('migration_prioridades_criticas.sql', 'r') as f:
    migration_sql = f.read()

print("=" * 80)
print("EJECUTANDO MIGRACIÓN: 4 Prioridades CRÍTICAS")
print("=" * 80)

try:
    # Conectar a la base de datos
    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()
    
    # Ejecutar el script de migración
    cursor.execute(migration_sql)
    
    # Commit de los cambios
    conn.commit()
    
    print("\n✅ MIGRACIÓN EXITOSA")
    print("\nTablas y columnas agregadas:")
    print("  - Tabla 'enlace' creada")
    print("  - Tabla 'vlan' creada")
    print("  - Columna 'vlan_id' agregada a 'puerto_switch'")
    print("  - Columnas firmware agregadas a 'camaras':")
    print("    * version_firmware")
    print("    * fecha_actualizacion_firmware")
    print("    * proxima_revision_firmware")
    print("  - Columnas autonomía agregadas a 'ups':")
    print("    * autonomia_minutos")
    print("    * porcentaje_carga_actual")
    print("    * alertas_bateria_baja")
    print("    * alertas_sobrecarga")
    
    # Cerrar conexión
    cursor.close()
    conn.close()
    
    print("\n✅ Sistema listo para deployment en Railway")
    
except Exception as e:
    print(f"\n❌ ERROR durante la migración: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
