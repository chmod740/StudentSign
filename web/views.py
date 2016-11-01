from django.shortcuts import render_to_response, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from web.models import Student, Teacher, Sign
from datetime import datetime
import time
import os
import platform

# Create your views here.
@csrf_exempt
def login(req):
    if req.method == "GET":
        return render_to_response('login.html')
    else:
        username = req.POST.get('username', None)
        password = req.POST.get('password', None)
        users = Teacher.objects.filter(teacher_num__exact=username, password__exact=password)
        if len(users) > 0:
            teacher = users[0]
            req.session['username'] = teacher.teacher_num
            req.session['teacher'] = True
            return HttpResponseRedirect('index.html')
        else:
            users = Student.objects.filter(stu_num__exact=username, password__exact=password)
            if len(users) > 0:
                student = users[0]
                req.session['username'] = student.stu_num
                req.session['teacher'] = False
                return HttpResponseRedirect('index.html')
            else:
                return render_to_response('login.html', {'msg': '用户名或者密码错误'})
@csrf_exempt
def register(req):
    if req.method == 'GET':
        type = req.GET.get('type')
        if type is None:
            return render_to_response('register_student.html')
        if type == 'student':
            return render_to_response('register_student.html')
        else:
            return render_to_response('register_teacher.html')
        return render_to_response('register.html', {'msg': None})
    else:
        type = req.POST.get('type')
        if type is None:
            type = 'student'
        if type == 'student':
            username = req.POST.get('username')
            name = req.POST.get('name')
            gender = req.POST.get('gender')
            password = req.POST.get('password')
            re_password = req.POST.get('re_password')
            college = req.POST.get('college')
            phone = req.POST.get('phone')
            weixin = req.POST.get('weixin')
            qq = req.POST.get('qq')
            work_location = req.POST.get('work_location')
            work_character = req.POST.get('work_character')
            if not password == re_password:
                return render_to_response('register_student.html', {'msg': '两次输入的密码不一致'})
            students = Student.objects.filter(stu_num__exact=username)
            if not len(students) == 0:
                return render_to_response('register_student.html', {'msg': '用户已经存在'})
            if gender == '' or username == '' or name == '' or password == '' or college == '' or phone == '' or weixin == '' or qq == '' or work_location == '' or work_character == '':
                return render_to_response('register_student.html', {'msg': '所有项均为必填项'})
            student_obj = Student()
            student_obj.stu_num = username
            student_obj.name = name
            student_obj.gender = int(gender)
            student_obj.password = password
            student_obj.college = college
            student_obj.phone = phone
            student_obj.weixin = weixin
            student_obj.qq = qq
            student_obj.work_location = work_location
            student_obj.work_character = work_character
            student_obj.register_time = datetime.now()
            student_obj.save()
            req.session['username'] = username
            req.session['teacher'] = False
            return HttpResponseRedirect('student.html')
        else:
            # username =
            username = req.POST.get('username')
            name = req.POST.get('name')
            password = req.POST.get('password')
            re_password = req.POST.get('re_password')
            department = req.POST.get('department')
            if not password == re_password:
                return render_to_response('register_teacher.html', {'msg': '两次输入的密码不一致'})
            teachers = Teacher.objects.filter(teacher_num__exact=username)
            if not len(teachers) == 0:
                return render_to_response('register_teacher.html', {'msg': '用户已经存在'})
            if username == '' or name == '' or password == '' or department == '':
                return render_to_response('register_teacher.html', {'msg': '所有项均为必填项'})
            teacher_obj = Teacher()
            teacher_obj.teacher_num = username
            teacher_obj.name = name
            teacher_obj.password = password
            teacher_obj.department = department
            teacher_obj.save()
            req.session['username'] = username
            req.session['teacher'] = True
            return HttpResponseRedirect('teacher.html')
        return render_to_response('register.html', {'script': '<script>alert("注册成功！");</script>'})

def index(req):
    isTeacher = req.session.get('teacher')
    if isTeacher is None:
        return HttpResponseRedirect('login.html')
    if isTeacher:
        return HttpResponseRedirect('teacher.html')
    else:
        return HttpResponseRedirect('student.html')

def logout(req):
    req.session.clear()
    return HttpResponseRedirect('login.html')

def student(req):
    page = req.GET.get('page')
    if page is None:
        page = 0
    page = int(page)
    is_teacher = req.session.get('teacher')
    student_obj = Student.objects.get(stu_num__exact=req.session.get('username'))
    if is_teacher is None:
        return HttpResponseRedirect('login.html')
    if is_teacher:
        return HttpResponseRedirect('teacher.html')
    teachers = Teacher.objects.all()
    f = datetime(2000, 1, 1, 0, 0)
    t = datetime(2000, 1, 2, 0, 0)
    signs = Sign.objects.filter(sign_off_time__range=(f, t))
    sign = None
    ts = sign

    if len(signs) > 0:
        sign = signs[0]
        ts = time.mktime(sign.sign_in_time.timetuple())
        ts = int(ts)
        sysstr = platform.system()
        if (sysstr == "Windows"):
            ts = ts + 8 * 60 * 60
    page_size = 10
    f = datetime(2001, 1, 1, 0, 0, 26, 423063)
    t = datetime.now()
    signs = Sign.objects.order_by('-id').filter(student__exact=student_obj, sign_off_time__range=(f, t))[page*page_size: page*page_size + page_size]
    sign_size = len(Sign.objects.all())
    page_range = int((sign_size + page_size - 1)/page_size)

    return render_to_response('student.html', {'teachers': teachers, 'sign': sign, 'ts': ts, 'student': student_obj, 'page': page, 'page_range': range(page_range), 'page_end': page_range-1, 'signs':signs})

def teacher(req):
    is_teacher = req.session.get('teacher')
    if is_teacher is None:
        return HttpResponseRedirect('login.html')
    if not is_teacher:
        return HttpResponseRedirect('student.html')
    return render_to_response('teacher.html')

@csrf_exempt
def sign_in(req):
    try:
        student_obj = Student.objects.get(stu_num__exact=req.session.get('username'))
        f = datetime(2000, 1, 1, 0, 0)
        t = datetime(2000, 1, 2, 0, 0)
        signs = Sign.objects.filter(sign_off_time__range=(f,t))
        if len(signs) == 0:
            teacher_num = req.POST.get('teacher_num')
            teachers = Teacher.objects.filter(teacher_num__exact=teacher_num)
            teacher_obj = teachers[0]
            sign = Sign()
            sign.teacher = teacher_obj
            sign.student = student_obj
            sign.sign_in_time = datetime.now()
            sign.sign_off_time = '2000-1-1 8:0:0.0'
            sign.save()
    except:
        pass
    return render_to_response('black.html', {'msg': '签到成功', 'location': 'student.html'})
@csrf_exempt
def sign_off(req):
    remark = req.POST.get('remark')
    try:
        student_obj = Student.objects.get(stu_num__exact=req.session.get('username'))
        f = datetime(2000, 1, 1, 0, 0)
        t = datetime(2000, 1, 2, 0, 0)
        signs = Sign.objects.filter(sign_off_time__range=(f, t))
        if not len(signs) == 0:

            sign = signs[0]
            sign.sign_off_time = datetime.now()
            sign.remark = remark
            sign.save()
    except:
        pass
    return render_to_response('black.html', {'msg': '签离成功', 'location': 'student.html'})

