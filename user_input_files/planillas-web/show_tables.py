import pandas as pd

def show_table(filename):
    try:
        df = pd.read_excel(filename)
        print(f"### {filename}\n")
        print(df.head().to_markdown(index=False))
        print("\n\n")
    except FileNotFoundError:
        print(f"Archivo no encontrado: {filename}")
    except Exception as e:
        print(f"Error al leer {filename}: {e}")

show_table("Listadecámaras_modificada.xlsx")
show_table("Gabinetes.xlsx")
show_table("Switches.xlsx")
show_table("Puertos_Switch.xlsx")
show_table("Equipos_Tecnicos.xlsx")
show_table("Fallas_Actualizada.xlsx")
show_table("Mantenimientos.xlsx")
show_table("Ubicaciones.xlsx")

