from django.db import models

# Create your models here.
class Student(models.Model):
    stu_num = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    gender = models.IntegerField(default=0)
    college = models.CharField(default='')
    phone = models.CharField(default='')
    weixin = models.CharField(default='')
    qq = models.CharField(default='')
