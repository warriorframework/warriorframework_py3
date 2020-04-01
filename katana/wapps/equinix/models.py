# -*- coding: utf-8 -*-


from django.db import models

class equinixgroups(models.Model):
        groupname = models.CharField(max_length=100,primary_key=True)
        interfacename = models.CharField(max_length=100)
        transpondername = models.CharField(max_length=100)  
        opsname = models.CharField(max_length=100)

class equinixops(models.Model):
        opsname = models.CharField(max_length=100,primary_key=True)
        opsport = models.CharField(max_length=100)
        opsip = models.CharField(max_length=100)
        opsusername = models.CharField(max_length=100)
        opspassword = models.CharField(max_length=100)
        

class equinixtransponder(models.Model):
        transpondername = models.CharField(max_length=100,primary_key=True)
        transponderport = models.CharField(max_length=100)
        transponderip = models.CharField(max_length=100)
        transponderusername = models.CharField(max_length=100)
        transponderpassword = models.CharField(max_length=100)
        