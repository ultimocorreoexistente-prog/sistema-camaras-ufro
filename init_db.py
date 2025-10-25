from app import app, db
from models import Usuario
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    print('Tablas creadas exitosamente')
    
    if Usuario.query.count() == 0:
        usuarios = [
            Usuario(email='charles.jelvez@ufro.cl', rol='superadmin', nombre='Charles Jélvez', activo=True),
            Usuario(email='admin@ufro.cl', rol='admin', nombre='Administrador', activo=True),
            Usuario(email='supervisor@ufro.cl', rol='supervisor', nombre='Supervisor', activo=True),
            Usuario(email='tecnico1@ufro.cl', rol='tecnico', nombre='Técnico 1', activo=True),
            Usuario(email='visualizador@ufro.cl', rol='visualizador', nombre='Visualizador', activo=True)
        ]
        
        passwords = ['charles123', 'admin123', 'super123', 'tecnico123', 'viz123']
        
        for user, password in zip(usuarios, passwords):
            user.set_password(password)
            db.session.add(user)
        
        db.session.commit()
        print('Usuarios creados exitosamente')
    else:
        print('Los usuarios ya existen')
    
    print(f'\nTotal usuarios: {Usuario.query.count()}')
