from django.shortcuts import render_to_response, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from web.models import Student, Teacher, Sign
from datetime import datetime

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
            if username == '' or name == '' or password == '' or college == '' or phone == '' or weixin == '' or qq == '' or work_location == '' or work_character == '':
                return render_to_response('register_student.html', {'msg': '所有项均为必填项'})
            student_obj = Student()
            student_obj.stu_num = username
            student_obj.name = name
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
    is_teacher = req.session.get('teacher')
    if is_teacher is None:
        return HttpResponseRedirect('login.html')
    if is_teacher:
        return HttpResponseRedirect('teacher.html')

    return render_to_response('student.html')

def teacher(req):
    is_teacher = req.session.get('teacher')
    if is_teacher is None:
        return HttpResponseRedirect('login.html')
    if not is_teacher:
        return HttpResponseRedirect('student.html')
    return render_to_response('teacher.html')