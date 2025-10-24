#!/usr/bin/env python3
import sqlite3
import json

db_path = 'sistema_camaras.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("\n" + "="*70)
print(" "*15 + "BASE DE DATOS ACTUALIZADA")
print("="*70)

# Tablas y conteo
print("\n📁 RESUMEN DE TABLAS:")
print("-" * 70)
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tablas = [row[0] for row in cursor.fetchall()]
for tabla in tablas:
    cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
    count = cursor.fetchone()[0]
    print(f"  {tabla:.<45} {count:>5} registros")

# Casos reales
print("\n📚 CASOS REALES INSERTADOS:")
print("-" * 70)
cursor.execute("""
    SELECT nombre_caso, fecha_caso, tiempo_resolucion_horas 
    FROM casos_reales 
    ORDER BY fecha_caso
""")
casos = cursor.fetchall()
for i, (nombre, fecha, tiempo) in enumerate(casos, 1):
    print(f"  {i}. {nombre}")
    print(f"     📅 {fecha} | ⏱️ {tiempo}h")

# Tipos de fallas por categoría
print("\n🚨 TIPOS DE FALLAS POR CATEGORÍA:")
print("-" * 70)
cursor.execute("""
    SELECT categoria, COUNT(*), GROUP_CONCAT(nombre, ', ') 
    FROM tipos_fallas 
    GROUP BY categoria
""")
for categoria, count, nombres in cursor.fetchall():
    print(f"  {categoria}: {count} tipos")
    # print(f"    {nombres[:60]}...")

# Infraestructura por campus
print("\n🌐 INFRAESTRUCTURA POR CAMPUS:")
print("-" * 70)
cursor.execute("""
    SELECT campus, COUNT(*), GROUP_CONCAT(DISTINCT tipo_componente, ', ')
    FROM infraestructura_red 
    GROUP BY campus
""")
for campus, count, tipos in cursor.fetchall():
    print(f"  {campus}: {count} componentes")
    print(f"    Tipos: {tipos}")

# Fallas específicas
print("\n⚠️ FALLAS ESPECÍFICAS REGISTRADAS:")
print("-" * 70)
cursor.execute("""
    SELECT fecha_falla, tipo_falla, descripcion_falla, estado
    FROM fallas_especificas
    ORDER BY fecha_falla DESC
""")
for fecha, tipo, desc, estado in cursor.fetchall():
    print(f"  • {fecha} - {tipo} ({estado})")
    print(f"    {desc[:65]}...")

print("\n" + "="*70)
print("✅ INTEGRACIÓN COMPLETA EXITOSA")
print("="*70)
print(f"\n💾 Archivo: sistema_camaras.db")
print(f"📄 Script: code/integracion_completa_sistema_camaras.py\n")

conn.close()
