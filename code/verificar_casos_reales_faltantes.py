import sqlite3
import pandas as pd

conn = sqlite3.connect('sistema_camaras.db')

# Ver los casos_reales originales (si aún existen)
print("=== VERIFICANDO CASOS_REALES ===")
try:
    casos = pd.read_sql_query("SELECT * FROM casos_reales", conn)
    print(f"Registros en casos_reales: {len(casos)}")
    if len(casos) > 0:
        print("\nDatos de casos_reales:")
        print(casos.to_string())
except Exception as e:
    print(f"Error o tabla no existe: {e}")

print("\n=== VERIFICANDO FALLAS (nuevas) ===")
fallas = pd.read_sql_query("SELECT * FROM fallas", conn)
print(f"Total fallas: {len(fallas)}")
print("\nFallas actuales:")
print(fallas[['id', 'camara_id', 'tipo_falla_id', 'descripcion', 'solucion', 'estado_id']].to_string())

print("\n=== VERIFICANDO MANTENIMIENTOS_REALIZADOS ===")
mant = pd.read_sql_query("SELECT * FROM mantenimientos_realizados", conn)
print(f"Total mantenimientos: {len(mant)}")
print("\nMantenimientos actuales:")
print(mant.to_string())

conn.close()
