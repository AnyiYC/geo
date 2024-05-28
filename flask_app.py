import os
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit

secret_key = os.urandom(24)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
socketio = SocketIO(app)

locations = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/locations')
def get_locations():
    return jsonify(locations), 200

@socketio.on('connect')
def handle_connect():
    emit('locations', locations)

@socketio.on('localizar')
def localizar_usuario(datos):
    nombre = datos.get('nombre')
    latitude = datos.get('latitude')
    longitude = datos.get('longitude')

    if nombre and latitude is not None and longitude is not None:
        location = {'name': nombre, 'latitude': latitude, 'longitude': longitude}
        locations.append(location)
        emit('new_location', location, broadcast=True)

if __name__ == '__main__':
    socketio.run(app,debug=True) #True
