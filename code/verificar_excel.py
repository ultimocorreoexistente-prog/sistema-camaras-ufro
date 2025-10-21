import pandas as pd

# Verificar un archivo para entender la estructura
df = pd.read_excel('sistema-camaras-flask/planillas/Equipos_Tecnicos.xlsx')
print("=== Equipos_Tecnicos.xlsx ===")
print(f"Filas totales: {len(df)}")
print(f"\nColumnas: {list(df.columns)}")
print(f"\nPrimeras 3 filas:")
print(df.head(3))
print(f"\nValores únicos en 'Nombre':")
for idx, row in df.iterrows():
    nombre = row.get('Nombre')
    print(f"  Fila {idx}: '{nombre}' (tipo: {type(nombre)}, es NaN: {pd.isna(nombre)})")
