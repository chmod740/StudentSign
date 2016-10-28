from django.shortcuts import render_to_response, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from web.models import Student, Teacher, Sign

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
            name = req.POST.eget('name')

        else:
            pass
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