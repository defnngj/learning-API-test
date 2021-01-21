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

cpu_thread = None
cpu_thread_lock = Lock()
menery_thread = None
menery_thread_lock = Lock()


@app.route('/')
def index():
    """
    Web页面
    """
    return render_template('index.html')


@socketio.on('connect', namespace='/get_cpu')
def cpu_connect():
    global cpu_thread
    with cpu_thread_lock:
        if cpu_thread is None:
            cpu_thread = socketio.start_background_task(target=cpu_background_thread)


def cpu_background_thread():
    count = 0
    while True:
        count += 1
        socketio.sleep(5)
        t = time.strftime('%H:%M:%S', time.localtime())
        cpu = psutil.cpu_percent(interval=None, percpu=True)
        print("t", t)
        print("cpu-->", t, cpu)
        socketio.emit('server_response',
                      {'data': [t, cpu], 'count': count}, namespace='/get_cpu')


@socketio.on('connect', namespace='/get_memory')
def memory_connect():
    global menery_thread
    with menery_thread_lock:
        if menery_thread is None:
            menery_thread = socketio.start_background_task(target=memory_background_thread)


def memory_background_thread():
    count = 0
    while True:
        count += 1
        socketio.sleep(5)
        t = time.strftime('%H:%M:%S', time.localtime())
        memory = psutil.virtual_memory()
        print("t", t)
        print("memory-->", t, memory)
        socketio.emit('server_response',
                      {'data': [t, memory], 'count': count}, namespace='/get_memory')


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=9090, debug=True)
