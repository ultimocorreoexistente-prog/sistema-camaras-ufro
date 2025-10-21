import sqlite3
import pandas as pd

conn = sqlite3.connect('sistema_camaras.db')

print("=== VERIFICACIÓN DE POSIBLES DUPLICADOS ===")

# Verificar si hay duplicados en mantenimientos
query_duplicados = """
SELECT 
    componente_tipo,
    componente_id,
    fecha_mantenimiento,
    COUNT(*) as cantidad
FROM mantenimientos_realizados
GROUP BY componente_tipo, componente_id, fecha_mantenimiento
HAVING COUNT(*) > 1
"""

duplicados = pd.read_sql_query(query_duplicados, conn)

if len(duplicados) > 0:
    print(f"\n⚠️  Se encontraron {len(duplicados)} duplicados:")
    print(duplicados.to_string())
    
    # Mostrar detalles de los duplicados
    for idx, dup in duplicados.iterrows():
        print(f"\n{'='*80}")
        print(f"Duplicado: {dup['componente_tipo']} - {dup['componente_id']} en {dup['fecha_mantenimiento']}")
        query_detalles = f"""
        SELECT 
            id,
            fecha_mantenimiento,
            tipo_mantenimiento,
            descripcion_trabajo,
            tecnico_responsable,
            duracion_horas,
            costo_total,
            created_at
        FROM mantenimientos_realizados
        WHERE componente_tipo = '{dup['componente_tipo']}'
          AND componente_id = '{dup['componente_id']}'
          AND fecha_mantenimiento = '{dup['fecha_mantenimiento']}'
        """
        detalles = pd.read_sql_query(query_detalles, conn)
        print(detalles.to_string())
else:
    print("\n✓ No se encontraron duplicados en mantenimientos_realizados")

print(f"\n{'='*80}")
print("\n=== TODOS LOS MANTENIMIENTOS (ORDENADOS) ===")
query_todos = """
SELECT 
    id,
    fecha_mantenimiento,
    tipo_mantenimiento,
    componente_tipo,
    componente_id,
    tecnico_responsable,
    duracion_horas,
    costo_total
FROM mantenimientos_realizados
ORDER BY fecha_mantenimiento, id
"""

todos = pd.read_sql_query(query_todos, conn)
print(f"\nTotal: {len(todos)} mantenimientos")
print(todos.to_string())

conn.close()
