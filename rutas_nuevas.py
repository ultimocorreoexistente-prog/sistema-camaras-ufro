# ============================================================================
# PRIORIDAD 1: RUTAS ENLACES - Gestión de Conectividad
# ============================================================================

@app.route('/enlaces')
@login_required
def enlaces():
    """Listar todos los enlaces de conectividad"""
    enlaces = Enlace.query.all()
    return render_template('enlaces_list.html', enlaces=enlaces)

@app.route('/enlaces/nuevo', methods=['GET', 'POST'])
@login_required
def enlaces_nuevo():
    """Crear nuevo enlace"""
    if request.method == 'POST':
        enlace = Enlace(
            codigo=request.form['codigo'],
            nombre=request.form.get('nombre'),
            tipo_enlace=request.form['tipo_enlace'],
            origen_ubicacion_id=request.form.get('origen_ubicacion_id') or None,
            destino_ubicacion_id=request.form.get('destino_ubicacion_id') or None,
            switch_origen_id=request.form.get('switch_origen_id') or None,
            switch_destino_id=request.form.get('switch_destino_id') or None,
            latencia_ms=float(request.form['latencia_ms']) if request.form.get('latencia_ms') else None,
            porcentaje_perdida_paquetes=float(request.form['porcentaje_perdida_paquetes']) if request.form.get('porcentaje_perdida_paquetes') else None,
            estado_conexion=request.form.get('estado_conexion', 'Activo'),
            ancho_banda_mbps=int(request.form['ancho_banda_mbps']) if request.form.get('ancho_banda_mbps') else None,
            proveedor=request.form.get('proveedor'),
            fecha_instalacion=datetime.strptime(request.form['fecha_instalacion'], '%Y-%m-%d').date() if request.form.get('fecha_instalacion') else None,
            fecha_ultimo_testeo=datetime.strptime(request.form['fecha_ultimo_testeo'], '%Y-%m-%d').date() if request.form.get('fecha_ultimo_testeo') else None,
            observaciones=request.form.get('observaciones')
        )
        db.session.add(enlace)
        db.session.commit()
        flash('Enlace creado exitosamente', 'success')
        return redirect(url_for('enlaces'))
    
    ubicaciones = Ubicacion.query.filter_by(activo=True).all()
    switches = Switch.query.filter_by(estado='Activo').all()
    return render_template('enlaces_form.html', enlace=None, ubicaciones=ubicaciones, switches=switches)

@app.route('/enlaces/<int:id>')
@login_required
def enlaces_detalle(id):
    """Ver detalle de un enlace"""
    enlace = Enlace.query.get_or_404(id)
    return render_template('enlaces_detalle.html', enlace=enlace)

@app.route('/enlaces/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def enlaces_editar(id):
    """Editar un enlace existente"""
    enlace = Enlace.query.get_or_404(id)
    
    if request.method == 'POST':
        enlace.codigo = request.form['codigo']
        enlace.nombre = request.form.get('nombre')
        enlace.tipo_enlace = request.form['tipo_enlace']
        enlace.origen_ubicacion_id = request.form.get('origen_ubicacion_id') or None
        enlace.destino_ubicacion_id = request.form.get('destino_ubicacion_id') or None
        enlace.switch_origen_id = request.form.get('switch_origen_id') or None
        enlace.switch_destino_id = request.form.get('switch_destino_id') or None
        enlace.latencia_ms = float(request.form['latencia_ms']) if request.form.get('latencia_ms') else None
        enlace.porcentaje_perdida_paquetes = float(request.form['porcentaje_perdida_paquetes']) if request.form.get('porcentaje_perdida_paquetes') else None
        enlace.estado_conexion = request.form.get('estado_conexion', 'Activo')
        enlace.ancho_banda_mbps = int(request.form['ancho_banda_mbps']) if request.form.get('ancho_banda_mbps') else None
        enlace.proveedor = request.form.get('proveedor')
        enlace.fecha_instalacion = datetime.strptime(request.form['fecha_instalacion'], '%Y-%m-%d').date() if request.form.get('fecha_instalacion') else None
        enlace.fecha_ultimo_testeo = datetime.strptime(request.form['fecha_ultimo_testeo'], '%Y-%m-%d').date() if request.form.get('fecha_ultimo_testeo') else None
        enlace.observaciones = request.form.get('observaciones')
        
        db.session.commit()
        flash('Enlace actualizado exitosamente', 'success')
        return redirect(url_for('enlaces_detalle', id=id))
    
    ubicaciones = Ubicacion.query.filter_by(activo=True).all()
    switches = Switch.query.filter_by(estado='Activo').all()
    return render_template('enlaces_form.html', enlace=enlace, ubicaciones=ubicaciones, switches=switches)

@app.route('/enlaces/<int:id>/eliminar', methods=['POST'])
@login_required
def enlaces_eliminar(id):
    """Eliminar un enlace"""
    enlace = Enlace.query.get_or_404(id)
    db.session.delete(enlace)
    db.session.commit()
    flash('Enlace eliminado exitosamente', 'success')
    return redirect(url_for('enlaces'))

# ============================================================================
# PRIORIDAD 3: RUTAS VLAN - Gestión de Redes Virtuales
# ============================================================================

@app.route('/vlans')
@login_required
def vlans():
    """Listar todas las VLANs"""
    vlans = VLAN.query.all()
    return render_template('vlans_list.html', vlans=vlans)

@app.route('/vlans/nuevo', methods=['GET', 'POST'])
@login_required
def vlans_nuevo():
    """Crear nueva VLAN"""
    if request.method == 'POST':
        vlan = VLAN(
            vlan_id=int(request.form['vlan_id']),
            vlan_nombre=request.form['vlan_nombre'],
            vlan_descripcion=request.form.get('vlan_descripcion'),
            red=request.form.get('red'),
            mascara=request.form.get('mascara'),
            gateway=request.form.get('gateway'),
            switch_id=request.form.get('switch_id') or None,
            estado=request.form.get('estado', 'Activo'),
            fecha_creacion=datetime.strptime(request.form['fecha_creacion'], '%Y-%m-%d').date() if request.form.get('fecha_creacion') else None,
            observaciones=request.form.get('observaciones')
        )
        db.session.add(vlan)
        db.session.commit()
        flash('VLAN creada exitosamente', 'success')
        return redirect(url_for('vlans'))
    
    switches = Switch.query.filter_by(estado='Activo').all()
    return render_template('vlans_form.html', vlan=None, switches=switches)

@app.route('/vlans/<int:id>')
@login_required
def vlans_detalle(id):
    """Ver detalle de una VLAN"""
    vlan = VLAN.query.get_or_404(id)
    return render_template('vlans_detalle.html', vlan=vlan)

@app.route('/vlans/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def vlans_editar(id):
    """Editar una VLAN existente"""
    vlan = VLAN.query.get_or_404(id)
    
    if request.method == 'POST':
        vlan.vlan_id = int(request.form['vlan_id'])
        vlan.vlan_nombre = request.form['vlan_nombre']
        vlan.vlan_descripcion = request.form.get('vlan_descripcion')
        vlan.red = request.form.get('red')
        vlan.mascara = request.form.get('mascara')
        vlan.gateway = request.form.get('gateway')
        vlan.switch_id = request.form.get('switch_id') or None
        vlan.estado = request.form.get('estado', 'Activo')
        vlan.fecha_creacion = datetime.strptime(request.form['fecha_creacion'], '%Y-%m-%d').date() if request.form.get('fecha_creacion') else None
        vlan.observaciones = request.form.get('observaciones')
        
        db.session.commit()
        flash('VLAN actualizada exitosamente', 'success')
        return redirect(url_for('vlans_detalle', id=id))
    
    switches = Switch.query.filter_by(estado='Activo').all()
    return render_template('vlans_form.html', vlan=vlan, switches=switches)

@app.route('/vlans/<int:id>/eliminar', methods=['POST'])
@login_required
def vlans_eliminar(id):
    """Eliminar una VLAN"""
    vlan = VLAN.query.get_or_404(id)
    db.session.delete(vlan)
    db.session.commit()
    flash('VLAN eliminada exitosamente', 'success')
    return redirect(url_for('vlans'))

# ============================================================================
# DASHBOARD DE CONECTIVIDAD - Métricas de Enlaces
# ============================================================================

@app.route('/dashboard-conectividad')
@login_required
def dashboard_conectividad():
    """Dashboard con métricas de conectividad"""
    enlaces = Enlace.query.all()
    
    # Estadísticas
    total_enlaces = len(enlaces)
    enlaces_activos = sum(1 for e in enlaces if e.estado_conexion == 'Activo')
    enlaces_degradados = sum(1 for e in enlaces if e.estado_conexion == 'Degradado')
    enlaces_inactivos = sum(1 for e in enlaces if e.estado_conexion == 'Inactivo')
    
    # Promedios
    latencias = [e.latencia_ms for e in enlaces if e.latencia_ms]
    perdidas = [e.porcentaje_perdida_paquetes for e in enlaces if e.porcentaje_perdida_paquetes]
    
    latencia_promedio = sum(latencias) / len(latencias) if latencias else 0
    perdida_promedio = sum(perdidas) / len(perdidas) if perdidas else 0
    
    return render_template('dashboard_conectividad.html',
                         enlaces=enlaces,
                         total_enlaces=total_enlaces,
                         enlaces_activos=enlaces_activos,
                         enlaces_degradados=enlaces_degradados,
                         enlaces_inactivos=enlaces_inactivos,
                         latencia_promedio=round(latencia_promedio, 2),
                         perdida_promedio=round(perdida_promedio, 2))
