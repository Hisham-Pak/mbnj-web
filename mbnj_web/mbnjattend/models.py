from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import RegexValidator


# Create your models here.
gender_choices = (('male','Male'),('female', 'Female'))
mbrid_choices = (('its', 'ITS'), ('other', 'Other'))
usertype_choices = (('student', 'Student'),
                    ('teacher', 'Teacher'),
                    ('committee', 'Committee'),
                    ('head moallim', 'Head Moallim'),
                    ('parent', 'Parent'))
state_choices = (('de', 'DE'), ('nj', 'NJ'), ('ny', 'NY'), ('pa', 'PA'))


class Course(models.Model):
    name = models.CharField(max_length = 90, verbose_name='Course Name')
    catnum = models.CharField(max_length = 90, verbose_name='Catalog Number', null=True, blank=True)
    desc = models.CharField(max_length = 255, verbose_name='Course Description', null=True, blank=True)
    hijriyear = models.ForeignKey('Schoolyear', on_delete=models.CASCADE, verbose_name='Year Hijri')
    grade = models.ForeignKey('Grade', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name) + '|' + str(self.grade) + '|' + str(self.hijriyear)


class Grade(models.Model):
    name = models.CharField(max_length = 90, verbose_name='Grade')
    desc = models.CharField(max_length = 255, verbose_name='Description', null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Information(models.Model):
    infotype = models.CharField(max_length = 90, verbose_name='Type')
    desc = models.CharField(max_length = 90, verbose_name='Description', null=True, blank=True)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.infotype)


class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    usertype = models.CharField(max_length = 90, choices=usertype_choices, verbose_name='Profile Type')
    userid = models.CharField(max_length = 90, verbose_name='User ID', unique=True)
    useridtype = models.CharField(max_length = 90, choices = mbrid_choices, verbose_name='ID Type')
    address = models.CharField(max_length = 255, verbose_name='Address')
    addressln2 = models.CharField(max_length = 255, verbose_name='Address Line 2', null=True, blank=True)
    city = models.CharField(max_length = 90, verbose_name='City')
    state = models.CharField(max_length = 90, choices=state_choices, verbose_name='State')
    zipcode = models.CharField(max_length=5, validators=[RegexValidator(r'^\d{1,10}$')], verbose_name='Zipcode')
    gender = models.CharField(max_length = 90, choices=gender_choices, verbose_name='Gender')
    phone = models.CharField(max_length = 90, verbose_name='Phone', null=True, blank=True)
    status = models.CharField(max_length=90, verbose_name='Status')
    dob = models.DateField(verbose_name = 'Date of Birth')
    rollnbr = models.IntegerField(verbose_name='Roll Number', null=True, blank=True)

    def __str__(self):
        return str(self.user.last_name) + ', ' + str(self.user.first_name)


class Roster(models.Model):
    student = models.ForeignKey('Profile', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.course) + '|' + str(self.student)


class Schedule(models.Model):

    sch_choices = (('','----'), ('ramadan', 'Ramadan'),
                   ('early_dismissal', 'Early dismissal'),
                   ('modified', 'Modified'), ('other', 'Other'),
                   ('cancelled', 'Cancelled'), ('special', 'Special'))

    date = models.DateField(verbose_name='Madrassah Date')
    schtype = models.CharField(max_length=90, choices=sch_choices,
                                verbose_name='Schedule', null=True, blank=True)
    comment = models.CharField(max_length=255, verbose_name='Comments',
                                null=True, blank=True)
    hijriyear = models.ForeignKey('Schoolyear', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date)

class Schoolyear(models.Model):
    hijriyear = models.CharField(max_length=4, validators=[RegexValidator(r'^\d{1,10}$')], verbose_name='Year Hijri')
    gregyear = models.CharField(max_length=4, validators=[RegexValidator(r'^\d{1,10}$')], verbose_name='Year AD')
    curyear = models.BooleanField(verbose_name='Current Year')

    def __str__(self):
        return str(self.hijriyear)


class Transaction(models.Model):
    type = models.CharField(max_length = 90, verbose_name='Type')
    transdate = models.DateTimeField(verbose_name='Transaction Date')
    status = models.CharField(max_length = 90, verbose_name='Status', blank=True, null=True)
    desc = models.CharField(max_length = 90, verbose_name='Description', blank=True, null=True)
    student = models.ForeignKey('Profile', on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Evaluator')
    hijriyear = models.ForeignKey('Schoolyear', on_delete=models.CASCADE, verbose_name='Year Hijri')

    def __str__(self):
        return str(self.type) + '|' + str(self.student)
