simple telegram bot for mentioneing users based on msg coming from groups 


1- simply clone the project 

2- install docker 

3- in the root directory run this command 

- To do run as a container.

``` bash
docker-compose  -p  YOUR_NAME  up --build -d 
```


- To stop the containers.

``` bash
docker-compose -p YOUR_NAME  down 
```

- To avoid cashing during build the container.
``` bash
docker-compose -p YOUR_NAME build  --no-cache && docker-compose up -d 