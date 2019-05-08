from flask import Flask, jsonify
from pymongo import MongoClient
from bson.binary import JAVA_LEGACY, UUIDLegacy
from bson.codec_options import CodecOptions
from uuid import UUID

app = Flask(__name__)
mongo_client = MongoClient(host='demdata_mongodb')
db = mongo_client.get_database('demdata_db', CodecOptions(uuid_representation=JAVA_LEGACY))

routes = [
    '/acquisitions/ACQUISITION_ID/devices/DEVICE_ID/metrics', #For a given acquisition and device, returns all metrics for all sensors
    '/acquisitions/ACQUISITION_ID/devices/DEVICE_ID/sensors/SENSOR_TYPE/metrics' #For a given acquisition, device and sensor, returns all metrics
    ]

@app.route('/')
def hello_world():
    return jsonify(routes)
           

@app.route('/acquisitions/<uuid:acquisitionId>/devices/<uuid:deviceId>/metrics')
def get_all_acquisition_device_metrics(acquisitionId, deviceId):
    query = {'_id': UUIDLegacy(acquisitionId), 'devices._id': UUIDLegacy(deviceId)} #Thanks https://stackoverflow.com/a/51284449
    projection = {'devices._id': 1, 'devices.$': 1}
    query_result = db.acquisitions.find_one(query, projection)

    result = {}
    if query_result is not None:
        result['_id'] = query_result['_id']
        result['device_id'] = query_result['devices'][0]['_id']
        result['sensors'] = [{'sensor': sensor['sensorType'].title(), 'metrics': sensor['metrics']} for sensor in query_result['devices'][0]['sensors']]

    return jsonify(result)

@app.route('/acquisitions/<uuid:acquisitionId>/devices/<uuid:deviceId>/sensors/<string:sensorType>/metrics')
def get_acquisition_device_sensor_metrics(acquisitionId, deviceId, sensorType):
    query = {'_id': UUIDLegacy(acquisitionId), 'devices._id': UUIDLegacy(deviceId)}
    projection = {'devices._id': 1, 'devices.$': 1}
    query_result = db.acquisitions.find_one(query, projection)

    result = {}
    if query_result is not None:
        result['_id'] = query_result['_id']
        result['device_id'] = query_result['devices'][0]['_id']
        result['sensor_type'] = sensorType
        result['metrics'] = next((sensor['metrics'] for sensor in query_result['devices'][0]['sensors'] if sensor['sensorType'].title() == sensorType.title()), dict())

    return jsonify(result)


app.run(debug=True, host='0.0.0.0', port=5050)

