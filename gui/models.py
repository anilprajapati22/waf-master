from operator import contains
from typing import Container
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class sgn(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text

class iptableRules(models.Model):
    project_name = models.CharField(max_length=200)
    rule = models.CharField(max_length=200)
    ipaddr = models.CharField(max_length=200)

class SQlFileterRules(models.Model):
    project_name = models.CharField(max_length=200)
    SQLFilterStr = models.CharField(max_length=200)


class wafdetails(models.Model):
    container_id =  models.CharField(max_length=200)
    container_name = models.CharField(max_length=200)
    container_port = models.CharField(max_length=200)
    container_ip = models.CharField(max_length=200)
    public_ip = models.CharField(max_length=200)
    project_name = models.CharField(max_length=200)

class ons(models.Model):
    question = models.ForeignKey(sgn, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)



class Bills(models.Model):
    Uid = models.ForeignKey(User, on_delete=models.CASCADE)   
    project_name = models.CharField(max_length=200)
    last_date_to_pay = models.DateField() 