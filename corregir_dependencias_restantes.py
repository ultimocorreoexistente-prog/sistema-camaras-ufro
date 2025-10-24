#!/usr/bin/env python3
"""
Diagnóstico de dependencias restantes y corrección final
"""

import os
import psycopg2
from urllib.parse import urlparse

def conectar_bd():
    """Conectar a la base de datos Railway PostgreSQL"""
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        db_url = "postgresql://postgres:WMQxvzTQsdkiAUOqfMgXmzgAHqxDkwRJ@tramway.proxy.rlwy.net:34726/railway"
    
    parsed = urlparse(db_url)
    
    return psycopg2.connect(
        host=parsed.hostname,
        port=parsed.port,
        database=parsed.path[1:],
        user=parsed.username,
        password=parsed.password
    )

def diagnosticar_dependencias_restantes():
    """Diagnosticar las dependencias que impiden la eliminación completa"""
    print("🔍 DIAGNÓSTICO DE DEPENDENCIAS RESTANTES")
    print("=" * 60)
    
    conn = conectar_bd()
    cur = conn.cursor()
    
    # 1. Identificar foreign keys que aún referencian tablas singulares
    print("\n🔗 FOREIGN KEYS HACIA TABLAS SINGULARES:")
    cur.execute("""
        SELECT 
            tc.constraint_name, 
            tc.table_name AS referencing_table,
            kcu.column_name AS referencing_column,
            ccu.table_name AS referenced_table,
            ccu.column_name AS referenced_column
        FROM information_schema.table_constraints AS tc 
        JOIN information_schema.key_column_usage AS kcu
            ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage AS ccu
            ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY' 
            AND ccu.table_name IN ('usuario', 'camara', 'ubicacion')
        ORDER BY ccu.table_name, tc.table_name
    """)
    
    dependencias_restantes = cur.fetchall()
    
    if dependencias_restantes:
        for dep in dependencias_restantes:
            print(f"   ⚠️  {dep[1]}.{dep[2]} → {dep[3]}.{dep[4]} (constraint: {dep[0]})")
    else:
        print("   ✅ No hay dependencias hacia tablas singulares")
    
    # 2. Verificar registros en tablas singulares
    print("\n📊 REGISTROS EN TABLAS SINGULARES:")
    tablas_singulares = ['usuario', 'camara', 'ubicacion']
    
    for tabla in tablas_singulares:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cur.fetchone()[0]
            if count > 0:
                print(f"   ⚠️  {tabla}: {count} registros")
                
                # Mostrar algunos registros
                cur.execute(f"SELECT * FROM {tabla} LIMIT 3")
                registros = cur.fetchall()
                for i, reg in enumerate(registros):
                    print(f"      Registro {i+1}: {reg}")
            else:
                print(f"   ✅ {tabla}: Sin registros")
        except psycopg2.errors.UndefinedTable:
            print(f"   ✅ {tabla}: Tabla no existe (correcto)")
        except Exception as e:
            print(f"   ❌ {tabla}: Error - {e}")
    
    # 3. Identificar qué tiene referencias a 'usuario'
    print("\n🔍 ANÁLISIS DE DEPENDENCIAS DE 'usuario':")
    
    # Buscar todas las referencias a la tabla 'usuario'
    try:
        cur.execute("""
            SELECT DISTINCT constraint_name, table_name, column_name
            FROM information_schema.key_column_usage kcu
            JOIN information_schema.table_constraints tc ON kcu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
            AND kcu.referenced_table_name = 'usuario'
        """)
        
        referencias = cur.fetchall()
        if referencias:
            print("   Referencias a tabla 'usuario':")
            for ref in referencias:
                print(f"      {ref[1]}.{ref[2]} (constraint: {ref[0]})")
        else:
            print("   ✅ No hay referencias directas a 'usuario'")
    except Exception as e:
        print(f"   ❌ Error analizando referencias: {e}")
    
    cur.close()
    conn.close()
    
    return dependencias_restantes

def corregir_dependencias_restantes(dependencias_restantes):
    """Corregir las dependencias restantes"""
    print("\n🛠️  CORRECCIÓN DE DEPENDENCIAS RESTANTES")
    print("=" * 60)
    
    if not dependencias_restantes:
        print("✅ No hay dependencias que corregir")
        return True
    
    conn = None
    try:
        conn = conectar_bd()
        cur = conn.cursor()
        
        for dep in dependencias_restantes:
            constraint_name = dep[0]
            referencing_table = dep[1]
            
            print(f"\n🗑️  Eliminando constraint: {constraint_name}")
            
            try:
                cur.execute(f"ALTER TABLE {referencing_table} DROP CONSTRAINT IF EXISTS {constraint_name}")
                print(f"   ✅ {constraint_name}: Eliminado exitosamente")
            except Exception as e:
                print(f"   ❌ Error eliminando {constraint_name}: {e}")
        
        conn.commit()
        
        # Intentar eliminar nuevamente las tablas
        print("\n🗑️  Eliminando tablas duplicadas restantes:")
        tablas_restantes = ['usuario', 'camara', 'ubicacion']
        
        for tabla in tablas_restantes:
            try:
                cur.execute(f"DROP TABLE {tabla} CASCADE")
                print(f"   ✅ {tabla}: Tabla eliminada")
            except psycopg2.errors.UndefinedTable:
                print(f"   ✅ {tabla}: Tabla ya no existe")
            except Exception as e:
                print(f"   ❌ Error eliminando {tabla}: {e}")
        
        conn.commit()
        print("\n   📝 Transacción confirmada")
        
        cur.close()
        return True
        
    except Exception as e:
        print(f"\n❌ Error durante la corrección: {e}")
        if conn:
            conn.rollback()
        return False
        
    finally:
        if conn:
            conn.close()

def main():
    """Función principal"""
    print("DIAGNÓSTICO Y CORRECCIÓN DE DEPENDENCIAS RESTANTES")
    print("=" * 60)
    
    # 1. Diagnosticar dependencias restantes
    dependencias = diagnosticar_dependencias_restantes()
    
    # 2. Corregir si es necesario
    if dependencias:
        print("\n🔄 Procediendo con corrección...")
        exito = corregir_dependencias_restantes(dependencias)
        
        if exito:
            print("\n🎉 CORRECCIÓN COMPLETADA")
            # Verificar nuevamente
            print("\n🔍 VERIFICACIÓN FINAL:")
            diagnosticar_dependencias_restantes()
        else:
            print("\n❌ FALLO EN LA CORRECCIÓN")
    else:
        print("\n✅ No se requiere corrección adicional")

if __name__ == "__main__":
    main()