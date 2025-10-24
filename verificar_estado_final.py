#!/usr/bin/env python3
"""
Verificación final del estado post-limpieza de foreign keys
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

def verificar_estado_final():
    """Verificar el estado final de la base de datos después de la limpieza"""
    print("🔍 VERIFICACIÓN FINAL POST-LIMPIEZA")
    print("=" * 60)
    
    conn = conectar_bd()
    cur = conn.cursor()
    
    # 1. Verificar tablas principales (deben existir)
    print("\n✅ VERIFICANDO TABLAS PRINCIPALES:")
    tablas_principales = ['usuarios', 'camaras', 'ubicaciones']
    
    for tabla in tablas_principales:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cur.fetchone()[0]
            print(f"   ✅ {tabla}: {count} registros")
        except Exception as e:
            print(f"   ❌ {tabla}: Error - {e}")
    
    # 2. Verificar tablas duplicadas (deben haber sido eliminadas)
    print("\n🗑️  VERIFICANDO TABLAS DUPLICADAS:")
    tablas_duplicadas = ['usuario', 'camara', 'ubicacion']
    
    for tabla in tablas_duplicadas:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cur.fetchone()[0]
            print(f"   ⚠️  {tabla}: {count} registros (NO debería existir)")
        except psycopg2.errors.UndefinedTable:
            print(f"   ✅ {tabla}: Correctamente eliminada")
        except Exception as e:
            print(f"   ❌ {tabla}: Error inesperado - {e}")
    
    # 3. Contar foreign keys restantes
    print("\n📊 VERIFICANDO FOREIGN KEYS:")
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
    
    # 4. Verificar que no hay FK hacia tablas singulares
    try:
        cur.execute("""
            SELECT COUNT(*) 
            FROM information_schema.table_constraints AS tc 
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY' 
            AND ccu.table_name IN ('usuario', 'camara', 'ubicacion')
        """)
        
        fk_singulares = cur.fetchone()[0]
        if fk_singulares == 0:
            print("   ✅ No hay foreign keys hacia tablas singulares")
        else:
            print(f"   ⚠️  Aún hay {fk_singulares} foreign keys hacia tablas singulares")
    except Exception as e:
        print(f"   ❌ Error verificando FK singulares: {e}")
    
    # 5. Estado general de tablas
    print("\n📋 ESTADO GENERAL DE TABLAS:")
    try:
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """)
        
        todas_tablas = [row[0] for row in cur.fetchall()]
        print(f"   📊 Total de tablas en BD: {len(todas_tablas)}")
        
        # Mostrar solo las más relevantes
        relevantes = [t for t in todas_tablas if any(x in t.lower() for x in ['usuario', 'camara', 'ubicacion', 'falla', 'mantenimiento'])]
        for tabla in sorted(relevantes):
            print(f"   📋 {tabla}")
    except Exception as e:
        print(f"   ❌ Error listando tablas: {e}")
    
    cur.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("🎉 VERIFICACIÓN COMPLETADA")
    print("=" * 60)

def main():
    """Función principal"""
    verificar_estado_final()

if __name__ == "__main__":
    main()