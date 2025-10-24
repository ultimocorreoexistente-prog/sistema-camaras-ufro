#!/usr/bin/env python3
"""
Script para generar todos los templates HTML faltantes del sistema de gestión de cámaras UFRO
"""

import os

# Directorio base de templates
TEMPLATES_DIR = "/workspace/sistema-camaras-flask/templates"

# Definir todos los templates
templates = {}

#  NVR/DVR DETALLE
templates["nvr_detalle.html"] = """{% extends "base.html" %}
{% block title %}Detalle NVR/DVR - Sistema UFRO{% endblock %}
{% block content %}
<div class="container mt-4">
    <div class="row mb-4">
        <div class="col-md-6">
            <h2><i class="bi bi-hdd-rack"></i> Detalle del NVR/DVR</h2>
        </div>
        <div class="col-md-6 text-end">
            {% if current_user.rol in ['admin', 'supervisor'] %}
            <a href="{{ url_for('nvr_editar', id=nvr.id) }}" class="btn btn-warning">
                <i class="bi bi-pencil"></i> Editar
            </a>
            {% endif %}
            <a href="{{ url_for('nvr_list') }}" class="btn btn-secondary">
                <i class="bi bi-arrow-left"></i> Volver
            </a>
        </div>
    </div>

    <div class="row">
        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h5 class="mb-0">Información General</h5>
                </div>
                <div class="card-body">
                    <table class="table table-sm">
                        <tr><th style="width: 40%;">Código:</th><td><strong>{{ nvr.codigo }}</strong></td></tr>
                        <tr><th>Tipo:</th><td><span class="badge bg-primary">{{ nvr.tipo }}</span></td></tr>
                        <tr><th>Modelo:</th><td>{{ nvr.modelo or 'N/A' }}</td></tr>
                        <tr><th>Marca:</th><td>{{ nvr.marca or 'N/A' }}</td></tr>
                        <tr><th>IP:</th><td>{{ nvr.ip or 'N/A' }}</td></tr>
                        <tr><th>Estado:</th><td><span class="badge bg-{{ 'success' if nvr.estado == 'Activo' else 'danger' }}">{{ nvr.estado }}</span></td></tr>
                        <tr><th>Gabinete:</th><td>{{ nvr.gabinete.codigo if nvr.gabinete else 'N/A' }}</td></tr>
                    </table>
                </div>
            </div>
        </div>

        <div class="col-md-6">
            <div class="card mb-4">
                <div class="card-header bg-info text-white">
                    <h5 class="mb-0">Capacidad de Canales</h5>
                </div>
                <div class="card-body">
                    <table class="table table-sm">
                        <tr><th style="width: 40%;">Canales Totales:</th><td><span class="badge bg-primary">{{ nvr.canales_totales or 0 }}</span></td></tr>
                        <tr><th>Canales Usados:</th><td><span class="badge bg-info">{{ nvr.canales_usados or 0 }}</span></td></tr>
                        <tr><th>Canales Disponibles:</th><td><span class="badge bg-success">{{ (nvr.canales_totales or 0) - (nvr.canales_usados or 0) }}</span></td></tr>
                    </table>
                    {% if nvr.canales_totales > 0 %}
                    <div class="mt-3">
                        <p class="mb-2"><strong>Uso de Canales:</strong></p>
                        <div class="progress" style="height: 25px;">
                            {% set porcentaje_usado = (nvr.canales_usados / nvr.canales_totales * 100) | int %}
                            <div class="progress-bar bg-info" role="progressbar" style="width: {{ porcentaje_usado }}%;">
                                {{ porcentaje_usado }}%
                            </div>
                        </div>
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>

    {% if camaras %}
    <div class="card mb-4">
        <div class="card-header bg-success text-white">
            <h5 class="mb-0">Cámaras Conectadas ({{ camaras|length }})</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-sm table-striped">
                    <thead>
                        <tr><th>Código</th><th>Nombre</th><th>IP</th><th>Puerto NVR</th><th>Estado</th><th>Acciones</th></tr>
                    </thead>
                    <tbody>
                        {% for camara in camaras %}
                        <tr>
                            <td><strong>{{ camara.codigo }}</strong></td>
                            <td>{{ camara.nombre }}</td>
                            <td>{{ camara.ip or 'N/A' }}</td>
                            <td>{{ camara.puerto_nvr or 'N/A' }}</td>
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

    {% if nvr.observaciones %}
    <div class="card mb-4">
        <div class="card-header"><h5 class="mb-0">Observaciones</h5></div>
        <div class="card-body"><p>{{ nvr.observaciones }}</p></div>
    </div>
    {% endif %}
</div>
{% endblock %}
"""

# UPS LIST
templates["ups_list.html"] = """{% extends "base.html" %}
{% block title %}UPS - Sistema UFRO{% endblock %}
{% block content %}
<div class="container-fluid mt-4">
    <div class="row mb-4">
        <div class="col-md-6"><h2><i class="bi bi-battery-charging"></i> Gestión de UPS</h2></div>
        <div class="col-md-6 text-end">
            {% if current_user.rol in ['admin', 'supervisor'] %}
            <a href="{{ url_for('ups_nuevo') }}" class="btn btn-primary"><i class="bi bi-plus-circle"></i> Nuevo UPS</a>
            {% endif %}
        </div>
    </div>

    <div class="card mb-4">
        <div class="card-body">
            <form method="GET" class="row g-3">
                <div class="col-md-4">
                    <label for="campus" class="form-label">Campus</label>
                    <select name="campus" id="campus" class="form-select">
                        <option value="">Todos</option>
                        {% for campus in campus_list %}<option value="{{ campus }}" {% if request.args.get('campus') == campus %}selected{% endif %}>{{ campus }}</option>{% endfor %}
                    </select>
                </div>
                <div class="col-md-4">
                    <label for="estado" class="form-label">Estado</label>
                    <select name="estado" id="estado" class="form-select">
                        <option value="">Todos</option>
                        <option value="Activo" {% if request.args.get('estado') == 'Activo' %}selected{% endif %}>Activo</option>
                        <option value="Inactivo" {% if request.args.get('estado') == 'Inactivo' %}selected{% endif %}>Inactivo</option>
                    </select>
                </div>
                <div class="col-md-4 d-flex align-items-end">
                    <button type="submit" class="btn btn-info w-100"><i class="bi bi-search"></i> Filtrar</button>
                </div>
            </form>
        </div>
    </div>

    <div class="card">
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead class="table-dark">
                        <tr><th>Código</th><th>Modelo</th><th>Marca</th><th>Capacidad (VA)</th><th>Baterías</th><th>Ubicación</th><th>Gabinete</th><th>Estado</th><th>Acciones</th></tr>
                    </thead>
                    <tbody>
                        {% for ups in ups_list %}
                        <tr>
                            <td><strong>{{ ups.codigo }}</strong></td>
                            <td>{{ ups.modelo or 'N/A' }}</td>
                            <td>{{ ups.marca or 'N/A' }}</td>
                            <td>{{ ups.capacidad_va or 'N/A' }}</td>
                            <td>{{ ups.numero_baterias or 'N/A' }}</td>
                            <td>{{ ups.ubicacion.edificio if ups.ubicacion else 'N/A' }}</td>
                            <td>{{ ups.gabinete.codigo if ups.gabinete else 'N/A' }}</td>
                            <td><span class="badge bg-{{ 'success' if ups.estado == 'Activo' else 'danger' }}">{{ ups.estado }}</span></td>
                            <td>
                                <a href="{{ url_for('ups_detalle', id=ups.id) }}" class="btn btn-sm btn-info" title="Ver detalle"><i class="bi bi-eye"></i></a>
                                {% if current_user.rol in ['admin', 'supervisor'] %}
                                <a href="{{ url_for('ups_editar', id=ups.id) }}" class="btn btn-sm btn-warning" title="Editar"><i class="bi bi-pencil"></i></a>
                                {% endif %}
                            </td>
                        </tr>
                        {% else %}
                        <tr><td colspan="9" class="text-center">No se encontraron UPS</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <div class="mt-3">
        <p class="text-muted">Total de UPS: <strong>{{ ups_list|length }}</strong></p>
    </div>
</div>
{% endblock %}
"""

# Crear todos los archivos
created_count = 0
for filename, content in templates.items():
    filepath = os.path.join(TEMPLATES_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Creado: {filename}")
    created_count += 1

print(f"\nTotal de templates creados: {created_count}")
