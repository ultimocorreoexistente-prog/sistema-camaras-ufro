#!/usr/bin/env python3
import os
import psycopg2
from psycopg2.extras import RealDictCursor

# URL externa de Railway
DATABASE_URL = 'postgresql://postgres:WMQxvzTQsdkiAUOqfMgXmzgAHqxDkwRJ@tramway.proxy.rlwy.net:34726/railway'

try:
    print('🔗 Conectando a Railway PostgreSQL...')
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    
    print('✅ Conexión establecida')
    
    # Truncar tabla
    print('🧹 Truncando tabla usuario...')
    cursor.execute('TRUNCATE TABLE usuario RESTART IDENTITY CASCADE;')
    conn.commit()
    print('✅ Tabla truncada')
    
    # Insertar usuarios con correos @ufrontera.cl
    usuarios = [
        ('charles.jelvez', 'pbkdf2:sha256:1000000$7d6451a5d0ffff3352524132761f2024$75d1a09870f58e7bca3701574b065345da26bd6c49a0ea3b2b5f925ac4fe521f', 'superadmin', 'Charles Jélvez', 'charles.jelvez@ufrontera.cl', True),
        ('admin', 'pbkdf2:sha256:1000000$84dd50328b5686e330934dc62963303a$462b026a7a49a85cd3551934a3177895c172e9987a5391ab5c99740885ed7a21', 'admin', 'Administrador Principal', 'admin@ufrontera.cl', True),
        ('supervisor', 'pbkdf2:sha256:1000000$c27c81b541d3a1dcb4688ee40c2c6bff$fb3d7cf30a77425be1468e849c8241248121b5fcd56f809501afe4505ee2f9e0', 'supervisor', 'Supervisor General', 'supervisor@ufrontera.cl', True),
        ('tecnico1', 'pbkdf2:sha256:1000000$74b68275edf4c5b327111d74c5efbe31$db4486b0844ce6df4750bf5c966c3309b25f47d035da6cf3f035da57af65607d', 'tecnico', 'Técnico Principal', 'tecnico@ufrontera.cl', True),
        ('visualizador', 'pbkdf2:sha256:1000000$e3c67d501499dda6b44431b2c3992f0a$e62efa69faa8174c8c76657c30e48bb34013a08c4f8631a51b9505e749c3b873', 'visualizador', 'Visualizador', 'visualizador@ufrontera.cl', True)
    ]
    
    print('👥 Insertando usuarios...')
    for username, password_hash, rol, nombre, email, activo in usuarios:
        cursor.execute(
            'INSERT INTO usuario (username, password_hash, rol, nombre_completo, email, activo, fecha_creacion) VALUES (%s, %s, %s, %s, %s, %s, NOW())',
            (username, password_hash, rol, nombre, email, activo)
        )
        print(f'✅ {username} ({rol}) - {email}')
    
    conn.commit()
    
    # Verificar usuarios creados
    cursor.execute('SELECT username, rol, nombre_completo, email FROM usuario ORDER BY rol, username')
    usuarios_db = cursor.fetchall()
    
    print(f'\n📊 Total usuarios creados: {len(usuarios_db)}')
    print('='*60)
    for u in usuarios_db:
        print(f'👤 {u["username"]} ({u["rol"]}) - {u["nombre_completo"]} - {u["email"]}')
    
    # Verificar Charles específicamente
    cursor.execute('SELECT * FROM usuario WHERE username = %s', ('charles.jelvez',))
    charles = cursor.fetchone()
    if charles:
        print(f'\n🎯 CHARLES JÉLVEZ VERIFICADO:')
        print(f'   Username: {charles["username"]}')
        print(f'   Rol: {charles["rol"]}')
        print(f'   Email: {charles["email"]}')
        print(f'   Hash: {charles["password_hash"][:50]}...')
        print('   ✅ LISTO PARA LOGIN')
    else:
        print('❌ Charles no encontrado')
    
    cursor.close()
    conn.close()
    print('\n🎉 SQL EJECUTADO EXITOSAMENTE')
    
except Exception as e:
    print(f'❌ ERROR: {e}')
    import traceback
    traceback.print_exc()