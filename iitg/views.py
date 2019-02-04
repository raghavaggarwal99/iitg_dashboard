from __future__ import print_function
from django.shortcuts import render

# Create your views here.
from .forms import SignUpForm,CreatePageForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .models import Student, Event, Page, Deadline
from django.db.models import Max
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from iitg import models
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('student_create')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def home(request):
    student=Student.objects.get(pk=request.user.student.id)
    return render(request, 'home.html',{'student':student})

@login_required
def my_pages(request):
    student=Student.objects.get(pk=request.user.student.id)
    return render(request, 'my_pages.html',{'student':student})


class StudentCreate(CreateView):
    model = Student
    fields=['user','rollNo']
    success_url = reverse_lazy('home')

@login_required
def page_detail(request,pk):
    page=Page.objects.get(pk=pk)
    # print(request.user)
    # print(list(page.admins.all()))
    if page.admins.filter(pk=request.user.student.id).exists():
        print("hi")
        return render(request, 'iitg/page_detail.html', {'page': page,'x':'Add an event','y':'create_event'})
    return render(request, 'iitg/page_detail.html', {'page': page,'x':'Subscribe','y':'subscribe'})

@login_required
def CreatePage(request):
    if request.method == 'POST':
        form = CreatePageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            description = form.cleaned_data.get('description')
            obj = models.Page(name= name , description=description)
            obj.save()
            user = Student.objects.get(user=request.user)
            obj.admins.add(user)
            obj.students.add(user)
            obj.save()

            return redirect('home')
    else:
        form = CreatePageForm()
    return render(request, 'page_form.html', {'form': form})


class EventCreate(CreateView):
    model = Event
    fields=['name','description','time','totalTime']
    def get_success_url(self):
        event = self.object
        print(self.kwargs)
        page=Page.objects.get(pk=self.kwargs['xy'])

        # 2018-09-27T17:00:00
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('calendar', 'v3', http=creds.authorize(Http()))
        s = str(event.time).split(' ')
        p = s[1].split(':')
        t = s[0]   +   'T'   +   str(int(p[0])+1)   +  ':'  +   ':'.join(p[1:])
        rem = {
            'summary' : event.name,
            'description' : event.description,
            'start' : {
                'dateTime' : 'T'.join(str(event.time).split(' ')),
                'timeZone' : "Asia/Kolkata",
            },
            'end' : {
                'dateTime' : t,
                'timeZone' : "Asia/Kolkata",
            },
        }
        rem = service.events().insert(calendarId='primary', body=rem).execute()
        print ('Event created: %s' % (rem.get('htmlLink')))

        event.link = rem.get('htmlLink')
        event.save()
        page.event.add(event)
        page.save()
        return reverse_lazy('home')

class DeadlineCreate(CreateView):
    model = Deadline
    fields=['name','totalTime','description','deadline']
    def get_success_url(self):
        deadline = self.object
        print(self.kwargs)
        page=Page.objects.get(pk=self.kwargs['xy'])
        page.deadline.add(deadline)
        page.save()
        return reverse_lazy('home')

class PageListView(generic.ListView):
    model=Page

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def appkey(request):
    json_data = json.loads(request.body.decode("utf-8"))
    user=User.objects.filter(email=json_data['email'])
    return JsonResponse({'key':user.first().id})

def subscribe(request,pk):
    page=Page.objects.get(pk=pk)
    page.students.add(request.user.student)
    return render(request,'subscribe.html')

def listing(request):
    events = Event.objects.annotate(
        t=Max("time")
    ).order_by("-t")
    deadlines = Deadline.objects.annotate(
        t=Max("deadline")
    ).order_by("-t")
    
    # list=[]
    # z=0
    print(list(events))
    print(deadlines)
    # cur_deadline=deadline.first()
    # answer_ids = set(answer.id for answer in events)
    # existing_question_answers = filter(lambda x: x.answer.id not in answers_id, existing_question_answers)
    # print(existing_question_answers)
    # for event in list(events):
        # while(deadline.)
    return JsonResponse({'success':'true'})

from django.core import serializers

def event_app(request):
    x=[]
    for page in request.user.student.subscribed_pages.all():
        # for event in page.event.all():
        x.append(serializers.serialize('json',page.event.all()))
    # events = request.user.student.annotate(
    #     t=Max("time")
    # ).order_by("t")
    # json_data=serializers.serialize('json',events)
    return JsonResponse({'events':x})

def deadlines_app(request):
    deadline = Deadline.objects.annotate(
        t=Max("time")
    ).order_by("t")
    json_data=serializers.serialize('json',deadline)
    return JsonResponse(json)
