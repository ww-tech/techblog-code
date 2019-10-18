FROM python:3.6-stretch

COPY wsgi_redis_middleware/ ./wsgi_redis_middleware/
COPY uwsgi.ini ./uwsgi.ini
COPY models/ models/
COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

ENV MODEL_PATH=./models/test_model_01.dill

ENTRYPOINT ["uwsgi", "--module", "wsgi_redis_middleware.myapp:app", "uwsgi.ini"]
