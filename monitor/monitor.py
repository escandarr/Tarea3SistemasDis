from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

contador_eventos = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evento', methods=['POST'])
def recibir_evento():
    global contador_eventos
    contador_eventos += 1
    socketio.emit('nuevo_evento', {'contador': contador_eventos})
    return '', 204

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)