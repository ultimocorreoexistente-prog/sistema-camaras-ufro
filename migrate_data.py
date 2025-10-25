import pandas as pd
from datetime import datetime
from app import app, db
from models import (Usuario, Ubicacion, Camara, Gabinete, Switch, Puerto_Switch, 
                   UPS, NVR_DVR, Fuente_Poder, Catalogo_Tipo_Falla, Falla, 
                   Mantenimiento, Equipo_Tecnico)
from werkzeug.security import generate_password_hash
import os

def safe_int(value):
    """Convierte valor a int manejando NaN"""
    try:
        if pd.isna(value):
            return None
        return int(value)
    except:
        return None

def safe_float(value):
    """Convierte valor a float manejando NaN"""
    try:
        if pd.isna(value):
            return None
        return float(value)
    except:
        return None

def safe_str(value):
    """Convierte valor a string manejando NaN"""
    if pd.isna(value):
        return None
    return str(value).strip() if str(value).strip() else None

def safe_date(value):
    """Convierte valor a date manejando NaN"""
    try:
        if pd.isna(value):
            return None
        if isinstance(value, str):
            return datetime.strptime(value, '%Y-%m-%d').date()
        return value.date() if hasattr(value, 'date') else None
    except:
        return None

def limpiar_filas_vacias(df):
    """Elimina filas completamente vacías o sin datos relevantes del DataFrame"""
    if df is None or df.empty:
        return df
    
    # Eliminar filas donde TODOS los valores son NaN
    df_limpio = df.dropna(how='all')
    
    # Eliminar filas donde TODOS los valores son strings vacíos o espacios
    df_limpio = df_limpio[~df_limpio.apply(
        lambda row: all(
            (pd.isna(val) or (isinstance(val, str) and not val.strip()))
            for val in row
        ), axis=1
    )]
    
    # Reset del índice después de limpiar
    df_limpio = df_limpio.reset_index(drop=True)
    
    filas_eliminadas = len(df) - len(df_limpio)
    if filas_eliminadas > 0:
        print(f"   → {filas_eliminadas} filas vacías eliminadas automáticamente")
    
    return df_limpio

def validar_falla_duplicada(equipo_tipo, equipo_id):
    """Valida si se puede insertar una nueva falla"""
    falla_activa = Falla.query.filter_by(
        equipo_tipo=equipo_tipo,
        equipo_id=equipo_id
    ).filter(
        Falla.estado.in_(['Pendiente', 'Asignada', 'En Proceso'])
    ).order_by(Falla.fecha_reporte.desc()).first()
    
    if falla_activa:
        return False, f'Falla duplicada rechazada (Equipo {equipo_tipo} ID {equipo_id})'
    return True, 'OK'

def migrar_datos():
    """Migra todas las planillas Excel a la base de datos"""
    
    print("=== INICIANDO MIGRACIÓN DE DATOS ===\n")
    
    base_path = 'planillas/'
    
    try:
        # 1. UBICACIONES
        print("1. Migrando Ubicaciones...")
        df = pd.read_excel(f'{base_path}Ubicaciones.xlsx')
        df = limpiar_filas_vacias(df)
        count = 0
        for _, row in df.iterrows():
            ubicacion = Ubicacion(
                campus=safe_str(row.get('Campus')),
                edificio=safe_str(row.get('Edificio')),
                piso=safe_str(row.get('Piso')),
                descripcion=safe_str(row.get('Descripcion')),
                latitud=safe_float(row.get('Latitud')),
                longitud=safe_float(row.get('Longitud')),
                activo=True
            )
            db.session.add(ubicacion)
            count += 1
        db.session.commit()
        print(f"   ✓ {count} ubicaciones insertadas\n")
        
        # 2. EQUIPOS TÉCNICOS
        print("2. Migrando Equipos Técnicos...")
        df = pd.read_excel(f'{base_path}Equipos_Tecnicos.xlsx')
        df = limpiar_filas_vacias(df)
        count = 0
        skipped = 0
        auto_generated = 0
        for idx, row in df.iterrows():
            nombre = safe_str(row.get('Nombre'))
            apellido = safe_str(row.get('Apellido'))
            
            # Si no tiene nombre pero tiene otros datos (email o especialidad), generar nombre automático
            if not nombre:
                email = safe_str(row.get('Email'))
                especialidad = safe_str(row.get('Especialidad'))
                if email or especialidad:
                    nombre = f"Tecnico_Auto_{idx}"
                    auto_generated += 1
                else:
                    skipped += 1
                    continue
            
            # Generar apellido por defecto si falta (campo NOT NULL)
            if not apellido:
                apellido = f"Auto_{idx}"
            
            equipo = Equipo_Tecnico(
                nombre=nombre,
                apellido=apellido,
                especialidad=safe_str(row.get('Especialidad')),
                telefono=safe_str(row.get('Telefono')),
                email=safe_str(row.get('Email')),
                estado=safe_str(row.get('Estado', 'Activo')),
                fecha_ingreso=safe_date(row.get('Fecha_Ingreso'))
            )
            db.session.add(equipo)
            count += 1
        db.session.commit()
        if auto_generated > 0:
            print(f"   ✓ {count} equipos técnicos insertados ({auto_generated} con nombres auto-generados, {skipped} filas omitidas)\n")
        else:
            print(f"   ✓ {count} equipos técnicos insertados ({skipped} filas omitidas)\n")
        
        # 3. CATÁLOGO TIPOS DE FALLAS
        print("3. Migrando Catálogo de Tipos de Fallas...")
        df = pd.read_excel(f'{base_path}Catalogo_Tipos_Fallas.xlsx')
        df = limpiar_filas_vacias(df)
        count = 0
        skipped = 0
        auto_generated = 0
        for idx, row in df.iterrows():
            nombre = safe_str(row.get('Nombre'))
            categoria = safe_str(row.get('Categoria'))
            descripcion = safe_str(row.get('Descripcion'))
            
            # Si no tiene nombre pero tiene categoría o descripción, generar nombre
            if not nombre:
                if categoria or descripcion:
                    nombre = f"Falla_Auto_{idx}"
                    auto_generated += 1
                else:
                    skipped += 1
                    continue
            tipo_falla = Catalogo_Tipo_Falla(
                nombre=nombre,
                categoria=safe_str(row.get('Categoria')),
                descripcion=safe_str(row.get('Descripcion')),
                gravedad=safe_str(row.get('Gravedad', 'Media')),
                tiempo_estimado_resolucion=safe_int(row.get('Tiempo_Estimado_Resolucion'))
            )
            db.session.add(tipo_falla)
            count += 1
        db.session.commit()
        if auto_generated > 0:
            print(f"   ✓ {count} tipos de fallas insertados ({auto_generated} con nombres auto-generados, {skipped} filas omitidas)\n")
        else:
            print(f"   ✓ {count} tipos de fallas insertados ({skipped} filas omitidas)\n")
        
        # 4. GABINETES
        print("4. Migrando Gabinetes...")
        df = pd.read_excel(f'{base_path}Gabinetes.xlsx')
        df = limpiar_filas_vacias(df)
        count = 0
        skipped = 0
        auto_generated = 0
        for idx, row in df.iterrows():
            codigo = safe_str(row.get('Codigo'))
            nombre = safe_str(row.get('Nombre'))
            ubicacion_id = safe_int(row.get('ID_Ubicacion'))
            
            # Si no tiene código pero tiene nombre o ubicación, generar código
            if not codigo:
                if nombre or ubicacion_id:
                    codigo = f"GAB-AUTO-{idx:03d}"
                    auto_generated += 1
                else:
                    skipped += 1
                    continue
            gabinete = Gabinete(
                codigo=codigo,
                nombre=safe_str(row.get('Nombre')),
                tipo_ubicacion_general=safe_str(row.get('Tipo_Ubicacion_General')),
                tipo_ubicacion_detallada=safe_str(row.get('Tipo_Ubicacion_Detallada')),
                ubicacion_id=safe_int(row.get('ID_Ubicacion')),
                capacidad=safe_int(row.get('Capacidad')),
                tiene_ups=bool(row.get('Tiene_UPS', False)),
                tiene_switch=bool(row.get('Tiene_Switch', False)),
                tiene_nvr=bool(row.get('Tiene_NVR', False)),
                conexion_fibra=bool(row.get('Conexion_Fibra', False)),
                estado=safe_str(row.get('Estado', 'Activo')),
                fecha_alta=safe_date(row.get('Fecha_Alta')),
                observaciones=safe_str(row.get('Observaciones')),
                latitud=safe_float(row.get('Latitud')),
                longitud=safe_float(row.get('Longitud'))
            )
            db.session.add(gabinete)
            count += 1
        db.session.commit()
        if auto_generated > 0:
            print(f"   ✓ {count} gabinetes insertados ({auto_generated} con códigos auto-generados, {skipped} filas omitidas)\n")
        else:
            print(f"   ✓ {count} gabinetes insertados ({skipped} filas omitidas)\n")
        
        # 5. SWITCHES
        print("5. Migrando Switches...")
        df = pd.read_excel(f'{base_path}Switches.xlsx')
        df = limpiar_filas_vacias(df)
        count = 0
        skipped = 0
        auto_generated = 0
        for idx, row in df.iterrows():
            codigo = safe_str(row.get('Codigo'))
            nombre = safe_str(row.get('Nombre'))
            ip = safe_str(row.get('IP'))
            modelo = safe_str(row.get('Modelo'))
            
            # Si no tiene código pero tiene otros datos, generar código
            if not codigo:
                if nombre or ip or modelo:
                    codigo = f"SW-AUTO-{idx:03d}"
                    auto_generated += 1
                else:
                    skipped += 1
                    continue
            switch = Switch(
                codigo=codigo,
                nombre=safe_str(row.get('Nombre')),
                ip=safe_str(row.get('IP')),
                modelo=safe_str(row.get('Modelo')),
                marca=safe_str(row.get('Marca')),
                numero_serie=safe_str(row.get('Numero_Serie')),
                gabinete_id=safe_int(row.get('ID_Gabinete')),
                puertos_totales=safe_int(row.get('Puertos_Totales')),
                puertos_usados=safe_int(row.get('Puertos_Usados', 0)),
                puertos_disponibles=safe_int(row.get('Puertos_Disponibles')),
                capacidad_poe=bool(row.get('Capacidad_PoE', False)),
                estado=safe_str(row.get('Estado', 'Activo')),
                fecha_alta=safe_date(row.get('Fecha_Alta')),
                observaciones=safe_str(row.get('Observaciones')),
                latitud=safe_float(row.get('Latitud')),
                longitud=safe_float(row.get('Longitud'))
            )
            db.session.add(switch)
            count += 1
        db.session.commit()
        if auto_generated > 0:
            print(f"   ✓ {count} switches insertados ({auto_generated} con códigos auto-generados, {skipped} filas omitidas)\n")
        else:
            print(f"   ✓ {count} switches insertados ({skipped} filas omitidas)\n")
        
        # 6. PUERTOS SWITCH
        print("6. Migrando Puertos de Switch...")
        df = pd.read_excel(f'{base_path}Puertos_Switch.xlsx')
        df = limpiar_filas_vacias(df)
        count = 0
        skipped = 0
        for _, row in df.iterrows():
            switch_id = safe_int(row.get('ID_Switch'))
            # Saltar filas sin switch_id (requerido)
            if not switch_id:
                skipped += 1
                continue
            puerto = Puerto_Switch(
                switch_id=switch_id,
                numero_puerto=safe_int(row.get('Numero_Puerto')),
                camara_id=safe_int(row.get('ID_Camara')),
                ip_dispositivo=safe_str(row.get('IP_Dispositivo')),
                estado=safe_str(row.get('Estado', 'Disponible')),
                tipo_conexion=safe_str(row.get('Tipo_Conexion')),
                nvr_id=safe_int(row.get('ID_NVR')),
                puerto_nvr=safe_str(row.get('Puerto_NVR'))
            )
            db.session.add(puerto)
            count += 1
        db.session.commit()
        print(f"   ✓ {count} puertos de switch insertados ({skipped} filas omitidas)\n")
        
        # 7. UPS
        print("7. Migrando UPS...")
        df = pd.read_excel(f'{base_path}UPS.xlsx')
        df = limpiar_filas_vacias(df)
        count = 0
        skipped = 0
        auto_generated = 0
        for idx, row in df.iterrows():
            codigo = safe_str(row.get('Codigo'))
            modelo = safe_str(row.get('Modelo'))
            marca = safe_str(row.get('Marca'))
            
            # Si no tiene código pero tiene modelo o marca, generar código
            if not codigo:
                if modelo or marca:
                    codigo = f"UPS-AUTO-{idx:03d}"
                    auto_generated += 1
                else:
                    skipped += 1
                    continue
            ups = UPS(
                codigo=codigo,
                modelo=safe_str(row.get('Modelo')),
                marca=safe_str(row.get('Marca')),
                capacidad_va=safe_int(row.get('Capacidad_VA')),
                numero_baterias=safe_int(row.get('Numero_Baterias')),
                ubicacion_id=safe_int(row.get('ID_Ubicacion')),
                gabinete_id=safe_int(row.get('ID_Gabinete')),
                equipos_que_alimenta=safe_str(row.get('Equipos_Que_Alimenta')),
                estado=safe_str(row.get('Estado', 'Activo')),
                fecha_alta=safe_date(row.get('Fecha_Alta')),
                observaciones=safe_str(row.get('Observaciones')),
                latitud=safe_float(row.get('Latitud')),
                longitud=safe_float(row.get('Longitud'))
            )
            db.session.add(ups)
            count += 1
        db.session.commit()
        if auto_generated > 0:
            print(f"   ✓ {count} UPS insertados ({auto_generated} con códigos auto-generados, {skipped} filas omitidas)\n")
        else:
            print(f"   ✓ {count} UPS insertados ({skipped} filas omitidas)\n")
        
        # 8. NVR/DVR
        print("8. Migrando NVR/DVR...")
        df = pd.read_excel(f'{base_path}NVR_DVR.xlsx')
        df = limpiar_filas_vacias(df)
        count = 0
        skipped = 0
        auto_generated = 0
        for idx, row in df.iterrows():
            codigo = safe_str(row.get('Codigo'))
            modelo = safe_str(row.get('Modelo'))
            tipo = safe_str(row.get('Tipo'))
            
            # Si no tiene código pero tiene modelo o tipo, generar código
            if not codigo:
                if modelo or tipo:
                    codigo = f"NVR-AUTO-{idx:03d}"
                    auto_generated += 1
                else:
                    skipped += 1
                    continue
            nvr = NVR_DVR(
                codigo=codigo,
                tipo=safe_str(row.get('Tipo', 'NVR')),
                modelo=safe_str(row.get('Modelo')),
                marca=safe_str(row.get('Marca')),
                canales_totales=safe_int(row.get('Canales_Totales')),
                canales_usados=safe_int(row.get('Canales_Usados', 0)),
                ip=safe_str(row.get('IP')),
                ubicacion_id=safe_int(row.get('ID_Ubicacion')),
                gabinete_id=safe_int(row.get('ID_Gabinete')),
                estado=safe_str(row.get('Estado', 'Activo')),
                fecha_alta=safe_date(row.get('Fecha_Alta')),
                observaciones=safe_str(row.get('Observaciones')),
                latitud=safe_float(row.get('Latitud')),
                longitud=safe_float(row.get('Longitud'))
            )
            db.session.add(nvr)
            count += 1
        db.session.commit()
        if auto_generated > 0:
            print(f"   ✓ {count} NVR/DVR insertados ({auto_generated} con códigos auto-generados, {skipped} filas omitidas)\n")
        else:
            print(f"   ✓ {count} NVR/DVR insertados ({skipped} filas omitidas)\n")
        
        # 9. FUENTES DE PODER
        print("9. Migrando Fuentes de Poder...")
        df = pd.read_excel(f'{base_path}Fuentes_Poder.xlsx')
        df = limpiar_filas_vacias(df)
        count = 0
        skipped = 0
        auto_generated = 0
        for idx, row in df.iterrows():
            codigo = safe_str(row.get('Codigo'))
            modelo = safe_str(row.get('Modelo'))
            voltaje = safe_str(row.get('Voltaje'))
            
            # Si no tiene código pero tiene modelo o voltaje, generar código
            if not codigo:
                if modelo or voltaje:
                    codigo = f"FP-AUTO-{idx:03d}"
                    auto_generated += 1
                else:
                    skipped += 1
                    continue
            fuente = Fuente_Poder(
                codigo=codigo,
                modelo=safe_str(row.get('Modelo')),
                voltaje=safe_str(row.get('Voltaje')),
                amperaje=safe_str(row.get('Amperaje')),
                equipos_que_alimenta=safe_str(row.get('Equipos_Que_Alimenta')),
                ubicacion_id=safe_int(row.get('ID_Ubicacion')),
                gabinete_id=safe_int(row.get('ID_Gabinete')),
                estado=safe_str(row.get('Estado', 'Activo')),
                fecha_alta=safe_date(row.get('Fecha_Alta')),
                observaciones=safe_str(row.get('Observaciones'))
            )
            db.session.add(fuente)
            count += 1
        db.session.commit()
        if auto_generated > 0:
            print(f"   ✓ {count} fuentes de poder insertadas ({auto_generated} con códigos auto-generados, {skipped} filas omitidas)\n")
        else:
            print(f"   ✓ {count} fuentes de poder insertadas ({skipped} filas omitidas)\n")
        
        # 10. CÁMARAS (474 unidades)
        print("10. Migrando Cámaras...")
        df = pd.read_excel(f'{base_path}Listadecámaras_modificada.xlsx')
        df = limpiar_filas_vacias(df)
        count = 0
        skipped = 0
        auto_generated = 0
        for idx, row in df.iterrows():
            codigo = safe_str(row.get('Codigo'))
            nombre = safe_str(row.get('Nombre'))
            ip = safe_str(row.get('IP'))
            modelo = safe_str(row.get('Modelo'))
            
            # Si no tiene código pero tiene otros datos, generar código
            if not codigo:
                if nombre or ip or modelo:
                    codigo = f"CAM-AUTO-{idx:04d}"
                    auto_generated += 1
                else:
                    skipped += 1
                    continue
            camara = Camara(
                codigo=codigo,
                nombre=safe_str(row.get('Nombre')),
                ip_address=safe_str(row.get('IP')),
                modelo=safe_str(row.get('Modelo')),
                marca=safe_str(row.get('Fabricante')),
                tipo_camara=safe_str(row.get('Tipo_Camara', 'Domo')),
                ubicacion_id=safe_int(row.get('ID_Ubicacion')),
                gabinete_id=safe_int(row.get('ID_Gabinete')),
                switch_id=safe_int(row.get('ID_Switch')),
                puertos_switch_id=safe_int(row.get('ID_Puerto_Switch')),
                nvr_id=safe_int(row.get('ID_NVR')),
                puerto_nvr=safe_str(row.get('Puerto_NVR')),
                requiere_poe_adicional=bool(row.get('Requiere_PoE_Adicional', False)),
                tipo_conexion=safe_str(row.get('Tipo_Conexion')),
                estado=safe_str(row.get('Estado', 'Activo')),
                fecha_alta=safe_date(row.get('Fecha_Alta')),
                instalador=safe_str(row.get('Instalador')),
                fecha_instalacion=safe_date(row.get('Fecha_Instalacion')),
                observaciones=safe_str(row.get('Observaciones')),
                latitud=safe_float(row.get('Latitud')),
                longitud=safe_float(row.get('Longitud'))
            )
            db.session.add(camara)
            count += 1
        db.session.commit()
        if auto_generated > 0:
            print(f"   ✓ {count} cámaras insertadas ({auto_generated} con códigos auto-generados, {skipped} filas omitidas)\n")
        else:
            print(f"   ✓ {count} cámaras insertadas ({skipped} filas omitidas)\n")
        
        # 11. FALLAS (con validación anti-duplicados)
        print("11. Migrando Fallas (con validación anti-duplicados)...")
        
        # Obtener usuario admin para reportado_por
        admin_user = Usuario.query.filter_by(email='admin').first()
        if not admin_user:
            print("   ⚠ Usuario admin no existe, creando...")
            admin_user = Usuario(
                email='admin',
                rol='admin',
                nombre='Administrador',
                activo=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
        
        count = 0
        rechazadas = 0
        
        # Fallas_Actualizada.xlsx
        try:
            df1 = pd.read_excel(f'{base_path}Fallas_Actualizada.xlsx')
            df1 = limpiar_filas_vacias(df1)
            for _, row in df1.iterrows():
                equipo_tipo = safe_str(row.get('Equipo_Tipo', 'Camara'))
                equipo_id = safe_int(row.get('Equipo_ID'))
                
                if equipo_id:
                    # Validar anti-duplicados
                    permitir, mensaje = validar_falla_duplicada(equipo_tipo, equipo_id)
                    if not permitir:
                        rechazadas += 1
                        continue
                    
                    falla = Falla(
                        equipo_tipo=equipo_tipo,
                        equipo_id=equipo_id,
                        tipo_falla_id=safe_int(row.get('Tipo_Falla_ID')),
                        descripcion=safe_str(row.get('Descripcion')),
                        prioridad=safe_str(row.get('Prioridad', 'Media')),
                        fecha_reporte=datetime.now(),
                        reportado_por_id=admin_user.id,
                        estado=safe_str(row.get('Estado', 'Pendiente'))
                    )
                    db.session.add(falla)
                    count += 1
        except Exception as e:
            print(f"   ⚠ Error procesando Fallas_Actualizada.xlsx: {e}")
        
        # Ejemplos_Fallas_Reales.xlsx
        try:
            df2 = pd.read_excel(f'{base_path}Ejemplos_Fallas_Reales.xlsx')
            df2 = limpiar_filas_vacias(df2)
            for _, row in df2.iterrows():
                equipo_tipo = safe_str(row.get('Equipo_Tipo', 'Camara'))
                equipo_id = safe_int(row.get('Equipo_ID'))
                
                if equipo_id:
                    # Validar anti-duplicados
                    permitir, mensaje = validar_falla_duplicada(equipo_tipo, equipo_id)
                    if not permitir:
                        rechazadas += 1
                        continue
                    
                    falla = Falla(
                        equipo_tipo=equipo_tipo,
                        equipo_id=equipo_id,
                        tipo_falla_id=safe_int(row.get('Tipo_Falla_ID')),
                        descripcion=safe_str(row.get('Descripcion')),
                        prioridad=safe_str(row.get('Prioridad', 'Media')),
                        fecha_reporte=datetime.now(),
                        reportado_por_id=admin_user.id,
                        estado=safe_str(row.get('Estado', 'Pendiente'))
                    )
                    db.session.add(falla)
                    count += 1
        except Exception as e:
            print(f"   ⚠ Error procesando Ejemplos_Fallas_Reales.xlsx: {e}")
        
        db.session.commit()
        print(f"   ✓ {count} fallas insertadas ({rechazadas} rechazadas por duplicado)\n")
        
        # 12. MANTENIMIENTOS
        print("12. Migrando Mantenimientos...")
        try:
            df = pd.read_excel(f'{base_path}Mantenimientos.xlsx')
            df = limpiar_filas_vacias(df)
            count = 0
            skipped = 0
            for _, row in df.iterrows():
                equipo_id = safe_int(row.get('Equipo_ID'))
                
                # equipo_id es NOT NULL en la BD - omitir si no existe
                if not equipo_id:
                    skipped += 1
                    continue
                
                mantenimiento = Mantenimiento(
                    equipo_tipo=safe_str(row.get('Equipo_Tipo', 'Camara')),
                    equipo_id=equipo_id,
                    tipo=safe_str(row.get('Tipo', 'Preventivo')),
                    fecha=datetime.now(),
                    tecnico_id=admin_user.id,
                    descripcion=safe_str(row.get('Descripcion')),
                    materiales_utilizados=safe_str(row.get('Materiales_Utilizados')),
                    tiempo_ejecucion_horas=safe_float(row.get('Tiempo_Ejecucion_Horas')),
                    costo=safe_float(row.get('Costo')),
                    observaciones=safe_str(row.get('Observaciones'))
                )
                db.session.add(mantenimiento)
                count += 1
            db.session.commit()
            print(f"   ✓ {count} mantenimientos insertados ({skipped} filas omitidas)\n")
        except Exception as e:
            print(f"   ⚠ Error procesando Mantenimientos.xlsx: {e}\n")
        
        print("=== MIGRACIÓN COMPLETADA EXITOSAMENTE ===")
        
        # Resumen final
        print("\n=== RESUMEN DE DATOS ===")
        print(f"Ubicaciones: {Ubicacion.query.count()}")
        print(f"Equipos Técnicos: {Equipo_Tecnico.query.count()}")
        print(f"Tipos de Fallas: {Catalogo_Tipo_Falla.query.count()}")
        print(f"Gabinetes: {Gabinete.query.count()}")
        print(f"Switches: {Switch.query.count()}")
        print(f"Puertos Switch: {Puerto_Switch.query.count()}")
        print(f"UPS: {UPS.query.count()}")
        print(f"NVR/DVR: {NVR_DVR.query.count()}")
        print(f"Fuentes de Poder: {Fuente_Poder.query.count()}")
        print(f"Cámaras: {Camara.query.count()}")
        print(f"Fallas: {Falla.query.count()}")
        print(f"Mantenimientos: {Mantenimiento.query.count()}")
        print(f"Usuarios: {Usuario.query.count()}")
        
    except Exception as e:
        print(f"\n⚠⚠⚠ ERROR EN MIGRACIÓN: {e}")
        db.session.rollback()
        raise

if __name__ == '__main__':
    with app.app_context():
        # Crear usuarios por defecto primero
        if Usuario.query.count() == 0:
            print("Creando usuarios por defecto...\n")
            usuarios = [
                Usuario(email='admin', rol='admin', nombre='Administrador', activo=True),
                Usuario(email='supervisor', rol='supervisor', nombre='Supervisor', activo=True),
                Usuario(email='tecnico1', rol='tecnico', nombre='Técnico 1', activo=True),
                Usuario(email='visualizador', rol='visualizador', nombre='Visualizador', activo=True)
            ]
            
            passwords = ['admin123', 'super123', 'tecnico123', 'viz123']
            
            for user, password in zip(usuarios, passwords):
                user.set_password(password)
                db.session.add(user)
            
            db.session.commit()
            print("✓ Usuarios creados\n")
        
        migrar_datos()
