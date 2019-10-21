# Flask/uWSGI Example Code

Code related to [this blogpost](https://medium.com/ww-tech-blog/well-do-it-live-updating-machine-learning-models-on-flask-uwsgi-with-no-downtime-9de8b5ffdff8) on updating ML models in production without downtime. Please read through the blogpost for a complete understanding of the code in this repo.


Three versions of the application detailed in the blogpost are available:
1. base_flask
    - The base flask application to start. This can be run with uwsgi for concurrency.
2. wsgi_redis
    - Adding a redis caching layer and checking the model hash to sync a new model between different processes.
3. wsgi_redis_middleware
    - Include wsgi middleware layer which allows to update model after responses are given to the requestor.


To run a particular version of the application, specify the module via the uwsgi command line argument. This assumes you have a redis instance running at `localhost:6379`.
```
uwsgi --module <directory>.myapp:app uwsgi.ini
```

Hitting the endpoints:
```
import requests

# make prediction
r = requests.get(url='http://127.0.0.1:5000/predict', params={'features': ['test', 1, 'blarg']})

# update model
r = requests.post(url='http://127.0.0.1:5000/update-model', params={'path': './models/test_model_02.dill'})
```

You can also see how each application handles requests before, during, and after model updates by running the example script. If the application needs a redis instance, start one at `localhost:6379` before executing this script. You can run it by providing the argument of which module to run:
```
bash ./scripts/run.sh wsgi_redis_middleware
```
