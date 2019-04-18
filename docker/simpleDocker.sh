# simple run contaiter from Docker Image with tag latest in daemon mode, for example with debian docker image
docker run -d debian:latest

# simple run container in interactive mode
docker run -it debian:latest

# show current runned containers
docker ps

# show all containers on current node (runned and stopped)
docker ps -a

# show all docker images donloaded to this node
docker images
