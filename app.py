from flask import Flask

app = Flask(__name__)
@app.route('/')
def inicio():
    return 'WS Interno 80'

if __name__ == '__main__':
    app.run(host='localhost', port=80)
