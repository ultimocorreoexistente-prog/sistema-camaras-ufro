import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
from datetime import datetime
from sqlalchemy import or_, func
from werkzeug.security import generate_password_hash

from models import db, Usuario, Ubicacion, Camara, Gabinete, Switch, Puerto_Switch, UPS, NVR_DVR, Fuente_Poder, Catalogo_Tipo_Falla, Falla, Mantenimiento, Equipo_Tecnico, Historial_Estado_Equipo

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Soportar SQLite (desarrollo) y PostgreSQL (producción)
database_url = os.environ.get('DATABASE_URL', 'sqlite:///sistema_camaras.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Debug: Información de base de datos para verificar configuración Railway
print(f"🔧 DEBUG: DATABASE_URL = {os.environ.get('DATABASE_URL', 'NO DEFINIDO')}")
print(f"🔧 DEBUG: SQLALCHEMY_DATABASE_URI = {app.config.get('SQLALCHEMY_DATABASE_URI', 'NO CONFIGURADO')}")
print(f"🔧 DEBUG: Usando SQLite = {'sqlite' in app.config.get('SQLALCHEMY_DATABASE_URI', '').lower()}")

# Logging del usuario Charles si existe
try:
    from models import Usuario
    charles_check = Usuario.query.filter_by(email='charles.jelvez').first()
    if charles_check:
        print(f"✅ Charles encontrado en BD: {charles_check.email} ({charles_check.rol})")
    else:
        print("❌ Charles NO encontrado en BD")
        total_users = Usuario.query.count()
        print(f"📊 Total usuarios en BD: {total_users}")
except Exception as e:
    print(f"❌ Error verificando usuarios: {e}")
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Decorador para verificar roles
def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.rol not in roles:
                flash('No tienes permisos para acceder a esta página', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Función para obtener modo del sistema
def obtener_modo_sistema():
    """Obtiene el modo actual del sistema (demo o real)"""
    return session.get('modo_sistema', 'real')

# Función de validación anti-duplicados
def validar_falla_duplicada(equipo_tipo, equipo_id):
    """Valida si se puede insertar una nueva falla para un equipo"""
    falla_activa = Falla.query.filter_by(
        equipo_tipo=equipo_tipo,
        equipo_id=equipo_id
    ).filter(
        Falla.estado.in_(['Pendiente', 'Asignada', 'En Proceso'])
    ).order_by(Falla.fecha_reporte.desc()).first()
    
    if falla_activa:
        return {
            'permitir': False,
            'mensaje': f'Ya existe una falla {falla_activa.estado} para este equipo (ID: {falla_activa.id}, reportada el {falla_activa.fecha_reporte.strftime("%d/%m/%Y")}). Debe cerrar o cancelar la falla anterior antes de reportar una nueva.',
            'falla_existente': falla_activa
        }
    
    return {
        'permitir': True,
        'mensaje': 'OK',
        'falla_existente': None
    }

# ========== AUTENTICACIÓN ==========
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Usuario.query.filter_by(email=username).first()
        
        if user and user.check_password(password) and user.activo:
            login_user(user)
            flash(f'Bienvenido {user.nombre}', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('login'))

# ========== DASHBOARD ==========
@app.route('/')
@login_required
def dashboard():
    # Estadísticas
    total_camaras = Camara.query.count()
    camaras_activas = Camara.query.filter_by(estado='Activo').count()
    fallas_pendientes = Falla.query.filter_by(estado='Pendiente').count()
    fallas_asignadas = Falla.query.filter_by(estado='Asignada').count()
    fallas_en_proceso = Falla.query.filter_by(estado='En Proceso').count()
    mantenimientos_mes = Mantenimiento.query.filter(
        func.extract('month', Mantenimiento.fecha) == datetime.now().month,
        func.extract('year', Mantenimiento.fecha) == datetime.now().year
    ).count()
    
    # Últimas fallas
    ultimas_fallas = Falla.query.order_by(Falla.fecha_reporte.desc()).limit(10).all()
    
    return render_template('dashboard.html',
                         total_camaras=total_camaras,
                         camaras_activas=camaras_activas,
                         fallas_pendientes=fallas_pendientes,
                         fallas_asignadas=fallas_asignadas,
                         fallas_en_proceso=fallas_en_proceso,
                         mantenimientos_mes=mantenimientos_mes,
                         ultimas_fallas=ultimas_fallas)

# ========== CÁMARAS ==========
@app.route('/camaras')
@login_required
def camaras_list():
    campus = request.args.get('campus', '')
    estado = request.args.get('estado', '')
    busqueda = request.args.get('busqueda', '')
    
    query = Camara.query.join(Ubicacion)
    
    if campus:
        query = query.filter(Ubicacion.campus == campus)
    if estado:
        query = query.filter(Camara.estado == estado)
    if busqueda:
        query = query.filter(or_(
            Camara.codigo.like(f'%{busqueda}%'),
            Camara.nombre.like(f'%{busqueda}%'),
            Camara.ip.like(f'%{busqueda}%')
        ))
    
    camaras = query.all()
    ubicaciones = Ubicacion.query.all()
    campus_list = db.session.query(Ubicacion.campus).distinct().all()
    
    return render_template('camaras_list.html', 
                         camaras=camaras, 
                         ubicaciones=ubicaciones,
                         campus_list=[c[0] for c in campus_list])

@app.route('/camaras/nuevo', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'supervisor')
def camaras_nuevo():
    if request.method == 'POST':
        camara = Camara(
            codigo=request.form.get('codigo'),
            nombre=request.form.get('nombre'),
            ip=request.form.get('ip'),
            modelo=request.form.get('modelo'),
            fabricante=request.form.get('fabricante'),
            tipo_camara=request.form.get('tipo_camara'),
            ubicacion_id=request.form.get('ubicacion_id'),
            gabinete_id=request.form.get('gabinete_id') or None,
            switch_id=request.form.get('switch_id') or None,
            nvr_id=request.form.get('nvr_id') or None,
            estado=request.form.get('estado', 'Activo'),
            fecha_alta=datetime.strptime(request.form.get('fecha_alta'), '%Y-%m-%d').date() if request.form.get('fecha_alta') else None,
            latitud=float(request.form.get('latitud')) if request.form.get('latitud') else None,
            longitud=float(request.form.get('longitud')) if request.form.get('longitud') else None,
            observaciones=request.form.get('observaciones')
        )
        db.session.add(camara)
        db.session.commit()
        flash('Cámara creada exitosamente', 'success')
        return redirect(url_for('camaras_list'))
    
    ubicaciones = Ubicacion.query.filter_by(activo=True).all()
    gabinetes = Gabinete.query.filter_by(estado='Activo').all()
    switches = Switch.query.filter_by(estado='Activo').all()
    nvrs = NVR_DVR.query.filter_by(estado='Activo').all()
    
    return render_template('camaras_form.html', 
                         ubicaciones=ubicaciones,
                         gabinetes=gabinetes,
                         switches=switches,
                         nvrs=nvrs,
                         camara=None)

@app.route('/camaras/<int:id>')
@login_required
def camaras_detalle(id):
    camara = Camara.query.get_or_404(id)
    fallas = Falla.query.filter_by(equipo_tipo='Camara', equipo_id=id).order_by(Falla.fecha_reporte.desc()).all()
    mantenimientos = Mantenimiento.query.filter_by(equipo_tipo='Camara', equipo_id=id).order_by(Mantenimiento.fecha.desc()).all()
    historial = Historial_Estado_Equipo.query.filter_by(equipo_tipo='Camara', equipo_id=id).order_by(Historial_Estado_Equipo.fecha_cambio.desc()).all()
    
    return render_template('camaras_detalle.html', 
                         camara=camara,
                         fallas=fallas,
                         mantenimientos=mantenimientos,
                         historial=historial)

@app.route('/camaras/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'supervisor')
def camaras_editar(id):
    camara = Camara.query.get_or_404(id)
    
    if request.method == 'POST':
        estado_anterior = camara.estado
        
        camara.codigo = request.form.get('codigo')
        camara.nombre = request.form.get('nombre')
        camara.ip = request.form.get('ip')
        camara.modelo = request.form.get('modelo')
        camara.fabricante = request.form.get('fabricante')
        camara.tipo_camara = request.form.get('tipo_camara')
        camara.ubicacion_id = request.form.get('ubicacion_id')
        camara.estado = request.form.get('estado')
        camara.latitud = float(request.form.get('latitud')) if request.form.get('latitud') else None
        camara.longitud = float(request.form.get('longitud')) if request.form.get('longitud') else None
        camara.observaciones = request.form.get('observaciones')
        
        # Registrar cambio de estado
        if estado_anterior != camara.estado:
            historial = Historial_Estado_Equipo(
                equipo_tipo='Camara',
                equipo_id=id,
                estado_anterior=estado_anterior,
                estado_nuevo=camara.estado,
                motivo=request.form.get('motivo_cambio', ''),
                usuario_id=current_user.id
            )
            db.session.add(historial)
        
        db.session.commit()
        flash('Cámara actualizada exitosamente', 'success')
        return redirect(url_for('camaras_detalle', id=id))
    
    ubicaciones = Ubicacion.query.filter_by(activo=True).all()
    gabinetes = Gabinete.query.filter_by(estado='Activo').all()
    switches = Switch.query.filter_by(estado='Activo').all()
    nvrs = NVR_DVR.query.filter_by(estado='Activo').all()
    
    return render_template('camaras_form.html', 
                         camara=camara,
                         ubicaciones=ubicaciones,
                         gabinetes=gabinetes,
                         switches=switches,
                         nvrs=nvrs)

# ========== GABINETES ==========
@app.route('/gabinetes')
@login_required
def gabinetes_list():
    campus = request.args.get('campus', '')
    estado = request.args.get('estado', '')
    
    query = Gabinete.query.join(Ubicacion)
    
    if campus:
        query = query.filter(Ubicacion.campus == campus)
    if estado:
        query = query.filter(Gabinete.estado == estado)
    
    gabinetes = query.all()
    campus_list = db.session.query(Ubicacion.campus).distinct().all()
    
    return render_template('gabinetes_list.html', 
                         gabinetes=gabinetes,
                         campus_list=[c[0] for c in campus_list])

@app.route('/gabinetes/<int:id>/mantencion')
@login_required
def gabinetes_mantencion(id):
    """Vista especial de mantención de gabinetes"""
    gabinete = Gabinete.query.get_or_404(id)
    
    # Obtener todos los equipos contenidos en este gabinete
    switches = Switch.query.filter_by(gabinete_id=id).all()
    nvrs = NVR_DVR.query.filter_by(gabinete_id=id).all()
    ups_list = UPS.query.filter_by(gabinete_id=id).all()
    fuentes = Fuente_Poder.query.filter_by(gabinete_id=id).all()
    
    # Historial de mantenimientos del gabinete
    mantenimientos = Mantenimiento.query.filter_by(
        equipo_tipo='Gabinete', 
        equipo_id=id
    ).order_by(Mantenimiento.fecha.desc()).all()
    
    return render_template('gabinetes_mantencion.html',
                         gabinete=gabinete,
                         switches=switches,
                         nvrs=nvrs,
                         ups_list=ups_list,
                         fuentes=fuentes,
                         mantenimientos=mantenimientos)

# ========== FALLAS ==========
@app.route('/fallas')
@login_required
def fallas_list():
    estado = request.args.get('estado', '')
    campus = request.args.get('campus', '')
    
    query = Falla.query
    
    if estado:
        query = query.filter(Falla.estado == estado)
    
    if current_user.rol == 'tecnico':
        query = query.filter(Falla.tecnico_asignado_id == current_user.id)
    
    fallas = query.order_by(Falla.fecha_reporte.desc()).all()
    
    return render_template('fallas_list.html', fallas=fallas)

@app.route('/fallas/nueva', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'supervisor', 'tecnico')
def fallas_nueva():
    if request.method == 'POST':
        equipo_tipo = request.form.get('equipo_tipo')
        equipo_id = int(request.form.get('equipo_id'))
        
        # Validar anti-duplicados
        validacion = validar_falla_duplicada(equipo_tipo, equipo_id)
        if not validacion['permitir']:
            flash(validacion['mensaje'], 'warning')
            return redirect(url_for('fallas_nueva'))
        
        falla = Falla(
            equipo_tipo=equipo_tipo,
            equipo_id=equipo_id,
            tipo_falla_id=request.form.get('tipo_falla_id'),
            descripcion=request.form.get('descripcion'),
            prioridad=request.form.get('prioridad'),
            reportado_por_id=current_user.id,
            estado='Pendiente'
        )
        db.session.add(falla)
        db.session.commit()
        flash('Falla reportada exitosamente', 'success')
        return redirect(url_for('fallas_list'))
    
    tipos_falla = Catalogo_Tipo_Falla.query.all()
    camaras = Camara.query.filter_by(estado='Activo').all()
    gabinetes = Gabinete.query.filter_by(estado='Activo').all()
    switches = Switch.query.filter_by(estado='Activo').all()
    
    return render_template('fallas_form.html',
                         tipos_falla=tipos_falla,
                         camaras=camaras,
                         gabinetes=gabinetes,
                         switches=switches)

@app.route('/fallas/<int:id>')
@login_required
def fallas_detalle(id):
    falla = Falla.query.get_or_404(id)
    tecnicos = Usuario.query.filter_by(rol='tecnico', activo=True).all()
    return render_template('fallas_detalle.html', falla=falla, tecnicos=tecnicos)

@app.route('/fallas/<int:id>/asignar', methods=['POST'])
@login_required
@role_required('admin', 'supervisor')
def fallas_asignar(id):
    falla = Falla.query.get_or_404(id)
    falla.tecnico_asignado_id = request.form.get('tecnico_id')
    falla.estado = 'Asignada'
    falla.fecha_asignacion = datetime.now()
    db.session.commit()
    flash('Falla asignada correctamente', 'success')
    return redirect(url_for('fallas_detalle', id=id))

@app.route('/fallas/<int:id>/iniciar', methods=['POST'])
@login_required
def fallas_iniciar(id):
    falla = Falla.query.get_or_404(id)
    if falla.tecnico_asignado_id != current_user.id and current_user.rol not in ['admin', 'supervisor']:
        flash('No tienes permisos para iniciar esta falla', 'danger')
        return redirect(url_for('fallas_detalle', id=id))
    
    falla.estado = 'En Proceso'
    falla.fecha_inicio_reparacion = datetime.now()
    db.session.commit()
    flash('Reparación iniciada', 'success')
    return redirect(url_for('fallas_detalle', id=id))

@app.route('/fallas/<int:id>/reparar', methods=['GET', 'POST'])
@login_required
def fallas_reparar(id):
    falla = Falla.query.get_or_404(id)
    
    if request.method == 'POST':
        falla.estado = 'Reparada'
        falla.fecha_fin_reparacion = datetime.now()
        falla.solucion_aplicada = request.form.get('solucion_aplicada')
        falla.materiales_utilizados = request.form.get('materiales_utilizados')
        falla.costo_reparacion = float(request.form.get('costo_reparacion', 0))
        
        if falla.fecha_inicio_reparacion:
            delta = falla.fecha_fin_reparacion - falla.fecha_inicio_reparacion
            falla.tiempo_resolucion_horas = delta.total_seconds() / 3600
        
        db.session.commit()
        flash('Falla marcada como reparada', 'success')
        return redirect(url_for('fallas_detalle', id=id))
    
    return render_template('fallas_reparar.html', falla=falla)

@app.route('/fallas/<int:id>/cerrar', methods=['POST'])
@login_required
@role_required('admin', 'supervisor')
def fallas_cerrar(id):
    falla = Falla.query.get_or_404(id)
    falla.estado = 'Cerrada'
    falla.fecha_cierre = datetime.now()
    db.session.commit()
    flash('Falla cerrada correctamente', 'success')
    return redirect(url_for('fallas_detalle', id=id))

# ========== MANTENIMIENTOS ==========
@app.route('/mantenimientos')
@login_required
def mantenimientos_list():
    mantenimientos = Mantenimiento.query.order_by(Mantenimiento.fecha.desc()).all()
    return render_template('mantenimientos_list.html', mantenimientos=mantenimientos)

@app.route('/mantenimientos/nuevo', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'supervisor', 'tecnico')
def mantenimientos_nuevo():
    if request.method == 'POST':
        mantenimiento = Mantenimiento(
            equipo_tipo=request.form.get('equipo_tipo'),
            equipo_id=request.form.get('equipo_id'),
            tipo=request.form.get('tipo'),
            fecha=datetime.now(),
            tecnico_id=current_user.id,
            descripcion=request.form.get('descripcion'),
            materiales_utilizados=request.form.get('materiales_utilizados'),
            tiempo_ejecucion_horas=float(request.form.get('tiempo_ejecucion_horas', 0)),
            costo=float(request.form.get('costo', 0)),
            observaciones=request.form.get('observaciones')
        )
        db.session.add(mantenimiento)
        db.session.commit()
        flash('Mantenimiento registrado exitosamente', 'success')
        return redirect(url_for('mantenimientos_list'))
    
    return render_template('mantenimientos_form.html')

# ========== MAPAS ==========
@app.route('/mapa-red')
@login_required
def mapa_red():
    campus = request.args.get('campus', '')
    
    # Obtener datos para generar diagrama Mermaid
    if campus:
        ubicaciones = Ubicacion.query.filter_by(campus=campus).all()
    else:
        ubicaciones = Ubicacion.query.all()
    
    gabinetes = Gabinete.query.join(Ubicacion).filter(Ubicacion.id.in_([u.id for u in ubicaciones])).all()
    switches = Switch.query.filter(Switch.gabinete_id.in_([g.id for g in gabinetes])).all()
    
    campus_list = db.session.query(Ubicacion.campus).distinct().all()
    
    return render_template('mapa_red.html',
                         campus_list=[c[0] for c in campus_list],
                         gabinetes=gabinetes,
                         switches=switches)

@app.route('/mapa-geolocalizacion')
@login_required
def mapa_geolocalizacion():
    camaras = Camara.query.filter(Camara.latitud.isnot(None), Camara.longitud.isnot(None)).all()
    gabinetes = Gabinete.query.filter(Gabinete.latitud.isnot(None), Gabinete.longitud.isnot(None)).all()
    
    return render_template('mapa_geolocalizacion.html',
                         camaras=camaras,
                         gabinetes=gabinetes)

@app.route('/informes-avanzados')
@login_required
def informes_avanzados():
    # Estadísticas generales
    stats_por_campus = db.session.query(
        Ubicacion.campus,
        func.count(Camara.id)
    ).join(Camara).group_by(Ubicacion.campus).all()
    
    fallas_por_tipo = db.session.query(
        Catalogo_Tipo_Falla.nombre,
        func.count(Falla.id)
    ).join(Falla).group_by(Catalogo_Tipo_Falla.nombre).all()
    
    return render_template('informes_avanzados.html',
                         stats_por_campus=stats_por_campus,
                         fallas_por_tipo=fallas_por_tipo)

# ========== API REST ==========
@app.route('/api/estadisticas')
@login_required
def api_estadisticas():
    stats = {
        'total_camaras': Camara.query.count(),
        'camaras_activas': Camara.query.filter_by(estado='Activo').count(),
        'fallas_pendientes': Falla.query.filter_by(estado='Pendiente').count(),
        'fallas_en_proceso': Falla.query.filter_by(estado='En Proceso').count()
    }
    return jsonify(stats)

@app.route('/api/fallas/validar')
@login_required
def api_validar_falla():
    equipo_tipo = request.args.get('equipo_tipo')
    equipo_id = request.args.get('equipo_id')
    
    if not equipo_tipo or not equipo_id:
        return jsonify({'error': 'Parámetros faltantes'}), 400
    
    resultado = validar_falla_duplicada(equipo_tipo, int(equipo_id))
    return jsonify(resultado)

@app.route('/api/gabinetes/<int:id>/equipos')
@login_required
def api_gabinete_equipos(id):
    """API para obtener todos los equipos de un gabinete"""
    gabinete = Gabinete.query.get_or_404(id)
    
    switches = Switch.query.filter_by(gabinete_id=id).all()
    nvrs = NVR_DVR.query.filter_by(gabinete_id=id).all()
    ups_list = UPS.query.filter_by(gabinete_id=id).all()
    fuentes = Fuente_Poder.query.filter_by(gabinete_id=id).all()
    
    return jsonify({
        'gabinete': {
            'id': gabinete.id,
            'codigo': gabinete.codigo,
            'nombre': gabinete.nombre
        },
        'switches': [{
            'id': s.id,
            'codigo': s.codigo,
            'modelo': s.modelo,
            'ip': s.ip,
            'estado': s.estado
        } for s in switches],
        'nvrs': [{
            'id': n.id,
            'codigo': n.codigo,
            'tipo': n.tipo,
            'modelo': n.modelo,
            'estado': n.estado
        } for n in nvrs],
        'ups': [{
            'id': u.id,
            'codigo': u.codigo,
            'modelo': u.modelo,
            'capacidad_va': u.capacidad_va,
            'estado': u.estado
        } for u in ups_list],
        'fuentes': [{
            'id': f.id,
            'codigo': f.codigo,
            'modelo': f.modelo,
            'voltaje': f.voltaje,
            'estado': f.estado
        } for f in fuentes]
    })

# ========== ADMINISTRACIÓN DE USUARIOS ==========
@app.route('/admin/usuarios')
@login_required
@role_required('superadmin', 'admin')
def admin_usuarios():
    """Lista todos los usuarios del sistema"""
    usuarios = Usuario.query.order_by(Usuario.fecha_creacion.desc()).all()
    return render_template('admin_usuarios_list.html', usuarios=usuarios)

@app.route('/admin/usuarios/nuevo', methods=['GET', 'POST'])
@login_required
@role_required('superadmin', 'admin')
def admin_usuarios_nuevo():
    """Crear nuevo usuario"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        rol = request.form.get('rol')
        nombre_completo = request.form.get('nombre_completo')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        
        # Validaciones
        if Usuario.query.filter_by(email=username).first():
            flash('El email ya existe', 'danger')
            return render_template('admin_usuarios_form.html')
        
        # Solo SUPERADMIN puede crear otros SUPERADMIN
        if rol == 'superadmin' and current_user.rol != 'superadmin':
            flash('Solo un SUPERADMIN puede crear otro SUPERADMIN', 'danger')
            return render_template('admin_usuarios_form.html')
        
        usuario = Usuario(
            email=username,
            rol=rol,
            nombre=nombre_completo,
            activo=True
        )
        usuario.set_password(password)
        
        db.session.add(usuario)
        db.session.commit()
        flash('Usuario creado exitosamente', 'success')
        return redirect(url_for('admin_usuarios'))
    
    return render_template('admin_usuarios_form.html')

@app.route('/admin/usuarios/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@role_required('superadmin', 'admin')
def admin_usuarios_editar(id):
    """Editar usuario existente"""
    usuario = Usuario.query.get_or_404(id)
    
    # Un usuario no puede editarse a sí mismo ni cambiar su propio rol
    if usuario.id == current_user.id:
        flash('No puedes editar tu propio perfil desde aquí', 'warning')
        return redirect(url_for('admin_usuarios'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        rol = request.form.get('rol')
        nombre_completo = request.form.get('nombre_completo')
        email = request.form.get('email')
        telefono = request.form.get('telefono')
        activo = request.form.get('activo') == 'on'
        
        # Validaciones
        if username != usuario.email and Usuario.query.filter_by(email=username).first():
            flash('El email ya existe', 'danger')
            return render_template('admin_usuarios_form.html', usuario=usuario)
        
        # Solo SUPERADMIN puede asignar rol SUPERADMIN
        if rol == 'superadmin' and current_user.rol != 'superadmin':
            flash('Solo un SUPERADMIN puede asignar rol SUPERADMIN', 'danger')
            return render_template('admin_usuarios_form.html', usuario=usuario)
        
        # No permitir que el último SUPERADMIN se desactive
        if usuario.rol == 'superadmin' and not activo and Usuario.query.filter_by(rol='superadmin').count() <= 1:
            flash('No se puede desactivar el último SUPERADMIN del sistema', 'danger')
            return render_template('admin_usuarios_form.html', usuario=usuario)
        
        usuario.email = username
        usuario.rol = rol
        usuario.nombre = nombre_completo
        usuario.email = email
        usuario.activo = activo
        
        db.session.commit()
        flash('Usuario actualizado exitosamente', 'success')
        return redirect(url_for('admin_usuarios'))
    
    return render_template('admin_usuarios_form.html', usuario=usuario)

@app.route('/admin/usuarios/<int:id>/eliminar', methods=['POST'])
@login_required
@role_required('superadmin', 'admin')
def admin_usuarios_eliminar(id):
    """Eliminar usuario"""
    usuario = Usuario.query.get_or_404(id)
    
    # Un usuario no puede eliminarse a sí mismo
    if usuario.id == current_user.id:
        flash('No puedes eliminar tu propio usuario', 'danger')
        return redirect(url_for('admin_usuarios'))
    
    # No permitir eliminar el último SUPERADMIN
    if usuario.rol == 'superadmin' and Usuario.query.filter_by(rol='superadmin').count() <= 1:
        flash('No se puede eliminar el último SUPERADMIN del sistema', 'danger')
        return redirect(url_for('admin_usuarios'))
    
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado exitosamente', 'success')
    return redirect(url_for('admin_usuarios'))

# ========== CONFIGURACIÓN DEL SISTEMA ==========
@app.route('/admin/configuracion')
@login_required
@role_required('superadmin')
def admin_configuracion():
    """Panel de configuración del sistema - Solo para SUPERADMIN"""
    return render_template('admin_configuracion.html')

@app.route('/admin/configuracion/modo', methods=['POST'])
@login_required
@role_required('superadmin')
def admin_configuracion_modo():
    """Cambiar entre modo Demo y Real - Solo para SUPERADMIN"""
    modo = request.form.get('modo')
    
    if modo not in ['demo', 'real']:
        flash('Modo inválido', 'danger')
        return redirect(url_for('admin_configuracion'))
    
    # Guardar modo en sesión
    session['modo_sistema'] = modo
    
    flash(f'Sistema configurado en modo {modo.upper()}', 'success')
    return redirect(url_for('admin_configuracion'))

# Inicializar base de datos y crear usuarios por defecto
@app.cli.command()
def init_db():
    """Inicializa la base de datos y crea usuarios por defecto"""
    db.create_all()
    
    # Verificar si ya existen usuarios
    if Usuario.query.count() == 0:
        usuarios = [
            Usuario(email='charles.jelvez', rol='superadmin', nombre='Charles Jélvez', activo=True),
            Usuario(email='admin', rol='admin', nombre='Administrador', activo=True),
            Usuario(email='supervisor', rol='supervisor', nombre='Supervisor', activo=True),
            Usuario(email='tecnico1', rol='tecnico', nombre='Técnico 1', activo=True),
            Usuario(email='visualizador', rol='visualizador', nombre='Visualizador', activo=True)
        ]
        
        passwords = ['charles123', 'admin123', 'super123', 'tecnico123', 'viz123']
        
        for user, password in zip(usuarios, passwords):
            user.set_password(password)
            db.session.add(user)
        
        db.session.commit()
        print('Base de datos inicializada con usuarios por defecto')
    else:
        print('Los usuarios ya existen')

# ========== RUTAS TEMPORALES PARA INICIALIZACIÓN EN RAILWAY ==========
@app.route('/init-usuarios-railway')
def init_usuarios_temporal():
    """Ruta temporal para inicializar usuarios en Railway PostgreSQL"""
    try:
        # Limpiar usuarios existentes
        Usuario.query.delete()
        db.session.commit()
        
        # Crear usuarios
        usuarios_data = [
            ('charles.jelvez', 'charles123', 'superadmin', 'Charles Jélvez', 'charles.jelvez@ufro.cl'),
            ('admin', 'admin123', 'admin', 'Administrador', 'admin@ufro.cl'),
            ('supervisor', 'super123', 'supervisor', 'Supervisor', 'supervisor@ufro.cl'),
            ('tecnico1', 'tecnico123', 'tecnico', 'Técnico 1', 'tecnico1@ufro.cl'),
            ('visualizador', 'viz123', 'visualizador', 'Visualizador', 'visualizador@ufro.cl')
        ]
        
        for username, password, rol, nombre, email in usuarios_data:
            usuario = Usuario(
                username=username,
                rol=rol,
                nombre=nombre,
                email=email,
                activo=True
            )
            usuario.set_password(password)
            db.session.add(usuario)
        
        db.session.commit()
        
        return f"""
        <h1>✅ Inicialización Exitosa</h1>
        <p><strong>Usuarios creados en Railway PostgreSQL:</strong></p>
        <ul>
        <li><strong>charles.jelvez</strong> / charles123 (SUPERADMIN)</li>
        <li><strong>admin</strong> / admin123 (ADMIN)</li>
        <li><strong>supervisor</strong> / super123 (SUPERVISOR)</li>
        <li><strong>tecnico1</strong> / tecnico123 (TÉCNICO)</li>
        <li><strong>visualizador</strong> / viz123 (VISUALIZADOR)</li>
        </ul>
        <p>🔗 <a href="/login">Ir al login</a></p>
        <p><em>Esta ruta se eliminará después de la inicialización</em></p>
        """
        
    except Exception as e:
        return f"<h1>❌ Error</h1><p>{str(e)}</p>"

@app.route('/crear-charles-superadmin')
def crear_charles_superadmin():
    """Ruta para crear específicamente Charles como SUPERADMIN"""
    try:
        # Verificar si Charles ya existe
        charles = Usuario.query.filter_by(username='charles.jelvez').first()
        
        if charles:
            # Actualizar contraseña y rol
            charles.set_password('charles123')
            charles.rol = 'superadmin'
            charles.activo = True
            db.session.commit()
            mensaje = f"✅ Charles actualizado: {charles.email} ({charles.rol})"
        else:
            # Crear nuevo Charles
            charles = Usuario(
                username='charles.jelvez',
                rol='superadmin',
                nombre='Charles Jélvez',
                email='charles.jelvez@ufro.cl',
                activo=True
            )
            charles.set_password('charles123')
            db.session.add(charles)
            db.session.commit()
            mensaje = f"✅ Charles creado: {charles.email} ({charles.rol})"
        
        # Mostrar todos los usuarios
        usuarios = Usuario.query.order_by(Usuario.rol.desc()).all()
        
        usuarios_html = ""
        credenciales = {
            'charles.jelvez': 'charles123',
            'admin': 'admin123',
            'supervisor': 'super123',
            'tecnico1': 'tecnico123',
            'visualizador': 'viz123'
        }
        
        for usuario in usuarios:
            pwd = credenciales.get(usuario.email, 'N/A')
            usuarios_html += f"<tr><td>{usuario.email}</td><td>{usuario.rol}</td><td>{pwd}</td><td>{'✅' if usuario.activo else '❌'}</td></tr>"
        
        return f"""
        <h1>👑 Configuración SUPERADMIN</h1>
        <p>{mensaje}</p>
        <h2>Usuarios en el Sistema:</h2>
        <table border="1" style="border-collapse: collapse; width: 100%;">
            <tr style="background: #f0f0f0;">
                <th>Usuario</th>
                <th>Rol</th>
                <th>Contraseña</th>
                <th>Estado</th>
            </tr>
            {usuarios_html}
        </table>
        <h2>🎯 Credenciales para Charles:</h2>
        <p><strong>URL:</strong> https://gestion-camaras-ufro.up.railway.app/</p>
        <p><strong>Usuario:</strong> charles.jelvez</p>
        <p><strong>Contraseña:</strong> charles123</p>
        <p><a href="/login">🔗 Ir al login</a></p>
        """
        
    except Exception as e:
        import traceback
        return f"<h1>❌ Error</h1><p>{str(e)}</p><pre>{traceback.format_exc()}</pre>"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
