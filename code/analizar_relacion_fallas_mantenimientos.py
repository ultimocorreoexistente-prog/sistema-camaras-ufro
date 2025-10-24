import sqlite3
import pandas as pd
from datetime import datetime, timedelta

conn = sqlite3.connect('sistema_camaras.db')
cursor = conn.cursor()

print("=== ANÁLISIS DETALLADO DE POSIBLES DUPLICADOS ===")

# Obtener todas las fallas y sus mantenimientos relacionados
print("\n1. FALLAS Y SUS MANTENIMIENTOS:\n")

query_fallas = """
SELECT 
    f.id as falla_id,
    f.equipo_tipo,
    f.equipo_id,
    f.descripcion,
    f.fecha_reporte,
    f.fecha_fin_reparacion,
    f.solucion_aplicada,
    f.estado
FROM fallas f
WHERE f.estado = 'Cerrada'
ORDER BY f.fecha_reporte
"""

fallas = pd.read_sql_query(query_fallas, conn)

print(f"Total fallas cerradas: {len(fallas)}\n")

# Para cada falla cerrada, buscar mantenimientos relacionados
for idx, falla in fallas.iterrows():
    print(f"Falla #{falla['falla_id']}: {falla['equipo_tipo']} - {falla['equipo_id']}")
    print(f"  Fecha: {falla['fecha_reporte']} → {falla['fecha_fin_reparacion']}")
    print(f"  Estado: {falla['estado']}")
    
    # Buscar mantenimientos relacionados (por fecha cercana o por ID de equipo)
    fecha_inicio = falla['fecha_reporte']
    fecha_fin = falla['fecha_fin_reparacion'] or falla['fecha_reporte']
    
    query_mant = f"""
    SELECT 
        id,
        fecha_mantenimiento,
        componente_tipo,
        componente_id,
        descripcion_trabajo,
        costo_total
    FROM mantenimientos_realizados
    WHERE fecha_mantenimiento BETWEEN '{fecha_inicio}' AND '{fecha_fin}'
       OR componente_id LIKE '%{falla['equipo_id'] if falla['equipo_id'] else ''}%'
    """
    
    mant_relacionados = pd.read_sql_query(query_mant, conn)
    
    if len(mant_relacionados) > 0:
        print(f"  → Mantenimientos relacionados: {len(mant_relacionados)}")
        for _, mant in mant_relacionados.iterrows():
            print(f"     - ID {mant['id']}: {mant['componente_tipo']} - {mant['componente_id']} (${mant['costo_total']})")
    else:
        print(f"  ⚠️  NO hay mantenimientos relacionados")
    print()

print(f"\n{'='*80}")
print("\n2. MANTENIMIENTOS SIN FALLA ASOCIADA:\n")

# Buscar mantenimientos que no tienen una falla clara asociada
query_mant_todos = """
SELECT 
    id,
    fecha_mantenimiento,
    componente_tipo,
    componente_id,
    descripcion_trabajo,
    costo_total
FROM mantenimientos_realizados
ORDER BY fecha_mantenimiento
"""

mant_todos = pd.read_sql_query(query_mant_todos, conn)

for idx, mant in mant_todos.iterrows():
    # Intentar encontrar la falla asociada
    componente = mant['componente_id']
    fecha = mant['fecha_mantenimiento']
    
    # Buscar falla con equipo_id similar o fecha cercana
    query_falla = f"""
    SELECT 
        id,
        equipo_tipo,
        equipo_id,
        fecha_reporte,
        fecha_fin_reparacion
    FROM fallas
    WHERE (equipo_id = '{componente}' OR equipo_id LIKE '%{componente}%')
       OR (fecha_reporte <= '{fecha}' AND 
           (fecha_fin_reparacion >= '{fecha}' OR fecha_fin_reparacion IS NULL))
    """
    
    fallas_asociadas = pd.read_sql_query(query_falla, conn)
    
    print(f"Mantenimiento #{mant['id']}: {mant['componente_tipo']} - {mant['componente_id']} (${mant['costo_total']})")
    print(f"  Fecha: {mant['fecha_mantenimiento']}")
    if len(fallas_asociadas) > 0:
        print(f"  → Fallas asociadas: {len(fallas_asociadas)}")
        for _, f in fallas_asociadas.iterrows():
            print(f"     - Falla #{f['id']}: {f['equipo_tipo']} - {f['equipo_id']}")
    else:
        print(f"  ⚠️  NO hay fallas asociadas claramente")
    print()

conn.close()
