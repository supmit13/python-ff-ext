# This file defines the models used by savewhatyoulookedat application. The models are based on DJango's model
# mechanism. The models specific to savewhatyoulookedat application are "users", "urls", "category" and "session".
# The corresponding table names are: "savewhatyoulookedat_users", "savewhatyoulookedat_urls", "savewhatyoulookedat_session"
# and "savewhatyoulookedat_category".
#
# -- Supriyo.


from django.db import models
import os

class users(models.Model):
    firstName = models.CharField(max_length=255)
    middleInitials = models.CharField(max_length=20)
    lastName = models.CharField(max_length=255) 
    userID = models.CharField(primary_key=True, max_length=20)
    emailID = models.EmailField()
    password = models.CharField(max_length=20)
    createtime = models.DateTimeField(auto_now=True)

class urls(models.Model):
    urlID = models.AutoField(primary_key=True)
    user = models.ForeignKey(users)
    savedURL = models.URLField(max_length=255)
    html = models.TextField()
    images = models.FilePathField(os.getcwd() + "/images")
    accesstime = models.DateTimeField(auto_now=True)
    categoryID = models.IntegerField()
    sessionID = models.CharField(max_length=20)
    recieveinfo = models.BooleanField()

class category(models.Model):
    categoryID = models.AutoField(primary_key=True)
    categoryname = models.CharField(max_length=255)

class session(models.Model):
    sessionID = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(users)
    startTime = models.DateTimeField(auto_now=True)
    sessionState = models.BooleanField()




