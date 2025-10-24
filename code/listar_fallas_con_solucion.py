import sqlite3
import pandas as pd
import json

conn = sqlite3.connect('sistema_camaras.db')

print("=== FALLAS CON SOLUCION APLICADA ===")
query = """
SELECT 
    id,
    equipo_tipo,
    equipo_id,
    descripcion,
    fecha_reporte,
    fecha_fin_reparacion,
    tiempo_resolucion_horas,
    solucion_aplicada,
    materiales_utilizados,
    costo_reparacion,
    tecnico_asignado_nombre,
    estado
FROM fallas
WHERE solucion_aplicada IS NOT NULL AND solucion_aplicada != ''
ORDER BY id
"""

fallas_con_solucion = pd.read_sql_query(query, conn)
print(f"\nTotal fallas con solución: {len(fallas_con_solucion)}")
print("\nDetalle de cada falla:")
for idx, row in fallas_con_solucion.iterrows():
    print(f"\n{'='*80}")
    print(f"FALLA #{row['id']}")
    print(f"  Equipo: {row['equipo_tipo']} - {row['equipo_id']}")
    print(f"  Descripción: {row['descripcion']}")
    print(f"  Fecha reporte: {row['fecha_reporte']}")
    print(f"  Fecha fin reparación: {row['fecha_fin_reparacion']}")
    print(f"  Tiempo resolución: {row['tiempo_resolucion_horas']} horas")
    print(f"  Técnico: {row['tecnico_asignado_nombre']}")
    print(f"  Estado: {row['estado']}")
    print(f"  Solución aplicada: {row['solucion_aplicada']}")
    print(f"  Materiales: {row['materiales_utilizados']}")
    print(f"  Costo: ${row['costo_reparacion']}")

print(f"\n{'='*80}")
print("\n=== TODAS LAS FALLAS (RESUMEN) ===")
query_todas = "SELECT id, equipo_tipo, equipo_id, descripcion, estado, solucion_aplicada FROM fallas ORDER BY id"
todas_fallas = pd.read_sql_query(query_todas, conn)
for idx, row in todas_fallas.iterrows():
    tiene_solucion = "✓ SÍ" if row['solucion_aplicada'] else "✗ NO"
    print(f"Falla #{row['id']}: {row['equipo_tipo']} {row['equipo_id']} | Estado: {row['estado']} | Solución: {tiene_solucion}")

conn.close()
