import os
import sys
from datetime import datetime

# Configurar path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sistema-camaras-flask'))

from app import app, db
from models import (
    Usuario, Ubicacion, Gabinete, Switch, Puerto_Switch,
    UPS, NVR_DVR, Fuente_Poder, Camara, Catalogo_Tipo_Falla,
    Falla, Mantenimiento, Equipo_Tecnico, Historial_Estado_Equipo
)

def verificar_tablas():
    """Verificar conteo de registros en todas las tablas"""
    
    tablas = [
        ('Usuario', Usuario),
        ('Ubicacion', Ubicacion),
        ('Gabinete', Gabinete),
        ('Switch', Switch),
        ('Puerto_Switch', Puerto_Switch),
        ('UPS', UPS),
        ('NVR_DVR', NVR_DVR),
        ('Fuente_Poder', Fuente_Poder),
        ('Camara', Camara),
        ('Catalogo_Tipo_Falla', Catalogo_Tipo_Falla),
        ('Falla', Falla),
        ('Mantenimiento', Mantenimiento),
        ('Equipo_Tecnico', Equipo_Tecnico),
        ('Historial_Estado_Equipo', Historial_Estado_Equipo),
    ]
    
    print("\n" + "="*70)
    print("VERIFICACIÓN DE TABLAS - BASE DE DATOS RAILWAY")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    tablas_vacias = []
    tablas_con_datos = []
    total_registros = 0
    
    print("\n{:<30} {:<15} {:<20}".format("TABLA", "REGISTROS", "ESTADO"))
    print("-"*70)
    
    for nombre, modelo in tablas:
        try:
            count = modelo.query.count()
            estado = "✅ CON DATOS" if count > 0 else "❌ VACÍA"
            
            print("{:<30} {:<15} {:<20}".format(nombre, count, estado))
            
            if count > 0:
                tablas_con_datos.append((nombre, count))
            else:
                tablas_vacias.append(nombre)
            
            total_registros += count
            
        except Exception as e:
            print("{:<30} {:<15} {:<20}".format(nombre, "ERROR", str(e)[:20]))
    
    print("-"*70)
    print(f"TOTAL DE REGISTROS EN BD: {total_registros}")
    print("="*70)
    
    # Resumen de tablas vacías
    if tablas_vacias:
        print("\n⚠️  TABLAS VACÍAS ({}):".format(len(tablas_vacias)))
        for tabla in tablas_vacias:
            print(f"   - {tabla}")
    else:
        print("\n✅ TODAS LAS TABLAS TIENEN DATOS")
    
    # Resumen de tablas con datos
    if tablas_con_datos:
        print("\n✅ TABLAS CON DATOS ({}):".format(len(tablas_con_datos)))
        for tabla, count in sorted(tablas_con_datos, key=lambda x: x[1], reverse=True):
            print(f"   - {tabla}: {count} registros")
    
    print("\n" + "="*70)
    
    return tablas_vacias, tablas_con_datos

def main():
    with app.app_context():
        try:
            tablas_vacias, tablas_con_datos = verificar_tablas()
            
            if tablas_vacias:
                print("\n⚠️  Se requiere acción para poblar las siguientes tablas:")
                for tabla in tablas_vacias:
                    print(f"   • {tabla}")
                return 1
            else:
                print("\n🎉 Base de datos completamente poblada")
                return 0
                
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            return 1

if __name__ == '__main__':
    exit(main())
