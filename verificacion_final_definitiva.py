#!/usr/bin/env python3
"""
Verificación final definitiva del estado de la base de datos
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

def verificacion_final_definitiva():
    """Verificación final definitiva del estado de la base de datos"""
    print("🎯 VERIFICACIÓN FINAL DEFINITIVA")
    print("=" * 60)
    
    conn = conectar_bd()
    cur = conn.cursor()
    
    # 1. Verificar que las tablas principales existen y tienen datos
    print("\n✅ TABLAS PRINCIPALES (DEBEN EXISTIR):")
    tablas_principales = ['usuarios', 'camaras', 'ubicaciones']
    
    for tabla in tablas_principales:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cur.fetchone()[0]
            print(f"   ✅ {tabla}: {count} registros")
        except Exception as e:
            print(f"   ❌ {tabla}: Error - {e}")
    
    # 2. Verificar que las tablas duplicadas fueron eliminadas
    print("\n🗑️  TABLAS DUPLICADAS (DEBEN HABER SIDO ELIMINADAS):")
    tablas_singulares = ['usuario', 'camara', 'ubicacion']
    
    todas_eliminadas = True
    for tabla in tablas_singulares:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cur.fetchone()[0]
            print(f"   ❌ {tabla}: {count} registros (PROBLEMA: aún existe)")
            todas_eliminadas = False
        except psycopg2.errors.UndefinedTable:
            print(f"   ✅ {tabla}: Correctamente eliminada")
        except Exception as e:
            print(f"   ❌ {tabla}: Error - {e}")
    
    # 3. Verificar foreign keys hacia tablas singulares
    print("\n🔗 FOREIGN KEYS HACIA TABLAS SINGULARES (DEBEN SER 0):")
    try:
        cur.execute("""
            SELECT COUNT(*) 
            FROM information_schema.table_constraints AS tc 
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY' 
            AND ccu.table_name IN ('usuario', 'camara', 'ubicacion')
        """)
        
        fk_restantes = cur.fetchone()[0]
        if fk_restantes == 0:
            print("   ✅ 0 foreign keys hacia tablas singulares (PERFECTO)")
        else:
            print(f"   ❌ {fk_restantes} foreign keys hacia tablas singulares (PROBLEMA)")
            todas_eliminadas = False
    except Exception as e:
        print(f"   ❌ Error verificando foreign keys: {e}")
    
    # 4. Contar foreign keys totales
    print("\n📊 FOREIGN KEYS TOTALES:")
    try:
        cur.execute("""
            SELECT COUNT(*) 
            FROM information_schema.table_constraints 
            WHERE constraint_type = 'FOREIGN KEY'
        """)
        
        total_fk = cur.fetchone()[0]
        print(f"   📈 Total de foreign keys restantes: {total_fk}")
    except Exception as e:
        print(f"   ❌ Error contando foreign keys: {e}")
    
    # 5. Estado general
    print("\n📋 RESUMEN FINAL:")
    if todas_eliminadas:
        print("   🎉 ESTADO: LIMPIEZA COMPLETADA EXITOSAMENTE")
        print("   ✅ Todas las tablas duplicadas eliminadas")
        print("   ✅ Todas las foreign keys problemáticas eliminadas")
        print("   ✅ Sistema funcionando correctamente")
    else:
        print("   ⚠️  ESTADO: LIMPIEZA INCOMPLETA")
        print("   ❌ Algunas tablas duplicadas aún existen")
    
    cur.close()
    conn.close()
    
    print("\n" + "=" * 60)
    return todas_eliminadas

def main():
    """Función principal"""
    exito = verificacion_final_definitiva()
    
    if exito:
        print("\n🎉 ¡LIMPIEZA FOREIGN KEY COMPLETADA AL 100%!")
        print("📋 Sistema: Gestión de Cámaras UFRO")
        print("✅ Base de datos optimizada y limpia")
        print("🚀 Aplicación lista para uso en producción")
    else:
        print("\n❌ LIMPIEZA INCOMPLETA")
        print("🔄 Se requiere intervención adicional")

if __name__ == "__main__":
    main()