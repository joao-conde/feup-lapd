from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Flask Dockerized'


app.run(debug=True, host='0.0.0.0', port=5050)

