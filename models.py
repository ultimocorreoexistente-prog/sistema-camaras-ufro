from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<Usuario {self.email}>'

class Ubicacion(db.Model):
    __tablename__ = 'ubicaciones'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    campus = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Ubicacion {self.nombre}>'

class Camara(db.Model):
    __tablename__ = 'camaras'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(15))
    ubicacion_id = db.Column(db.Integer, db.ForeignKey('ubicaciones.id'))
    estado = db.Column(db.String(20), nullable=False, default='Activo')
    tipo = db.Column(db.String(50))
    marca = db.Column(db.String(50))
    modelo = db.Column(db.String(50))
    nvr_id = db.Column(db.Integer, db.ForeignKey('nvr_dvrs.id'))
    puerto = db.Column(db.Integer)
    observaciones = db.Column(db.Text)
    fecha_instalacion = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ubicacion = db.relationship('Ubicacion', backref='camaras_ubicacion')
    nvr = db.relationship('NVR_DVR', backref='camaras')
    
    def __repr__(self):
        return f'<Camara {self.codigo}>'

class Gabinete(db.Model):
    __tablename__ = 'gabinetes'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(200))
    tipo_ubicacion_general = db.Column(db.String(50))  # Interior/Exterior/Subterraneo
    tipo_ubicacion_detallada = db.Column(db.String(200))
    ubicacion_id = db.Column(db.Integer, db.ForeignKey('ubicaciones.id'))
    capacidad = db.Column(db.Integer)
    tiene_ups = db.Column(db.Boolean, default=False)
    tiene_switch = db.Column(db.Boolean, default=False)
    tiene_nvr = db.Column(db.Boolean, default=False)
    conexion_fibra = db.Column(db.Boolean, default=False)
    estado = db.Column(db.String(20), default='Activo')
    fecha_alta = db.Column(db.Date)
    fecha_baja = db.Column(db.Date)
    motivo_baja = db.Column(db.Text)
    fecha_ultima_revision = db.Column(db.Date)
    observaciones = db.Column(db.Text)
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    
    # Relationships
    ubicacion = db.relationship('Ubicacion', backref='gabinetes')

class Switch(db.Model):
    __tablename__ = 'switches'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(200))
    ip = db.Column(db.String(45))
    modelo = db.Column(db.String(100))
    marca = db.Column(db.String(100))
    numero_serie = db.Column(db.String(100))
    gabinete_id = db.Column(db.Integer, db.ForeignKey('gabinetes.id'))
    puertos_totales = db.Column(db.Integer)
    puertos_usados = db.Column(db.Integer, default=0)
    puertos_disponibles = db.Column(db.Integer)
    capacidad_poe = db.Column(db.Boolean, default=False)
    estado = db.Column(db.String(20), default='Activo')
    fecha_alta = db.Column(db.Date)
    fecha_baja = db.Column(db.Date)
    motivo_baja = db.Column(db.Text)
    fecha_mantenimiento = db.Column(db.Date)
    observaciones = db.Column(db.Text)
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    
    gabinete = db.relationship('Gabinete', backref='switches_gabinete')

class Puerto_Switch(db.Model):
    __tablename__ = 'puertos_switch'
    id = db.Column(db.Integer, primary_key=True)
    switch_id = db.Column(db.Integer, db.ForeignKey('switches.id'), nullable=False)
    numero_puerto = db.Column(db.Integer, nullable=False)
    camara_id = db.Column(db.Integer, nullable=True)  # Campo directo sin FK
    ip_dispositivo = db.Column(db.String(45))
    estado = db.Column(db.String(20), default='Disponible')  # En uso/Disponible/Averiado
    tipo_conexion = db.Column(db.String(20))  # PoE/Fibra/Normal
    nvr_id = db.Column(db.Integer, db.ForeignKey('nvr_dvrs.id'))
    puerto_nvr = db.Column(db.String(20))
    
    switch = db.relationship('Switch', backref='puertos')

class UPS(db.Model):
    __tablename__ = 'upss'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    modelo = db.Column(db.String(100))
    marca = db.Column(db.String(100))
    capacidad_va = db.Column(db.Integer)
    numero_baterias = db.Column(db.Integer)
    ubicacion_id = db.Column(db.Integer, db.ForeignKey('ubicaciones.id'))
    gabinete_id = db.Column(db.Integer, db.ForeignKey('gabinetes.id'))
    equipos_que_alimenta = db.Column(db.Text)
    estado = db.Column(db.String(20), default='Activo')
    fecha_alta = db.Column(db.Date)
    fecha_baja = db.Column(db.Date)
    motivo_baja = db.Column(db.Text)
    fecha_instalacion = db.Column(db.Date)
    ultimo_mantenimiento = db.Column(db.Date)
    observaciones = db.Column(db.Text)
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    
    # Relationships
    ubicacion = db.relationship('Ubicacion', backref='upss_ubicacion')
    gabinete = db.relationship('Gabinete', backref='upss')

class NVR_DVR(db.Model):
    __tablename__ = 'nvr_dvrs'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # NVR/DVR
    modelo = db.Column(db.String(100))
    marca = db.Column(db.String(100))
    canales_totales = db.Column(db.Integer)
    canales_usados = db.Column(db.Integer, default=0)
    ip = db.Column(db.String(45))
    ubicacion_id = db.Column(db.Integer, db.ForeignKey('ubicaciones.id'))
    gabinete_id = db.Column(db.Integer, db.ForeignKey('gabinetes.id'))
    estado = db.Column(db.String(20), default='Activo')
    fecha_alta = db.Column(db.Date)
    fecha_baja = db.Column(db.Date)
    motivo_baja = db.Column(db.Text)
    observaciones = db.Column(db.Text)
    latitud = db.Column(db.Float)
    longitud = db.Column(db.Float)
    
    # Relationships
    ubicacion = db.relationship('Ubicacion', backref='nvr_dvr_ubicacion')
    gabinete = db.relationship('Gabinete', backref='nvr_dvr')

class Fuente_Poder(db.Model):
    __tablename__ = 'fuentes_poder'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    modelo = db.Column(db.String(100))
    voltaje = db.Column(db.String(20))
    amperaje = db.Column(db.String(20))
    equipos_que_alimenta = db.Column(db.Text)
    ubicacion_id = db.Column(db.Integer, db.ForeignKey('ubicaciones.id'))
    gabinete_id = db.Column(db.Integer, db.ForeignKey('gabinetes.id'))
    estado = db.Column(db.String(20), default='Activo')
    fecha_alta = db.Column(db.Date)
    fecha_baja = db.Column(db.Date)
    motivo_baja = db.Column(db.Text)
    observaciones = db.Column(db.Text)
    
    # Relationships
    ubicacion = db.relationship('Ubicacion', backref='fuentes_poder_ubicacion')
    gabinete = db.relationship('Gabinete', backref='fuentes_poder')



class Catalogo_Tipo_Falla(db.Model):
    __tablename__ = 'catalogo_tipo_falla'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    gravedad = db.Column(db.String(20))  # Baja/Media/Alta/Critica
    tiempo_estimado_resolucion = db.Column(db.Integer)  # en horas

class Falla(db.Model):
    __tablename__ = 'falla'
    id = db.Column(db.Integer, primary_key=True)
    equipo_tipo = db.Column(db.String(50), nullable=False)  # Camara/Gabinete/Switch/UPS/NVR/Fuente
    equipo_id = db.Column(db.Integer, nullable=False)
    tipo_falla_id = db.Column(db.Integer, db.ForeignKey('catalogo_tipo_falla.id'))
    descripcion = db.Column(db.Text)
    prioridad = db.Column(db.String(20))  # Baja/Media/Alta/Critica
    fecha_reporte = db.Column(db.DateTime, default=datetime.utcnow)
    reportado_por_id = db.Column(db.Integer, nullable=True)  # Campo directo sin FK
    estado = db.Column(db.String(20), default='Pendiente')  # Pendiente/Asignada/En Proceso/Reparada/Cerrada/Cancelada
    fecha_asignacion = db.Column(db.DateTime)
    tecnico_asignado_id = db.Column(db.Integer, nullable=True)  # Campo directo sin FK
    fecha_inicio_reparacion = db.Column(db.DateTime)
    fecha_fin_reparacion = db.Column(db.DateTime)
    tiempo_resolucion_horas = db.Column(db.Float)
    solucion_aplicada = db.Column(db.Text)
    materiales_utilizados = db.Column(db.Text)
    costo_reparacion = db.Column(db.Float)
    observaciones = db.Column(db.Text)
    fecha_cierre = db.Column(db.DateTime)
    
    tipo_falla = db.relationship('Catalogo_Tipo_Falla', backref='fallas')
    # reportado_por relationship eliminado
    # tecnico_asignado relationship eliminado

class Mantenimiento(db.Model):
    __tablename__ = 'mantenimiento'
    id = db.Column(db.Integer, primary_key=True)
    equipo_tipo = db.Column(db.String(50), nullable=False)
    equipo_id = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # Preventivo/Correctivo/Predictivo
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    tecnico_id = db.Column(db.Integer, nullable=True)  # Campo directo sin FK
    descripcion = db.Column(db.Text)
    materiales_utilizados = db.Column(db.Text)
    equipos_afectados = db.Column(db.Text)
    tiempo_ejecucion_horas = db.Column(db.Float)
    costo = db.Column(db.Float)
    observaciones = db.Column(db.Text)
    
    # tecnico relationship eliminado

class Equipo_Tecnico(db.Model):
    __tablename__ = 'equipo_tecnico'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(200))
    estado = db.Column(db.String(20), default='Activo')  # Activo/Inactivo
    fecha_ingreso = db.Column(db.Date)

class Historial_Estado_Equipo(db.Model):
    __tablename__ = 'historial_estado_equipo'
    id = db.Column(db.Integer, primary_key=True)
    equipo_tipo = db.Column(db.String(50), nullable=False)
    equipo_id = db.Column(db.Integer, nullable=False)
    estado_anterior = db.Column(db.String(20))
    estado_nuevo = db.Column(db.String(20), nullable=False)
    fecha_cambio = db.Column(db.DateTime, default=datetime.utcnow)
    motivo = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, nullable=True)  # Campo directo sin FK
    
    # usuario relationship eliminado
