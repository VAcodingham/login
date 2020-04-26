from __future__ import unicode_literals
import re
from datetime import date, datetime
from django.db import models

class UserManager(models.Manager):
    def user_validator(self,postData):
        errors={}
        #username verification/authenticator
        if len(postData['username'])<2:
            errors['username']="!Username must be longer than 2 characters!"
        UserName=User.objects.all()
        for x in UserName:
            if x.username==postData['username']:
                errors['username']="!Username already exists. If this is you please login!"
        if len(postData['first_name'])<2:
            errors['first_name']="!First name must be longer than 2 characters!"
        if len(postData['last_name'])<2:
            errors['last_name']="!Last name must be longer than 2 characters!"
        if postData['birthdate']=='':
            errors['birthdate']="!Please enter your date of birth!"
        else:
            datetime_object = datetime.strptime(postData['birthdate'],'%Y-%m-%d')
            if datetime_object>datetime.today():
                errors['birthdate']="!Date of birth must be in the past!"
        
        #email validations
        EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email']="!Invalid email address!"
        useremail=User.objects.all()
        for i in useremail:
            if i.email == postData['email']:
                errors['email']="!This email already exists! If this is you please login!"

        #password validations
        password_REGEX=re.compile(r'[A-Za-z0-9!@#$%^&+=]+[A-Za-z]|[0-9]|[!@#$%^&+=]+[A-Za-z0-9!@#$%^&+=]+$')
        if not password_REGEX.match(postData['password']):
            errors['password']="!Password must contain 1 letter, 1 number, and one special character!"
        if len(postData['password'])<8:
            errors['password']="!Password must be at least 8 characters!"
        if postData['password']!=postData['confirm_password']:
            errors['password']="!Passwords do not match!"
        return errors
    
    #Create your models here.
class User(models.Model):
    username=models.CharField(max_length=255)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    birthdate=models.DateTimeField()
    password=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()




