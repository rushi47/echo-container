from flask import Flask, request
import subprocess
import time
import os
import threading
import socket
app = Flask(__name__)

ready = True


def get_app_in_rotation():
    '''
    Will make readiness probe success after 220 seconds automatically if not SLEEP TIME
    '''
    time_sleep = os.getenv('ECHO_SLEEP_TIME', 220)
    global ready
    while True:
        if not ready:
            time.sleep(int(time_sleep))
            ready = True
            

@app.route('/')
@app.route('/health')
@app.route('/lprobe')
@app.route('/liveness_probe')
def hello():
    global ready
    
    if ready:
        return f"Hello World! : {socket.gethostname()}", 200

    return f"Failing Health as set in maintainance : {ready}", 503

@app.route('/ip')    
@app.route('/getip')
def hello_name():
    status, output = subprocess.getstatusoutput('hostname -I')
    return output, 200

@app.route('/rprobe')
@app.route('/rediness_probe')
def rediness_probe():
    if ready:
        return 'ok', 200
    else:
        return f'readiness probe failing : {ready}', 503

@app.route('/setm')
@app.route('/set_maintenance')
def set_maintenance():
    '''
    will fail rediness
    '''
    global ready
    ready = False

    return f'Readiness Probe, will fail, ready_value: {ready}', 200

@app.route('/remom')
@app.route('/remove_maintenance')
def remove_maintenance():
    '''
    rediness probe will succed
    ''' 
    global ready
    ready = True

    return f'Readiness Probe, will succeed, ready_value: {ready}', 200

@app.route('/cluster_name')
def refresh_index():
    '''
        - Set cluster name environment varibale and make it retrieve it
    '''
    env_variable = os.getenv('CLUSTER_NAME', "no_cluster_specified")
    return f'Hello from: {env_variable}.', 200    

if __name__ == '__main__':
    readiness_app = threading.Thread(target=get_app_in_rotation)
    readiness_app.start()

    app.run('0.0.0.0', port=os.getenv('ECHO_PORT', 8080), debug=os.getenv('ECHO_DEBUG', True))
