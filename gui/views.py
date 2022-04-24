from multiprocessing import context
from plistlib import UID
from django.shortcuts import render,redirect
from django.http import HttpResponse
import docker
import time
from .models import iptableRules,wafdetails,Bills
from .forms import UserRegistrationForm
from django.contrib.auth import login
import requests
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
base_port_url = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


client = docker.from_env() #start connection with docker

# Create your views here.
#shree ganeshay namah
#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
import boto3
from dateutil.relativedelta import relativedelta
from datetime import datetime as dt

queue_url = "https://sqs.us-east-1.amazonaws.com/590852515231/AnilP-sqs-waf"

def sgn(request):
    return HttpResponse("sgnons jkh jbm jam jkh jcs jkb jjb jjb jsb jsd jam jom jsm jlm jsm jsm jkb jhd jgb jjb jd jd jd jmp jg")

def index(request):
    context={}
    return render(request, 'index.html', context)    



def getPublicIP():
    # write here code for getting public ip
    try:
        public_ip = requests.get("http://169.254.169.254/latest/meta-data/public-ipv4")
        if public_ip:
            return public_ip.content.decode('UTF-8')
        else:    
            public_ip = "sgnons"
            return public_ip
    except:
        return "localhost"

def getPort():
    f = open(os.path.join(base_port_url, 'portmapping.txt'),"r")
    port = f.read()
    f.close()
    f = open(os.path.join(base_port_url, 'portmapping.txt'),"w")
    f.write(str(int(port)+3))
    f.close()
    return str(port)

def addWafDetails(container_id,project_name):
    cobjs =  [ container.attrs for container in [client.containers.get(container_id)] ]
    cobjs = [ [ d['Config']['Hostname'], d['Name'][1:], d['Id'], d['NetworkSettings']['Ports'][list(d['NetworkSettings']['Ports'].keys())[0]][0]['HostPort'], d['NetworkSettings']['IPAddress'] , "localhost"+":"+ d['NetworkSettings']['Ports'][list(d['NetworkSettings']['Ports'].keys())[0]][0]['HostPort'] , list(d['NetworkSettings']['Ports'].keys())[0] ] for d in cobjs if "container" in d['Name']] 

    waf_obj = wafdetails(
        container_id =  cobjs[0][2],
        container_name = cobjs[0][1],
        container_port = cobjs[0][3],
        container_ip = cobjs[0][4],
        public_ip = getPublicIP(),
        project_name = project_name
    )
    waf_obj.save()

    print("\n\n")
    print(cobjs,"\n\n")


def dockerRun(request):
    request.session['msg']=""
    bill_pay = Bills.objects.filter(Uid = request.user.id)
    if len(bill_pay) > 0 :
        is_bill_pending = is_bill_payed(bill_pay[0].last_date_to_pay)
    else:
        is_bill_pending = True

    if request.method == "GET":
        return render(request=request, template_name="dockerRun.html",context={
            'images' : getImages(),
            "is_bill_pending" : is_bill_pending
        })	

    if request.method == "POST":
        print(request.POST)

        is_detach=False
        # try:
        print("\n\n\n\nsgn\n\n")
        port_c = getPort()
        sgncontainer = client.containers.run("anilprajapati18/sgn-waf-saas", 
                detach=True,
                ports={str(8080)+'/tcp':port_c,str(80)+'/tcp':str(int(port_c)+1),str(22)+'/tcp':str(int(port_c)+2)},
                tty = True,
                cap_add = ['NET_ADMIN'],
                volumes=['/home/anilprajapati/sem8/:/sgn-waf'],
                name=request.POST["name"]+"container")
        print(sgncontainer.name) #name of the container
        print(sgncontainer.attrs)
        container_id = sgncontainer.id        
        context = { 'container_id' : container_id }

        addWafDetails(container_id,request.POST["name"])
        date_after_month = date_after_month = dt.now() + relativedelta(months=1)
        add_bill = Bills(Uid = request.user,
                        project_name = request.POST["name"],
                        last_date_to_pay = date_after_month)
        add_bill.save()
        return redirect(containerList)
            #return render(request=request, template_name="dockerRun.html",context=context)	            

        # except:
        #     print("sgnons error")

        #     #if same name container was there
        #     if "sgn-python" in [container.name for container in client.containers.list()]:
        #         print("container name is already there ! please change the name")
        #     return render(request=request, template_name="dockerRun.html",context={})	
	


#{% url '{{ containerLink }}' %}

def containerDetails(request, container_id ):
    #get containers details from attr
    cobj=client.containers.get(container_id)
    cobjs = [ cobj.attrs ]
    #cobjs =  [ container.attrs for container in client.containers.list() ]
    cobjs = [ [ d['Config']['Hostname'], d['Name'][1:], d['Id'], d['NetworkSettings']['Ports'][list(d['NetworkSettings']['Ports'].keys())[0]][0]['HostPort'], d['NetworkSettings']['IPAddress'] , "localhost"+":"+ d['NetworkSettings']['Ports'][list(d['NetworkSettings']['Ports'].keys())[0]][0]['HostPort'] , list(d['NetworkSettings']['Ports'].keys())[0] ] for d in cobjs if "container" in d['Name']] 
    print("\n\n")
    #print(cobjs.keys(),"\n\n")
    context= {  "cobjs" : cobjs, "cid" : cobj.attrs['Id'][:10] , "container_id"  :  container_id }
    return render(request=request, template_name="containerDetails.html",context=context)

# def containerRemove(request, container_id):
#     # remove container
#     cobj=client.containers.get(container_id)
#     cobj.kill()
#     cobj.remove()
#     wafdetails.objects.all().delete()
#     context = { "msg" : "Your Container Is Removed !!" }
#     return render(request=request, template_name="containerDetails.html",context=context)
            
def getImages():
    images=[image.tags[0] for image in  client.images.list() if image.tags]
    return images

def containerRemove(request, container_id):
    # remove container
    request.session['msg']=""
    cobj=client.containers.get(container_id)
    cobj.kill()
    cobj.remove()
    print("\n\n deleting all containers \n\n")
    wafdetails.objects.all().delete()
    Bills.objects.all().delete()
    context = { "msg" : "Your Container Is Removed !!" }
    return redirect(containerList)

def containerList(request):
    cobjs =  [ container.attrs for container in client.containers.list() ]
    cobjs = [ [ d['Config']['Hostname'], d['Name'][1:], d['Id'], d['NetworkSettings']['Ports'][list(d['NetworkSettings']['Ports'].keys())[0]][0]['HostPort'], d['NetworkSettings']['IPAddress'] , "localhost"+":"+ d['NetworkSettings']['Ports'][list(d['NetworkSettings']['Ports'].keys())[0]][0]['HostPort'] , list(d['NetworkSettings']['Ports'].keys())[0] ] for d in cobjs if "container" in d['Name']] 
    context = None
    bill_pay = Bills.objects.filter(Uid = request.user.id)
    if len(bill_pay) > 0 :
        is_bill_pending = is_bill_payed(bill_pay[0].last_date_to_pay)
    else:
        is_bill_pending = True

    if len(cobjs) >= 1:
        context= {  "cobjs" : cobjs , 
        "cDetails" : wafdetails.objects.all()[0] , 
        "port1" : int(cobjs[0][3])-1,
        "port2" : int(cobjs[0][3])-2,
        "public_ip" : getPublicIP(),
        "is_bill_pending" : is_bill_pending}
        print("\n\n")
        print(cobjs,"\n\n")
    else:
        context= {  "cobjs" : cobjs ,
        "is_bill_pending" : is_bill_pending            
        }

    return render(request=request, template_name="containerDetails.html",context=context)
 
def serviceList(request,msg=None):
    serviceattrs=[ service.attrs for service in client.services.list() ]
    cobjs = [[d["ID"] , d['Spec']['Name'], d['ID'] , d['Spec']['EndpointSpec']['Ports'][0]['PublishedPort'] , "-" , "" , d['Spec']['EndpointSpec']['Ports'][0]['TargetPort'] , d['Spec']['Mode']['Replicated']['Replicas'] ] for d in serviceattrs ]
    context = { 'services' : serviceattrs , "cobjs" : cobjs , "msg" : request.session['msg'] }
    return render(request=request, template_name="containerDetails.html",context=context)	            

def serviceRemove(request, service_id):
    # remove container
    cobj=client.services.get(service_id)
    cobj.remove()
    context = { "msg" : "Your Container Is Removed !!" }
    return redirect(serviceList)

def serviceScale(request):
    # remove container
    service_id = request.POST['service_id']

    cobj=client.services.get(service_id)
    print("\n\n\n",cobj.id)
    try:
        scale_count = int(request.POST['scale'])
        cobj.scale(scale_count)
        request.session['msg'] = "Scaling Completed"
        return redirect(serviceList)
    except:
        print("error in scaling 2")  
        request.session['msg'] = "Error In Scaling 2"   
        return redirect(serviceList)

def pullimages(request):
    if request.method == "GET":
        request.session['msg']=""
        bill_pay = Bills.objects.filter(Uid = request.user.id)
        if len(bill_pay) > 0 :
            is_bill_pending = is_bill_payed(bill_pay[0].last_date_to_pay)
        else:
            is_bill_pending = True
        return render(request=request, template_name="pullimages.html",context={ 
            "is_bill_pending" : is_bill_pending
        })	

    if request.method == "POST":
        try:
            if request.POST['tag']:        
                client.images.pull(request.POST["image"],tag=request.POST['tag'])
            else:
                client.images.pull(request.POST["image"],tag="latest")        
            return redirect(dockerRun)
        except:
            request.session['msg']="error while pulling images"
            return render(request=request, template_name="pullimages.html",context={
                'msg': request.session['msg']
             })	

def getAuthenticateEmail(email):
    sqs = boto3.client('sqs',region_name='us-east-1')

    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes={
            'email': {
                'DataType': 'String',
                'StringValue': email
            },
            'is_secret': {
                'DataType': 'String',
                'StringValue': "no"
            }					
        },
        MessageBody=(
            'sgnons'
        )
    )
    print("\n\n\n\n\n")
    print(response['MessageId'])



def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            getAuthenticateEmail(request.POST['email'])            
            user = form.save()
            login(request, user)
            return redirect("dockerRun")
    form = UserRegistrationForm()
    return render (request=request, template_name="registration/register.html", context={"register_form":form})    

def is_bill_payed(last_date_to_pay):
    diff_days = relativedelta( dt.now() , last_date_to_pay )
    print("\n\n\n",diff_days.days)
    print(last_date_to_pay)
    print(diff_days)
    if diff_days.days < 0 or diff_days.months < 0 or diff_days.hours < 0 or  diff_days.minutes < 0:
        return True
    else:
        return False    
    return days


def payBill(request):
    bill_pay = Bills.objects.filter(Uid = request.user.id)
    if len(bill_pay) >0:
        if request.method == "POST":
            bill_pay[0].last_date_to_pay = bill_pay[0].last_date_to_pay +  relativedelta(months=1)
            bill_pay[0].save()
            callSQS(request.user.email,bill_pay[0].last_date_to_pay)
        context = {
            "last_date_to_pay" : bill_pay[0].last_date_to_pay
        }    
        return render (request=request, template_name="payBill.html",context=context)    
    else:
        return render (request=request, template_name="payBill.html",context={"msg":"request for service"})

def callSQS(email,Ddate):
	sqs = boto3.client('sqs',region_name='us-east-1')

	#queue_url = 'https://sqs.ap-south-1.amazonaws.com/675270067251/SgnCovidPlazmaSQS'

	# Send message to SQS queue
	response = sqs.send_message(
		QueueUrl=queue_url,
		DelaySeconds=10,
		MessageAttributes={
			'email': {
				'DataType': 'String',
				'StringValue': email
			},
			'Ddate': {
				'DataType': 'String',
				'StringValue': str(Ddate)
			},
			'is_secret': {
				'DataType': 'String',
				'StringValue': "yes"
			}
		},
		MessageBody=(
			'sgnons'
		)
	)

	print(response['MessageId'])
