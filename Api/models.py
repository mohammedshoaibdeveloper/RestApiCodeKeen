from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.mail import send_mail
from django.conf import settings
from decouple import config

# Create your models here.


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=12)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=255,null=True,blank=True)
    email_verification_token = models.CharField(max_length=200,null=True,blank=True)
    forget_password_token = models.CharField(max_length=200,null=True,blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email 

import uuid
@receiver(post_save,sender=User)
def send_email_token(sender,instance,created,**kwargs):
    if created:
        print("run------------")
        try:
            subject = "You email needs to be verified"
            message = f'Hi ,click on the link to verify email http://127.0.0.1:8000/{uuid.uuid4()}/'
            email_from = config('EMAIL_HOST_USER')
            receipent_list = [instance.email]
            send_mail(subject,message,email_from,receipent_list)


        except Exception as e:
            print(e)

class Category(models.Model):
    category_name = models.CharField(max_length=100)


class Book(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    book_title = models.CharField(max_length=100)

class Student(models.Model):

    name = models.CharField(max_length=255,default='')
    age = models.IntegerField(default=18)
    address = models.CharField(max_length=255,default='')
    father_name = models.CharField(max_length=255,default='')

class Excelfileuupload(models.Model):
    excel_file_upload = models.FileField(upload_to="excel")