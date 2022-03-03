from flask import Flask, request
import subprocess
import time
import os
import threading
app = Flask(__name__)

ready = True


def get_app_in_rotation():
    '''
    Will make readiness probe success after 220 seconds automatically
    '''
    time_sleep = os.getenv('SLEEP_TIME', 220)
    global ready
    while True:
        if not ready:
            time.sleep(int(time_sleep))
            ready = True
            

@app.route('/')
@app.route('/health')
def hello():
    return "Hello World!"

@app.route('/getip')
def hello_name():
    status, output = subprocess.getstatusoutput('hostname -I')
    return output

@app.route('/process_wg', methods=['POST'])
def get_wg():
    print('Work group received')
    return 200

@app.route('/create_index')
def refresh_index():
    '''
    Index will be loaded for specific wg
    '''
    domain_name = None
    try:
        domain_name = request.args['domain_name']
    except Exception as e:
        return 'Require domain name to load index', 400

    return f'Index being loaded for wg: {domain_name}.', 200

@app.route('/rediness_probe')
def rediness_probe():
    if ready:
        return 'ok', 200
    else:
        return f'Ready: {ready}', 503

@app.route('/set_maintenance')
def set_maintenance():
    '''
    will fail rediness
    '''
    global ready
    ready = False

    return f'Readiness Probe, will fail, ready_value: {ready}', 200

@app.route('/remove_maintenance')
def remove_maintenance():
    '''
    rediness probe will succed
    ''' 
    global ready
    ready = True

    return f'Readiness Probe, will succeed, ready_value: {ready}', 200

if __name__ == '__main__':
    readiness_app = threading.Thread(target=get_app_in_rotation)
    readiness_app.start()

    app.run('0.0.0.0', port=4747, debug=True)
