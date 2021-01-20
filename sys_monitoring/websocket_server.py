"""
实现前后端webSockets长连接。
"""
import time
import psutil
from random import randint
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit
from threading import Lock

app = Flask(__name__, template_folder='./')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')
thread = None
thread_lock = Lock()


@app.route('/')
def index():
    """
    Web页面
    """
    return render_template('index.html')


@socketio.on('connect', namespace='/test_conn')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


def background_thread():
    count = 0
    while True:
        count += 1
        socketio.sleep(5)
        t = time.strftime('%M:%S', time.localtime())
        cpus = psutil.cpu_percent(interval=None, percpu=True)
        print("t", t)
        print("cpu", cpus)
        socketio.emit('server_response',
                      {'data': [t, cpus], 'count': count}, namespace='/test_conn')




@socketio.on('client_event')
def client_msg(msg):
    print("啥情况", msg)
    emit('server_response', {'data': msg['data']})


@socketio.on('connect_event')
def connected_msg(msg):
    emit('server_response', {'data': msg['data']})


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=9090, debug=True)
