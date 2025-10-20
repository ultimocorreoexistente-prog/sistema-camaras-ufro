import sqlite3
import pandas as pd

conn = sqlite3.connect('sistema_camaras.db')
cursor = conn.cursor()

print("=== ESQUEMA DE LA TABLA FALLAS ===")
cursor.execute("PRAGMA table_info(fallas)")
columnas = cursor.fetchall()
for col in columnas:
    print(f"- {col[1]} ({col[2]})")

print("\n=== DATOS EN FALLAS ===")
fallas = pd.read_sql_query("SELECT * FROM fallas", conn)
print(f"Total registros: {len(fallas)}")
print("\nColumnas disponibles:", list(fallas.columns))
print("\nPrimeros registros:")
print(fallas.head(10).to_string())

print("\n=== ESQUEMA DE MANTENIMIENTOS_REALIZADOS ===")
cursor.execute("PRAGMA table_info(mantenimientos_realizados)")
columnas_mant = cursor.fetchall()
for col in columnas_mant:
    print(f"- {col[1]} ({col[2]})")

print("\n=== DATOS EN MANTENIMIENTOS_REALIZADOS ===")
mant = pd.read_sql_query("SELECT * FROM mantenimientos_realizados", conn)
print(f"Total registros: {len(mant)}")
if len(mant) > 0:
    print("\nMantenimientos actuales:")
    print(mant.to_string())

conn.close()
