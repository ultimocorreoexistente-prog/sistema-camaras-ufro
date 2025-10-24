#!/usr/bin/env python3
"""
Script para agregar el cuarto caso real de falla al archivo Excel.
"""

import pandas as pd
from datetime import datetime
import os

def agregar_cuarto_caso():
    """Agrega el cuarto caso real de falla al archivo Excel."""
    
    archivo_excel = "/workspace/extracted_planillas/Ejemplos_Fallas_Reales.xlsx"
    
    print("🔍 Leyendo archivo de casos reales...")
    
    try:
        # Leer el archivo Excel existente
        df = pd.read_excel(archivo_excel)
        print(f"✅ Archivo leído correctamente. Casos actuales: {len(df)}")
        print("\n📋 Estructura actual:")
        print(df.head())
        print(f"\nColumnas: {list(df.columns)}")
        
    except Exception as e:
        print(f"❌ Error leyendo archivo: {e}")
        return
    
    # Datos del nuevo caso (Caso 4)
    nuevo_caso = {
        'Caso': 4,
        'Fecha': '2025-10-17',
        'Hora': '15:45',
        'Tipo_Falla': 'Eléctrica',
        'Descripcion': 'Caída de 3 cámaras del ZM por falla eléctrica',
        'Camaras_Afectadas': 'ZM-container_Ciclovia, ZM-Ciclovia a AM, ZM-Bodega_Ciclovia',
        'Ubicacion': 'Zona ZM - Ciclovia',
        'Campus': 'Andrés Bello',
        'Causa': 'Automático desconectado en caseta guardia frente a taller',
        'Solucion': 'Subir automático en caseta guardia',
        'Responsable_Reparacion': 'Marco Contreras',
        'Cargo': 'Encargado Seguridad',
        'Tiempo_Resolucion': '15 minutos',
        'Estado': 'Resuelto',
        'Observaciones': 'Automático ubicado fuera de los gabinetes principales, en caseta guardia frente a taller',
        'Prioridad': 'Alta',
        'Impacto': 'Medio'
    }
    
    print("\n📝 Datos del nuevo caso:")
    for key, value in nuevo_caso.items():
        print(f"   {key}: {value}")
    
    # Agregar el nuevo caso
    try:
        # Si las columnas no coinciden exactamente, adaptamos
        if len(df.columns) > 0:
            # Crear una nueva fila con las mismas columnas que el DataFrame existente
            nueva_fila = {}
            for col in df.columns:
                if col in nuevo_caso:
                    nueva_fila[col] = nuevo_caso[col]
                else:
                    nueva_fila[col] = ''
            
            # Agregar datos adicionales si hay columnas que no están en nuevo_caso
            for key, value in nuevo_caso.items():
                if key not in nueva_fila:
                    nueva_fila[key] = value
            
            # Convertir a DataFrame y concatenar
            df_nuevo = pd.DataFrame([nueva_fila])
            df_actualizado = pd.concat([df, df_nuevo], ignore_index=True)
        else:
            # Si el archivo está vacío, crear desde cero
            df_actualizado = pd.DataFrame([nuevo_caso])
        
        print(f"\n✅ Caso agregado. Total de casos: {len(df_actualizado)}")
        
        # Guardar el archivo actualizado
        archivo_backup = archivo_excel.replace('.xlsx', '_backup.xlsx')
        
        # Crear backup
        if os.path.exists(archivo_excel):
            df.to_excel(archivo_backup, index=False)
            print(f"💾 Backup creado: {archivo_backup}")
        
        # Guardar archivo actualizado
        df_actualizado.to_excel(archivo_excel, index=False)
        print(f"💾 Archivo actualizado guardado: {archivo_excel}")
        
        # Mostrar resumen
        print("\n📊 RESUMEN DE CASOS:")
        print("="*50)
        for i, row in df_actualizado.iterrows():
            caso_num = row.get('Caso', i+1)
            fecha = row.get('Fecha', 'Sin fecha')
            descripcion = row.get('Descripcion', row.get('Descripción', 'Sin descripción'))
            print(f"Caso {caso_num}: {fecha} - {descripcion}")
        
        print("\n🎉 ¡Cuarto caso agregado exitosamente!")
        print(f"📁 Archivo actualizado: {archivo_excel}")
        
        # También crear una versión con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archivo_timestamped = f"/workspace/Ejemplos_Fallas_Reales_actualizado_{timestamp}.xlsx"
        df_actualizado.to_excel(archivo_timestamped, index=False)
        print(f"📁 Copia con timestamp: {archivo_timestamped}")
        
    except Exception as e:
        print(f"❌ Error agregando caso: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Agregando cuarto caso real de falla...")
    print("="*50)
    agregar_cuarto_caso()