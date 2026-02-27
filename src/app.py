from flask import Flask, send_file

app = Flask(__name__)

@app.get('/')
def getRoot():
    return send_file('../public/index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8443)