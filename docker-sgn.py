import docker
client = docker.from_env() #start connection with docker

try:
    sgncontainer = client.containers.run("sgn-waf", detach=True,
            ports={'9080/tcp':8080},
            volumes=['/home/anil/sem8:/sgn-waf'],
            name="sgn-python")

    print(sgncontainer.name) #name of the container
    print(sgncontainer.attrs)

except:
    print("sgnons error")

    #if same name container was there
    if "sgn-python" in [container.name for container in client.containers.list()]:
        print("container name is already there ! please change the name")


#run docker
#to remove docker container

# sgncontainer.kill()
# sgncontainer.remove()


#to create dictioney of containers that are running
#  name:id
d={container.name:container for container in client.containers.list()}

#list of names 

[container.name for container in client.containers.list()]