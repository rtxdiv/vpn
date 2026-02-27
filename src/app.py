from flask import Flask

app = Flask(__name__, static_folder='../public', static_url_path='')

@app.get('/')
def getRoot():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8443)