from flask import Flask, render_template, request, jsonify, redirect, url_for
import database as db
from product import Producto

# Instancia principal de la aplicación Flask
app = Flask(__name__)

# Conexión con la base de datos MongoDB
db = db.dbConnection()

# 1. Ruta Principal (Lectura / GET): Obtiene los productos y carga la plantilla index.html
@app.route('/')
def home():
    products = db['products']
    products_received = products.find()
    return render_template('index.html', products=products_received)

# 2. Ruta para Agregar (Crear / POST): Recibe los datos del formulario e inserta un nuevo documento
@app.route('/products', methods=['POST'])
def addProduct():
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']

    if name and price and quantity:
        product = Producto(name, price, quantity)
        products.insert_one(product.toDBCollection())
        response = jsonify({
            'name': name,
            'price': price,
            'quantity': quantity
        })
        return redirect(url_for('home'))
    else:
        return notFound()

# 3. Ruta para Eliminar (Borrar / GET): Elimina un producto por su nombre
@app.route('/delete/<string:product_name>')
def delete(product_name):
    products = db['products']
    products.delete_one({'name': product_name})
    return redirect(url_for('home'))

# 4. Ruta para Editar (Actualizar / POST): Actualiza los datos de un producto existente
@app.route('/edit/<string:product_name>', methods=['POST'])
def edit(product_name):
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']

    if name and price and quantity:
        products.update_one({'name': product_name}, {'$set': {'name': name, 'price': price, 'quantity': quantity}})
        response = jsonify({'message': 'Producto ' + product_name + ' actualizado correctamente'})
        return redirect(url_for('home'))
    else:
        return notFound()

# Manejador de errores para rutas o datos no encontrados (404)
@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'No encontrado ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

# Inicio del servidor en modo depuración (puerto 4000)
if __name__ == '__main__':
    app.run(debug=True, port=4000)
