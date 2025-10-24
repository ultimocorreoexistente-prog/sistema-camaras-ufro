# RUTAS CRUD ADICIONALES PARA INTEGRAR EN APP.PY
# Este archivo contiene todas las rutas para las entidades faltantes

# ========== SWITCHES ==========
@app.route('/switches')
@login_required
def switches_list():
    campus = request.args.get('campus', '')
    estado = request.args.get('estado', '')
    busqueda = request.args.get('busqueda', '')
    
    query = Switch.query.join(Gabinete).join(Ubicacion)
    
    if campus:
        query = query.filter(Ubicacion.campus == campus)
    if estado:
        query = query.filter(Switch.estado == estado)
    if busqueda:
        query = query.filter(or_(
            Switch.codigo.like(f'%{busqueda}%'),
            Switch.nombre.like(f'%{busqueda}%'),
            Switch.ip.like(f'%{busqueda}%')
        ))
    
    switches = query.all()
    campus_list = db.session.query(Ubicacion.campus).distinct().all()
    
    return render_template('switches_list.html', 
                         switches=switches,
                         campus_list=[c[0] for c in campus_list])

@app.route('/switches/nuevo', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'supervisor')
def switches_nuevo():
    if request.method == 'POST':
        switch = Switch(
            codigo=request.form.get('codigo'),
            nombre=request.form.get('nombre'),
            ip=request.form.get('ip'),
            modelo=request.form.get('modelo'),
            marca=request.form.get('marca'),
            numero_serie=request.form.get('numero_serie'),
            gabinete_id=request.form.get('gabinete_id') or None,
            puertos_totales=int(request.form.get('puertos_totales', 0)),
            puertos_usados=int(request.form.get('puertos_usados', 0)),
            puertos_disponibles=int(request.form.get('puertos_disponibles', 0)),
            capacidad_poe=request.form.get('capacidad_poe') == 'on',
            estado=request.form.get('estado', 'Activo'),
            fecha_alta=datetime.strptime(request.form.get('fecha_alta'), '%Y-%m-%d').date() if request.form.get('fecha_alta') else None,
            latitud=float(request.form.get('latitud')) if request.form.get('latitud') else None,
            longitud=float(request.form.get('longitud')) if request.form.get('longitud') else None,
            observaciones=request.form.get('observaciones')
        )
        db.session.add(switch)
        db.session.commit()
        flash('Switch creado exitosamente', 'success')
        return redirect(url_for('switches_list'))
    
    gabinetes = Gabinete.query.filter_by(estado='Activo').all()
    return render_template('switches_form.html', gabinetes=gabinetes, switch=None)

@app.route('/switches/<int:id>')
@login_required
def switches_detalle(id):
    switch = Switch.query.get_or_404(id)
    puertos = Puerto_Switch.query.filter_by(switch_id=id).all()
    camaras = Camara.query.filter_by(switch_id=id).all()
    return render_template('switches_detalle.html', 
                         switch=switch,
                         puertos=puertos,
                         camaras=camaras)

@app.route('/switches/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'supervisor')
def switches_editar(id):
    switch = Switch.query.get_or_404(id)
    
    if request.method == 'POST':
        switch.codigo = request.form.get('codigo')
        switch.nombre = request.form.get('nombre')
        switch.ip = request.form.get('ip')
        switch.modelo = request.form.get('modelo')
        switch.marca = request.form.get('marca')
        switch.numero_serie = request.form.get('numero_serie')
        switch.gabinete_id = request.form.get('gabinete_id') or None
        switch.puertos_totales = int(request.form.get('puertos_totales', 0))
        switch.puertos_usados = int(request.form.get('puertos_usados', 0))
        switch.puertos_disponibles = int(request.form.get('puertos_disponibles', 0))
        switch.capacidad_poe = request.form.get('capacidad_poe') == 'on'
        switch.estado = request.form.get('estado')
        switch.latitud = float(request.form.get('latitud')) if request.form.get('latitud') else None
        switch.longitud = float(request.form.get('longitud')) if request.form.get('longitud') else None
        switch.observaciones = request.form.get('observaciones')
        
        db.session.commit()
        flash('Switch actualizado exitosamente', 'success')
        return redirect(url_for('switches_detalle', id=id))
    
    gabinetes = Gabinete.query.filter_by(estado='Activo').all()
    return render_template('switches_form.html', switch=switch, gabinetes=gabinetes)

@app.route('/switches/<int:id>/eliminar', methods=['POST'])
@login_required
@role_required('superadmin', 'admin')
def switches_eliminar(id):
    switch = Switch.query.get_or_404(id)
    db.session.delete(switch)
    db.session.commit()
    flash('Switch eliminado exitosamente', 'success')
    return redirect(url_for('switches_list'))

# ========== NVR/DVR ==========
@app.route('/nvr')
@login_required
def nvr_list():
    campus = request.args.get('campus', '')
    estado = request.args.get('estado', '')
    tipo = request.args.get('tipo', '')
    
    query = NVR_DVR.query
    
    if campus and NVR_DVR.ubicacion_id:
        query = query.join(Ubicacion).filter(Ubicacion.campus == campus)
    if estado:
        query = query.filter(NVR_DVR.estado == estado)
    if tipo:
        query = query.filter(NVR_DVR.tipo == tipo)
    
    nvrs = query.all()
    campus_list = db.session.query(Ubicacion.campus).distinct().all()
    
    return render_template('nvr_list.html', 
                         nvrs=nvrs,
                         campus_list=[c[0] for c in campus_list])

@app.route('/nvr/nuevo', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'supervisor')
def nvr_nuevo():
    if request.method == 'POST':
        nvr = NVR_DVR(
            codigo=request.form.get('codigo'),
            tipo=request.form.get('tipo'),
            modelo=request.form.get('modelo'),
            marca=request.form.get('marca'),
            canales_totales=int(request.form.get('canales_totales', 0)),
            canales_usados=int(request.form.get('canales_usados', 0)),
            ip=request.form.get('ip'),
            ubicacion_id=request.form.get('ubicacion_id') or None,
            gabinete_id=request.form.get('gabinete_id') or None,
            estado=request.form.get('estado', 'Activo'),
            fecha_alta=datetime.strptime(request.form.get('fecha_alta'), '%Y-%m-%d').date() if request.form.get('fecha_alta') else None,
            latitud=float(request.form.get('latitud')) if request.form.get('latitud') else None,
            longitud=float(request.form.get('longitud')) if request.form.get('longitud') else None,
            observaciones=request.form.get('observaciones')
        )
        db.session.add(nvr)
        db.session.commit()
        flash('NVR/DVR creado exitosamente', 'success')
        return redirect(url_for('nvr_list'))
    
    ubicaciones = Ubicacion.query.filter_by(activo=True).all()
    gabinetes = Gabinete.query.filter_by(estado='Activo').all()
    return render_template('nvr_form.html', ubicaciones=ubicaciones, gabinetes=gabinetes, nvr=None)

@app.route('/nvr/<int:id>')
@login_required
def nvr_detalle(id):
    nvr = NVR_DVR.query.get_or_404(id)
    camaras = Camara.query.filter_by(nvr_id=id).all()
    return render_template('nvr_detalle.html', nvr=nvr, camaras=camaras)

@app.route('/nvr/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'supervisor')
def nvr_editar(id):
    nvr = NVR_DVR.query.get_or_404(id)
    
    if request.method == 'POST':
        nvr.codigo = request.form.get('codigo')
        nvr.tipo = request.form.get('tipo')
        nvr.modelo = request.form.get('modelo')
        nvr.marca = request.form.get('marca')
        nvr.canales_totales = int(request.form.get('canales_totales', 0))
        nvr.canales_usados = int(request.form.get('canales_usados', 0))
        nvr.ip = request.form.get('ip')
        nvr.ubicacion_id = request.form.get('ubicacion_id') or None
        nvr.gabinete_id = request.form.get('gabinete_id') or None
        nvr.estado = request.form.get('estado')
        nvr.latitud = float(request.form.get('latitud')) if request.form.get('latitud') else None
        nvr.longitud = float(request.form.get('longitud')) if request.form.get('longitud') else None
        nvr.observaciones = request.form.get('observaciones')
        
        db.session.commit()
        flash('NVR/DVR actualizado exitosamente', 'success')
        return redirect(url_for('nvr_detalle', id=id))
    
    ubicaciones = Ubicacion.query.filter_by(activo=True).all()
    gabinetes = Gabinete.query.filter_by(estado='Activo').all()
    return render_template('nvr_form.html', nvr=nvr, ubicaciones=ubicaciones, gabinetes=gabinetes)

@app.route('/nvr/<int:id>/eliminar', methods=['POST'])
@login_required
@role_required('superadmin', 'admin')
def nvr_eliminar(id):
    nvr = NVR_DVR.query.get_or_404(id)
    db.session.delete(nvr)
    db.session.commit()
    flash('NVR/DVR eliminado exitosamente', 'success')
    return redirect(url_for('nvr_list'))

# ========== UPS ==========
@app.route('/ups')
@login_required
def ups_list():
    campus = request.args.get('campus', '')
    estado = request.args.get('estado', '')
    
    query = UPS.query
    
    if campus and UPS.ubicacion_id:
        query = query.join(Ubicacion).filter(Ubicacion.campus == campus)
    if estado:
        query = query.filter(UPS.estado == estado)
    
    ups_list = query.all()
    campus_list = db.session.query(Ubicacion.campus).distinct().all()
    
    return render_template('ups_list.html', 
                         ups_list=ups_list,
                         campus_list=[c[0] for c in campus_list])

@app.route('/ups/nuevo', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'supervisor')
def ups_nuevo():
    if request.method == 'POST':
        ups = UPS(
            codigo=request.form.get('codigo'),
            modelo=request.form.get('modelo'),
            marca=request.form.get('marca'),
            capacidad_va=int(request.form.get('capacidad_va', 0)),
            numero_baterias=int(request.form.get('numero_baterias', 0)),
            ubicacion_id=request.form.get('ubicacion_id') or None,
            gabinete_id=request.form.get('gabinete_id') or None,
            equipos_que_alimenta=request.form.get('equipos_que_alimenta'),
            estado=request.form.get('estado', 'Activo'),
            fecha_alta=datetime.strptime(request.form.get('fecha_alta'), '%Y-%m-%d').date() if request.form.get('fecha_alta') else None,
            fecha_instalacion=datetime.strptime(request.form.get('fecha_instalacion'), '%Y-%m-%d').date() if request.form.get('fecha_instalacion') else None,
            latitud=float(request.form.get('latitud')) if request.form.get('latitud') else None,
            longitud=float(request.form.get('longitud')) if request.form.get('longitud') else None,
            observaciones=request.form.get('observaciones')
        )
        db.session.add(ups)
        db.session.commit()
        flash('UPS creado exitosamente', 'success')
        return redirect(url_for('ups_list'))
    
    ubicaciones = Ubicacion.query.filter_by(activo=True).all()
    gabinetes = Gabinete.query.filter_by(estado='Activo').all()
    return render_template('ups_form.html', ubicaciones=ubicaciones, gabinetes=gabinetes, ups=None)

@app.route('/ups/<int:id>')
@login_required
def ups_detalle(id):
    ups = UPS.query.get_or_404(id)
    mantenimientos = Mantenimiento.query.filter_by(equipo_tipo='UPS', equipo_id=id).order_by(Mantenimiento.fecha.desc()).all()
    return render_template('ups_detalle.html', ups=ups, mantenimientos=mantenimientos)

@app.route('/ups/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'supervisor')
def ups_editar(id):
    ups = UPS.query.get_or_404(id)
    
    if request.method == 'POST':
        ups.codigo = request.form.get('codigo')
        ups.modelo = request.form.get('modelo')
        ups.marca = request.form.get('marca')
        ups.capacidad_va = int(request.form.get('capacidad_va', 0))
        ups.numero_baterias = int(request.form.get('numero_baterias', 0))
        ups.ubicacion_id = request.form.get('ubicacion_id') or None
        ups.gabinete_id = request.form.get('gabinete_id') or None
        ups.equipos_que_alimenta = request.form.get('equipos_que_alimenta')
        ups.estado = request.form.get('estado')
        ups.latitud = float(request.form.get('latitud')) if request.form.get('latitud') else None
        ups.longitud = float(request.form.get('longitud')) if request.form.get('longitud') else None
        ups.observaciones = request.form.get('observaciones')
        
        db.session.commit()
        flash('UPS actualizado exitosamente', 'success')
        return redirect(url_for('ups_detalle', id=id))
    
    ubicaciones = Ubicacion.query.filter_by(activo=True).all()
    gabinetes = Gabinete.query.filter_by(estado='Activo').all()
    return render_template('ups_form.html', ups=ups, ubicaciones=ubicaciones, gabinetes=gabinetes)

@app.route('/ups/<int:id>/eliminar', methods=['POST'])
@login_required
@role_required('superadmin', 'admin')
def ups_eliminar(id):
    ups = UPS.query.get_or_404(id)
    db.session.delete(ups)
    db.session.commit()
    flash('UPS eliminado exitosamente', 'success')
    return redirect(url_for('ups_list'))

# ========== FUENTES DE PODER ==========
@app.route('/fuentes')
@login_required
def fuentes_list():
    campus = request.args.get('campus', '')
    estado = request.args.get('estado', '')
    
    query = Fuente_Poder.query
    
    if campus and Fuente_Poder.ubicacion_id:
        query = query.join(Ubicacion).filter(Ubicacion.campus == campus)
    if estado:
        query = query.filter(Fuente_Poder.estado == estado)
    
    fuentes = query.all()
    campus_list = db.session.query(Ubicacion.campus).distinct().all()
    
    return render_template('fuentes_list.html', 
                         fuentes=fuentes,
                         campus_list=[c[0] for c in campus_list])

@app.route('/fuentes/nuevo', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'supervisor')
def fuentes_nuevo():
    if request.method == 'POST':
        fuente = Fuente_Poder(
            codigo=request.form.get('codigo'),
            modelo=request.form.get('modelo'),
            voltaje=request.form.get('voltaje'),
            amperaje=request.form.get('amperaje'),
            equipos_que_alimenta=request.form.get('equipos_que_alimenta'),
            ubicacion_id=request.form.get('ubicacion_id') or None,
            gabinete_id=request.form.get('gabinete_id') or None,
            estado=request.form.get('estado', 'Activo'),
            fecha_alta=datetime.strptime(request.form.get('fecha_alta'), '%Y-%m-%d').date() if request.form.get('fecha_alta') else None,
            observaciones=request.form.get('observaciones')
        )
        db.session.add(fuente)
        db.session.commit()
        flash('Fuente de poder creada exitosamente', 'success')
        return redirect(url_for('fuentes_list'))
    
    ubicaciones = Ubicacion.query.filter_by(activo=True).all()
    gabinetes = Gabinete.query.filter_by(estado='Activo').all()
    return render_template('fuentes_form.html', ubicaciones=ubicaciones, gabinetes=gabinetes, fuente=None)

@app.route('/fuentes/<int:id>')
@login_required
def fuentes_detalle(id):
    fuente = Fuente_Poder.query.get_or_404(id)
    return render_template('fuentes_detalle.html', fuente=fuente)

@app.route('/fuentes/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'supervisor')
def fuentes_editar(id):
    fuente = Fuente_Poder.query.get_or_404(id)
    
    if request.method == 'POST':
        fuente.codigo = request.form.get('codigo')
        fuente.modelo = request.form.get('modelo')
        fuente.voltaje = request.form.get('voltaje')
        fuente.amperaje = request.form.get('amperaje')
        fuente.equipos_que_alimenta = request.form.get('equipos_que_alimenta')
        fuente.ubicacion_id = request.form.get('ubicacion_id') or None
        fuente.gabinete_id = request.form.get('gabinete_id') or None
        fuente.estado = request.form.get('estado')
        fuente.observaciones = request.form.get('observaciones')
        
        db.session.commit()
        flash('Fuente de poder actualizada exitosamente', 'success')
        return redirect(url_for('fuentes_detalle', id=id))
    
    ubicaciones = Ubicacion.query.filter_by(activo=True).all()
    gabinetes = Gabinete.query.filter_by(estado='Activo').all()
    return render_template('fuentes_form.html', fuente=fuente, ubicaciones=ubicaciones, gabinetes=gabinetes)

@app.route('/fuentes/<int:id>/eliminar', methods=['POST'])
@login_required
@role_required('superadmin', 'admin')
def fuentes_eliminar(id):
    fuente = Fuente_Poder.query.get_or_404(id)
    db.session.delete(fuente)
    db.session.commit()
    flash('Fuente de poder eliminada exitosamente', 'success')
    return redirect(url_for('fuentes_list'))

# ========== PUERTOS SWITCH ==========
@app.route('/puertos')
@login_required
def puertos_list():
    switch_id = request.args.get('switch_id', '')
    estado = request.args.get('estado', '')
    
    query = Puerto_Switch.query
    
    if switch_id:
        query = query.filter(Puerto_Switch.switch_id == switch_id)
    if estado:
        query = query.filter(Puerto_Switch.estado == estado)
    
    puertos = query.all()
    switches = Switch.query.filter_by(estado='Activo').all()
    
    return render_template('puertos_list.html', 
                         puertos=puertos,
                         switches=switches)

@app.route('/puertos/nuevo', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'supervisor', 'tecnico')
def puertos_nuevo():
    if request.method == 'POST':
        puerto = Puerto_Switch(
            switch_id=request.form.get('switch_id'),
            numero_puerto=int(request.form.get('numero_puerto')),
            camara_id=request.form.get('camara_id') or None,
            ip_dispositivo=request.form.get('ip_dispositivo'),
            estado=request.form.get('estado', 'Disponible'),
            tipo_conexion=request.form.get('tipo_conexion'),
            nvr_id=request.form.get('nvr_id') or None,
            puerto_nvr=request.form.get('puerto_nvr')
        )
        db.session.add(puerto)
        db.session.commit()
        flash('Puerto creado exitosamente', 'success')
        return redirect(url_for('puertos_list'))
    
    switches = Switch.query.filter_by(estado='Activo').all()
    camaras = Camara.query.filter_by(estado='Activo').all()
    nvrs = NVR_DVR.query.filter_by(estado='Activo').all()
    return render_template('puertos_form.html', switches=switches, camaras=camaras, nvrs=nvrs, puerto=None)

@app.route('/puertos/<int:id>')
@login_required
def puertos_detalle(id):
    puerto = Puerto_Switch.query.get_or_404(id)
    return render_template('puertos_detalle.html', puerto=puerto)

@app.route('/puertos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'supervisor', 'tecnico')
def puertos_editar(id):
    puerto = Puerto_Switch.query.get_or_404(id)
    
    if request.method == 'POST':
        puerto.switch_id = request.form.get('switch_id')
        puerto.numero_puerto = int(request.form.get('numero_puerto'))
        puerto.camara_id = request.form.get('camara_id') or None
        puerto.ip_dispositivo = request.form.get('ip_dispositivo')
        puerto.estado = request.form.get('estado')
        puerto.tipo_conexion = request.form.get('tipo_conexion')
        puerto.nvr_id = request.form.get('nvr_id') or None
        puerto.puerto_nvr = request.form.get('puerto_nvr')
        
        db.session.commit()
        flash('Puerto actualizado exitosamente', 'success')
        return redirect(url_for('puertos_detalle', id=id))
    
    switches = Switch.query.filter_by(estado='Activo').all()
    camaras = Camara.query.filter_by(estado='Activo').all()
    nvrs = NVR_DVR.query.filter_by(estado='Activo').all()
    return render_template('puertos_form.html', puerto=puerto, switches=switches, camaras=camaras, nvrs=nvrs)

@app.route('/puertos/<int:id>/eliminar', methods=['POST'])
@login_required
@role_required('superadmin', 'admin')
def puertos_eliminar(id):
    puerto = Puerto_Switch.query.get_or_404(id)
    db.session.delete(puerto)
    db.session.commit()
    flash('Puerto eliminado exitosamente', 'success')
    return redirect(url_for('puertos_list'))

# ========== EQUIPOS TECNICOS ==========
@app.route('/tecnicos')
@login_required
def tecnicos_list():
    especialidad = request.args.get('especialidad', '')
    estado = request.args.get('estado', '')
    
    query = Equipo_Tecnico.query
    
    if especialidad:
        query = query.filter(Equipo_Tecnico.especialidad == especialidad)
    if estado:
        query = query.filter(Equipo_Tecnico.estado == estado)
    
    tecnicos = query.all()
    especialidades = db.session.query(Equipo_Tecnico.especialidad).distinct().all()
    
    return render_template('tecnicos_list.html', 
                         tecnicos=tecnicos,
                         especialidades=[e[0] for e in especialidades if e[0]])

@app.route('/tecnicos/nuevo', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'supervisor')
def tecnicos_nuevo():
    if request.method == 'POST':
        tecnico = Equipo_Tecnico(
            nombre=request.form.get('nombre'),
            apellido=request.form.get('apellido'),
            especialidad=request.form.get('especialidad'),
            telefono=request.form.get('telefono'),
            email=request.form.get('email'),
            estado=request.form.get('estado', 'Activo'),
            fecha_ingreso=datetime.strptime(request.form.get('fecha_ingreso'), '%Y-%m-%d').date() if request.form.get('fecha_ingreso') else None
        )
        db.session.add(tecnico)
        db.session.commit()
        flash('Técnico creado exitosamente', 'success')
        return redirect(url_for('tecnicos_list'))
    
    return render_template('tecnicos_form.html', tecnico=None)

@app.route('/tecnicos/<int:id>')
@login_required
def tecnicos_detalle(id):
    tecnico = Equipo_Tecnico.query.get_or_404(id)
    fallas_asignadas = Falla.query.filter_by(tecnico_asignado_id=id).order_by(Falla.fecha_reporte.desc()).all()
    mantenimientos = Mantenimiento.query.filter_by(tecnico_id=id).order_by(Mantenimiento.fecha.desc()).all()
    return render_template('tecnicos_detalle.html', 
                         tecnico=tecnico,
                         fallas_asignadas=fallas_asignadas,
                         mantenimientos=mantenimientos)

@app.route('/tecnicos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'supervisor')
def tecnicos_editar(id):
    tecnico = Equipo_Tecnico.query.get_or_404(id)
    
    if request.method == 'POST':
        tecnico.nombre = request.form.get('nombre')
        tecnico.apellido = request.form.get('apellido')
        tecnico.especialidad = request.form.get('especialidad')
        tecnico.telefono = request.form.get('telefono')
        tecnico.email = request.form.get('email')
        tecnico.estado = request.form.get('estado')
        
        db.session.commit()
        flash('Técnico actualizado exitosamente', 'success')
        return redirect(url_for('tecnicos_detalle', id=id))
    
    return render_template('tecnicos_form.html', tecnico=tecnico)

@app.route('/tecnicos/<int:id>/eliminar', methods=['POST'])
@login_required
@role_required('superadmin', 'admin')
def tecnicos_eliminar(id):
    tecnico = Equipo_Tecnico.query.get_or_404(id)
    db.session.delete(tecnico)
    db.session.commit()
    flash('Técnico eliminado exitosamente', 'success')
    return redirect(url_for('tecnicos_list'))
