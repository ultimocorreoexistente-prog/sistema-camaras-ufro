import sqlite3
import pandas as pd

conn = sqlite3.connect('sistema_camaras.db')
cursor = conn.cursor()

print("=== LIMPIEZA DE DUPLICADOS CONCEPTUALES EN MANTENIMIENTOS ===")

# Analizar duplicados conceptuales
print("\nAnalizando mantenimientos duplicados...\n")

# Obtener todos los mantenimientos
query = """
SELECT 
    id,
    fecha_mantenimiento,
    tipo_mantenimiento,
    componente_tipo,
    componente_id,
    descripcion_trabajo,
    tecnico_responsable,
    duracion_horas,
    costo_total,
    observaciones
FROM mantenimientos_realizados
ORDER BY fecha_mantenimiento, id
"""

mant = pd.read_sql_query(query, conn)

print(f"Total mantenimientos antes de limpieza: {len(mant)}\n")

# Identificar duplicados conceptuales manualmente basado en fecha y descripción
duplicados_a_eliminar = []

# Reglas de limpieza:
# 1. Si hay un mantenimiento con componente_tipo="MULTIPLE", verificar si hay otro más específico
# 2. Mantener el que tenga más información (costo, técnico específico, etc.)

for idx, row in mant.iterrows():
    if row['componente_tipo'] == 'MULTIPLE':
        # Buscar si hay otro mantenimiento en la misma fecha con más detalles
        fecha = row['fecha_mantenimiento']
        
        # Buscar candidatos más específicos en la misma fecha o cercana
        candidatos = mant[
            (mant['fecha_mantenimiento'] == fecha) & 
            (mant['componente_tipo'] != 'MULTIPLE') &
            (mant['id'] != row['id'])
        ]
        
        # Si hay un candidato con más detalles, marcar este como duplicado
        for _, candidato in candidatos.iterrows():
            # Verificar si el candidato tiene relación con este mantenimiento
            desc_multiple = str(row['componente_id']).lower()
            desc_candidato = str(candidato['descripcion_trabajo']).lower()
            
            # Casos específicos:
            if 'ups' in desc_multiple and candidato['componente_tipo'] == 'UPS':
                duplicados_a_eliminar.append(row['id'])
                print(f"⚠️  Duplicado encontrado:")
                print(f"    ID {row['id']} (MULTIPLE - {row['componente_id']})")
                print(f"    reemplazado por ID {candidato['id']} ({candidato['componente_tipo']} - {candidato['componente_id']})")
                print(f"    Razón: El ID {candidato['id']} tiene más detalles (costo: ${candidato['costo_total']})\n")
                break

# Eliminar duplicados identificados
if duplicados_a_eliminar:
    print(f"\nEliminando {len(duplicados_a_eliminar)} duplicados...")
    for id_eliminar in duplicados_a_eliminar:
        cursor.execute("DELETE FROM mantenimientos_realizados WHERE id = ?", (id_eliminar,))
        print(f"  ✓ Eliminado mantenimiento ID {id_eliminar}")
    
    conn.commit()
    print(f"\n✓ Duplicados eliminados exitosamente")
else:
    print("\n✓ No se encontraron duplicados conceptuales para eliminar")

# Verificación final
print(f"\n{'='*80}")
print("\n=== VERIFICACIÓN FINAL ===")

cursor.execute("SELECT COUNT(*) FROM mantenimientos_realizados")
total_final = cursor.fetchone()[0]
print(f"\nTotal mantenimientos después de limpieza: {total_final}")

print("\nMantenimientos finales:")
query_final = """
SELECT 
    id,
    fecha_mantenimiento,
    tipo_mantenimiento,
    componente_tipo,
    componente_id,
    tecnico_responsable,
    costo_total
FROM mantenimientos_realizados
ORDER BY fecha_mantenimiento, id
"""

mant_final = pd.read_sql_query(query_final, conn)
print(mant_final.to_string())

print("\nMantenimientos por tipo:")
cursor.execute("""
    SELECT tipo_mantenimiento, COUNT(*) as cantidad, SUM(costo_total) as costo_total
    FROM mantenimientos_realizados
    GROUP BY tipo_mantenimiento
""")
for row in cursor.fetchall():
    print(f"  - {row[0]}: {row[1]} mantenimientos (Costo total: ${row[2]:,.2f})")

conn.close()
print("\n✓ Limpieza completada")
