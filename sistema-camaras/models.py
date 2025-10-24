from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(20), default='tecnico')
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

class Ubicacion(db.Model):
    __tablename__ = 'ubicaciones'
    id = db.Column(db.Integer, primary_key=True)
    campus = db.Column(db.String(100))
    edificio = db.Column(db.String(100))
    piso = db.Column(db.String(50))
    zona = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    gabinetes_en_ubicacion = db.Column(db.String(200))
    cantidad_camaras = db.Column(db.Integer)
    observaciones = db.Column(db.Text)

class Gabinete(db.Model):
    __tablename__ = 'gabinetes'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True)
    nombre = db.Column(db.String(100))
    ubicacion = db.Column(db.String(200))
    campus = db.Column(db.String(100))
    edificio = db.Column(db.String(100))
    piso = db.Column(db.String(50))
    coordenadas = db.Column(db.String(100))
    tipo = db.Column(db.String(50))
    estado = db.Column(db.String(50))
    switch_principal = db.Column(db.String(50))
    nvr_asociado = db.Column(db.String(50))
    camaras_conectadas = db.Column(db.Integer)
    fecha_instalacion = db.Column(db.Date)
    observaciones = db.Column(db.Text)
    switches = db.relationship('Switch', backref='gabinete', lazy=True)
    equipos = db.relationship('EquipoTecnico', backref='gabinete', lazy=True)

class Switch(db.Model):
    __tablename__ = 'switches'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True)
    nombre = db.Column(db.String(100))
    marca = db.Column(db.String(100))
    modelo = db.Column(db.String(100))
    numero_serie = db.Column(db.String(100))
    gabinete_id = db.Column(db.Integer, db.ForeignKey('gabinetes.id'))
    puertos_totales = db.Column(db.Integer)
    puertos_usados = db.Column(db.Integer)
    puertos_disponibles = db.Column(db.Integer)
    soporta_poe = db.Column(db.Boolean)
    estado = db.Column(db.String(50))
    fecha_instalacion = db.Column(db.Date)
    fecha_ultimo_mantenimiento = db.Column(db.Date)
    observaciones = db.Column(db.Text)
    puertos = db.relationship('PuertoSwitch', backref='switch', lazy=True)

class PuertoSwitch(db.Model):
    __tablename__ = 'puertos_switch'
    id = db.Column(db.Integer, primary_key=True)
    switch_id = db.Column(db.Integer, db.ForeignKey('switches.id'))
    numero_puerto = db.Column(db.Integer)
    estado = db.Column(db.String(50))
    dispositivo_conectado = db.Column(db.String(100))
    ip_dispositivo = db.Column(db.String(45))
    tipo_conexion = db.Column(db.String(50))
    nvr_asociado = db.Column(db.String(50))
    puerto_nvr = db.Column(db.String(50))
    observaciones = db.Column(db.Text)

class Camara(db.Model):
    __tablename__ = 'camaras'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True)
    nombre = db.Column(db.String(100))
    campus = db.Column(db.String(100))
    edificio = db.Column(db.String(100))
    piso = db.Column(db.String(50))
    ubicacion = db.Column(db.String(200))
    ip = db.Column(db.String(45))
    marca = db.Column(db.String(100))
    modelo = db.Column(db.String(100))
    tipo = db.Column(db.String(50))
    resolucion = db.Column(db.String(50))
    estado = db.Column(db.String(50))
    gabinete_asociado = db.Column(db.String(50))
    switch_conectado = db.Column(db.String(50))
    puerto_switch = db.Column(db.String(20))
    nvr_asociado = db.Column(db.String(50))
    puerto_nvr = db.Column(db.String(20))
    fecha_instalacion = db.Column(db.Date)
    observaciones = db.Column(db.Text)
    fallas = db.relationship('Falla', backref='camara', lazy=True)

class EquipoTecnico(db.Model):
    __tablename__ = 'equipos_tecnicos'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))
    marca = db.Column(db.String(100))
    modelo = db.Column(db.String(100))
    numero_serie = db.Column(db.String(100))
    capacidad = db.Column(db.String(50))
    ubicacion = db.Column(db.String(200))
    gabinete_id = db.Column(db.Integer, db.ForeignKey('gabinetes.id'))
    estado = db.Column(db.String(50))
    fecha_instalacion = db.Column(db.Date)
    fecha_ultimo_mantenimiento = db.Column(db.Date)
    proximo_mantenimiento = db.Column(db.Date)
    observaciones = db.Column(db.Text)

class Falla(db.Model):
    __tablename__ = 'fallas'
    id = db.Column(db.Integer, primary_key=True)
    fecha_reporte = db.Column(db.DateTime, default=datetime.utcnow)
    reportado_por = db.Column(db.String(100))
    tipo = db.Column(db.String(100))
    subtipo = db.Column(db.String(100))
    camara_id = db.Column(db.Integer, db.ForeignKey('camaras.id'))
    camara_afectada = db.Column(db.String(100))
    ubicacion = db.Column(db.String(200))
    descripcion = db.Column(db.Text)
    impacto_visibilidad = db.Column(db.String(20))
    afecta_vision_nocturna = db.Column(db.String(10))
    estado = db.Column(db.String(50), default='Abierta')
    prioridad = db.Column(db.String(20))
    tecnico_asignado = db.Column(db.String(100))
    fecha_inicio = db.Column(db.DateTime)
    fecha_resolucion = db.Column(db.DateTime)
    solucion = db.Column(db.Text)
    gravedad = db.Column(db.String(20))
    componente_afectado = db.Column(db.String(100))
    observaciones = db.Column(db.Text)

class Mantenimiento(db.Model):
    __tablename__ = 'mantenimientos'
    id = db.Column(db.Integer, primary_key=True)
    fecha_programada = db.Column(db.Date)
    fecha_realizacion = db.Column(db.Date)
    tipo = db.Column(db.String(50))
    categoria = db.Column(db.String(50))
    equipo_gabinete = db.Column(db.String(100))
    ubicacion = db.Column(db.String(200))
    descripcion = db.Column(db.Text)
    estado = db.Column(db.String(50))
    tecnico_responsable = db.Column(db.String(100))
    materiales_utilizados = db.Column(db.Text)
    costo_aproximado = db.Column(db.Float)
    equipos_camaras_afectadas = db.Column(db.Text)
    tiempo_ejecucion = db.Column(db.String(50))
    observaciones = db.Column(db.Text)

class TipoFalla(db.Model):
    __tablename__ = 'tipos_fallas'
    id = db.Column(db.Integer, primary_key=True)
    categoria_principal = db.Column(db.String(100))
    tipo_falla = db.Column(db.String(100))
    impacto_tipico = db.Column(db.String(100))
    tipo_mantenimiento = db.Column(db.String(100))
    prioridad_sugerida = db.Column(db.String(20))
    frecuencia_observada = db.Column(db.String(50))
