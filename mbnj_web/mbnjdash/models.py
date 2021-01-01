from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Announcement(models.Model):
    chgdate = models.DateTimeField(verbose_name = 'Change Date')
    text = models.CharField(max_length = 90, verbose_name='Announcement')

    def __str__(self):
        return str(self.chgdate)


class Parental(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey('mbnjattend.Profile', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.student.last_name)


class Performance(models.Model):
    eval = models.CharField(max_length = 90, verbose_name='Exam Name')
    desc = models.CharField(max_length = 255, verbose_name='Description')
    subject = models.CharField(max_length = 90, verbose_name='Subject', blank=True, null=True)
    score = models.FloatField(blank=True, verbose_name='Score')
    totalscore = models.FloatField(blank=True, verbose_name='Possible Score')
    lettergrade = models.CharField(max_length = 2, verbose_name='Letter Grade', blank=True, null=True)
    testdate = models.DateTimeField(verbose_name='Test Date')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Evaluator')
    course = models.ForeignKey('mbnjattend.Course', on_delete=models.CASCADE)
    student = models.ForeignKey('mbnjattend.Profile', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.eval) + '|' + str(self.student.last_name)
