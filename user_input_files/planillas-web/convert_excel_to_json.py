import pandas as pd
import json
import os

def convert_excel_to_json(excel_filename, json_filename):
    try:
        df = pd.read_excel(excel_filename)
        # Convertir NaN a None para que se serialice correctamente a null en JSON
        df = df.where(pd.notna(df), None)
        df.to_json(json_filename, orient='records', indent=4, force_ascii=False)
        print(f'✓ Convertido {excel_filename} a {json_filename}')
    except FileNotFoundError:
        print(f'Error: El archivo {excel_filename} no fue encontrado.')
    except Exception as e:
        print(f'Ocurrió un error al convertir {excel_filename}: {e}')

output_dir = './camaras-ufro/public/data'
os.makedirs(output_dir, exist_ok=True)

convert_excel_to_json('Listadecámaras_modificada.xlsx', os.path.join(output_dir, 'cameras.json'))
convert_excel_to_json('Gabinetes.xlsx', os.path.join(output_dir, 'gabinetes.json'))
convert_excel_to_json('Switches.xlsx', os.path.join(output_dir, 'switches.json'))
convert_excel_to_json('Puertos_Switch.xlsx', os.path.join(output_dir, 'switch_ports.json'))
convert_excel_to_json('Equipos_Tecnicos.xlsx', os.path.join(output_dir, 'technical_equipment.json'))
convert_excel_to_json('Fallas_Actualizada.xlsx', os.path.join(output_dir, 'failures.json'))
convert_excel_to_json('Mantenimientos.xlsx', os.path.join(output_dir, 'maintenance.json'))
convert_excel_to_json('Ubicaciones.xlsx', os.path.join(output_dir, 'locations.json'))
convert_excel_to_json('Catalogo_Tipos_Fallas.xlsx', os.path.join(output_dir, 'failure_types.json'))
convert_excel_to_json('Ejemplos_Fallas_Reales.xlsx', os.path.join(output_dir, 'real_failure_examples.json'))

