#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corregir datos del Caso 5 (Bicicletero Principal)
- Actualizar tiempo de resolución a 1.62 horas (1h 37min)
- Actualizar técnico asignado a Charles Jélvez
- Actualizar número de cámaras a 3
"""

import sqlite3
import sys
from datetime import datetime

def conectar_db():
    """Conecta a la base de datos"""
    try:
        conn = sqlite3.connect('sistema_camaras.db')
        return conn
    except sqlite3.Error as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        sys.exit(1)

def inspeccionar_estructura(cursor):
    """Muestra la estructura de la tabla casos_reales"""
    print("\n" + "="*80)
    print("📋 ESTRUCTURA DE LA TABLA casos_reales")
    print("="*80)
    
    cursor.execute("PRAGMA table_info(casos_reales);")
    columnas = cursor.fetchall()
    
    print(f"\n{'ID':<5} {'Columna':<30} {'Tipo':<15} {'Nulo':<8} {'Default'}")
    print("-" * 80)
    for col in columnas:
        col_id, nombre, tipo, not_null, default_val, pk = col
        nulo = "NO" if not_null else "SI"
        default = default_val if default_val else "NULL"
        print(f"{col_id:<5} {nombre:<30} {tipo:<15} {nulo:<8} {default}")
    
    print("\n" + "="*80)
    return [col[1] for col in columnas]  # Retorna lista de nombres de columnas

def mostrar_caso_actual(cursor):
    """Muestra los datos actuales del Caso 5"""
    print("\n" + "="*80)
    print("📄 DATOS ACTUALES DEL CASO 5 (Bicicletero Principal)")
    print("="*80)
    
    cursor.execute("""
        SELECT id, nombre_caso, fecha_caso, descripcion, 
               componentes_involucrados, solucion_aplicada, tiempo_resolucion_horas
        FROM casos_reales 
        WHERE descripcion LIKE '%Bicicletero%' OR nombre_caso LIKE '%Bicicletero%'
    """)
    
    caso = cursor.fetchone()
    if caso:
        print(f"\nID: {caso[0]}")
        print(f"Nombre Caso: {caso[1]}")
        print(f"Fecha: {caso[2]}")
        print(f"Descripción: {caso[3]}")
        print(f"Componentes: {caso[4]}")
        print(f"Solución: {caso[5]}")
        print(f"Tiempo Resolución: {caso[6]} horas")
        print("\n" + "="*80)
        return caso[0]  # Retorna el ID
    else:
        print("\n⚠️  No se encontró el caso del Bicicletero")
        return None

def actualizar_caso_5(cursor, caso_id):
    """Actualiza los datos del Caso 5"""
    print("\n" + "="*80)
    print("🔄 ACTUALIZANDO CASO 5")
    print("="*80)
    
    # Nueva descripción que refleja 3 cámaras
    nueva_descripcion = """Falla eléctrica - Bicicletero Principal
3 cámaras afectadas:
- Bicicletero_Entrada
- Bicicletero_Estacionamiento
- Bicicletero_Lateral

Causa: Automático desconectado en caseta de guardia
Horario: 15:20 → 16:57
Duración real: 1 hora 37 minutos (1.62 horas)"""
    
    componentes = """3 cámaras del Bicicletero Principal
Técnico: Charles Jélvez
Tipo: Falla eléctrica (automático desconectado)"""
    
    solucion = """Reconexión del automático eléctrico + verificación completa del sistema
Todas las cámaras recuperadas exitosamente
Tiempo total: 1h 37min"""
    
    try:
        cursor.execute("""
            UPDATE casos_reales
            SET tiempo_resolucion_horas = ?,
                descripcion = ?,
                componentes_involucrados = ?,
                solucion_aplicada = ?
            WHERE id = ?
        """, (1.62, nueva_descripcion, componentes, solucion, caso_id))
        
        print("\n✅ Actualizaciones aplicadas:")
        print("   • Tiempo de resolución: 1.62 horas (1h 37min)")
        print("   • Técnico asignado: Charles Jélvez")
        print("   • Descripción actualizada: 3 cámaras especificadas")
        print("   • Componentes y solución detallados")
        print("\n" + "="*80)
        
        return True
    except sqlite3.Error as e:
        print(f"\n❌ Error al actualizar: {e}")
        return False

def verificar_actualizacion(cursor, caso_id):
    """Verifica que la actualización fue exitosa"""
    print("\n" + "="*80)
    print("✓ VERIFICACIÓN POST-ACTUALIZACIÓN")
    print("="*80)
    
    cursor.execute("""
        SELECT descripcion, componentes_involucrados, solucion_aplicada, tiempo_resolucion_horas
        FROM casos_reales 
        WHERE id = ?
    """, (caso_id,))
    
    caso = cursor.fetchone()
    if caso:
        print(f"\nTiempo Resolución: {caso[3]} horas ✓")
        print(f"\nDescripción actualizada:")
        print("-" * 80)
        print(caso[0])
        print("-" * 80)
        print(f"\nComponentes involucrados:")
        print("-" * 80)
        print(caso[1])
        print("-" * 80)
        print(f"\nSolución aplicada:")
        print("-" * 80)
        print(caso[2])
        print("-" * 80)
        print("\n✅ ACTUALIZACIÓN EXITOSA")
        print("="*80)

def main():
    print("\n" + "="*80)
    print("🚀 SCRIPT: Corrección de Datos - Caso 5 (Bicicletero Principal)")
    print("="*80)
    print(f"Fecha/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Conectar a la base de datos
    conn = conectar_db()
    cursor = conn.cursor()
    
    try:
        # 1. Inspeccionar estructura de la tabla
        columnas = inspeccionar_estructura(cursor)
        
        # 2. Mostrar datos actuales
        caso_id = mostrar_caso_actual(cursor)
        
        if not caso_id:
            print("\n❌ No se puede continuar sin el ID del caso")
            return
        
        # 3. Actualizar el caso
        if actualizar_caso_5(cursor, caso_id):
            conn.commit()
            
            # 4. Verificar actualización
            verificar_actualizacion(cursor, caso_id)
        else:
            conn.rollback()
            print("\n❌ La transacción fue revertida debido a un error")
    
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        conn.close()
        print("\n🔌 Conexión a la base de datos cerrada")
        print("="*80 + "\n")

if __name__ == "__main__":
    main()
