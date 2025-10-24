#!/usr/bin/env python3
"""Script para ejecutar la migración de datos a Railway"""

import os
import sys

# Configurar la URL de la base de datos pública de Railway
PUBLIC_DATABASE_URL = "postgresql://postgres:WMQxvzTQsdkiAUOqfMgXmzgAHqxDkwRJ@tramway.proxy.rlwy.net:34726/railway"

# Establecer la variable de entorno
os.environ['DATABASE_URL'] = PUBLIC_DATABASE_URL

# Cambiar al directorio del proyecto Flask
project_dir = '/workspace/sistema-camaras-flask'
os.chdir(project_dir)
sys.path.insert(0, project_dir)

print("="*60)
print("MIGRACIÓN DE DATOS A RAILWAY")
print("="*60)
print(f"Directorio de trabajo: {os.getcwd()}")
print(f"Base de datos: tramway.proxy.rlwy.net:34726/railway")
print("="*60)
print()

# Importar y ejecutar el script de migración
try:
    from migrate_data import migrar_datos
    from app import app
    
    with app.app_context():
        migrar_datos()
        print("\n" + "="*60)
        print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("="*60)
        
except Exception as e:
    print(f"\n❌ ERROR DURANTE LA MIGRACIÓN: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
