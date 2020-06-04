# run this after setting up the docker-compose
echo "DEPLOYING SYSTEM"
docker-compose up -d --build

# this will initiate replica set for mongodb
echo "Initiating MongoDB replica set"
docker exec node1 mongo --eval "
rs.initiate(
    {
    _id: 'rs0',
    members: [
        {_id: 0, host: '172.21.0.11:27017'},
        {_id: 1, host: '172.21.0.12:27017'},
        {_id: 2, host: '172.21.0.13:27017'}
        ]
    }
)
"
sleep 2

# initialize database and store some test data
echo "Initializing database with test data..."
docker exec inventory_service python manage.py makemigrations service_app
sleep 2
docker exec inventory_service python manage.py migrate
docker exec -e JAVA_OPTS="-Dhazelcast.local.publicAddress=172.21.0.14:5701" -p 5701:5701 hazelcast/hazelcast:3.12
sleep 3
docker exec inventory_service python manage.py collectstatic --noinput
docker exec inventory_service python fill_db.py
echo "SYSTEM ONLINE"
