from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

# Route für die Hauptseite
@app.route('/')
def index():
    return render_template('index.html')

# Funktion, um Nachrichten vom Kafka-Consumer zu empfangen
@socketio.on('new_log')
def handle_new_log(log_data):
    # Die empfangenen Log-Daten an die UI-Clients weiterleiten
    socketio.emit('new_log', log_data, namespace='/')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
