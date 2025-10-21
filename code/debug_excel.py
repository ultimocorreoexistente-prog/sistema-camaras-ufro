import pandas as pd
import sys

# Función de limpieza (copia del script migrate_data.py)
def limpiar_filas_vacias(df):
    """Elimina filas completamente vacías o sin datos relevantes del DataFrame"""
    if df is None or df.empty:
        return df
    
    print(f"\nDataFrame original: {len(df)} filas")
    print(f"Primeras 10 filas (valores):\n{df.head(10)}\n")
    
    # Eliminar filas donde TODOS los valores son NaN
    df_limpio = df.dropna(how='all')
    print(f"Después de dropna(how='all'): {len(df_limpio)} filas")
    
    # Eliminar filas donde TODOS los valores son strings vacíos o espacios
    df_limpio = df_limpio[~df_limpio.apply(
        lambda row: all(
            (pd.isna(val) or (isinstance(val, str) and not val.strip()))
            for val in row
        ), axis=1
    )]
    print(f"Después de eliminar strings vacíos: {len(df_limpio)} filas")
    
    # Reset del índice después de limpiar
    df_limpio = df_limpio.reset_index(drop=True)
    
    filas_eliminadas = len(df) - len(df_limpio)
    print(f"\nFILAS ELIMINADAS: {filas_eliminadas}")
    print(f"\nDataFrame limpio (primeras 10 filas):\n{df_limpio.head(10)}")
    
    return df_limpio

# Probar con Equipos_Tecnicos.xlsx
print("="*60)
print("DEBUGGEANDO: Equipos_Tecnicos.xlsx")
print("="*60)

df = pd.read_excel('sistema-camaras-flask/planillas/Equipos_Tecnicos.xlsx')
df_limpio = limpiar_filas_vacias(df)

print("\n" + "="*60)
print("VERIFICANDO CAMPO 'Nombre' (requerido)")
print("="*60)
for idx, row in df_limpio.iterrows():
    nombre = row.get('Nombre')
    if pd.isna(nombre):
        print(f"Fila {idx}: Nombre = NaN")
    elif isinstance(nombre, str) and not nombre.strip():
        print(f"Fila {idx}: Nombre = '{nombre}' (vacío)")
    else:
        print(f"Fila {idx}: Nombre = '{nombre}' ✓")
