import pandas as pd
import sys

# Leer el archivo Excel más reciente con los casos reales
file_path = 'user_input_files/sistema-camaras-ufro-main/sistema-camaras-ufro-main/planillas/Ejemplos_Fallas_Reales_corregido_20251019_005201.xlsx'

print(f"Intentando leer: {file_path}")

try:
    # Leer la hoja de fallas con openpyxl engine
    df = pd.read_excel(file_path, engine='openpyxl')
    
    print("\n" + "="*100)
    print("CASOS REALES DOCUMENTADOS - SISTEMA DE GESTIÓN DE CÁMARAS UFRO")
    print("="*100)
    print(f"\nTotal de casos: {len(df)}")
    print(f"Columnas: {list(df.columns)}\n")
    
    # Mostrar información por cada caso
    for idx, row in df.iterrows():
        print(f"\n{'='*100}")
        print(f"CASO {idx + 1}")
        print(f"{'='*100}")
        
        for col in df.columns:
            value = row[col]
            if pd.notna(value) and str(value).strip() != '':
                print(f"  • {col}: {value}")
    
except Exception as e:
    print(f"\nError: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
