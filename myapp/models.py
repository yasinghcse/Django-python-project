from django.db import models
import datetime
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator



# Create your models here.

class Author(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    birthdate = models.DateField()
    #age = models.IntegerField()
    city=models.CharField(max_length=20, null=True, blank=True)
    def __str__(self):
        return str(self.id)



class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author)
    in_stock = models.BooleanField(default=True)
    numpages= models.IntegerField(default=0, validators=[MaxValueValidator(1000), MinValueValidator(50)])
    def __str__(self):
        return str(self.id)


class Student(User):
    PROVINCE_CHOICES = (
        ('AB','Alberta'), # First value is stored in db, the second is descriptive
        ('MB', 'Manitoba'),
        ('ON', 'Ontario'),
        ('QC', 'Quebec'),
    )
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=20, default='Windsor')
    province=models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    age = models.IntegerField(default=20)
    stud_pic = models.ImageField(upload_to='myapp/pictures/', default='myapp/pictures/None/profile.jpg')
    def __str__(self):
        return self.first_name

#course table
class Course(models.Model):
    course_no = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100, default="courseTitle")
    textbook = models.ForeignKey(Book,null=True, blank=True)
    students = models.ManyToManyField(Student)
    def __str__(self):
        return str(self.course_no)


#topic
class Topic(models.Model):
    subject = models.CharField(max_length=100, unique=True)
    intro_course = models.BooleanField(default=True)
    NO_PREFERENCE = 0
    MORNING = 1
    AFTERNOON = 2
    EVENING = 3
    TIME_CHOICES = (
        (0, 'No preference'),
        (1, 'Morning'),
        (2, 'Afternoon'),
        (3, 'Evening')
    )
    time = models.IntegerField(default=0, choices=TIME_CHOICES)
    num_responses = models.IntegerField(default=0)
    avg_age =models.IntegerField(default=20)
    def __str__(self):
        return str(self.subject)


# Page hit Db - not currently in use
class PageHitCount(models.Model):
    count= models.IntegerField(default=0)
    def __str__(self):
        return str(self.count)