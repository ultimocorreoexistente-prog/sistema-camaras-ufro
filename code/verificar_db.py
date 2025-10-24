import sqlite3
import os

# Verificar si el archivo existe
db_path = 'sistema_camaras.db'
if os.path.exists(db_path):
    print(f"✓ Base de datos encontrada: {db_path}")
    print(f"  Tamaño: {os.path.getsize(db_path)} bytes")
    
    # Conectar y verificar tablas
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Listar tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tablas = [row[0] for row in cursor.fetchall()]
    print(f"\n✓ Tablas en la base de datos ({len(tablas)}):")
    for tabla in tablas:
        cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
        count = cursor.fetchone()[0]
        print(f"  - {tabla}: {count} registros")
    
    conn.close()
else:
    print(f"✗ Base de datos no encontrada: {db_path}")
