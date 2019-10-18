APP_DIR=$1


echo "booting up uwsgi"
mkdir -p tmp
uwsgi --module $APP_DIR.myapp:app --pidfile tmp/myapp.pid uwsgi.ini &

function cleanup() {
    echo ""
    echo "shutting down uwsgi..."
    # make sure uwsgi is running before we try to shut it down
    curl -s "http://localhost:5000" > /dev/null
    # sometimes issues stopping uwsgi via stop command - use pkill for now
    # uwsgi --stop tmp/myapp.pid
    pkill -f uwsgi -9
    echo "removing temp files..."
    rm -rf tmp
    exit
}

trap cleanup SIGINT SIGTERM

echo ""
echo "initial model response"
curl "http://127.0.0.1:5000/predict?features=test&features=3"
sleep 2

echo ""
echo "updating model"
curl -X POST "http://127.0.0.1:5000/update-model?path=models/test_model_02.dill" &
sleep 5

echo ""
echo "get requests during/after model update"
for i in {1..30}
do
    echo ""
    echo "request $i"
    curl "http://127.0.0.1:5000/predict?features=test&features=3"
    sleep 2
done ;

echo ""
cleanup
