from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('new_log')
def handle_new_log(log_data):
    socketio.emit('new_log', log_data, namespace='/')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
