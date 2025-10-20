import pandas as pd

def generate_missing_fields_report(filename):
    try:
        df = pd.read_excel(filename)
        report = []
        report.append(f"# Informe de Campos Faltantes en {filename}")
        report.append(f"\nEste informe detalla las columnas con valores faltantes (vacíos o nulos) en la planilla de cámaras, para facilitar su completado.\n")

        missing_data = df.isnull().sum()
        missing_data = missing_data[missing_data > 0]

        if missing_data.empty:
            report.append("No se encontraron campos faltantes en la planilla.\\")
        else:
            report.append("## Resumen de Campos Faltantes por Columna\n")
            report.append("| Columna | Valores Faltantes | Porcentaje Faltante |\\")
            report.append("|:--------|:------------------|:--------------------|\\")
            
            total_rows = len(df)
            for col, count in missing_data.items():
                percentage = (count / total_rows) * 100
                report.append(f"| {col} | {count} | {percentage:.2f}% |\\")
            report.append("\n")

            report.append("## Detalles de Campos Faltantes (Primeras 5 filas con valores nulos)\n")
            for col in missing_data.index:
                missing_rows = df[df[col].isnull()].head(5)
                if not missing_rows.empty:
                    report.append(f"### Columna: {col}\n")
                    report.append(f"Primeras 5 filas donde `{col}` está faltante:\\")
                    # Ensure 'col' is treated as a string and correctly added to the list of columns
                    cols_to_display = [c for c in ["Nombre de Cámara", "IP de Cámara", col] if c in df.columns]
                    report.append(missing_rows[cols_to_display].to_markdown(index=False))
                    report.append("\n")

        with open("informe_campos_faltantes.md", "w", encoding="utf-8") as f:
            f.write("\n".join(report))
        print("Informe de campos faltantes generado en informe_campos_faltantes.md")

    except FileNotFoundError:
        print(f"Error: El archivo {filename} no fue encontrado.\\")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

generate_missing_fields_report("Listadecámaras_modificada.xlsx")

