import pandas as pd
import os

# Ruta base
base_path = "user_input_files/sistema-camaras-ufro-main/sistema-camaras-ufro-main/planillas"

# Listar archivos
print("📁 Archivos Excel encontrados:")
excel_files = []
for file in os.listdir(base_path):
    if file.endswith('.xlsx'):
        filepath = os.path.join(base_path, file)
        print(f"\n✅ {file}")
        excel_files.append(filepath)

# Analizar cada archivo
for filepath in excel_files:
    print(f"\n{'='*80}")
    print(f"📊 ANALIZANDO: {os.path.basename(filepath)}")
    print(f"{'='*80}")
    
    try:
        # Leer Excel
        xl_file = pd.ExcelFile(filepath)
        
        print(f"\n📋 Hojas disponibles: {xl_file.sheet_names}")
        
        # Analizar cada hoja
        for sheet in xl_file.sheet_names:
            df = pd.read_excel(filepath, sheet_name=sheet)
            print(f"\n  📄 Hoja: '{sheet}'")
            print(f"     - Filas: {len(df)}")
            print(f"     - Columnas: {len(df.columns)}")
            print(f"     - Columnas: {list(df.columns)[:10]}")  # Primeras 10 columnas
            
            # Mostrar primeras filas
            if len(df) > 0:
                print(f"\n     Primeras 3 filas:")
                print(df.head(3).to_string(index=False)[:500])
                
    except Exception as e:
        print(f"❌ Error leyendo {filepath}: {e}")

print("\n\n✅ Análisis completado")
