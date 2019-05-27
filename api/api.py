from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.binary import JAVA_LEGACY, UUIDLegacy
from bson.codec_options import CodecOptions
from uuid import UUID

app = Flask(__name__)
mongo_client = MongoClient(host='demdata_mongodb')
db = mongo_client.get_database('demdata_db', CodecOptions(uuid_representation=JAVA_LEGACY))

routes = [
    '/acquisitions/ACQUISITION_ID/metrics', #For a given acquisition, get all metrics for all sensors of all devices
    '/acquisitions/ACQUISITION_ID/devices/DEVICE_ID/metrics[?metric=METRIC[&gt=MIN_VALUE|&gte=MIN_VALUE][&lt=MAX_VALUE|&lte=MAX_VALUE]]', #For a given acquisition and device, returns all metrics for all sensors. Optionally, filter by sensors with a specific metric, optionally bound between a specific range
    '/acquisitions/ACQUISITION_ID/devices/DEVICE_ID/sensors/SENSOR_TYPE/metrics', #For a given acquisition, device and sensor, returns all metrics
    '/acquisitions/ACQUISITION_ID/devices/DEVICE_ID/sensors/SENSOR_TYPE/metrics/METRIC' #For a given acquisition, device, sensor and metric, return the value of the metric
    ]

@app.route('/')
def hello_world():
    return jsonify(routes)

# Obtains a nested property from a document, given a list of successive keys
def get_nested_metric(metrics, metric_nested):
    try:
        metric = metrics[metric_nested[0]]
        for component in metric_nested[1::]:
            metric = metric[component.lower()]         
        return float(metric)
    except KeyError:
        return None

# Checks if a given number if within a specific range. Lt has preference over lte (same applies to gt/gte)
def is_value_within_limits(value, lt, lte, gt, gte):
    if lt is not None:
        if value >= float(lt):
            return False
    elif lte is not None:
        if value > float(lte):
            return False
    if gt is not None:
        if value <= float(gt):
            return False
    elif gte is not None:
        if value < float(gte):
            return False
    
    return True


@app.route('/acquisitions/<uuid:acquisitionId>/metrics')
def get_acquisition_metrics(acquisitionId):
    query = {'_id': UUIDLegacy(acquisitionId)}
    projection = {'devices': 1}
    query_result = db.acquisitions.find_one(query, projection)

    result = []
    if query_result is not None:
        for device in query_result['devices']:
            device_entry = {'device': device['model'], 'sensors': []}
            for sensor in device['sensors']:
                device_entry['sensors'].append({'sensor': sensor['sensorType'].title(), 'metrics': sensor['metrics']})
            result.append(device_entry)

    return jsonify(result)           

@app.route('/acquisitions/<uuid:acquisitionId>/devices/<uuid:deviceId>/metrics')
def get_all_acquisition_device_metrics(acquisitionId, deviceId):
    query = {'_id': UUIDLegacy(acquisitionId), 'devices._id': UUIDLegacy(deviceId)} #Thanks https://stackoverflow.com/a/51284449
    projection = {'devices._id': 1, 'devices.$': 1}
    query_result = db.acquisitions.find_one(query, projection)

    result = {}
    if query_result is not None:
        if request.args.get('metric') is not None:
            metric_nested = request.args.get('metric').split('.')
            gte = request.args.get('gte', None)
            gt = request.args.get('gt', None)
            lte = request.args.get('lte', None)
            lt = request.args.get('lt', None)
            result['sensors'] = [{'sensor': sensor['sensorType'].title(), 'metrics': sensor['metrics']} for sensor in query_result['devices'][0]['sensors'] if get_nested_metric(sensor['metrics'], metric_nested) is not None and is_value_within_limits(float(get_nested_metric(sensor['metrics'], metric_nested)), lt, lte, gt, gte)]
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
        value = get_nested_metric(metrics, metric.split('.'))
        result['value'] = value if value is not None else 'NOT_FOUND'

    return jsonify(result)


app.run(debug=True, host='0.0.0.0', port=5050)

