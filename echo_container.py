from flask import Flask
import subprocess

app = Flask(__name__)


@app.route('/health')
def hello():
    return "Hello World!"


@app.route('/getip')
def hello_name():
    status, output = subprocess.getstatusoutput('hostname -I')
    return output



if __name__ == '__main__':
    app.run('0.0.0.0', port=4747, debug=True)
