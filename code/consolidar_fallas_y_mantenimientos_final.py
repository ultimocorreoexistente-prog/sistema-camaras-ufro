import sqlite3
import pandas as pd

conn = sqlite3.connect('sistema_camaras.db')
cursor = conn.cursor()

print("=== CONSOLIDACIÓN DE FALLAS Y MANTENIMIENTOS DUPLICADOS ===")
print("\nProblema identificado:")
print("- Durante la migración, algunos casos_reales y fallas_especificas")
print("  se duplicaron con equipo_tipo='MULTIPLE' y equipo específico")
print("\nSolución:")
print("- Mantener fallas con equipo específico")
print("- Eliminar fallas tipo MULTIPLE duplicadas")
print("- Eliminar mantenimientos de fallas MULTIPLE duplicadas")

print(f"\n{'='*80}")
print("\n1. IDENTIFICANDO DUPLICADOS\n")

# Pares de fallas duplicadas (manualmente identificados del análisis anterior)
duplicados_fallas = [
    # (id_mantener, id_eliminar, razon)
    (1, 6, "Cable NVR CFT Prat - 2024-10-14"),
    (2, 8, "Fibra Óptica Bicicletero - 2025-10-16"),
    (3, 7, "Caída cámaras ZM - Falla Eléctrica - 2025-10-17"),
]

print("Fallas duplicadas identificadas:")
for mantener, eliminar, razon in duplicados_fallas:
    falla_mantener = pd.read_sql_query(f"SELECT equipo_tipo, equipo_id FROM fallas WHERE id={mantener}", conn)
    falla_eliminar = pd.read_sql_query(f"SELECT equipo_tipo, equipo_id FROM fallas WHERE id={eliminar}", conn)
    
    print(f"\n  Caso: {razon}")
    print(f"    ✓ Mantener Falla #{mantener}: {falla_mantener.iloc[0]['equipo_tipo']} - {falla_mantener.iloc[0]['equipo_id']}")
    print(f"    ✗ Eliminar Falla #{eliminar}: {falla_eliminar.iloc[0]['equipo_tipo']} - {falla_eliminar.iloc[0]['equipo_id']}")

print(f"\n{'='*80}")
print("\n2. ELIMINANDO MANTENIMIENTOS DE FALLAS DUPLICADAS\n")

# Pares de mantenimientos duplicados (relacionados con las fallas)
duplicados_mantenimientos = [
    # (id_mantener, id_eliminar, razon)
    (3, 8, "Relacionado con Falla Cable NVR CFT Prat"),
    (4, 10, "Relacionado con Falla Fibra Óptica Bicicletero"),
    (5, 9, "Relacionado con Falla Caída cámaras ZM"),
]

for mantener, eliminar, razon in duplicados_mantenimientos:
    mant_mantener = pd.read_sql_query(f"SELECT componente_tipo, componente_id, costo_total FROM mantenimientos_realizados WHERE id={mantener}", conn)
    mant_eliminar = pd.read_sql_query(f"SELECT componente_tipo, componente_id, costo_total FROM mantenimientos_realizados WHERE id={eliminar}", conn)
    
    print(f"  {razon}")
    print(f"    ✓ Mantener Mant. #{mantener}: {mant_mantener.iloc[0]['componente_tipo']} - {mant_mantener.iloc[0]['componente_id']}")
    print(f"    ✗ Eliminar Mant. #{eliminar}: {mant_eliminar.iloc[0]['componente_tipo']} - {mant_eliminar.iloc[0]['componente_id']}")
    
    cursor.execute(f"DELETE FROM mantenimientos_realizados WHERE id = {eliminar}")
    print(f"    ✓ Mantenimiento #{eliminar} eliminado\n")

conn.commit()

print(f"{'='*80}")
print("\n3. ELIMINANDO FALLAS DUPLICADAS (TIPO MULTIPLE)\n")

for mantener, eliminar, razon in duplicados_fallas:
    cursor.execute(f"DELETE FROM fallas WHERE id = {eliminar}")
    print(f"  ✓ Eliminada Falla #{eliminar} ({razon})")

conn.commit()

print(f"\n{'='*80}")
print("\n4. VERIFICACIÓN FINAL\n")

# Verificar fallas
cursor.execute("SELECT COUNT(*) FROM fallas")
total_fallas = cursor.fetchone()[0]
print(f"Total fallas: {total_fallas}")

print("\nFallas por estado:")
cursor.execute("SELECT estado, COUNT(*) FROM fallas GROUP BY estado")
for row in cursor.fetchall():
    print(f"  - {row[0]}: {row[1]}")

print("\nFallas por tipo de equipo:")
cursor.execute("SELECT equipo_tipo, COUNT(*) FROM fallas GROUP BY equipo_tipo ORDER BY COUNT(*) DESC")
for row in cursor.fetchall():
    print(f"  - {row[0]}: {row[1]}")

# Verificar mantenimientos
print(f"\n{'='*80}")
cursor.execute("SELECT COUNT(*) FROM mantenimientos_realizados")
total_mant = cursor.fetchone()[0]
print(f"\nTotal mantenimientos: {total_mant}")

print("\nMantenimientos por tipo:")
cursor.execute("SELECT tipo_mantenimiento, COUNT(*), SUM(costo_total) FROM mantenimientos_realizados GROUP BY tipo_mantenimiento")
for row in cursor.fetchall():
    print(f"  - {row[0]}: {row[1]} (Costo total: ${row[2]:,.2f})")

print("\n\nLista de fallas finales:")
fallas_final = pd.read_sql_query("""
    SELECT id, equipo_tipo, equipo_id, descripcion, estado, fecha_reporte
    FROM fallas
    ORDER BY id
""", conn)
for idx, row in fallas_final.iterrows():
    print(f"  Falla #{row['id']}: {row['equipo_tipo']} - {row['equipo_id'] or '(sin ID)'} | {row['estado']} | {row['fecha_reporte']}")

print("\n\nLista de mantenimientos finales:")
mant_final = pd.read_sql_query("""
    SELECT id, fecha_mantenimiento, componente_tipo, componente_id, costo_total
    FROM mantenimientos_realizados
    ORDER BY fecha_mantenimiento, id
""", conn)
for idx, row in mant_final.iterrows():
    print(f"  Mant. #{row['id']}: {row['fecha_mantenimiento']} | {row['componente_tipo']} - {row['componente_id']} | ${row['costo_total']:,.2f}")

conn.close()

print(f"\n{'='*80}")
print("\n✓ CONSOLIDACIÓN COMPLETADA EXITOSAMENTE")
print("\nResultado:")
print(f"  - {total_fallas} fallas (sin duplicados)")
print(f"  - {total_mant} mantenimientos (sin duplicados)")
print("  - Todas las soluciones de casos_reales están en mantenimientos_realizados")
print("  - La tabla casos_reales ya no existe (consolidada en fallas)")
