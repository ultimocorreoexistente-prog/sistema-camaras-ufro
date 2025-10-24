#!/usr/bin/env python3
import subprocess
import sys
import os

print("="*60)
print("INSTALANDO DEPENDENCIAS")
print("="*60)

# Instalar dependencias
result = subprocess.run(
    ["uv", "pip", "install", "-q", "flask", "flask-sqlalchemy", "psycopg2-binary", "werkzeug", "openpyxl", "pandas"],
    capture_output=True,
    text=True
)

if result.returncode != 0:
    print(f"Error instalando dependencias: {result.stderr}")
    sys.exit(1)

print("✓ Dependencias instaladas\n")

# Configurar entorno
os.environ['DATABASE_URL'] = "postgresql://postgres:WMQxvzTQsdkiAUOqfMgXmzgAHqxDkwRJ@tramway.proxy.rlwy.net:34726/railway"
os.chdir('/workspace/sistema-camaras-flask')

print("="*60)
print("EJECUTANDO MIGRACIÓN")
print("="*60)
print()

# Ejecutar migración
try:
    from migrate_data import migrar_datos
    from app import app
    
    with app.app_context():
        migrar_datos()
        print("\n" + "="*60)
        print("✓ MIGRACIÓN COMPLETADA")
        print("="*60)
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
