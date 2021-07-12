from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def inicio():
    return render_template('Login.html')
@app.route('/CrearCuenta')
def CrearCuenta():
    return render_template('CrearCuenta.html')
@app.route('/paginaPrincipal')
def PaginaPrincipal():
    return render_template('Index.html')
@app.route('/categorias/new')
def CrearCategoria():
    return render_template('Categorias.html')
@app.route('/productos/new')
def CrearProducto():
    return render_template('CrearProducto.html')

if __name__ == '__main__':
    app.run(debug=True)