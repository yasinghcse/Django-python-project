# Import necessary classes
from django.db.models.functions.base import Coalesce
from django.http import HttpResponse, response
from myapp.models import Author, Book, Course, Topic, Student
from myapp.forms import TopicForm, InterestForm, StudentForm
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



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
def index(request):
    courselist = Course.objects.all().order_by('title')[:10]
    return render(request, 'myapp/index.html', {'courselist': courselist,'request.user':request.user })


#create view for about page
#def about(request):
#    response = HttpResponse()
#    heading= '<p>'+'This is a Course List App'+'</p>'
#    response.write(heading)
#   return response

# new about page using url namespacing
def about(request):
    return render(request, 'myapp/about.html', {'request.user':request.user})

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
#@login_required
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