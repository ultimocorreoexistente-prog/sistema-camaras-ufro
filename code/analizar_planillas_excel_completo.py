import pandas as pd
import os
from openpyxl import load_workbook

planillas_dir = 'user_input_files/planillas-web'

print("=== ANÁLISIS COMPLETO DE PLANILLAS EXCEL ===")
print()

planillas = [
    'Catalogo_Tipos_Fallas.xlsx',
    'Ejemplos_Fallas_Reales.xlsx',
    'Equipos_Tecnicos.xlsx',
    'Fallas_Actualizada.xlsx',
    'Fuentes_Poder.xlsx',
    'Gabinetes.xlsx',
    'Listadecámaras_modificada.xlsx',
    'Mantenimientos.xlsx',
    'NVR_DVR.xlsx',
    'Puertos_Switch.xlsx',
    'Switches.xlsx',
    'UPS.xlsx',
    'Ubicaciones.xlsx'
]

resumen = []

for planilla in planillas:
    path = os.path.join(planillas_dir, planilla)
    if os.path.exists(path):
        try:
            df = pd.read_excel(path)
            print(f"{'='*80}")
            print(f"📄 {planilla}")
            print(f"{'='*80}")
            print(f"Filas: {len(df)} | Columnas: {len(df.columns)}")
            print(f"\nColumnas: {list(df.columns)}")
            
            # Verificar si tiene ID Ubicación
            tiene_id_ubicacion = 'ID Ubicación' in df.columns
            
            # Contar datos vacíos por columna
            print(f"\nDatos vacíos por columna:")
            for col in df.columns:
                vacios = df[col].isna().sum()
                total = len(df)
                pct = (vacios/total*100) if total > 0 else 0
                if vacios > 0:
                    print(f"  - {col}: {vacios}/{total} ({pct:.1f}%)")
            
            # Mostrar primeras 3 filas
            if len(df) > 0:
                print(f"\nPrimeras filas:")
                print(df.head(3).to_string())
            else:
                print("\n⚠️ PLANILLA VACÍA")
            
            resumen.append({
                'Archivo': planilla,
                'Filas': len(df),
                'Columnas': len(df.columns),
                'Tiene ID Ubicación': tiene_id_ubicacion,
                'Estado': 'OK' if len(df) > 0 else 'VACÍA'
            })
            
            print()
            
        except Exception as e:
            print(f"❌ Error al leer {planilla}: {e}")
            print()
            resumen.append({
                'Archivo': planilla,
                'Filas': 0,
                'Columnas': 0,
                'Tiene ID Ubicación': False,
                'Estado': f'ERROR: {str(e)}'
            })

print(f"\n{'='*80}")
print("\n📊 RESUMEN GENERAL")
print(f"{'='*80}\n")

df_resumen = pd.DataFrame(resumen)
print(df_resumen.to_string(index=False))

print(f"\n\n🔍 RECOMENDACIONES:\n")

# Identificar planillas con pocos datos
for item in resumen:
    if item['Filas'] > 0 and item['Filas'] < 5:
        print(f"⚠️  {item['Archivo']}: Solo {item['Filas']} registros - considerar añadir más datos de ejemplo")
    elif item['Filas'] == 0:
        print(f"❌ {item['Archivo']}: VACÍA - requiere datos")

print("\n✓ Análisis completado")
