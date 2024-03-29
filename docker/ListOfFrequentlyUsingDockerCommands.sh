# simple run contaiter from Docker Image with tag latest in daemon mode, for example with debian docker image
docker run -d debian:latest

# simple run container in interactive mode
docker run -it debian:latest

# show current runned containers
docker ps

# show all containers on current node (runned and stopped)
docker ps -a

# filter container(s) by defined name or mask with grep util
docker ps -a | grep container_name

# show all docker images donloaded to this node
docker images

# stop docker-compose stack, delete unused data, rebuild docker-compose stack und rise up !
# you must run this in directory where your docker-compose.yml file
docker-compose down && docker system prune && docker-compose build && docker-compose up -d
