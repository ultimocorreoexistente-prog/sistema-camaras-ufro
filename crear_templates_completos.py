#!/usr/bin/env python3
"""
Script completo para generar TODOS los templates HTML faltantes
Sistema de Gestión de Cámaras UFRO
"""

import os

# Crear templates completos
def crear_nvr_form():
    return """{% extends "base.html" %}
{% block title %}{{ 'Editar' if nvr else 'Nuevo' }} NVR/DVR - Sistema UFRO{% endblock %}
{% block content %}
<div class="container mt-4">
    <h2><i class="bi bi-hdd-rack"></i> {{ 'Editar' if nvr else 'Nuevo' }} NVR/DVR</h2>
    <hr>
    <form method="POST">
        <div class="row">
            <div class="col-md-6 mb-3">
                <label class="form-label">Código <span class="text-danger">*</span></label>
                <input type="text" class="form-control" name="codigo" value="{{ nvr.codigo if nvr else '' }}" required>
            </div>
            <div class="col-md-6 mb-3">
                <label class="form-label">Tipo <span class="text-danger">*</span></label>
                <select class="form-select" name="tipo" required>
                    <option value="NVR" {% if nvr and nvr.tipo == 'NVR' %}selected{% endif %}>NVR</option>
                    <option value="DVR" {% if nvr and nvr.tipo == 'DVR' %}selected{% endif %}>DVR</option>
                </select>
            </div>
        </div>
        <div class="row">
            <div class="col-md-4 mb-3">
                <label class="form-label">Modelo</label>
                <input type="text" class="form-control" name="modelo" value="{{ nvr.modelo if nvr else '' }}">
            </div>
            <div class="col-md-4 mb-3">
                <label class="form-label">Marca</label>
                <input type="text" class="form-control" name="marca" value="{{ nvr.marca if nvr else '' }}">
            </div>
            <div class="col-md-4 mb-3">
                <label class="form-label">IP</label>
                <input type="text" class="form-control" name="ip" value="{{ nvr.ip if nvr else '' }}">
            </div>
        </div>
        <div class="row">
            <div class="col-md-6 mb-3">
                <label class="form-label">Canales Totales</label>
                <input type="number" class="form-control" name="canales_totales" value="{{ nvr.canales_totales if nvr else 0 }}" min="0">
            </div>
            <div class="col-md-6 mb-3">
                <label class="form-label">Canales Usados</label>
                <input type="number" class="form-control" name="canales_usados" value="{{ nvr.canales_usados if nvr else 0 }}" min="0">
            </div>
        </div>
        <div class="row">
            <div class="col-md-6 mb-3">
                <label class="form-label">Ubicación</label>
                <select class="form-select" name="ubicacion_id">
                    <option value="">Seleccione ubicación</option>
                    {% for ubicacion in ubicaciones %}
                    <option value="{{ ubicacion.id }}" {% if nvr and nvr.ubicacion_id == ubicacion.id %}selected{% endif %}>{{ ubicacion.campus }} - {{ ubicacion.edificio }}</option>
                    {% endfor %}
                </select>
            </div>
            <div class="col-md-6 mb-3">
                <label class="form-label">Gabinete</label>
                <select class="form-select" name="gabinete_id">
                    <option value="">Sin gabinete</option>
                    {% for gabinete in gabinetes %}
                    <option value="{{ gabinete.id }}" {% if nvr and nvr.gabinete_id == gabinete.id %}selected{% endif %}>{{ gabinete.codigo }}</option>
                    {% endfor %}
                </select>
            </div>
        </div>
        <div class="row">
            <div class="col-md-6 mb-3">
                <label class="form-label">Estado</label>
                <select class="form-select" name="estado">
                    <option value="Activo" {% if nvr and nvr.estado == 'Activo' %}selected{% endif %}>Activo</option>
                    <option value="Inactivo" {% if nvr and nvr.estado == 'Inactivo' %}selected{% endif %}>Inactivo</option>
                </select>
            </div>
            <div class="col-md-6 mb-3">
                <label class="form-label">Fecha de Alta</label>
                <input type="date" class="form-control" name="fecha_alta" value="{{ nvr.fecha_alta if nvr and nvr.fecha_alta else '' }}">
            </div>
        </div>
        <div class="row">
            <div class="col-md-6 mb-3">
                <label class="form-label">Latitud</label>
                <input type="number" step="any" class="form-control" name="latitud" value="{{ nvr.latitud if nvr else '' }}">
            </div>
            <div class="col-md-6 mb-3">
                <label class="form-label">Longitud</label>
                <input type="number" step="any" class="form-control" name="longitud" value="{{ nvr.longitud if nvr else '' }}">
            </div>
        </div>
        <div class="row">
            <div class="col-md-12 mb-3">
                <label class="form-label">Observaciones</label>
                <textarea class="form-control" name="observaciones" rows="3">{{ nvr.observaciones if nvr else '' }}</textarea>
            </div>
        </div>
        <button type="submit" class="btn btn-primary"><i class="bi bi-save"></i> Guardar</button>
        <a href="{{ url_for('nvr_list') }}" class="btn btn-secondary"><i class="bi bi-x-circle"></i> Cancelar</a>
    </form>
</div>
{% endblock %}
"""

def crear_nvr_detalle():
    return """{% extends "base.html" %}
{% block title %}Detalle NVR/DVR - Sistema UFRO{% endblock %}
{% block content %}
<div class="container mt-4">
    <div class="row mb-4">
        <div class="col-md-6"><h2><i class="bi bi-hdd-rack"></i> Detalle del NVR/DVR</h2></div>
        <div class="col-md-6 text-end">
            {% if current_user.rol in ['admin', 'supervisor'] %}
            <a href="{{ url_for('nvr_editar', id=nvr.id) }}" class="btn btn-warning"><i class="bi bi-pencil"></i> Editar</a>
            {% endif %}
            <a href="{{ url_for('nvr_list') }}" class="btn btn-secondary"><i class="bi bi-arrow-left"></i> Volver</a>
        </div>
    </div>

    <div class="row">
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header bg-primary text-white"><h5 class="mb-0">Información General</h5></div>
                <div class="card-body">
                    <table class="table table-sm">
                        <tr><th style="width:40%;">Código:</th><td><strong>{{ nvr.codigo }}</strong></td></tr>
                        <tr><th>Tipo:</th><td><span class="badge bg-primary">{{ nvr.tipo }}</span></td></tr>
                        <tr><th>Modelo:</th><td>{{ nvr.modelo or 'N/A' }}</td></tr>
                        <tr><th>Marca:</th><td>{{ nvr.marca or 'N/A' }}</td></tr>
                        <tr><th>IP:</th><td>{{ nvr.ip or 'N/A' }}</td></tr>
                        <tr><th>Estado:</th><td><span class="badge bg-{{ 'success' if nvr.estado == 'Activo' else 'danger' }}">{{ nvr.estado }}</span></td></tr>
                    </table>
                </div>
            </div>
        </div>

        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header bg-info text-white"><h5 class="mb-0">Capacidad de Canales</h5></div>
                <div class="card-body">
                    <table class="table table-sm">
                        <tr><th style="width:40%;">Canales Totales:</th><td><span class="badge bg-primary">{{ nvr.canales_totales or 0 }}</span></td></tr>
                        <tr><th>Canales Usados:</th><td><span class="badge bg-info">{{ nvr.canales_usados or 0 }}</span></td></tr>
                        <tr><th>Canales Disponibles:</th><td><span class="badge bg-success">{{ (nvr.canales_totales or 0) - (nvr.canales_usados or 0) }}</span></td></tr>
                    </table>
                    {% if nvr.canales_totales > 0 %}
                    <div class="progress mt-3" style="height:25px;">
                        {% set porcentaje = (nvr.canales_usados / nvr.canales_totales * 100) | int %}
                        <div class="progress-bar bg-info" style="width:{{ porcentaje }}%;">{{ porcentaje }}%</div>
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>

    {% if camaras %}
    <div class="card mb-4">
        <div class="card-header bg-success text-white"><h5 class="mb-0">Cámaras Conectadas ({{ camaras|length }})</h5></div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-sm table-striped">
                    <thead><tr><th>Código</th><th>Nombre</th><th>IP</th><th>Estado</th><th>Acciones</th></tr></thead>
                    <tbody>
                        {% for camara in camaras %}
                        <tr>
                            <td><strong>{{ camara.codigo }}</strong></td>
                            <td>{{ camara.nombre }}</td>
                            <td>{{ camara.ip or 'N/A' }}</td>
                            <td><span class="badge bg-{{ 'success' if camara.estado == 'Activo' else 'danger' }}">{{ camara.estado }}</span></td>
                            <td><a href="{{ url_for('camaras_detalle', id=camara.id) }}" class="btn btn-sm btn-info"><i class="bi bi-eye"></i></a></td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    {% endif %}
</div>
{% endblock %}
"""

# Función principal
def generar_todos_los_templates():
    templates_dir = "templates"
    
    templates = {
        "nvr_form.html": crear_nvr_form(),
        "nvr_detalle.html": crear_nvr_detalle(),
    }
    
    for filename, content in templates.items():
        filepath = os.path.join(templates_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Creado: {filename}")
    
    print(f"\nTotal de templates creados: {len(templates)}")

if __name__ == "__main__":
    generar_todos_los_templates()
