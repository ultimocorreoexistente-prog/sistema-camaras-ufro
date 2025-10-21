#!/usr/bin/env python3
"""
Script para corregir la hora de reparación del cuarto caso real.
"""

import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os

def calcular_tiempo_resolucion(hora_inicio, hora_fin):
    """Calcula el tiempo de resolución entre dos horas."""
    try:
        inicio = datetime.strptime(hora_inicio, "%H:%M")
        fin = datetime.strptime(hora_fin, "%H:%M")
        
        # Si la hora de fin es menor, asumimos que pasó al día siguiente
        if fin < inicio:
            fin += timedelta(days=1)
        
        diferencia = fin - inicio
        horas = diferencia.seconds // 3600
        minutos = (diferencia.seconds % 3600) // 60
        
        if horas > 0:
            return f"{horas} horas y {minutos} minutos"
        else:
            return f"{minutos} minutos"
    except:
        return "No calculado"

def corregir_hora_reparacion():
    """Corrige la hora de reparación en Excel y base de datos."""
    
    print("🔧 Corrigiendo hora de reparación del cuarto caso...")
    print("="*60)
    
    # 1. CORREGIR EN EXCEL
    print("\n📊 1. Actualizando archivo Excel...")
    archivo_excel = "/workspace/extracted_planillas/Ejemplos_Fallas_Reales.xlsx"
    
    try:
        df = pd.read_excel(archivo_excel)
        print(f"✅ Excel leído. Casos: {len(df)}")
        
        # Buscar el caso más reciente (último agregado)
        ultimo_indice = len(df) - 1
        
        if ultimo_indice >= 0:
            # Datos corregidos
            hora_reporte = "15:45"
            hora_reparacion = "18:25"
            tiempo_resolucion = calcular_tiempo_resolucion(hora_reporte, hora_reparacion)
            
            print(f"\n📝 Corrección de datos:")
            print(f"   • Hora de reporte: {hora_reporte}")
            print(f"   • Hora de reparación: {hora_reparacion}")
            print(f"   • Tiempo de resolución: {tiempo_resolucion}")
            
            # Actualizar las columnas relevantes
            if 'Hora' in df.columns:
                df.at[ultimo_indice, 'Hora'] = f"Reporte: {hora_reporte}, Reparación: {hora_reparacion}"
            if 'Tiempo_Resolucion' in df.columns:
                df.at[ultimo_indice, 'Tiempo_Resolucion'] = tiempo_resolucion
            if 'Observaciones' in df.columns:
                observacion_actualizada = f"Automático ubicado fuera de los gabinetes principales, en caseta guardia frente a taller. Falla detectada a las {hora_reporte}, reparada a las {hora_reparacion}"
                df.at[ultimo_indice, 'Observaciones'] = observacion_actualizada
            
            # Guardar
            df.to_excel(archivo_excel, index=False)
            print(f"✅ Excel actualizado: {archivo_excel}")
            
            # Crear backup con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo_corregido = f"/workspace/Ejemplos_Fallas_Reales_corregido_{timestamp}.xlsx"
            df.to_excel(archivo_corregido, index=False)
            print(f"📁 Copia corregida: {archivo_corregido}")
        
    except Exception as e:
        print(f"❌ Error actualizando Excel: {e}")
    
    # 2. CORREGIR EN BASE DE DATOS
    print("\n🗃️ 2. Actualizando base de datos...")
    db_path = "/workspace/sistema_camaras.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Buscar el último caso insertado
        cursor.execute("SELECT id, fecha_reporte, hora_reporte FROM fallas ORDER BY id DESC LIMIT 1")
        ultimo_caso = cursor.fetchone()
        
        if ultimo_caso:
            caso_id = ultimo_caso[0]
            
            # Datos corregidos
            hora_reporte = "15:45"
            hora_reparacion = "18:25"
            tiempo_resolucion = calcular_tiempo_resolucion(hora_reporte, hora_reparacion)
            
            # Actualizar observaciones y tiempos
            observaciones_corregidas = f"Automático ubicado fuera de los gabinetes principales, en caseta guardia frente a taller. Falla detectada a las {hora_reporte}, reparada a las {hora_reparacion}. Tiempo total de resolución: {tiempo_resolucion}"
            
            cursor.execute('''
                UPDATE fallas 
                SET hora_reporte = ?,
                    tiempo_resolucion = ?,
                    observaciones = ?
                WHERE id = ?
            ''', (
                f"Reporte: {hora_reporte}, Reparación: {hora_reparacion}",
                tiempo_resolucion,
                observaciones_corregidas,
                caso_id
            ))
            
            conn.commit()
            
            # Verificar actualización
            cursor.execute("SELECT hora_reporte, tiempo_resolucion FROM fallas WHERE id = ?", (caso_id,))
            datos_actualizados = cursor.fetchone()
            
            print(f"✅ Base de datos actualizada:")
            print(f"   • ID del caso: {caso_id}")
            print(f"   • Hora actualizada: {datos_actualizados[0]}")
            print(f"   • Tiempo resolución: {datos_actualizados[1]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error actualizando BD: {e}")
    
    # 3. RESUMEN DE LA CORRECCIÓN
    print("\n📋 RESUMEN DE CORRECCIÓN:")
    print("="*40)
    print("✅ Información corregida:")
    print(f"   📅 Fecha: 2025-10-17")
    print(f"   🕒 Hora de detección/reporte: 15:45")
    print(f"   🔧 Hora de reparación: 18:25")
    print(f"   ⏱️ Tiempo total de resolución: {calcular_tiempo_resolucion('15:45', '18:25')}")
    print(f"   👨‍🔧 Reparado por: Marco Contreras")
    print(f"   📍 Ubicación: Caseta guardia frente a taller")
    
    print(f"\n🎉 ¡Corrección completada exitosamente!")

if __name__ == "__main__":
    corregir_hora_reparacion()