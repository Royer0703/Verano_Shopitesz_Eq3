from datetime import timedelta

from flask import Flask,render_template,request,redirect,url_for,flash,session,abort
from flask_bootstrap import Bootstrap
from modelo.Dao import db, Categoria, Producto, Usuario, Envios, Paqueterias
from flask_login import login_required,login_user,logout_user,current_user,LoginManager
app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://user_shopitesz:Shopit3sz.123@localhost/shopitesz'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='Cl4v3'
#Implementación de la gestion de usuarios con flask-login
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='mostrar_login'
login_manager.login_message='¡ Tu sesión expiró !'
login_manager.login_message_category="info"

# Urls defininas para el control de usuario
@app.before_request
def before_request():
    session.permanent=True
    app.permanent_session_lifetime=timedelta(minutes=10)

@app.route("/")
def inicio():
    return render_template('Index.html')

@app.route('/Usuarios/iniciarSesion')
def mostrar_login():
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return render_template('usuarios/Login.html')

@login_manager.user_loader
def cargar_usuario(id):
    return Usuario.query.get(int(id))

@app.route('/Usuarios/nuevo')
def nuevoUsuario():
    if current_user.is_authenticated and not current_user.is_admin():
        return render_template('principal.html')
    else:
        return render_template('usuarios/CrearCuenta.html')

@app.route('/Usuarios/agregar',methods=['post'])
def agregarUsuario():
    #try:
    usuario=Usuario()
    usuario.nombreCompleto=request.form['nombre']
    usuario.telefono=request.form['telefono']
    usuario.direccion=request.form['direccion']
    usuario.email=request.form['email']
    usuario.genero=request.form['genero']
    usuario.password=request.form['password']
    usuario.tipo=request.values.get("tipo","Comprador")
    usuario.estatus='Activo'
    usuario.agregar()
       # flash('¡ Usuario registrado con exito')
    #except:
       # flash('¡ Error al agregar al usuario !')
    return render_template('usuarios/CrearCuenta.html')


@app.route("/Usuarios/validarSesion",methods=['POST'])
def login():
    correo=request.form['correo']
    password=request.form['password']
    usuario=Usuario()
    user=usuario.validar(correo,password)
    if user!=None:
        login_user(user)
        return render_template('Index.html')
    else:
        flash('Nombre de usuario o contraseña incorrectos')
        return render_template('usuarios/Login.html')

@app.route('/Usuarios/cerrarSesion')
@login_required
def cerrarSesion():
    logout_user()
    return redirect(url_for('mostrar_login'))

@app.route('/Usuarios/verPerfil')
@login_required
def consultarUsuario():
    return render_template('usuarios/editar.html')
#fin del manejo de usuarios

#PRODUCTOS-------------------------------------
@app.route("/productos")
def consultarProductos():
    producto=Producto()
    return render_template("productos/consultaGeneral.html",productos=producto.consultaGeneral())
@app.route('/productos/<int:id>')
@login_required
def consultarProducto(id):
    if current_user.is_authenticated and current_user.is_admin():
        producto=Producto()
        return render_template('productos/editar.html',producto=producto.consultaIndividuall(id))
    else:
        return redirect(url_for('mostrar_login'))
@app.route('/productos/agregar',methods=['post'])
def agregarProductos():
    #try:
    producto=Producto()
    producto.idCategoria=request.form['categoria']
    producto.nombre=request.form['nombre']
    producto.descripcion=request.form['descripcion']
    producto.precioVenta=request.form['precio']
    producto.existencia=request.form['existencia']
    producto.foto=request.files['imagen'].stream.read()
    producto.especificaciones=request.files['archivo'].stream.read()
    producto.estatus='Activo'
    producto.agregar()
       # flash('¡ Usuario registrado con exito')
    #except:
       # flash('¡ Error al agregar al usuario !')
    return redirect(url_for('consultarProductos'))

@app.route('/productos/editar',methods=['POST'])
@login_required
def editarProducto():
    if current_user.is_authenticated and current_user.is_admin():

        producto = Producto()
        producto.idCategoria = request.form['categoria']
        producto.nombre = request.form['nombre']
        producto.descripcion = request.form['descripcion']
        producto.precioVenta = request.form['precio']
        producto.existencia = request.form['existencia']
        imagen = request.files['imagen'].stream.read()
        if imagen:
            producto.foto = imagen
        archivo = request.files['archivo'].stream.read()
        if archivo:
            producto.especificaciones = archivo
        producto.estatus = request.values.get("estatus","Inactiva")
        producto.editar()
        return redirect(url_for('consultarProductos'))

@app.route('/productos/eliminar/<int:id>')
@login_required
def eliminarProducto(id):
    if current_user.is_authenticated and current_user.is_admin():
        try:
            producto=Producto()
            producto.eliminacionLogica(id)
            flash('Producto eliminada con exito')
        except:
            flash('Error al eliminar la categoria')
        return redirect(url_for('consultarProductos'))
    else:
        return redirect(url_for('mostrar_login'))

@app.route("/productos/nuevo")
def agregarProducto():
    return render_template("productos/CrearProducto.html")

@app.route("/productos/actualizar")
def actualizarProducto():
    return "actualizando un producto"
@app.route("/cesta")
def consultarCesta():
    return "consultando la cesta de compra"

@app.route("/productos/categoria/<int:id>")
def consultarProductosCategoria(id):
    return "consultando los productos de la cetogoria: "+str(id)

@app.route("/clientes/<string:nombre>")
def consultarCliente(nombre):
    return "consultando al cliente:"+nombre

@app.route("/productos/<float:precio>")
def consultarPorductosPorPrecio(precio):
    return "Hola"+str(precio)

#CRUD de Categorias
@app.route('/Categorias')
def consultaCategorias():
    cat=Categoria()
    return render_template('categorias/consultaGeneral.html',categorias=cat.consultaGeneral())

@app.route('/Categorias/consultarImagen/<int:id>')
def consultarImagenCategoria(id):
    cat=Categoria()
    return cat.consultarImagen(id)


@app.route('/Categorias/nueva')
@login_required
def nuevaCategoria():
   # if current_user.is_authenticated and current_user.is_admin():
    return render_template('categorias/agregar.html')
    #else:
        #abort(404)

@app.route('/Categorias/agregar',methods=['post'])
@login_required
def agregarCategoria():
    try:
        if current_user.is_authenticated:
            if current_user.is_admin():
                try:
                    cat=Categoria()
                    cat.nombre=request.form['nombre']
                    cat.imagen=request.files['imagen'].stream.read()
                    cat.estatus='Activa'
                    cat.agregar()
                    flash('¡ Categoria agregada con exito !')
                except:
                    flash('¡ Error al agregar la categoria !')
                return redirect(url_for('consultaCategorias'))
            else:
                abort(404)

        else:
            return redirect(url_for('mostrar_login'))
    except:
        abort(500)

@app.route('/Categorias/<int:id>')
@login_required
def consultarCategoria(id):
    if current_user.is_authenticated and current_user.is_admin():
        cat=Categoria()
        return render_template('categorias/editar.html',cat=cat.consultaIndividuall(id))
    else:
        return redirect(url_for('mostrar_login'))


@app.route('/Categorias/editar',methods=['POST'])
@login_required
def editarCategoria():
    if current_user.is_authenticated and current_user.is_admin():
        try:
            cat=Categoria()
            cat.idCategoria=request.form['id']
            cat.nombre=request.form['nombre']
            imagen=request.files['imagen'].stream.read()
            if imagen:
                cat.imagen=imagen
            cat.estatus=request.values.get("estatus","Inactiva")
            cat.editar()
            flash('¡ Categoria editada con exito !')
        except:
            flash('¡ Error al editar la categoria !')

        return redirect(url_for('consultaCategorias'))
    else:
        return redirect(url_for('mostrar_login'))

@app.route('/Categorias/eliminar/<int:id>')
@login_required
def eliminarCategoria(id):
    if current_user.is_authenticated and current_user.is_admin():
        try:
            categoria=Categoria()
            #categoria.eliminar(id)
            categoria.eliminacionLogica(id)
            flash('Categoria eliminada con exito')
        except:
            flash('Error al eliminar la categoria')
        return redirect(url_for('consultaCategorias'))
    else:
        return redirect(url_for('mostrar_login'))

#Fin del crud de categorias


#Envios
@app.route('/envios')
def consultaEnvios():
    envio=Envios()
    return render_template('Envios/consultageneral.html', envios=envio.consultaGeneral())

@app.route('/envios/nuevo')
def agregarenvio():
    return render_template('/Envios/agregar.html')

@app.route('/envios/agregar',methods=['post'])
def agregarEnvio():

    envio = Envios()
    envio.IDPEDIDO = request.form['idpedido']
    envio.IDPAQUETERIA = request.form['idpaqueteria']
    envio.FECHAENVIO = request.form['fechaenvio']
    envio.FECHAENTREGA = request.form['fechaentrega']
    envio.NOGUIA = request.form['numeroguia']
    envio.PESOPAQUETE = request.form['pesopaquete']
    envio.PRECIOGR = request.form['precio']
    envio.TOTALAPAGAR = request.form['total']
    envio.ESTATUS = 'Activa'
    envio.agregar()
    return redirect(url_for('consultaEnvios'))

@app.route('/envios/<int:id>')
@login_required
def consultarEnvios(id):
    if current_user.is_authenticated and current_user.is_admin():
        envios=Envios()
        return render_template('Envios/editar.html',env=envios.consultaIndividuall(id))
    else:
        return redirect(url_for('mostrar_login'))



#PAQUETERIAS
@app.route('/paqueterias')
def consultaPaqueterias():
    paqueterias=Paqueterias()
    return render_template('paqueterias/consultageneral.html', paqueteria=paqueterias.consultaGeneral())


# manejo de pedidos
@app.route('/Pedidos')
@login_required
def consultarPedidos():
    return "Pedidos del usuario:"+current_user.nombreCompleto+", tipo:"+current_user.tipo

# fin del manejo de pedidos

#REDIRECCIONA A LA PAGINA PARA AGREGAR TARJETAS
@app.route('/usuarios/AltaTarjeta',methods=['post'])
def agregarTarjeta():
    try:
        tar=Tarjetas()
        tar.idUsuario = request.form['idUsuario']
        tar.noTarjeta = request.form['noTarjeta']
        tar.saldo = request.form['saldo']
        tar.banco = request.form['banco']
        tar.estatus = 'A'
        tar.agregar()
        flash('¡ Tarjeta agregada con exito !')
    except:
        flash('¡ Error al agregar la Tarjeta !')
    return redirect(url_for('consultaTarjetas'))

#REDIRECCIONA A LA PAGINA PARA CONSULTAR TARJETAS
@app.route('/usuarios/Tarjetas')
def consultaTarjetas():
    tar=Tarjetas()
    return render_template('Tarjetas/ConsultaTarjetas.html', Tarjetas = tar.consultaGeneral())

#REDIRECCIONA A LA PAGINA PARA EDITAR TARJETAS
@app.route('/usuarios/EditarTarjeta',methods=['POST'])
def editarTarjeta():
    try:
        tar=Tarjetas()
        tar.idTarjeta = request.form['idTarjeta']
        tar.idUsuario = request.form['idUsuario']
        tar.noTarjeta = request.form['noTarjeta']
        tar.saldo = request.form['saldo']
        tar.banco = request.form['banco']
        tar.estatus = request.values.get("estatus","Inactiva")
        tar.editar()
        flash('¡ Tarjeta editada con exito !')
    except:
        flash('¡ Error al editar la Tarjeta !')

    return redirect(url_for('consultaTarjetas'))

#ELIMINAR TARJETAS
@app.route('/tarjetas/eliminar/<int:id>')
def eliminarTarjeta(id):
    try:
        tar=Tarjetas()
        #tarjeta.eliminar(id)
        tar.eliminacionLogica(id)
        flash('Tarjeta eliminada con exito')
    except:
        flash('Error al eliminar la Tarjeta')
    return redirect(url_for('consultaTarjetas'))

#CONSULTAR TARJETA ESPECIFICA
@app.route('/Tarjetas/<int:id>')
def consultarTarjeta(id):
    tar = Tarjetas()
    ur = Usuario()
    return render_template('Tarjetas/EditarTarjeta.html', tar = tar.consultaIndividuall(id))

#manejo de errores
@app.errorhandler(404)
def error_404(e):
    return render_template('comunes/error_404.html'),404

@app.errorhandler(500)
def error_500(e):
    return render_template('comunes/error_500.html'),500
if __name__=='__main__':
    db.init_app(app)#Inicializar la BD - pasar la configuración de la url de la BD
    app.run(debug=True)

