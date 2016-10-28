from django.db import models

# Create your models here.
class Student(models.Model):
    stu_num = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
