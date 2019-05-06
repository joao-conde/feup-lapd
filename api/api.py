from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
mongo_client = MongoClient(host='demdata_mongodb')
db = mongo_client.demdata_db

@app.route('/')
def hello_world():
    return str(db.datasets.count_documents({}))

@app.route('/cenas')
def hello():
    return 'hello world'


app.run(debug=True, host='0.0.0.0', port=5050)

