from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_from_directory
from flask_cors import CORS
import os
import hashlib
from urllib.parse import urlparse
from datetime import datetime
from models import db, Usuario, Camara, Gabinete, Switch, PuertoSwitch, EquipoTecnico, Falla, Mantenimiento, Ubicacion, TipoFalla

app = Flask(__name__, static_folder='dist', static_url_path='')
app.secret_key = os.environ.get('SECRET_KEY', 'clave_secreta_dev_2025')
CORS(app)

# Configuración de base de datos
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

if DATABASE_URL:
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sistema_camaras.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def init_db():
    """Inicializa la base de datos"""
    with app.app_context():
        db.create_all()
        
        # Crear usuarios de prueba si no existen
        if Usuario.query.count() == 0:
            usuarios_prueba = [
                Usuario(username='admin', password_hash=hashlib.md5('admin123'.encode()).hexdigest(), 
                       nombre='Administrador Sistema', rol='administrador'),
                Usuario(username='tecnico1', password_hash=hashlib.md5('tecnico123'.encode()).hexdigest(), 
                       nombre='Juan Pérez', rol='tecnico'),
                Usuario(username='supervisor', password_hash=hashlib.md5('super123'.encode()).hexdigest(), 
                       nombre='Carlos Rodríguez', rol='supervisor')
            ]
            for user in usuarios_prueba:
                db.session.add(user)
            db.session.commit()
            print(f"Usuarios de prueba creados: {len(usuarios_prueba)}")

# API Endpoints

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    password_hash = hashlib.md5(password.encode()).hexdigest()
    user = Usuario.query.filter_by(username=username, password_hash=password_hash, activo=True).first()
    
    if user:
        session['user_id'] = user.id
        session['username'] = user.username
        session['nombre'] = user.nombre
        session['rol'] = user.rol
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'nombre': user.nombre,
                'rol': user.rol
            }
        })
    return jsonify({'success': False, 'message': 'Credenciales incorrectas'}), 401

@app.route('/api/auth/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'success': True})

@app.route('/api/auth/user', methods=['GET'])
def get_current_user():
    if 'user_id' in session:
        return jsonify({
            'success': True,
            'user': {
                'id': session['user_id'],
                'username': session['username'],
                'nombre': session['nombre'],
                'rol': session['rol']
            }
        })
    return jsonify({'success': False}), 401

# CRUD Cámaras
@app.route('/api/camaras', methods=['GET'])
def get_camaras():
    camaras = Camara.query.all()
    return jsonify([{
        'id': c.id, 'codigo': c.codigo, 'nombre': c.nombre, 'campus': c.campus,
        'edificio': c.edificio, 'piso': c.piso, 'ubicacion': c.ubicacion,
        'ip': c.ip, 'marca': c.marca, 'modelo': c.modelo, 'tipo': c.tipo,
        'resolucion': c.resolucion, 'estado': c.estado, 'gabinete_asociado': c.gabinete_asociado,
        'switch_conectado': c.switch_conectado, 'puerto_switch': c.puerto_switch,
        'nvr_asociado': c.nvr_asociado, 'puerto_nvr': c.puerto_nvr,
        'fecha_instalacion': c.fecha_instalacion.isoformat() if c.fecha_instalacion else None,
        'observaciones': c.observaciones
    } for c in camaras])

@app.route('/api/camaras/<int:id>', methods=['GET'])
def get_camara(id):
    camara = Camara.query.get_or_404(id)
    return jsonify({
        'id': camara.id, 'codigo': camara.codigo, 'nombre': camara.nombre,
        'campus': camara.campus, 'edificio': camara.edificio, 'piso': camara.piso,
        'ubicacion': camara.ubicacion, 'ip': camara.ip, 'marca': camara.marca,
        'modelo': camara.modelo, 'tipo': camara.tipo, 'estado': camara.estado
    })

# CRUD Gabinetes
@app.route('/api/gabinetes', methods=['GET'])
def get_gabinetes():
    gabinetes = Gabinete.query.all()
    return jsonify([{
        'id': g.id, 'codigo': g.codigo, 'nombre': g.nombre, 'ubicacion': g.ubicacion,
        'campus': g.campus, 'edificio': g.edificio, 'piso': g.piso,
        'coordenadas': g.coordenadas, 'tipo': g.tipo, 'estado': g.estado,
        'switch_principal': g.switch_principal, 'nvr_asociado': g.nvr_asociado,
        'camaras_conectadas': g.camaras_conectadas,
        'fecha_instalacion': g.fecha_instalacion.isoformat() if g.fecha_instalacion else None,
        'observaciones': g.observaciones
    } for g in gabinetes])

# CRUD Switches
@app.route('/api/switches', methods=['GET'])
def get_switches():
    switches = Switch.query.all()
    return jsonify([{
        'id': s.id, 'codigo': s.codigo, 'nombre': s.nombre, 'marca': s.marca,
        'modelo': s.modelo, 'numero_serie': s.numero_serie, 'gabinete_id': s.gabinete_id,
        'puertos_totales': s.puertos_totales, 'puertos_usados': s.puertos_usados,
        'puertos_disponibles': s.puertos_disponibles, 'soporta_poe': s.soporta_poe,
        'estado': s.estado,
        'fecha_instalacion': s.fecha_instalacion.isoformat() if s.fecha_instalacion else None,
        'fecha_ultimo_mantenimiento': s.fecha_ultimo_mantenimiento.isoformat() if s.fecha_ultimo_mantenimiento else None,
        'observaciones': s.observaciones
    } for s in switches])

# CRUD Puertos Switch
@app.route('/api/puertos_switch', methods=['GET'])
def get_puertos_switch():
    puertos = PuertoSwitch.query.all()
    return jsonify([{
        'id': p.id, 'switch_id': p.switch_id, 'numero_puerto': p.numero_puerto,
        'estado': p.estado, 'dispositivo_conectado': p.dispositivo_conectado,
        'ip_dispositivo': p.ip_dispositivo, 'tipo_conexion': p.tipo_conexion,
        'nvr_asociado': p.nvr_asociado, 'puerto_nvr': p.puerto_nvr,
        'observaciones': p.observaciones
    } for p in puertos])

# CRUD Equipos Técnicos
@app.route('/api/equipos_tecnicos', methods=['GET'])
def get_equipos_tecnicos():
    equipos = EquipoTecnico.query.all()
    return jsonify([{
        'id': e.id, 'tipo': e.tipo, 'marca': e.marca, 'modelo': e.modelo,
        'numero_serie': e.numero_serie, 'capacidad': e.capacidad,
        'ubicacion': e.ubicacion, 'gabinete_id': e.gabinete_id, 'estado': e.estado,
        'fecha_instalacion': e.fecha_instalacion.isoformat() if e.fecha_instalacion else None,
        'fecha_ultimo_mantenimiento': e.fecha_ultimo_mantenimiento.isoformat() if e.fecha_ultimo_mantenimiento else None,
        'proximo_mantenimiento': e.proximo_mantenimiento.isoformat() if e.proximo_mantenimiento else None,
        'observaciones': e.observaciones
    } for e in equipos])

# CRUD Fallas
@app.route('/api/fallas', methods=['GET'])
def get_fallas():
    fallas = Falla.query.order_by(Falla.fecha_reporte.desc()).all()
    return jsonify([{
        'id': f.id, 'fecha_reporte': f.fecha_reporte.isoformat() if f.fecha_reporte else None,
        'reportado_por': f.reportado_por, 'tipo': f.tipo, 'subtipo': f.subtipo,
        'camara_id': f.camara_id, 'camara_afectada': f.camara_afectada,
        'ubicacion': f.ubicacion, 'descripcion': f.descripcion,
        'impacto_visibilidad': f.impacto_visibilidad, 'afecta_vision_nocturna': f.afecta_vision_nocturna,
        'estado': f.estado, 'prioridad': f.prioridad, 'tecnico_asignado': f.tecnico_asignado,
        'fecha_inicio': f.fecha_inicio.isoformat() if f.fecha_inicio else None,
        'fecha_resolucion': f.fecha_resolucion.isoformat() if f.fecha_resolucion else None,
        'solucion': f.solucion, 'gravedad': f.gravedad,
        'componente_afectado': f.componente_afectado, 'observaciones': f.observaciones
    } for f in fallas])

@app.route('/api/fallas', methods=['POST'])
def create_falla():
    data = request.get_json()
    nueva_falla = Falla(
        reportado_por=data.get('reportado_por'),
        tipo=data.get('tipo'),
        subtipo=data.get('subtipo'),
        camara_id=data.get('camara_id'),
        camara_afectada=data.get('camara_afectada'),
        ubicacion=data.get('ubicacion'),
        descripcion=data.get('descripcion'),
        prioridad=data.get('prioridad', 'Media'),
        estado=data.get('estado', 'Abierta')
    )
    db.session.add(nueva_falla)
    db.session.commit()
    return jsonify({'success': True, 'id': nueva_falla.id}), 201

# CRUD Mantenimientos
@app.route('/api/mantenimientos', methods=['GET'])
def get_mantenimientos():
    mantenimientos = Mantenimiento.query.order_by(Mantenimiento.fecha_programada.desc()).all()
    return jsonify([{
        'id': m.id, 
        'fecha_programada': m.fecha_programada.isoformat() if m.fecha_programada else None,
        'fecha_realizacion': m.fecha_realizacion.isoformat() if m.fecha_realizacion else None,
        'tipo': m.tipo, 'categoria': m.categoria, 'equipo_gabinete': m.equipo_gabinete,
        'ubicacion': m.ubicacion, 'descripcion': m.descripcion, 'estado': m.estado,
        'tecnico_responsable': m.tecnico_responsable, 'materiales_utilizados': m.materiales_utilizados,
        'costo_aproximado': m.costo_aproximado, 'equipos_camaras_afectadas': m.equipos_camaras_afectadas,
        'tiempo_ejecucion': m.tiempo_ejecucion, 'observaciones': m.observaciones
    } for m in mantenimientos])

# CRUD Ubicaciones
@app.route('/api/ubicaciones', methods=['GET'])
def get_ubicaciones():
    ubicaciones = Ubicacion.query.all()
    return jsonify([{
        'id': u.id, 'campus': u.campus, 'edificio': u.edificio, 'piso': u.piso,
        'zona': u.zona, 'descripcion': u.descripcion,
        'gabinetes_en_ubicacion': u.gabinetes_en_ubicacion,
        'cantidad_camaras': u.cantidad_camaras, 'observaciones': u.observaciones
    } for u in ubicaciones])

# Tipos de Fallas
@app.route('/api/tipos_fallas', methods=['GET'])
def get_tipos_fallas():
    tipos = TipoFalla.query.all()
    return jsonify([{
        'id': t.id, 'categoria_principal': t.categoria_principal,
        'tipo_falla': t.tipo_falla, 'impacto_tipico': t.impacto_tipico,
        'tipo_mantenimiento': t.tipo_mantenimiento, 'prioridad_sugerida': t.prioridad_sugerida,
        'frecuencia_observada': t.frecuencia_observada
    } for t in tipos])

# Estadísticas Dashboard
@app.route('/api/estadisticas', methods=['GET'])
def get_estadisticas():
    total_camaras = Camara.query.count()
    camaras_activas = Camara.query.filter_by(estado='Operativa').count()
    fallas_pendientes = Falla.query.filter_by(estado='Abierta').count()
    mantenimientos_programados = Mantenimiento.query.filter_by(estado='Programado').count()
    
    return jsonify({
        'total_camaras': total_camaras,
        'camaras_activas': camaras_activas,
        'camaras_inactivas': total_camaras - camaras_activas,
        'fallas_pendientes': fallas_pendientes,
        'mantenimientos_programados': mantenimientos_programados,
        'total_gabinetes': Gabinete.query.count(),
        'total_switches': Switch.query.count()
    })

# Mapa de red (datos para Mermaid)
@app.route('/api/mapa_red', methods=['GET'])
def get_mapa_red():
    gabinetes = Gabinete.query.all()
    switches = Switch.query.all()
    camaras = Camara.query.all()
    
    mapa = {
        'gabinetes': [{'id': g.id, 'codigo': g.codigo, 'campus': g.campus, 'edificio': g.edificio} for g in gabinetes],
        'switches': [{'id': s.id, 'codigo': s.codigo, 'gabinete_id': s.gabinete_id} for s in switches],
        'camaras': [{'id': c.id, 'codigo': c.codigo, 'gabinete_asociado': c.gabinete_asociado, 
                     'switch_conectado': c.switch_conectado} for c in camaras]
    }
    return jsonify(mapa)

# Servir el frontend React
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
