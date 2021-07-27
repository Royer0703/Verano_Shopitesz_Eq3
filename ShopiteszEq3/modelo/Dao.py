from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,BLOB,ForeignKey,Float
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
db=SQLAlchemy()

class Categoria(db.Model):
    __tablename__='Categorias'
    idCategoria=Column(Integer,primary_key=True)
    nombre=Column(String,unique=True)
    estatus=Column(String,nullable=False)
    imagen=Column(BLOB)

    def consultaGeneral(self):
        return self.query.all()
        #return self.query.filter(Categoria.estatus=='Activa').all()

    def consultaIndividuall(self,id):
        return Categoria.query.get(id)

    def consultarImagen(self,id):
        return self.consultaIndividuall(id).imagen

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        cat=self.consultaIndividuall(id)
        db.session.delete(cat)
        db.session.commit()

    def eliminacionLogica(self,id):
        cat = self.consultaIndividuall(id)
        cat.estatus='Inactiva'
        cat.editar()

class Producto(db.Model):
    __tablename__='Productos'
    idProducto=Column(Integer,primary_key=True)
    idCategoria=Column(Integer,ForeignKey('Categorias.idCategoria'))
    nombre=Column(String,nullable=False)
    descripcion=Column(String,nullable=True)
    precioVenta=Column(Float,nullable=False)
    existencia=Column(Integer,nullable=False)
    foto=Column(BLOB)
    especificaciones=Column(BLOB)
    estatus=Column(String,nullable=False)
    categoria=relationship('Categoria',backref='productos',lazy='select')

    def consultaGeneral(self):
        return self.query.all()
    def consultaIndividuall(self,id):
        return Producto.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        Producto=self.consultaIndividuall(id)
        db.session.delete(Producto)
        db.session.commit()

    def eliminacionLogica(self,id):
        Producto = self.consultaIndividuall(id)
        Producto.estatus='Inactiva'
        Producto.editar()

class Usuario(UserMixin,db.Model):
    __tablename__='Usuarios'
    idUsuario=Column(Integer,primary_key=True)
    nombreCompleto=Column(String,nullable=False)
    direccion=Column(String,nullable=False)
    telefono=Column(String,nullable=False)
    email=Column(String,unique=True)
    password_hash=Column(String(128),nullable=False)
    tipo=Column(String,nullable=False)
    estatus=Column(String,nullable=False)
    genero=Column(String,nullable=False)

    def consultaGeneral(self):
        return self.query.all()
    def consultaIndividuall(self,id):
        return Usuario.query.get(id)


    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        Usuario=self.consultaIndividuall(id)
        db.session.delete(Usuario)
        db.session.commit()

    def eliminacionLogica(self,id):
        Usuario = self.consultaIndividuall(id)
        Usuario.estatus='Inactiva'
        Usuario.editar()

    @property #Implementa el metodo Get (para acceder a un valor)
    def password(self):
        raise AttributeError('El password no tiene acceso de lectura')

    @password.setter #Definir el metodo set para el atributo password_hash
    def password(self,password):#Se informa el password en formato plano para hacer el cifrado
        self.password_hash=generate_password_hash(password)

    def validarPassword(self,password):
        return check_password_hash(self.password_hash,password)
    #Definición de los métodos para el perfilamiento
    def is_authenticated(self):
        return True

    def is_active(self):
        if self.estatus=='Activo':
            return True
        else:
            return False
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.idUsuario

    def is_admin(self):
        if self.tipo=='Administrador':
            return True
        else:
            return False
    def is_vendedor(self):
        if self.tipo=='Vendedor':
            return True
        else:
            return False
    def is_comprador(self):
        if self.tipo=='Comprador':
            return True
        else:
            return False
    #Definir el método para la autenticacion
    def validar(self,email,password):
        usuario=Usuario.query.filter(Usuario.email==email).first()
        if usuario!=None and usuario.validarPassword(password) and usuario.is_active():
            return usuario
        else:
            return None
    #Método para agregar una cuenta de usuario
    def agregar(self):
        db.session.add(self)
        db.session.commit()



#ENVIOS
class Envios(UserMixin,db.Model):
    __tablename__='ENVIOS'
    IDENVIO=Column(Integer,primary_key=True)
    IDPEDIDO=Column(Integer,ForeignKey('Pedidos.idPedido'))
    IDPAQUETERIA=Column(Integer,ForeignKey('PAQUETERIAS.IDPAQUETERIA'))
    FECHAENVIO=Column(String,nullable=False)
    FECHAENTREGA=Column(String,nullable=True)
    NOGUIA=Column(Integer,nullable=False)
    PESOPAQUETE=Column(Integer,nullable=False)
    PRECIOGR=Column(Integer,nullable=False)
    TOTALPAGAR=Column(Integer,nullable=False)
    ESTATUS=Column(String,nullable=False)
    paqueteria = relationship('Paqueterias', backref='ENVIOS', lazy='select')
    pedidos = relationship('Pedidos', backref='ENVIOS', lazy='select')

    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividuall(self,id):
        return Envios.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        envios=self.consultaIndividuall(id)
        db.session.delete(envios)
        db.session.commit()

    def eliminacionLogica(self,id):
        envios = self.consultaIndividuall(id)
        envios.estatus='Inactiva'
        envios.editar()

#PAQUETERIAS
class Paqueterias(UserMixin,db.Model):
    __tablename__='PAQUETERIAS'
    IDPAQUETERIA=Column(Integer,primary_key=True)
    NOMBRE=Column(String,nullable=False)
    PAGINAWEB=Column(String,nullable=True)
    PRECIOGR=Column(Integer,nullable=False)
    TELEFONO=Column(String,nullable=False)
    ESTATUS=Column(String,nullable=False)

    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividuall(self,id):
        return Paqueterias.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        paqueteria=self.consultaIndividuall(id)
        db.session.delete(paqueteria)
        db.session.commit()

    def eliminacionLogica(self,id):
        paqueteria = self.consultaIndividuall(id)
        paqueteria.estatus='Inactiva'
        paqueteria.editar()

#PEDIDOS
class Pedidos(UserMixin,db.Model):
    __tablename__='Pedidos'
    idPedido=Column(Integer,primary_key=True)
    idComprador=Column(Integer,nullable=False)
    idVendedor=Column(Integer,nullable=False)
    idTarjeta=Column(Integer,nullable=False)
    fechaRegistro=Column(String,nullable=False)
    fechaAtencion=Column(String,nullable=True)
    fechaRecepcion=Column(String,nullable=False)
    fechaCierre=Column(String,nullable=False)
    total=Column(Integer,nullable=False)
    estatus=Column(String,nullable=False)

    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividuall(self,id):
        return Pedidos.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        pedidos=self.consultaIndividuall(id)
        db.session.delete(pedidos)
        db.session.commit()

    def eliminacionLogica(self,id):
        pedidos = self.consultaIndividuall(id)
        pedidos.estatus='Inactiva'
        pedidos.editar()


#TARJETAS---------------------
#TABLA DE TARJETAS
class Tarjetas(db.Model):
    _tablename_='Tarjetas'
    idTarjeta = Column( Integer, primary_key = True )
    idUsuario = Column( Integer,ForeignKey('Usuarios.idUsuario') )
    noTarjeta = Column( String, unique = True )
    saldo = Column( String, nullable = False )
    banco = Column( String, nullable = False )
    estatus = Column( String, nullable = False )

    def consultaGeneral(self):
        return self.query.all()
        #return self.query.filter(Tarjetas.estatus=='Activa').all()

    def consultaIndividuall(self,id):
        return Tarjetas.query.get(id)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        tar=self.consultaIndividuall(id)
        db.session.delete(tar)
        db.session.commit()

    def eliminacionLogica(self,id):
        tar = self.consultaIndividuall(id)
        tar.estatus='Inactiva'
        tar.editar()

