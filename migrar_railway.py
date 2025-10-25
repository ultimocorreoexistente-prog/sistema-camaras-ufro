#!/usr/bin/env python3
"""
Script para ejecutar la migración de las 4 Prioridades CRÍTICAS en Railway
Fecha: 2025-10-25
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def ejecutar_migracion():
    """Ejecuta la migración de prioridades críticas en la base de datos"""
    
    # Obtener DATABASE_URL del entorno
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ ERROR: DATABASE_URL no encontrada en variables de entorno")
        print("💡 Para ejecutar este script necesitas:")
        print("   1. Configurar DATABASE_URL de Railway")
        print("   2. Ejecutar desde el dashboard de Railway")
        return False
    
    # Convertir postgres:// a postgresql:// si es necesario
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    print(f"🔗 Conectando a la base de datos...")
    print(f"📍 URL: {database_url[:50]}...")
    
    try:
        # Crear conexión
        engine = create_engine(database_url)
        
        with engine.connect() as connection:
            print("✅ Conexión establecida exitosamente")
            
            # Leer archivo de migración
            with open('migration_prioridades_criticas.sql', 'r', encoding='utf-8') as file:
                migration_sql = file.read()
            
            print("📄 Archivo de migración leído exitosamente")
            print("🚀 Ejecutando migración...")
            
            # Ejecutar migración por partes (separadas por ;)
            statements = [stmt.strip() for stmt in migration_sql.split(';') if stmt.strip()]
            
            executed_count = 0
            for i, statement in enumerate(statements, 1):
                if statement:
                    try:
                        connection.execute(text(statement))
                        executed_count += 1
                        print(f"✅ Statement {i}/{len(statements)} ejecutado")
                    except SQLAlchemyError as e:
                        print(f"⚠️  Statement {i} - Warning: {str(e)}")
                        # Continuar con el siguiente statement
                        continue
            
            # Confirmar transacción
            connection.commit()
            
            print(f"\n🎉 MIGRACIÓN COMPLETADA EXITOSAMENTE")
            print(f"📊 {executed_count} statements ejecutados")
            
            # Verificar que las nuevas tablas y columnas existen
            print("\n🔍 Verificando implementación...")
            
            # Verificar tabla vlan
            result = connection.execute(text("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'vlan'"))
            vlan_exists = result.fetchone()[0] > 0
            print(f"   📡 Tabla VLAN: {'✅ Existe' if vlan_exists else '❌ No existe'}")
            
            # Verificar tabla enlace
            result = connection.execute(text("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'enlace'"))
            enlace_exists = result.fetchone()[0] > 0
            print(f"   🔗 Tabla Enlace: {'✅ Existe' if enlace_exists else '❌ No existe'}")
            
            # Verificar campos en camaras
            result = connection.execute(text("""
                SELECT COUNT(*) FROM information_schema.columns 
                WHERE table_name = 'camaras' AND column_name IN ('version_firmware', 'fecha_actualizacion_firmware', 'proxima_revision_firmware')
            """))
            firmware_fields = result.fetchone()[0]
            print(f"   📱 Campos Firmware Cámaras: {'✅ ' + str(firmware_fields) + '/3' if firmware_fields > 0 else '❌ 0/3'}")
            
            # Verificar campos en ups
            result = connection.execute(text("""
                SELECT COUNT(*) FROM information_schema.columns 
                WHERE table_name = 'ups' AND column_name IN ('autonomia_minutos', 'porcentaje_carga_actual', 'alertas_bateria_baja', 'alertas_sobrecarga')
            """))
            ups_fields = result.fetchone()[0]
            print(f"   🔋 Campos Autonomía UPS: {'✅ ' + str(ups_fields) + '/4' if ups_fields > 0 else '❌ 0/4'}")
            
            # Resumen final
            print(f"\n📋 RESUMEN DE IMPLEMENTACIÓN:")
            print(f"   ✅ Modelo Enlace: {enlace_exists}")
            print(f"   ✅ Modelo VLAN: {vlan_exists}")
            print(f"   ✅ Firmware Cámaras: {firmware_fields == 3}")
            print(f"   ✅ Autonomía UPS: {ups_fields == 4}")
            
            if all([enlace_exists, vlan_exists, firmware_fields == 3, ups_fields == 4]):
                print(f"\n🎯 TODAS LAS PRIORIDADES CRÍTICAS IMPLEMENTADAS CORRECTAMENTE")
                return True
            else:
                print(f"\n⚠️  Algunas implementaciones no están completas")
                return False
            
    except SQLAlchemyError as e:
        print(f"❌ ERROR de base de datos: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ ERROR inesperado: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO MIGRACIÓN DE PRIORIDADES CRÍTICAS")
    print("=" * 60)
    
    success = ejecutar_migracion()
    
    print("=" * 60)
    if success:
        print("✅ Migración completada exitosamente")
        print("💡 Ahora puedes acceder a las nuevas funcionalidades:")
        print("   📡 /vlans - Gestión de VLANs")
        print("   🔗 /enlaces - Gestión de Enlaces")
        print("   📱 Firmware en formularios de cámaras")
        print("   🔋 Autonomía UPS en dashboard de UPS")
        sys.exit(0)
    else:
        print("❌ La migración falló")
        print("💡 Instrucciones para ejecutar en Railway:")
        print("   1. Ve a https://railway.app")
        print("   2. Abre tu proyecto → PostgreSQL → Query")
        print("   3. Copia y pega el contenido de migration_prioridades_criticas.sql")
        print("   4. Ejecuta la consulta")
        sys.exit(1)
