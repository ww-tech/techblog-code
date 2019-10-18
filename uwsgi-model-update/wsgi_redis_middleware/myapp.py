from flask import Flask, request, jsonify, g
import dill
import sys
import os
import redis
from werkzeug.local import Local
# sleep for illustrative purposes
from time import sleep

# import our after response middleware
from .middleware import AfterResponse


app = Flask(__name__)
AfterResponse(app)

# global model
model = None

# create werkzeug context since we are doing operations outside of g
local = Local()


@app.route('/predict', methods=['GET'])
def predict():
    features = request.args.getlist('features')
    pred = model.predict(features)
    return jsonify({'prediction': pred})


@app.route('/update-model', methods=['POST'])
def update_model():
    r = get_cache()
    new_path = request.args.get('path')
    busy_signal = int(r.get('busy_signal'))
    if not busy_signal:
        r.set('busy_signal', 1)
        load_model(new_path, r)
        r.set('busy_signal', 0)
    return jsonify({'status': 'update complete!'})


@app.after_response
def check_cache():
    r = get_cache()
    global model
    cached_hash = r.get('model_hash')
    if model.hash != cached_hash:
        busy_signal = int(r.get('busy_signal'))
        if not busy_signal:
            # if not busy, we update and first set signal to busy
            r.set('busy_signal', 1)
            model_location = r.get('model_location')
            load_model(model_location, r)
            r.set('busy_signal', 0)


def get_cache():
    cache = getattr(local, 'cache', None)
    if cache is None:
        local.cache = redis.Redis(decode_responses='utf-8')
    return local.cache


def load_model(model_path, r):
    global model
    print('loading model at {}'.format(model_path))

    # sleep to simulate long model load
    sleep(15)
    
    with open(model_path, 'rb') as f:
        model = dill.load(f)
    
    r.set('model_hash', model.hash)
    r.set('model_location', model_path)

# prefork load model so each uWSGI process has a copy
# will not run if this is in main
# need connection to redis outside of flask context to initialize
model_path = os.environ.get('MODEL_PATH', './models/test_model_01.dill')
r = redis.Redis()
load_model(model_path, r)
r.set('busy_signal', 0)
del r


if __name__ == '__main__':
    app.run()
