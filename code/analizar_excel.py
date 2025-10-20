import pandas as pd
import os

# Directorio de planillas
planillas_dir = "user_input_files/planillas-web"

# Listar archivos Excel
excel_files = [f for f in os.listdir(planillas_dir) if f.endswith('.xlsx')]

print("=== ARCHIVOS EXCEL ENCONTRADOS ===")
for f in excel_files:
    print(f"- {f}")

print("\n=== ANÁLISIS DE ESTRUCTURA DE DATOS ===\n")

# Analizar cada archivo
for file in excel_files:
    try:
        file_path = os.path.join(planillas_dir, file)
        df = pd.read_excel(file_path)
        print(f"\n📊 {file}")
        print(f"   Filas: {len(df)}")
        print(f"   Columnas ({len(df.columns)}): {list(df.columns)}")
    except Exception as e:
        print(f"\n❌ Error en {file}: {e}")
