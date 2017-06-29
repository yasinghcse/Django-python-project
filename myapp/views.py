# Import necessary classes
from django.db.models.functions.base import Coalesce
from django.http import HttpResponse, response
from myapp.models import Author, Book, Course, Topic, Student, PageHitCount
from myapp.forms import TopicForm, InterestForm, StudentForm, PageHitCountForm, ForgetPwdForm, ModifyPwdForm
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
import smtplib

from datetime import datetime



# Create your views here.
#def index(request):
#    courselist = Course.objects.all() [:10]
#    response = HttpResponse()
#    heading1 = '<p>' + 'List of courses: ' + '</p>'
#    response.write(heading1)
#    for course in courselist:
#        para = '<p>' + str(course) + '</p>'
#        response.write(para)

#    authorlist = Author.objects.all().order_by('-birthdate')[:5]
#    heading1 = '<p>' + 'List of authors: ' + '</p>'
#    response.write(heading1)
#    for author in authorlist:
#        para = '<p>' + str(author) + '</p>'
#        response.write(para)
#   return response

# new index function using templates
#def index(request):
#    courselist = Course.objects.all().order_by('title')[:10]
#    return render(request, 'myapp/index.html', {'courselist': courselist,'request.user':request.user })

hitcount=1
class IndexView(View):

    def get(self,request):
        #hitcount=int(request.COOKIES.get('visited',0))+1
        global hitcount
        courselist = Course.objects.all().order_by('title')[:10]
        if  request.session.has_key('hitcount'):
            print("no need to increment the counter")
        else:
            request.session['hitcount']=1
            hitcount+=1

        return render(request, 'myapp/index.html', {'courselist': courselist, 'request.user': request.user, 'hitcount':hitcount})


#create view for about page
#def about(request):
#    response = HttpResponse()
#    heading= '<p>'+'This is a Course List App'+'</p>'
#    response.write(heading)
#   return response

# new about page using url namespacing
#def about(request):
#    return render(request, 'myapp/about.html', {'request.user':request.user})
class AboutView(View):
    def get(self, request):
        return render(request, 'myapp/about.html', {'request.user': request.user})


#create view for detail page
#def detail(request,course_no):
#    response = HttpResponse()
#    courseList=get_object_or_404(Course,course_no=course_no)
#    #courseList=Course.objects.get(course_no=course_no)
#    para = '<p>' + str(courseList.title) + ' ' + str(courseList.course_no) + ' ' + str(courseList.textbook.title)+'</p>'
#    response.write(para)
#    return response

#new detail page
def detail(request,course_no):
    course = get_object_or_404(Course, course_no=course_no)
    return render(request, 'myapp/detail.html', {'course':course,'request.user':request.user})


#topic page
def topics(request):
    topiclist = Topic.objects.all()[:10]
    return render(request, 'myapp/topic.html',{'topiclist':   topiclist,'request.user':request.user})

#add topic
def addtopic(request):
    topiclist = Topic.objects.all()
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.num_responses = 1
            topic.save()
        return HttpResponseRedirect(reverse('myapp:topics'))
    else:
        form = TopicForm()
        return render(request, 'myapp/addtopic.html', {'form': form,'topiclist': topiclist,'request.user':request.user})

#topic details
def topicdetail(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if(form.cleaned_data['interested'] == 1):
                topic.avg_age =((topic.avg_age * topic.num_responses)+(form.cleaned_data['age']))/(topic.num_responses + 1)
                topic.num_responses = topic.num_responses + 1
                topic.save()
        return HttpResponseRedirect(reverse('myapp:topics'))
    else:
        form = InterestForm()
        return render(request, 'myapp/topicdetail.html', {'form': form,'topic': topic,'request.user':request.user})

#add student
def register(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
        return HttpResponseRedirect(reverse('myapp:topics'))
    else:
        form = StudentForm()
        return render(request, 'myapp/register.html', {'form': form,'request.user':request.user})

#authenticate user
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('myapp:index')) #
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html',{'request.user':request.user})

#logout func
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))

#MyCourses
def mycourses(request):
    if request.user.is_authenticated():
        student= Student.objects.filter(username=request.user)
        if student:
            courselist=Course.objects.filter(students=student)
            return render(request, 'myapp/mycourses.html', {'courselist':courselist,'request.user': request.user})
        else:
            return render(request, 'myapp/mycourses.html', {'request.user': request.user})
    else:
        return render(request, 'myapp/login.html', {'request.user': request.user})


def ForgetPwdView(request):
    if request.method == 'POST':
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            username = request.POST.get("username", "")
            email = request.POST.get("email", "")
            u = Student.objects.filter(username=username, email=email)
            print(u)
            if u:
                modify_form = ModifyPwdForm()
                return render(request, "myapp/password_reset.html", {"modify_form": modify_form, "email": email, 'username':username})
            else:
                forget_form = ForgetPwdForm()
                return render(request, "myapp/forgetpwd.html", {"forget_form": forget_form})
        else:
            forget_form = ForgetPwdForm()
            return render(request, "myapp/forgetpwd.html", {"forget_form": forget_form})
    else:
        forget_form = ForgetPwdForm()
        return render(request, "myapp/forgetpwd.html", {"forget_form": forget_form})


def ModifyPwdView(request):
    if request.method == 'POST':
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            username = request.POST.get("username", "")
            if pwd1 != pwd2:
                return render(request, "myapp/password_reset.html", {"email": email, "msg": u"Please insert the same password."})
            user = Student.objects.get(username=username,email=email)
            user.password = make_password(pwd1)
            user.save()

            smtp = smtplib.SMTP('smtp.gmail.com:587')
            smtp.starttls()
            smtp.login('team531uwin@gmail.com', 'test1234567890')
            resetMsg='Password is here.'+ pwd1
            smtp.sendmail('team531uwin@gmail.com', email, resetMsg)
            smtp.close()
            return render(request, "myapp/login.html")
        else:
            return render(request, "myapp/login.html")
    else:
        modify_form = ModifyPwdForm()
        return render(request, "myapp/password_reset.html", {"modify_form": modify_form})
