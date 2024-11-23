from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
import sys

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb+srv://carlossv3130:4VJd4yX8viAsDjqB@cluster0.w7fek.mongodb.net/crm_db?retryWrites=true&w=majority&appName=Cluster0"
mongo = PyMongo(app)

# Verificar conexión con MongoDB
try:
    mongo.cx.server_info()
    print("Conexión exitosa con MongoDB Atlas.")
except Exception as e:
    print(f"Error al conectar con MongoDB Atlas: {e}", file=sys.stderr)

# Ruta principal (Inicio)
@app.route('/')
def inicio():
    productos = mongo.db.products.find()
    clientes = mongo.db.clientes.find()
    nombre_tienda = "Tienda de Productos"
    return render_template('inicio.html', productos=productos, tienda=nombre_tienda, clientes=clientes)

# Agregar producto
@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        # Capturar los datos del formulario
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        cantidad = int(request.form['cantidad'])

        # Guardar el producto en la base de datos
        producto = {"nombre": nombre, "precio": precio, "cantidad": cantidad}
        mongo.db.products.insert_one(producto)

        # Redirigir a la página de inicio
        return redirect(url_for('inicio'))
    
    return render_template('agregar_producto.html')

# Registrar cliente
@app.route('/registrar_cliente', methods=['GET', 'POST'])
def registrar_cliente():
    if request.method == 'POST':
        # Capturar los datos del formulario
        nombre_cliente = request.form['nombre_cliente']
        documento_cliente = request.form['documento_cliente']

        # Guardar el cliente en la base de datos
        cliente = {"nombre_cliente": nombre_cliente, "documento_cliente": documento_cliente}
        mongo.db.clientes.insert_one(cliente)

        # Redirigir a la página de inicio
        return redirect(url_for('inicio'))
    
    return render_template('registrar_cliente.html')

# Eliminar producto
@app.route('/eliminar_producto/<producto_id>', methods=['POST'])
def eliminar_producto(producto_id):
    mongo.db.products.delete_one({'_id': ObjectId(producto_id)})
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True, port=3000)
