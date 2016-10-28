from django.db import models

# Create your models here.
class Student(models.Model):
    stu_num = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    gender = models.IntegerField(default=0)
    college = models.CharField(max_length=30, default='')
    phone = models.CharField(max_length=30, default='')
    weixin = models.CharField(max_length=30, default='')
    qq = models.CharField(max_length=30, default='')
    work_location = models.CharField(max_length=30, default='')
    work_character = models.CharField(max_length=30, default='')
    register_time = models.DateTimeField(auto_now=False)

class Teacher(models.Model):
    teacher_num = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    department = models.CharField(max_length=50, default='')

class Sign(models.Model):
    student = models.ForeignKey(Student)
    teacher = models.ForeignKey(Teacher)
    sign_in_time = models.DateTimeField(auto_now=False)
    sign_off_time = models.DateTimeField(auto_now=False)
    remark = models.CharField(max_length=200, default='')

