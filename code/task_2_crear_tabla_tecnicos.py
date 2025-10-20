#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear la tabla de técnicos en la base de datos
- Crear tabla 'tecnicos' con estructura completa
- Insertar 4 técnicos iniciales
- Configurar constraints y validaciones
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

def verificar_tabla_existente(cursor):
    """Verifica si la tabla técnicos ya existe"""
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='tecnicos';
    """)
    return cursor.fetchone() is not None

def crear_tabla_tecnicos(cursor):
    """Crea la tabla técnicos con estructura completa"""
    print("\n" + "="*80)
    print("🔧 CREANDO TABLA TÉCNICOS")
    print("="*80)
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tecnicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT,
                nombre_completo TEXT NOT NULL,
                email TEXT UNIQUE,
                telefono TEXT,
                especialidad TEXT,
                rol TEXT DEFAULT 'Técnico',
                estado TEXT DEFAULT 'Activo' CHECK(estado IN ('Activo', 'Inactivo', 'Licencia')),
                fecha_ingreso DATE,
                fecha_baja DATE,
                notas TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("\n✅ Tabla 'tecnicos' creada exitosamente")
        print("\n📋 Estructura de la tabla:")
        print("   • id: INTEGER PRIMARY KEY AUTOINCREMENT")
        print("   • nombre: TEXT NOT NULL")
        print("   • apellido: TEXT")
        print("   • nombre_completo: TEXT NOT NULL")
        print("   • email: TEXT UNIQUE")
        print("   • telefono: TEXT")
        print("   • especialidad: TEXT")
        print("   • rol: TEXT (default: 'Técnico')")
        print("   • estado: TEXT (Activo/Inactivo/Licencia)")
        print("   • fecha_ingreso: DATE")
        print("   • fecha_baja: DATE")
        print("   • notas: TEXT")
        print("   • created_at: TIMESTAMP")
        print("   • updated_at: TIMESTAMP")
        print("\n" + "="*80)
        return True
    except sqlite3.Error as e:
        print(f"\n❌ Error al crear tabla: {e}")
        return False

def insertar_tecnicos_iniciales(cursor):
    """Inserta los 4 técnicos iniciales"""
    print("\n" + "="*80)
    print("👥 INSERTANDO TÉCNICOS INICIALES")
    print("="*80)
    
    tecnicos = [
        {
            'nombre': 'Oliver',
            'apellido': 'Carrasco',
            'nombre_completo': 'Oliver Carrasco',
            'rol': 'Técnico',
            'especialidad': 'Mantenimiento de Cámaras',
            'estado': 'Activo'
        },
        {
            'nombre': 'Marcos',
            'apellido': 'Altamirano',
            'nombre_completo': 'Marcos Altamirano',
            'rol': 'Técnico',
            'especialidad': 'Sistemas de Vigilancia',
            'estado': 'Activo'
        },
        {
            'nombre': 'Charles',
            'apellido': 'Jélvez',
            'nombre_completo': 'Charles Jélvez',
            'rol': 'SuperAdmin',
            'especialidad': 'Administración de Sistemas',
            'estado': 'Activo',
            'notas': 'SuperAdmin del sistema - Desarrollador'
        },
        {
            'nombre': 'Marco',
            'apellido': 'Contreras',
            'nombre_completo': 'Marco Contreras',
            'rol': 'Supervisor',
            'especialidad': 'Supervisión de Seguridad',
            'estado': 'Activo',
            'notas': 'Supervisor de Seguridad'
        }
    ]
    
    insertados = 0
    try:
        for tec in tecnicos:
            cursor.execute("""
                INSERT INTO tecnicos 
                (nombre, apellido, nombre_completo, rol, especialidad, estado, notas)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                tec['nombre'],
                tec['apellido'],
                tec['nombre_completo'],
                tec['rol'],
                tec['especialidad'],
                tec['estado'],
                tec.get('notas', '')
            ))
            insertados += 1
            print(f"   ✓ {tec['nombre_completo']} - {tec['rol']}")
        
        print(f"\n✅ {insertados} técnicos insertados exitosamente")
        print("="*80)
        return True
    except sqlite3.IntegrityError as e:
        print(f"\n⚠️  Advertencia: Algunos técnicos ya existen: {e}")
        return True
    except sqlite3.Error as e:
        print(f"\n❌ Error al insertar técnicos: {e}")
        return False

def verificar_datos(cursor):
    """Verifica los datos insertados"""
    print("\n" + "="*80)
    print("✓ VERIFICACIÓN DE DATOS")
    print("="*80)
    
    cursor.execute("""
        SELECT id, nombre_completo, rol, especialidad, estado 
        FROM tecnicos
        ORDER BY 
            CASE rol 
                WHEN 'SuperAdmin' THEN 1
                WHEN 'Supervisor' THEN 2
                WHEN 'Técnico' THEN 3
                ELSE 4
            END,
            nombre_completo
    """)
    
    tecnicos = cursor.fetchall()
    
    if tecnicos:
        print(f"\n📊 Total de técnicos en base de datos: {len(tecnicos)}")
        print("\n" + "-" * 80)
        print(f"{'ID':<5} {'Nombre':<25} {'Rol':<15} {'Especialidad':<25} {'Estado'}")
        print("-" * 80)
        
        for tec in tecnicos:
            id_tec, nombre, rol, esp, estado = tec
            print(f"{id_tec:<5} {nombre:<25} {rol:<15} {esp:<25} {estado}")
        
        print("-" * 80)
        print("\n✅ VERIFICACIÓN EXITOSA")
        print("="*80)
    else:
        print("\n⚠️  No se encontraron técnicos en la base de datos")

def crear_indices(cursor):
    """Crea índices para mejorar el rendimiento"""
    print("\n" + "="*80)
    print("📑 CREANDO ÍNDICES")
    print("="*80)
    
    try:
        # Índice para búsqueda por nombre
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tecnicos_nombre 
            ON tecnicos(nombre_completo)
        """)
        print("   ✓ Índice: idx_tecnicos_nombre")
        
        # Índice para filtrado por rol
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tecnicos_rol 
            ON tecnicos(rol)
        """)
        print("   ✓ Índice: idx_tecnicos_rol")
        
        # Índice para filtrado por estado
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tecnicos_estado 
            ON tecnicos(estado)
        """)
        print("   ✓ Índice: idx_tecnicos_estado")
        
        print("\n✅ Índices creados exitosamente")
        print("="*80)
        return True
    except sqlite3.Error as e:
        print(f"\n❌ Error al crear índices: {e}")
        return False

def main():
    print("\n" + "="*80)
    print("🚀 SCRIPT: Creación de Tabla Técnicos")
    print("="*80)
    print(f"Fecha/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    conn = conectar_db()
    cursor = conn.cursor()
    
    try:
        # 1. Verificar si la tabla ya existe
        tabla_existe = verificar_tabla_existente(cursor)
        if tabla_existe:
            print("\n⚠️  La tabla 'tecnicos' ya existe. Continuando con la verificación...")
        
        # 2. Crear tabla
        if not crear_tabla_tecnicos(cursor):
            conn.rollback()
            print("\n❌ Error al crear la tabla. Operación cancelada.")
            return
        
        # 3. Crear índices
        if not crear_indices(cursor):
            conn.rollback()
            print("\n⚠️  Advertencia: Error al crear índices, pero la tabla fue creada")
        
        # 4. Insertar técnicos iniciales
        if not insertar_tecnicos_iniciales(cursor):
            conn.rollback()
            print("\n❌ Error al insertar técnicos. Operación cancelada.")
            return
        
        # 5. Commit
        conn.commit()
        print("\n💾 Cambios guardados en la base de datos")
        
        # 6. Verificar datos
        verificar_datos(cursor)
        
        print("\n" + "="*80)
        print("✅ PROCESO COMPLETADO EXITOSAMENTE")
        print("="*80)
        print("\n📝 Próximos pasos:")
        print("   1. Actualizar casos reales para vincular con técnicos")
        print("   2. Crear vista/relación entre casos_reales y tecnicos")
        print("   3. Implementar CRUD en la aplicación web")
        print("="*80)
        
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
