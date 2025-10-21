import pandas as pd
import sys

print("Analizando Equipos_Tecnicos.xlsx...")
df = pd.read_excel('sistema-camaras-flask/planillas/Equipos_Tecnicos.xlsx')

print(f"\nTOTAL FILAS: {len(df)}")
print(f"COLUMNAS: {list(df.columns)}")

print("\nPRIMERAS 10 FILAS (columna 'Nombre'):")
for idx in range(min(10, len(df))):
    nombre = df.iloc[idx].get('Nombre')
    print(f"  Fila {idx}: {repr(nombre)} | es NaN: {pd.isna(nombre)}")

# Contar cuántas filas tienen Nombre válido
validos = 0
for idx, row in df.iterrows():
    nombre = row.get('Nombre')
    if not pd.isna(nombre) and str(nombre).strip():
        validos += 1

print(f"\nFILAS CON NOMBRE VÁLIDO: {validos}/{len(df)}")
