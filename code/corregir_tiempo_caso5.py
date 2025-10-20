#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corregir el tiempo de resolución del Caso 5 (Bicicletero)
Cambio: de 8.95 horas a 2.67 horas (2h 40min)
"""

import sqlite3
from datetime import datetime

# Conectar a la base de datos
conn = sqlite3.connect('sistema_camaras.db')
cursor = conn.cursor()

print("="*70)
print("         CORRECCIÓN TIEMPO CASO 5 - BICICLETERO")
print("="*70)
print()

# Mostrar datos actuales del Caso 5
print("📋 DATOS ACTUALES DEL CASO 5:")
print("-"*70)
cursor.execute("""
    SELECT id, fecha, descripcion, tiempo_resolucion_horas
    FROM casos_reales
    WHERE descripcion LIKE '%Bicicletero%'
    ORDER BY fecha DESC
    LIMIT 1
""")
caso_actual = cursor.fetchone()
if caso_actual:
    print(f"  ID: {caso_actual[0]}")
    print(f"  Fecha: {caso_actual[1]}")
    print(f"  Descripción: {caso_actual[2][:60]}...")
    print(f"  ❌ Tiempo actual: {caso_actual[3]} horas")
print()

# Actualizar el tiempo de resolución
print("🔧 ACTUALIZANDO TIEMPO DE RESOLUCIÓN...")
print("-"*70)
try:
    cursor.execute("""
        UPDATE casos_reales
        SET tiempo_resolucion_horas = 2.67
        WHERE descripcion LIKE '%Bicicletero%'
        AND fecha = '2025-10-16'
    """)
    
    conn.commit()
    print("  ✓ Tiempo actualizado correctamente")
    print("  ✓ Nuevo valor: 2.67 horas (2h 40min)")
except Exception as e:
    print(f"  ❌ Error al actualizar: {e}")
    conn.rollback()

print()

# Verificar el cambio
print("✅ VERIFICACIÓN DEL CAMBIO:")
print("-"*70)
cursor.execute("""
    SELECT id, fecha, descripcion, tiempo_resolucion_horas
    FROM casos_reales
    WHERE descripcion LIKE '%Bicicletero%'
    ORDER BY fecha DESC
    LIMIT 1
""")
caso_actualizado = cursor.fetchone()
if caso_actualizado:
    print(f"  ID: {caso_actualizado[0]}")
    print(f"  Fecha: {caso_actualizado[1]}")
    print(f"  Descripción: {caso_actualizado[2][:60]}...")
    print(f"  ✅ Tiempo corregido: {caso_actualizado[3]} horas")
print()

# Mostrar resumen actualizado de todos los casos
print("📊 RESUMEN ACTUALIZADO DE TODOS LOS CASOS:")
print("-"*70)
cursor.execute("""
    SELECT 
        id,
        fecha,
        SUBSTR(descripcion, 1, 40) as desc_corta,
        tiempo_resolucion_horas
    FROM casos_reales
    ORDER BY fecha
""")
casos = cursor.fetchall()
tiempo_total = 0
for caso in casos:
    print(f"  {caso[0]}. [{caso[1]}] {caso[2]}... → {caso[3]}h")
    tiempo_total += caso[3]

print()
print(f"  📈 Tiempo total acumulado: {tiempo_total:.2f} horas")
print(f"  📊 Promedio por caso: {tiempo_total/len(casos):.2f} horas")

print()
print("="*70)
print("✅ CORRECCIÓN COMPLETADA EXITOSAMENTE")
print("="*70)

conn.close()
