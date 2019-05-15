from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.binary import JAVA_LEGACY, UUIDLegacy
from bson.codec_options import CodecOptions
from uuid import UUID

app = Flask(__name__)
mongo_client = MongoClient(host='demdata_mongodb')
db = mongo_client.get_database('demdata_db', CodecOptions(uuid_representation=JAVA_LEGACY))

routes = [
    '/acquisitions/ACQUISITION_ID/devices/DEVICE_ID/metrics[?metric=METRIC[&gt=MIN_VALUE][&lt=MAX_VALUE]]', #For a given acquisition and device, returns all metrics for all sensors. Optionally, filter by sensors with a specific metric, optionally bound between a specific range
    '/acquisitions/ACQUISITION_ID/devices/DEVICE_ID/sensors/SENSOR_TYPE/metrics', #For a given acquisition, device and sensor, returns all metrics
    '/acquisitions/ACQUISITION_ID/devices/DEVICE_ID/sensors/SENSOR_TYPE/metrics/METRIC' #For a given acquisition, device, sensor and metric, return the metric's value
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
        if request.args.get('metric') is not None:
            metric = request.args.get('metric')
            lower_bound = int(request.args.get('gt', '0'))
            upper_bound = int(request.args.get('lt', '1000000'))
            result['sensors'] = [{'sensor': sensor['sensorType'].title(), 'metrics': sensor['metrics']} for sensor in query_result['devices'][0]['sensors'] if metric in sensor['metrics'] and sensor['metrics'][metric] >= lower_bound and sensor['metrics'][metric] <= upper_bound]
        else:
            result['sensors'] = [{'sensor': sensor['sensorType'].title(), 'metrics': sensor['metrics']} for sensor in query_result['devices'][0]['sensors']]

    return jsonify(result)

@app.route('/acquisitions/<uuid:acquisitionId>/devices/<uuid:deviceId>/sensors/<string:sensorType>/metrics')
def get_acquisition_device_sensor_metrics(acquisitionId, deviceId, sensorType):
    query = {'_id': UUIDLegacy(acquisitionId), 'devices._id': UUIDLegacy(deviceId)}
    projection = {'devices._id': 1, 'devices.$': 1}
    query_result = db.acquisitions.find_one(query, projection)

    result = {}
    if query_result is not None:
        result['metrics'] = next((sensor['metrics'] for sensor in query_result['devices'][0]['sensors'] if sensor['sensorType'].title() == sensorType.title()), dict())

    return jsonify(result)

@app.route('/acquisitions/<uuid:acquisitionId>/devices/<uuid:deviceId>/sensors/<string:sensorType>/metrics/<string:metric>')
def get_acquisition_device_sensor_specific_metric(acquisitionId, deviceId, sensorType, metric):
    query = {'_id': UUIDLegacy(acquisitionId), 'devices._id': UUIDLegacy(deviceId)}
    projection = {'devices._id': 1, 'devices.$': 1}
    query_result = db.acquisitions.find_one(query, projection)

    result = {}
    if query_result is not None:
        metrics = next((sensor['metrics'] for sensor in query_result['devices'][0]['sensors'] if sensor['sensorType'].title() == sensorType.title()), dict())
        result['value'] = metrics[metric] if metric.lower() in metrics else 'NOT_FOUND'

    return jsonify(result)


app.run(debug=True, host='0.0.0.0', port=5050)

