import sqlite3
from datetime import datetime
import json

conn = sqlite3.connect('sistema_camaras.db')
cursor = conn.cursor()

print("=== MIGRACIÓN DE SOLUCIONES A MANTENIMIENTOS_REALIZADOS ===")

# Obtener todas las fallas con solución aplicada
query = """
SELECT 
    id,
    equipo_tipo,
    equipo_id,
    descripcion,
    fecha_reporte,
    fecha_fin_reparacion,
    tiempo_resolucion_horas as duracion_horas,
    solucion_aplicada,
    materiales_utilizados,
    costo_reparacion,
    tecnico_asignado_nombre,
    estado,
    observaciones
FROM fallas
WHERE solucion_aplicada IS NOT NULL 
  AND solucion_aplicada != ''
  AND estado = 'Cerrada'
ORDER BY id
"""

cursor.execute(query)
fallas_resueltas = cursor.fetchall()

print(f"\nFallas con solución aplicada: {len(fallas_resueltas)}")

# Obtener mantenimientos existentes para no duplicar
cursor.execute("SELECT componente_tipo, componente_id, fecha_mantenimiento FROM mantenimientos_realizados")
mantenimientos_existentes = cursor.fetchall()
existentes_set = {(m[0], m[1], m[2]) for m in mantenimientos_existentes}

print(f"Mantenimientos ya existentes: {len(mantenimientos_existentes)}")

insertados = 0
omitidos = 0

for falla in fallas_resueltas:
    (
        falla_id,
        equipo_tipo,
        equipo_id,
        descripcion_falla,
        fecha_reporte,
        fecha_fin_reparacion,
        duracion_horas,
        solucion_aplicada,
        materiales_utilizados,
        costo_reparacion,
        tecnico_asignado,
        estado,
        observaciones
    ) = falla
    
    # Usar la fecha de fin de reparación como fecha del mantenimiento
    fecha_mantenimiento = fecha_fin_reparacion or fecha_reporte
    
    # Verificar si ya existe un mantenimiento para este componente en esta fecha
    if (equipo_tipo, equipo_id, fecha_mantenimiento) in existentes_set:
        print(f"  ⚠️  Omitido: Falla #{falla_id} - Ya existe mantenimiento para {equipo_tipo} {equipo_id} en {fecha_mantenimiento}")
        omitidos += 1
        continue
    
    # Determinar tipo de mantenimiento basado en la descripción
    tipo_mantenimiento = "Correctivo"  # Por defecto
    if descripcion_falla and "preventivo" in descripcion_falla.lower():
        tipo_mantenimiento = "Preventivo"
    elif descripcion_falla and "limpieza" in descripcion_falla.lower():
        tipo_mantenimiento = "Preventivo"
    
    # Preparar descripción del trabajo
    descripcion_trabajo = solucion_aplicada or f"Resolución de falla: {descripcion_falla}"
    
    # Preparar materiales (si existen)
    materiales_json = None
    if materiales_utilizados:
        try:
            # Si ya es JSON, usarlo directamente
            if materiales_utilizados.startswith('[') or materiales_utilizados.startswith('{'):
                materiales_json = materiales_utilizados
            else:
                materiales_json = json.dumps([materiales_utilizados])
        except:
            materiales_json = json.dumps([str(materiales_utilizados)])
    
    # Insertar en mantenimientos_realizados
    insert_query = """
    INSERT INTO mantenimientos_realizados (
        fecha_mantenimiento,
        tipo_mantenimiento,
        componente_tipo,
        componente_id,
        descripcion_trabajo,
        materiales_utilizados,
        tecnico_responsable,
        duracion_horas,
        costo_total,
        resultado,
        observaciones,
        created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    values = (
        fecha_mantenimiento,
        tipo_mantenimiento,
        equipo_tipo,
        equipo_id,
        descripcion_trabajo,
        materiales_json,
        tecnico_asignado or "No especificado",
        duracion_horas or 0,
        costo_reparacion or 0,
        "Exitoso" if estado == "Cerrada" else "En proceso",
        observaciones or f"Mantenimiento generado desde falla #{falla_id}",
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    
    cursor.execute(insert_query, values)
    insertados += 1
    print(f"  ✓ Insertado: Falla #{falla_id} → Mantenimiento para {equipo_tipo} {equipo_id}")
    print(f"    - Fecha: {fecha_mantenimiento}")
    print(f"    - Tipo: {tipo_mantenimiento}")
    print(f"    - Técnico: {tecnico_asignado or 'No especificado'}")
    print(f"    - Duración: {duracion_horas or 0} horas")
    print(f"    - Costo: ${costo_reparacion or 0}")
    print()

conn.commit()

print(f"\n{'='*80}")
print(f"\n✓ MIGRACIÓN COMPLETADA")
print(f"  - Mantenimientos insertados: {insertados}")
print(f"  - Registros omitidos (ya existían): {omitidos}")
print(f"  - Total mantenimientos en BD: {len(mantenimientos_existentes) + insertados}")

# Verificar resultado final
print(f"\n{'='*80}")
print("\n=== VERIFICACIÓN FINAL ===")
cursor.execute("SELECT COUNT(*) FROM mantenimientos_realizados")
total_final = cursor.fetchone()[0]
print(f"Total de mantenimientos en la base de datos: {total_final}")

print("\nMantenimientos por tipo:")
cursor.execute("""
    SELECT tipo_mantenimiento, COUNT(*) as cantidad
    FROM mantenimientos_realizados
    GROUP BY tipo_mantenimiento
""")
for row in cursor.fetchall():
    print(f"  - {row[0]}: {row[1]}")

print("\nÚltimos 5 mantenimientos registrados:")
cursor.execute("""
    SELECT 
        id,
        fecha_mantenimiento,
        tipo_mantenimiento,
        componente_tipo,
        componente_id,
        tecnico_responsable,
        costo_total
    FROM mantenimientos_realizados
    ORDER BY created_at DESC
    LIMIT 5
""")
for row in cursor.fetchall():
    print(f"  #{row[0]}: {row[1]} | {row[2]} | {row[3]} {row[4]} | Técnico: {row[5]} | ${row[6]}")

conn.close()
print("\n✓ Script completado exitosamente")
