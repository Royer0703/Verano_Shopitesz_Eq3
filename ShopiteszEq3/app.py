from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def inicio():
    return render_template('/usuarios/Login.html')
@app.route('/CrearCuenta')
def CrearCuenta():
    return render_template('/usuarios/CrearCuenta.html')
@app.route('/paginaPrincipal')
def PaginaPrincipal():
    return render_template('Index.html')
@app.route('/categorias/new')
def CrearCategoria():
    return render_template('/categorias/Categorias.html')
@app.route('/productos/new')
def CrearProducto():
    return render_template('/productos/CrearProducto.html')
@app.route('/carrito')
def Carrito():
    return render_template('Carrito.html')
@app.route('/detallespedido')
def DetallesPedido():
    return render_template('/pedidos/DetallePedidos.html')
@app.route('/tarjetas')
def Tarjetas():
    return render_template('tarjetas.html')
@app.route('/pedidos')
def Pedidos():
    return render_template('/pedidos/pedido.html')

if __name__ == '__main__':
    app.run(debug=True)