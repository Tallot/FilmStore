# run this after setting up the docker-compose
docker-compose up -d --build
sleep 1

# this will initiate replica set for mongodb
docker exec node1 mongo --eval "
rs.initiate(
    {
    _id: 'rs0',
    members: [
        {_id: 0, host: 'node1:27017'},
        {_id: 1, host: 'node2:27017'},
        {_id: 2, host: 'node3:27017'}
        ]
    }
)
"
