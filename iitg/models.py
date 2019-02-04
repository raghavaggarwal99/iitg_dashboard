from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
# Create your models here.
import datetime


class Event(models.Model):

    name=models.TextField(max_length=2000, help_text="Enter event name")

    description=models.TextField(max_length=2000, help_text="Enter description",blank=True, null=True)

    link=models.CharField(max_length=2000,blank=True,null=True)
    
    time = models.DateTimeField(default=timezone.now)

    totalTime =models.IntegerField(help_text="Enter Time required in hours to complete the work")

    def get_absolute_url(self):
        return reverse('event-detail', args=[str(self.id)])

    def __str__(self):
        return "%s" % (self.name)



class Deadline(models.Model):
    totalTime =models.DurationField(help_text="Enter Time required to complete the work")

    description=models.TextField(max_length=2000, help_text="Enter description",blank=True, null=True)

    perDone = models.IntegerField(help_text="Percentage remaining",default=0)

    deadline = models.DateTimeField(default=timezone.now)

    name=models.TextField(max_length=2000, help_text="Enter event name")


class Student(models.Model):

    user=models.OneToOneField(User, help_text="a",related_name='student',on_delete=models.CASCADE)

    rollNo=models.IntegerField(help_text="Enter your IITG roll No.")

    key=models.TextField(max_length=2000, help_text="Enter page name",blank=True, null=True)


    def __str__(self):
        return "%s" % (self.user.username)


class Page(models.Model):

    name=models.TextField(max_length=2000, help_text="Enter page name")

    description=models.TextField(max_length=2000, help_text="Enter description",blank=True, null=True)

    event = models.ManyToManyField(Event,blank=True, null=True)

    deadline = models.ManyToManyField(Deadline, help_text='Deadline of the page',blank=True, null=True)

    admins = models.ManyToManyField(Student, help_text='Select page(s) which you want to subscribe',related_name='my_pages')

    students = models.ManyToManyField(Student, help_text='Select page(s) which you want to subscribe',related_name='subscribed_pages')


    def get_absolute_url(self):
        return reverse('page_detail', args=[str(self.id)])

    def __str__(self):
        return "%s" % (self.name)




    # activeEvent=models.ForeignKey(Event, related_name="events", on_delete=models.CASCADE, help_text="a",blank=True, null=True)
