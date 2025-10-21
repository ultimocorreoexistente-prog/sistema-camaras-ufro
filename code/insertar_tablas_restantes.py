import os
import sys
from datetime import datetime, date, timedelta
import random

# Configurar path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sistema-camaras-flask'))

from app import app, db
from models import (
    Puerto_Switch, Falla, Historial_Estado_Equipo,
    Switch, Camara, Catalogo_Tipo_Falla, Usuario
)

def insertar_puertos_switch():
    """Insertar puertos para cada switch existente"""
    print("\n=== INSERTANDO PUERTOS DE SWITCH ===")
    
    switches = Switch.query.all()
    if not switches:
        print("⚠ No hay switches disponibles")
        return 0
    
    camaras = Camara.query.limit(50).all()  # Tomar primeras 50 cámaras
    
    estados_puerto = ['En uso', 'Disponible', 'Averiado']
    tipos_conexion = ['PoE', 'Normal', 'Fibra']
    
    insertados = 0
    camara_idx = 0
    
    for switch in switches:
        # Cada switch tiene puertos_totales puertos
        puertos_totales = switch.puertos_totales if switch.puertos_totales else 24
        puertos_usados = switch.puertos_usados if switch.puertos_usados else 0
        
        print(f"  Switch {switch.codigo}: {puertos_totales} puertos")
        
        for num_puerto in range(1, puertos_totales + 1):
            # Verificar si ya existe
            existe = Puerto_Switch.query.filter_by(
                switch_id=switch.id,
                numero_puerto=num_puerto
            ).first()
            
            if existe:
                continue
            
            # Determinar si el puerto está en uso
            if num_puerto <= puertos_usados and camara_idx < len(camaras):
                # Puerto en uso con cámara
                puerto_data = {
                    'switch_id': switch.id,
                    'numero_puerto': num_puerto,
                    'camara_id': camaras[camara_idx].id,
                    'ip_dispositivo': camaras[camara_idx].ip,
                    'estado': 'En uso',
                    'tipo_conexion': random.choice(['PoE', 'Normal']),
                    'nvr_id': None,
                    'puerto_nvr': None
                }
                camara_idx += 1
            else:
                # Puerto disponible o averiado
                estado = random.choice(['Disponible', 'Disponible', 'Disponible', 'Averiado'])
                puerto_data = {
                    'switch_id': switch.id,
                    'numero_puerto': num_puerto,
                    'camara_id': None,
                    'ip_dispositivo': None,
                    'estado': estado,
                    'tipo_conexion': random.choice(tipos_conexion) if estado == 'Disponible' else None,
                    'nvr_id': None,
                    'puerto_nvr': None
                }
            
            puerto = Puerto_Switch(**puerto_data)
            db.session.add(puerto)
            insertados += 1
        
        # Commit cada switch
        db.session.commit()
    
    print(f"✓ {insertados} puertos de switch insertados")
    return insertados

def insertar_fallas():
    """Insertar fallas ficticias para diferentes equipos"""
    print("\n=== INSERTANDO FALLAS ===")
    
    # Obtener datos necesarios
    camaras = Camara.query.limit(20).all()
    tipos_falla = Catalogo_Tipo_Falla.query.all()
    usuarios = Usuario.query.all()
    
    if not camaras or not tipos_falla or not usuarios:
        print("⚠ Faltan datos necesarios para crear fallas")
        return 0
    
    prioridades = ['Baja', 'Media', 'Alta', 'Critica']
    estados = ['Pendiente', 'Asignada', 'En Proceso', 'Reparada', 'Cerrada']
    
    fallas_data = []
    
    # Crear 15 fallas ficticias
    for i in range(15):
        camara = random.choice(camaras)
        tipo_falla = random.choice(tipos_falla)
        reportador = random.choice(usuarios)
        estado = random.choice(estados)
        
        fecha_reporte = datetime.now() - timedelta(days=random.randint(1, 90))
        
        falla = {
            'equipo_tipo': 'Camara',
            'equipo_id': camara.id,
            'tipo_falla_id': tipo_falla.id,
            'descripcion': f"Falla ficticia {i+1}: {tipo_falla.nombre} en {camara.nombre}",
            'prioridad': random.choice(prioridades),
            'fecha_reporte': fecha_reporte,
            'reportado_por_id': reportador.id,
            'estado': estado,
            'observaciones': "Falla ficticia generada automáticamente"
        }
        
        # Si está asignada o en proceso, agregar técnico y fechas
        if estado in ['Asignada', 'En Proceso', 'Reparada', 'Cerrada']:
            tecnico = random.choice(usuarios)
            falla['tecnico_asignado_id'] = tecnico.id
            falla['fecha_asignacion'] = fecha_reporte + timedelta(hours=random.randint(1, 24))
        
        # Si está en proceso o reparada, agregar fecha inicio
        if estado in ['En Proceso', 'Reparada', 'Cerrada']:
            falla['fecha_inicio_reparacion'] = falla['fecha_asignacion'] + timedelta(hours=random.randint(1, 48))
        
        # Si está reparada o cerrada, agregar solución
        if estado in ['Reparada', 'Cerrada']:
            falla['fecha_fin_reparacion'] = falla['fecha_inicio_reparacion'] + timedelta(hours=random.randint(1, 8))
            tiempo_resolucion = (falla['fecha_fin_reparacion'] - falla['fecha_inicio_reparacion']).total_seconds() / 3600
            falla['tiempo_resolucion_horas'] = round(tiempo_resolucion, 2)
            falla['solucion_aplicada'] = f"Solución ficticia aplicada: {tipo_falla.nombre} corregida"
            falla['materiales_utilizados'] = "Materiales ficticios"
            falla['costo_reparacion'] = random.choice([0, 5000, 10000, 15000, 25000, 50000])
        
        # Si está cerrada, agregar fecha cierre
        if estado == 'Cerrada':
            falla['fecha_cierre'] = falla['fecha_fin_reparacion'] + timedelta(days=random.randint(0, 3))
        
        fallas_data.append(falla)
    
    # Insertar todas las fallas
    insertados = 0
    for falla_dict in fallas_data:
        falla = Falla(**falla_dict)
        db.session.add(falla)
        insertados += 1
    
    db.session.commit()
    print(f"✓ {insertados} fallas insertadas")
    return insertados

def insertar_historial_estado():
    """Insertar historial de cambios de estado para equipos"""
    print("\n=== INSERTANDO HISTORIAL DE ESTADO ===")
    
    # Obtener equipos y usuarios
    camaras = Camara.query.limit(30).all()
    usuarios = Usuario.query.all()
    
    if not camaras or not usuarios:
        print("⚠ Faltan datos necesarios para crear historial")
        return 0
    
    estados = ['Activo', 'Inactivo', 'Mantenimiento', 'Baja']
    motivos = [
        "Cambio de estado manual por administrador",
        "Mantenimiento programado",
        "Falla detectada",
        "Reparación completada",
        "Equipo dado de baja por obsolescencia",
        "Reactivación tras mantenimiento",
        "Cambio de ubicación",
        "Actualización de firmware"
    ]
    
    insertados = 0
    
    # Crear 20 registros de historial
    for i in range(20):
        camara = random.choice(camaras)
        usuario = random.choice(usuarios)
        
        # Simular cambio de estado
        estado_actual = camara.estado
        posibles_estados = [e for e in estados if e != estado_actual]
        estado_nuevo = random.choice(posibles_estados) if posibles_estados else estado_actual
        
        historial_data = {
            'equipo_tipo': 'Camara',
            'equipo_id': camara.id,
            'estado_anterior': random.choice(estados),
            'estado_nuevo': estado_nuevo,
            'fecha_cambio': datetime.now() - timedelta(days=random.randint(1, 180)),
            'motivo': random.choice(motivos),
            'usuario_id': usuario.id
        }
        
        historial = Historial_Estado_Equipo(**historial_data)
        db.session.add(historial)
        insertados += 1
    
    db.session.commit()
    print(f"✓ {insertados} registros de historial insertados")
    return insertados

def main():
    print("\n" + "="*60)
    print("INSERCIÓN DE DATOS FICTICIOS - TABLAS RESTANTES")
    print("Base de Datos: Railway PostgreSQL")
    print("="*60)
    
    with app.app_context():
        try:
            # 1. Puertos de Switch
            puertos = insertar_puertos_switch()
            
            # 2. Fallas
            fallas = insertar_fallas()
            
            # 3. Historial de Estado
            historial = insertar_historial_estado()
            
            # Resumen final
            print("\n" + "="*60)
            print("✅ INSERCIÓN COMPLETADA")
            print("="*60)
            print(f"✓ Puertos de Switch: {puertos} insertados")
            print(f"✓ Fallas: {fallas} insertadas")
            print(f"✓ Historial de Estado: {historial} insertados")
            print("\nTOTAL: {} registros insertados".format(
                puertos + fallas + historial
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
