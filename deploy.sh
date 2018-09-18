#! /bin/sh

# Hack to make .env work in stack deploy mode...
source <(cat .env | sed -e "s+^\([^# ]\)+export \1+g")
export DOCKER_HOST=tcp://ymslanda.innovationgarage.tech:2375

docker build --tag ymslanda.innovationgarage.tech:5000/portpollution_weatherindex:latest .
docker push ymslanda.innovationgarage.tech:5000/portpollution_weatherindex:latest 
docker stack deploy -c docker-compose.yml portpollution_weatherindex
