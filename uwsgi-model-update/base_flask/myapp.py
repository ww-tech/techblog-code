from flask import Flask, request, jsonify
import dill
import sys
import os

# sleep for illustrative purposes
from time import sleep

app = Flask(__name__)

# global model
model = None

@app.route('/predict', methods=['GET'])
def predict():
    features = request.args.getlist('features')
    pred = model.predict(features)
    return jsonify({'prediction': pred})

@app.route('/update-model', methods=['POST'])
def update_model():
    new_path = request.args.get('path')
    load_model(new_path)
    return jsonify({'status': 'update complete!'})

def load_model(model_path):
    global model
    print('loading model at {}'.format(model_path))
        
    # sleep to simulate long model load
    sleep(15)

    with open(model_path, 'rb') as f:
        model = dill.load(f)

# prefork load model so each uWSGI process has a copy
# will not run if this is in main
model_path = os.environ.get('MODEL_PATH', './models/test_model_01.dill')
load_model(model_path)


if __name__ == '__main__':
    app.run()
