import pandas as pd
import os
from datetime import datetime
from app import app, db
from models import (Camara, Gabinete, Switch, PuertoSwitch, EquipoTecnico, 
                    Falla, Mantenimiento, Ubicacion, TipoFalla)

def limpiar_valor(valor):
    """Limpia valores NaN y None"""
    if pd.isna(valor) or valor is None:
        return None
    return str(valor).strip() if isinstance(valor, str) else valor

def parsear_fecha(fecha_str):
    """Parsea fechas en diferentes formatos"""
    if pd.isna(fecha_str) or fecha_str is None:
        return None
    try:
        if isinstance(fecha_str, str):
            return datetime.strptime(fecha_str, '%Y-%m-%d').date()
        return fecha_str.date() if hasattr(fecha_str, 'date') else None
    except:
        return None

def migrar_ubicaciones():
    print("\nMigrando Ubicaciones...")
    df = pd.read_excel('planillas/Ubicaciones.xlsx')
    for _, row in df.iterrows():
        ubicacion = Ubicacion(
            campus=limpiar_valor(row.get('Campus')),
            edificio=limpiar_valor(row.get('Edificio')),
            piso=limpiar_valor(row.get('Piso/Nivel')),
            zona=limpiar_valor(row.get('Zona')),
            gabinetes_en_ubicacion=limpiar_valor(row.get('Gabinetes en Ubicación')),
            cantidad_camaras=int(row.get('Cantidad de Cámaras', 0)) if pd.notna(row.get('Cantidad de Cámaras')) else None,
            observaciones=limpiar_valor(row.get('Observaciones'))
        )
        db.session.add(ubicacion)
    db.session.commit()
    print(f"✓ {len(df)} ubicaciones migradas")

def migrar_gabinetes():
    print("\nMigrando Gabinetes...")
    df = pd.read_excel('planillas/Gabinetes.xlsx')
    for _, row in df.iterrows():
        gabinete = Gabinete(
            codigo=limpiar_valor(row.get('ID Gabinete')),
            nombre=limpiar_valor(row.get('Nombre del Gabinete')),
            ubicacion=limpiar_valor(row.get('Ubicación Detallada')),
            campus=limpiar_valor(row.get('Campus')),
            edificio=limpiar_valor(row.get('Edificio')),
            piso=limpiar_valor(row.get('Piso')),
            coordenadas=limpiar_valor(row.get('Coordenadas')),
            tipo=limpiar_valor(row.get('Tipo de Gabinete')),
            estado=limpiar_valor(row.get('Estado')),
            switch_principal=limpiar_valor(row.get('Switch Principal')),
            nvr_asociado=limpiar_valor(row.get('NVR Asociado')),
            camaras_conectadas=int(row.get('Número de Cámaras Conectadas', 0)) if pd.notna(row.get('Número de Cámaras Conectadas')) else None,
            fecha_instalacion=parsear_fecha(row.get('Fecha de Instalación')),
            observaciones=limpiar_valor(row.get('Observaciones'))
        )
        db.session.add(gabinete)
    db.session.commit()
    print(f"✓ {len(df)} gabinetes migrados")

def migrar_switches():
    print("\nMigrando Switches...")
    df = pd.read_excel('planillas/Switches.xlsx')
    for _, row in df.iterrows():
        # Buscar gabinete asociado
        gabinete_codigo = limpiar_valor(row.get('Gabinete Asociado'))
        gabinete = Gabinete.query.filter_by(codigo=gabinete_codigo).first() if gabinete_codigo else None
        
        switch = Switch(
            codigo=limpiar_valor(row.get('ID Switch')),
            nombre=limpiar_valor(row.get('Nombre/Modelo')),
            marca=limpiar_valor(row.get('Marca')),
            numero_serie=limpiar_valor(row.get('Número de Serie')),
            gabinete_id=gabinete.id if gabinete else None,
            puertos_totales=int(row.get('Número Total de Puertos', 0)) if pd.notna(row.get('Número Total de Puertos')) else None,
            puertos_usados=int(row.get('Puertos Usados', 0)) if pd.notna(row.get('Puertos Usados')) else None,
            puertos_disponibles=int(row.get('Puertos Disponibles', 0)) if pd.notna(row.get('Puertos Disponibles')) else None,
            soporta_poe=row.get('Soporta PoE') == 'Sí' if pd.notna(row.get('Soporta PoE')) else False,
            estado=limpiar_valor(row.get('Estado')),
            fecha_instalacion=parsear_fecha(row.get('Fecha de Instalación')),
            fecha_ultimo_mantenimiento=parsear_fecha(row.get('Fecha de Último Mantenimiento')),
            observaciones=limpiar_valor(row.get('Observaciones'))
        )
        db.session.add(switch)
    db.session.commit()
    print(f"✓ {len(df)} switches migrados")

def migrar_puertos_switch():
    print("\nMigrando Puertos de Switch...")
    df = pd.read_excel('planillas/Puertos_Switch.xlsx')
    for _, row in df.iterrows():
        # Buscar switch asociado
        switch_codigo = limpiar_valor(row.get('ID Switch'))
        switch = Switch.query.filter_by(codigo=switch_codigo).first() if switch_codigo else None
        
        puerto = PuertoSwitch(
            switch_id=switch.id if switch else None,
            numero_puerto=int(row.get('Número de Puerto', 0)) if pd.notna(row.get('Número de Puerto')) else None,
            estado=limpiar_valor(row.get('Estado Puerto')),
            dispositivo_conectado=limpiar_valor(row.get('Dispositivo Conectado')),
            ip_dispositivo=limpiar_valor(row.get('IP Dispositivo')),
            tipo_conexion=limpiar_valor(row.get('Tipo de Conexión')),
            nvr_asociado=limpiar_valor(row.get('NVR Asociado (Puerto)')),
            puerto_nvr=limpiar_valor(row.get('Puerto NVR (Puerto)')),
            observaciones=limpiar_valor(row.get('Observaciones'))
        )
        db.session.add(puerto)
    db.session.commit()
    print(f"✓ {len(df)} puertos migrados")

def migrar_camaras():
    print("\nMigrando Cámaras...")
    df = pd.read_excel('planillas/Listadecámaras_modificada.xlsx')
    for _, row in df.iterrows():
        camara = Camara(
            codigo=limpiar_valor(row.get('Código Cámara')),
            nombre=limpiar_valor(row.get('Nombre de Cámara')),
            campus=limpiar_valor(row.get('Campus')),
            edificio=limpiar_valor(row.get('Edificio')),
            piso=limpiar_valor(row.get('Piso')),
            ubicacion=limpiar_valor(row.get('Ubicación Detallada')),
            ip=limpiar_valor(row.get('Dirección IP')),
            marca=limpiar_valor(row.get('Marca')),
            modelo=limpiar_valor(row.get('Modelo')),
            tipo=limpiar_valor(row.get('Tipo de Cámara')),
            resolucion=limpiar_valor(row.get('Resolución')),
            estado=limpiar_valor(row.get('Estado')),
            gabinete_asociado=limpiar_valor(row.get('Gabinete Asociado')),
            switch_conectado=limpiar_valor(row.get('Switch Conectado')),
            puerto_switch=limpiar_valor(row.get('Puerto Switch')),
            nvr_asociado=limpiar_valor(row.get('NVR Asociado')),
            puerto_nvr=limpiar_valor(row.get('Puerto NVR')),
            fecha_instalacion=parsear_fecha(row.get('Fecha de Instalación')),
            observaciones=limpiar_valor(row.get('Observaciones'))
        )
        db.session.add(camara)
    db.session.commit()
    print(f"✓ {len(df)} cámaras migradas")

def migrar_equipos_tecnicos():
    print("\nMigrando Equipos Técnicos...")
    df = pd.read_excel('planillas/Equipos_Tecnicos.xlsx')
    for _, row in df.iterrows():
        # Buscar gabinete asociado
        ubicacion_str = limpiar_valor(row.get('Ubicación'))
        gabinete = Gabinete.query.filter(Gabinete.codigo.like(f'%{ubicacion_str}%')).first() if ubicacion_str else None
        
        equipo = EquipoTecnico(
            tipo=limpiar_valor(row.get('Tipo de Equipo')),
            marca=limpiar_valor(row.get('Marca')),
            modelo=limpiar_valor(row.get('Modelo')),
            numero_serie=limpiar_valor(row.get('Número de Serie')),
            capacidad=limpiar_valor(row.get('Capacidad (VA/W/Canales)')),
            ubicacion=ubicacion_str,
            gabinete_id=gabinete.id if gabinete else None,
            estado=limpiar_valor(row.get('Estado')),
            fecha_instalacion=parsear_fecha(row.get('Fecha de Instalación')),
            fecha_ultimo_mantenimiento=parsear_fecha(row.get('Última Revisión')),
            proximo_mantenimiento=parsear_fecha(row.get('Próximo Mantenimiento Programado')),
            observaciones=limpiar_valor(row.get('Observaciones'))
        )
        db.session.add(equipo)
    db.session.commit()
    print(f"✓ {len(df)} equipos técnicos migrados")

def migrar_fallas():
    print("\nMigrando Fallas...")
    df = pd.read_excel('planillas/Fallas_Actualizada.xlsx')
    for _, row in df.iterrows():
        # Buscar cámara asociada
        camara_codigo = limpiar_valor(row.get('Cámara Afectada'))
        camara = Camara.query.filter_by(codigo=camara_codigo).first() if camara_codigo else None
        
        falla = Falla(
            fecha_reporte=parsear_fecha(row.get('Fecha de Reporte')),
            reportado_por=limpiar_valor(row.get('Reportado Por')),
            tipo=limpiar_valor(row.get('Tipo')),
            subtipo=limpiar_valor(row.get('Subtipo')),
            camara_id=camara.id if camara else None,
            camara_afectada=camara_codigo,
            ubicacion=limpiar_valor(row.get('Ubicación')),
            descripcion=limpiar_valor(row.get('Descripción')),
            impacto_visibilidad=limpiar_valor(row.get('Impacto en Visibilidad')),
            afecta_vision_nocturna=limpiar_valor(row.get('Afecta Visión Nocturna')),
            estado=limpiar_valor(row.get('Estado')),
            prioridad=limpiar_valor(row.get('Prioridad')),
            tecnico_asignado=limpiar_valor(row.get('Técnico Asignado')),
            observaciones=limpiar_valor(row.get('Observaciones'))
        )
        db.session.add(falla)
    db.session.commit()
    print(f"✓ {len(df)} fallas migradas")

def migrar_ejemplos_fallas_reales():
    print("\nMigrando Ejemplos de Fallas Reales...")
    try:
        df = pd.read_excel('planillas/Ejemplos_Fallas_Reales.xlsx')
        for _, row in df.iterrows():
            # Buscar cámara asociada
            camara_codigo = limpiar_valor(row.get('Cámara Afectada'))
            camara = Camara.query.filter_by(codigo=camara_codigo).first() if camara_codigo else None
            
            falla = Falla(
                fecha_reporte=parsear_fecha(row.get('Fecha de Reporte')),
                reportado_por=limpiar_valor(row.get('Reportado Por')),
                tipo=limpiar_valor(row.get('Tipo de Falla')),
                subtipo=limpiar_valor(row.get('Subtipo')),
                camara_id=camara.id if camara else None,
                camara_afectada=camara_codigo,
                ubicacion=limpiar_valor(row.get('Ubicación')),
                descripcion=limpiar_valor(row.get('Descripción')),
                impacto_visibilidad=limpiar_valor(row.get('Impacto en Visibilidad')),
                afecta_vision_nocturna=limpiar_valor(row.get('Afecta Visión Nocturna')),
                estado=limpiar_valor(row.get('Estado')),
                prioridad=limpiar_valor(row.get('Prioridad')),
                tecnico_asignado=limpiar_valor(row.get('Técnico Asignado')),
                observaciones=limpiar_valor(row.get('Observaciones'))
            )
            db.session.add(falla)
        db.session.commit()
        print(f"✓ {len(df)} casos reales migrados")
    except Exception as e:
        print(f"Error en migración de casos reales: {e}")

def migrar_mantenimientos():
    print("\nMigrando Mantenimientos...")
    df = pd.read_excel('planillas/Mantenimientos.xlsx')
    for _, row in df.iterrows():
        mantenimiento = Mantenimiento(
            fecha_programada=parsear_fecha(row.get('Fecha Programada')),
            fecha_realizacion=parsear_fecha(row.get('Fecha de Realización')),
            tipo=limpiar_valor(row.get('Tipo de Mantenimiento')),
            categoria=limpiar_valor(row.get('Categoría')),
            equipo_gabinete=limpiar_valor(row.get('Equipo/Gabinete')),
            ubicacion=limpiar_valor(row.get('Ubicación')),
            descripcion=limpiar_valor(row.get('Descripción del Trabajo')),
            estado=limpiar_valor(row.get('Estado')),
            tecnico_responsable=limpiar_valor(row.get('Técnico Responsable')),
            materiales_utilizados=limpiar_valor(row.get('Materiales Utilizados')),
            costo_aproximado=float(row.get('Costo Aproximado', 0)) if pd.notna(row.get('Costo Aproximado')) else None,
            equipos_camaras_afectadas=limpiar_valor(row.get('Equipos/Cámaras Afectadas')),
            tiempo_ejecucion=limpiar_valor(row.get('Tiempo de Ejecución')),
            observaciones=limpiar_valor(row.get('Observaciones'))
        )
        db.session.add(mantenimiento)
    db.session.commit()
    print(f"✓ {len(df)} mantenimientos migrados")

def migrar_tipos_fallas():
    print("\nMigrando Catálogo de Tipos de Fallas...")
    df = pd.read_excel('planillas/Catalogo_Tipos_Fallas.xlsx')
    for _, row in df.iterrows():
        tipo_falla = TipoFalla(
            categoria_principal=limpiar_valor(row.get('Categoría Principal')),
            tipo_falla=limpiar_valor(row.get('Tipo de Falla')),
            impacto_tipico=limpiar_valor(row.get('Impacto Típico')),
            tipo_mantenimiento=limpiar_valor(row.get('Tipo de Mantenimiento')),
            prioridad_sugerida=limpiar_valor(row.get('Prioridad Sugerida')),
            frecuencia_observada=limpiar_valor(row.get('Frecuencia Observada'))
        )
        db.session.add(tipo_falla)
    db.session.commit()
    print(f"✓ {len(df)} tipos de fallas migrados")

def ejecutar_migracion():
    print("="*60)
    print("INICIANDO MIGRACIÓN DE DATOS - SISTEMA CAMARAS UFRO")
    print("="*60)
    
    with app.app_context():
        # Limpiar tablas existentes
        print("\nLimpiando base de datos...")
        db.drop_all()
        db.create_all()
        print("✓ Base de datos limpia")
        
        # Ejecutar migraciones en orden
        try:
            migrar_ubicaciones()
            migrar_gabinetes()
            migrar_switches()
            migrar_puertos_switch()
            migrar_camaras()
            migrar_equipos_tecnicos()
            migrar_tipos_fallas()
            migrar_fallas()
            migrar_ejemplos_fallas_reales()
            migrar_mantenimientos()
            
            print("\n" + "="*60)
            print("MIGRACIÓN COMPLETADA EXITOSAMENTE")
            print("="*60)
            
            # Estadísticas finales
            print("\nEstadísticas:")
            print(f"  - Ubicaciones: {Ubicacion.query.count()}")
            print(f"  - Gabinetes: {Gabinete.query.count()}")
            print(f"  - Switches: {Switch.query.count()}")
            print(f"  - Puertos: {PuertoSwitch.query.count()}")
            print(f"  - Cámaras: {Camara.query.count()}")
            print(f"  - Equipos Técnicos: {EquipoTecnico.query.count()}")
            print(f"  - Fallas: {Falla.query.count()}")
            print(f"  - Mantenimientos: {Mantenimiento.query.count()}")
            print(f"  - Tipos de Fallas: {TipoFalla.query.count()}")
            
        except Exception as e:
            print(f"\n❌ Error durante la migración: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    ejecutar_migracion()
