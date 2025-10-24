import os
import sys
from datetime import datetime, date, timedelta
import random

# Configurar path para importar desde sistema-camaras-flask
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sistema-camaras-flask'))

from app import app, db
from models import (
    Catalogo_Tipo_Falla, Gabinete, Camara, Mantenimiento,
    Ubicacion, Switch, NVR_DVR, Usuario
)

def insertar_tipos_fallas():
    """Insertar 17 tipos de fallas ficticios"""
    print("\n=== INSERTANDO TIPOS DE FALLAS ===")
    
    tipos_fallas = [
        {"nombre": "Tela de araña", "categoria": "Limpieza", "descripcion": "Obstrucción visual por telas de araña", "gravedad": "Baja", "tiempo_estimado_resolucion": 1},
        {"nombre": "Imagen borrosa", "categoria": "Calidad de imagen", "descripcion": "Falta de nitidez en la imagen", "gravedad": "Media", "tiempo_estimado_resolucion": 2},
        {"nombre": "Mica rallada", "categoria": "Daño físico", "descripcion": "Rayones en la cubierta protectora", "gravedad": "Media", "tiempo_estimado_resolucion": 3},
        {"nombre": "Desconectada", "categoria": "Conectividad", "descripcion": "Sin conexión de red o energía", "gravedad": "Alta", "tiempo_estimado_resolucion": 2},
        {"nombre": "Mancha en lente", "categoria": "Limpieza", "descripcion": "Suciedad en el lente de la cámara", "gravedad": "Baja", "tiempo_estimado_resolucion": 1},
        {"nombre": "Empañada", "categoria": "Condiciones ambientales", "descripcion": "Condensación en el lente", "gravedad": "Media", "tiempo_estimado_resolucion": 1},
        {"nombre": "Intermitencia", "categoria": "Conectividad", "descripcion": "Pérdida intermitente de señal", "gravedad": "Alta", "tiempo_estimado_resolucion": 4},
        {"nombre": "Sin energía", "categoria": "Eléctrica", "descripcion": "Falta de alimentación eléctrica", "gravedad": "Critica", "tiempo_estimado_resolucion": 2},
        {"nombre": "Vandalizmo", "categoria": "Daño físico", "descripcion": "Daño intencional al equipo", "gravedad": "Critica", "tiempo_estimado_resolucion": 8},
        {"nombre": "Desalineación", "categoria": "Posicionamiento", "descripcion": "Cámara fuera de posición correcta", "gravedad": "Media", "tiempo_estimado_resolucion": 1},
        {"nombre": "Cable suelto", "categoria": "Conectividad", "descripcion": "Conector de red o energía suelto", "gravedad": "Alta", "tiempo_estimado_resolucion": 1},
        {"nombre": "Puerto dañado", "categoria": "Hardware", "descripcion": "Puerto de red o energía dañado", "gravedad": "Alta", "tiempo_estimado_resolucion": 4},
        {"nombre": "Firmware corrupto", "categoria": "Software", "descripcion": "Error en el firmware de la cámara", "gravedad": "Alta", "tiempo_estimado_resolucion": 3},
        {"nombre": "Sobrecalentamiento", "categoria": "Hardware", "descripcion": "Temperatura excesiva del equipo", "gravedad": "Alta", "tiempo_estimado_resolucion": 2},
        {"nombre": "Ruido en imagen", "categoria": "Calidad de imagen", "descripcion": "Interferencia o ruido visual", "gravedad": "Media", "tiempo_estimado_resolucion": 2},
        {"nombre": "Sin visión nocturna", "categoria": "Hardware", "descripcion": "LEDs IR no funcionan", "gravedad": "Media", "tiempo_estimado_resolucion": 4},
        {"nombre": "Falla de grabación", "categoria": "Software", "descripcion": "No graba en NVR/DVR", "gravedad": "Alta", "tiempo_estimado_resolucion": 3},
    ]
    
    insertados = 0
    for tipo_data in tipos_fallas:
        # Verificar si ya existe
        existe = Catalogo_Tipo_Falla.query.filter_by(nombre=tipo_data['nombre']).first()
        if not existe:
            tipo = Catalogo_Tipo_Falla(**tipo_data)
            db.session.add(tipo)
            insertados += 1
    
    db.session.commit()
    print(f"✓ {insertados} tipos de fallas insertados")
    return insertados

def insertar_gabinetes():
    """Insertar 6 gabinetes ficticios"""
    print("\n=== INSERTANDO GABINETES ===")
    
    # Obtener ubicaciones existentes
    ubicaciones = Ubicacion.query.all()
    if not ubicaciones:
        print("⚠ No hay ubicaciones disponibles")
        return 0
    
    gabinetes = [
        {"codigo": "GAB-FICT-001", "nombre": "Gabinete Exterior Norte", "tipo_ubicacion_general": "Exterior", 
         "tipo_ubicacion_detallada": "Patio norte edificio principal", "capacidad": 12, 
         "tiene_ups": True, "tiene_switch": True, "tiene_nvr": False, "conexion_fibra": True,
         "estado": "Activo", "latitud": -38.7359, "longitud": -72.5986},
        
        {"codigo": "GAB-FICT-002", "nombre": "Gabinete Interior Sur", "tipo_ubicacion_general": "Interior", 
         "tipo_ubicacion_detallada": "Pasillo central piso 2", "capacidad": 8, 
         "tiene_ups": True, "tiene_switch": True, "tiene_nvr": True, "conexion_fibra": True,
         "estado": "Activo", "latitud": -38.7360, "longitud": -72.5987},
        
        {"codigo": "GAB-FICT-003", "nombre": "Gabinete Subterráneo Este", "tipo_ubicacion_general": "Subterraneo", 
         "tipo_ubicacion_detallada": "Subsuelo sector estacionamiento", "capacidad": 16, 
         "tiene_ups": True, "tiene_switch": True, "tiene_nvr": True, "conexion_fibra": True,
         "estado": "Activo", "latitud": -38.7361, "longitud": -72.5988},
        
        {"codigo": "GAB-FICT-004", "nombre": "Gabinete Exterior Oeste", "tipo_ubicacion_general": "Exterior", 
         "tipo_ubicacion_detallada": "Área verde sector oeste", "capacidad": 10, 
         "tiene_ups": False, "tiene_switch": True, "tiene_nvr": False, "conexion_fibra": False,
         "estado": "Activo", "latitud": -38.7362, "longitud": -72.5989},
        
        {"codigo": "GAB-FICT-005", "nombre": "Gabinete Interior Centro", "tipo_ubicacion_general": "Interior", 
         "tipo_ubicacion_detallada": "Hall principal planta baja", "capacidad": 6, 
         "tiene_ups": True, "tiene_switch": False, "tiene_nvr": False, "conexion_fibra": True,
         "estado": "Activo", "latitud": -38.7363, "longitud": -72.5990},
        
        {"codigo": "GAB-FICT-006", "nombre": "Gabinete Exterior Ingreso", "tipo_ubicacion_general": "Exterior", 
         "tipo_ubicacion_detallada": "Porton de ingreso principal", "capacidad": 14, 
         "tiene_ups": True, "tiene_switch": True, "tiene_nvr": True, "conexion_fibra": True,
         "estado": "Activo", "latitud": -38.7364, "longitud": -72.5991},
    ]
    
    insertados = 0
    for i, gab_data in enumerate(gabinetes):
        # Verificar si ya existe
        existe = Gabinete.query.filter_by(codigo=gab_data['codigo']).first()
        if not existe:
            # Asignar ubicación rotativa
            gab_data['ubicacion_id'] = ubicaciones[i % len(ubicaciones)].id
            gab_data['fecha_alta'] = date.today() - timedelta(days=random.randint(30, 365))
            gab_data['fecha_ultima_revision'] = date.today() - timedelta(days=random.randint(1, 30))
            gab_data['observaciones'] = "Gabinete ficticio generado automáticamente"
            
            gabinete = Gabinete(**gab_data)
            db.session.add(gabinete)
            insertados += 1
    
    db.session.commit()
    print(f"✓ {insertados} gabinetes insertados")
    return insertados

def insertar_camaras_placeholder():
    """Insertar 467 cámaras con valores placeholder"""
    print("\n=== INSERTANDO CÁMARAS PLACEHOLDER ===")
    
    # Obtener datos para foreign keys
    ubicaciones = Ubicacion.query.all()
    gabinetes = Gabinete.query.all()
    switches = Switch.query.all()
    nvrs = NVR_DVR.query.all()
    
    if not ubicaciones:
        print("⚠ No hay ubicaciones disponibles")
        return 0
    
    tipos_camara = ['Domo', 'PTZ', 'Bullet']
    estados = ['Activo', 'Inactivo', 'Mantenimiento']
    
    insertados = 0
    camaras_existentes = Camara.query.count()
    
    for i in range(467):
        codigo = f"CAM-PLCH-{str(i+1).zfill(4)}"
        
        # Verificar si ya existe
        existe = Camara.query.filter_by(codigo=codigo).first()
        if existe:
            continue
        
        camara_data = {
            'codigo': codigo,
            'nombre': f"Cámara Placeholder {i+1}",
            'ip': f"192.168.{random.randint(1,254)}.{random.randint(1,254)}",
            'modelo': "vacio",
            'fabricante': "vacio",
            'tipo_camara': random.choice(tipos_camara),
            'ubicacion_id': ubicaciones[i % len(ubicaciones)].id,
            'gabinete_id': gabinetes[i % len(gabinetes)].id if gabinetes else None,
            'switch_id': switches[i % len(switches)].id if switches else None,
            'nvr_id': nvrs[i % len(nvrs)].id if nvrs else None,
            'puerto_nvr': str(12345),
            'requiere_poe_adicional': random.choice([True, False]),
            'tipo_conexion': "vacio",
            'estado': random.choice(estados),
            'fecha_alta': date.today() - timedelta(days=random.randint(30, 730)),
            'instalador': "vacio",
            'fecha_instalacion': date.today() - timedelta(days=random.randint(30, 730)),
            'observaciones': "Cámara placeholder - datos incompletos a completar",
            'latitud': 12345.0,
            'longitud': 12345.0
        }
        
        camara = Camara(**camara_data)
        db.session.add(camara)
        insertados += 1
        
        # Commit cada 50 registros para evitar sobrecarga
        if (i + 1) % 50 == 0:
            db.session.commit()
            print(f"  Progreso: {i+1}/467 cámaras...")
    
    db.session.commit()
    print(f"✓ {insertados} cámaras placeholder insertadas")
    return insertados

def insertar_mantenimientos():
    """Insertar 6 mantenimientos ficticios"""
    print("\n=== INSERTANDO MANTENIMIENTOS ===")
    
    # Obtener usuarios técnicos
    tecnicos = Usuario.query.filter(Usuario.rol.in_(['tecnico', 'admin'])).all()
    if not tecnicos:
        print("⚠ No hay técnicos disponibles")
        return 0
    
    # Obtener equipos para referenciar
    camaras = Camara.query.limit(3).all()
    switches = Switch.query.limit(2).all()
    ups_list = NVR_DVR.query.limit(1).all()
    
    mantenimientos = [
        {
            "equipo_tipo": "Camara",
            "equipo_id": camaras[0].id if camaras else 1,
            "tipo": "Preventivo",
            "descripcion": "Limpieza preventiva de lente y carcasa",
            "materiales_utilizados": "Alcohol isopropílico, paño microfibra",
            "equipos_afectados": "Ninguno",
            "tiempo_ejecucion_horas": 0.5,
            "costo": 5000.0,
            "observaciones": "Mantenimiento ficticio - limpieza rutinaria"
        },
        {
            "equipo_tipo": "Switch",
            "equipo_id": switches[0].id if switches else 1,
            "tipo": "Correctivo",
            "descripcion": "Reemplazo de puerto dañado",
            "materiales_utilizados": "Puerto RJ45, soldadura",
            "equipos_afectados": "2 cámaras desconectadas temporalmente",
            "tiempo_ejecucion_horas": 2.0,
            "costo": 15000.0,
            "observaciones": "Mantenimiento ficticio - reparación puerto"
        },
        {
            "equipo_tipo": "Camara",
            "equipo_id": camaras[1].id if len(camaras) > 1 else 1,
            "tipo": "Preventivo",
            "descripcion": "Verificación de conexiones y ajuste de foco",
            "materiales_utilizados": "Ninguno",
            "equipos_afectados": "Ninguno",
            "tiempo_ejecucion_horas": 0.75,
            "costo": 0.0,
            "observaciones": "Mantenimiento ficticio - revisión técnica"
        },
        {
            "equipo_tipo": "NVR",
            "equipo_id": ups_list[0].id if ups_list else 1,
            "tipo": "Predictivo",
            "descripcion": "Análisis de logs y rendimiento del NVR",
            "materiales_utilizados": "Software de diagnóstico",
            "equipos_afectados": "Ninguno",
            "tiempo_ejecucion_horas": 1.5,
            "costo": 0.0,
            "observaciones": "Mantenimiento ficticio - análisis preventivo"
        },
        {
            "equipo_tipo": "Camara",
            "equipo_id": camaras[2].id if len(camaras) > 2 else 1,
            "tipo": "Correctivo",
            "descripcion": "Reemplazo de cubierta dañada por vandalismo",
            "materiales_utilizados": "Cubierta domo nueva, tornillos",
            "equipos_afectados": "Cámara fuera de servicio 3 horas",
            "tiempo_ejecucion_horas": 3.0,
            "costo": 45000.0,
            "observaciones": "Mantenimiento ficticio - reparación vandálica"
        },
        {
            "equipo_tipo": "Switch",
            "equipo_id": switches[1].id if len(switches) > 1 else 1,
            "tipo": "Preventivo",
            "descripcion": "Limpieza de switch y verificación de puertos",
            "materiales_utilizados": "Aire comprimido, limpiador de contactos",
            "equipos_afectados": "Ninguno",
            "tiempo_ejecucion_horas": 1.0,
            "costo": 8000.0,
            "observaciones": "Mantenimiento ficticio - mantenimiento preventivo"
        },
    ]
    
    insertados = 0
    for mant_data in mantenimientos:
        mant_data['tecnico_id'] = random.choice(tecnicos).id
        mant_data['fecha'] = datetime.now() - timedelta(days=random.randint(1, 90))
        
        mantenimiento = Mantenimiento(**mant_data)
        db.session.add(mantenimiento)
        insertados += 1
    
    db.session.commit()
    print(f"✓ {insertados} mantenimientos insertados")
    return insertados

def main():
    print("\n" + "="*60)
    print("INSERCIÓN DE DATOS FICTICIOS Y PLACEHOLDER")
    print("Base de Datos: Railway PostgreSQL")
    print("="*60)
    
    with app.app_context():
        try:
            # 1. Tipos de Fallas
            tipos = insertar_tipos_fallas()
            
            # 2. Gabinetes
            gabinetes = insertar_gabinetes()
            
            # 3. Cámaras Placeholder
            camaras = insertar_camaras_placeholder()
            
            # 4. Mantenimientos
            mantenimientos = insertar_mantenimientos()
            
            # Resumen final
            print("\n" + "="*60)
            print("✅ INSERCIÓN COMPLETADA")
            print("="*60)
            print(f"✓ Tipos de Fallas: {tipos} insertados")
            print(f"✓ Gabinetes: {gabinetes} insertados")
            print(f"✓ Cámaras Placeholder: {camaras} insertadas")
            print(f"✓ Mantenimientos: {mantenimientos} insertados")
            print("\nTOTAL: {} registros insertados".format(
                tipos + gabinetes + camaras + mantenimientos
            ))
            print("="*60)
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
