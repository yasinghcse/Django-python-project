# Import necessary classes
from django.db.models.functions.base import Coalesce
from django.http import HttpResponse, response
from myapp.models import Author, Book, Course, Topic
from myapp.forms import TopicForm, InterestForm
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse



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
    return render(request, 'myapp/index.html', {'courselist': courselist})


#create view for about page
#def about(request):
#    response = HttpResponse()
#    heading= '<p>'+'This is a Course List App'+'</p>'
#    response.write(heading)
#   return response

# new about page using url namespacing
def about(request):
    return render(request, 'myapp/about.html', {})

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
    return render(request, 'myapp/detail.html', {'course':course})


#topic page
def topics(request):
    topiclist = Topic.objects.all()[:10]
    return render(request, 'myapp/topic.html',{'topiclist':   topiclist})

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
        return render(request, 'myapp/addtopic.html', {'form': form,'topiclist': topiclist})

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
        return render(request, 'myapp/topicdetail.html', {'form': form,'topic': topic})
