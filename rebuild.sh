# Stop containers
sudo docker stop $(sudo docker ps -aq)

# Rebuild and start
sudo docker-compose down
sudo docker-compose build --no-cache
sudo docker-compose up
