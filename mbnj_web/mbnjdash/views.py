from django.shortcuts import render
from django.db import transaction
from django.db.models import Avg, Q

from mbnjattend.models import (Course, Grade, Information,
                                Profile, Roster, Schedule, Schoolyear,
                                Transaction)

from django.views.generic import (ListView, CreateView, DetailView,
                                  UpdateView, TemplateView)
from mbnjattend import forms, models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, date, time
import pytz

#use sourcetree for code management
def is_student(user):
    return user.groups.filter(name='students').exists()

def is_teacher(user):
    return user.groups.filter(name='teachers').exists()

def is_admin(user):
    return user.groups.filter(name='committee').exists()

def is_parent(user):
    return user.groups.filter(name='parents').exists()

def is_moallim(user):
    return user.groups.filter(name='moallims').exists()

def is_faculty(user):
    return user.groups.filter(name__in=['teachers', 'committee', 'moallims']).exists()


@login_required
@user_passes_test(is_student)
def dashboard(request):
    fname = request.user.first_name
    curyear = int(Schoolyear.objects.get(curyear=True).hijriyear)
    min_date = date.min
    max_date = datetime.combine(date.today(), datetime.max.time()).replace(tzinfo=pytz.UTC)
    year_list = [x for x in range(curyear-2, curyear+1)]
    trace1 = []
    trace2 = []
    for year in year_list:
        day_count = Schedule.objects.filter(~Q(schtype='cancelled'),
                                            hijriyear__hijriyear=str(year),
                                            date__range=(min_date, max_date)).count()
        print('Total days this year= ', day_count)
        t2 = Transaction.objects.filter(hijriyear__hijriyear=str(year),
                                        type='absent').count()
        s = Profile.objects.filter(usertype='Student').count()
        trace2.append(day_count-(t2/s))
        t1 = Transaction.objects.filter(hijriyear__hijriyear=str(year),
                                        type='absent', student__user = request.user).count()
        trace1.append(day_count-t1)
        print(t1, s, t2)

    return render(request, 'mbnjdash/dashboard.html',
                                    {'fname':fname.capitalize(), 'year_list':year_list,
                                     'trace1': trace1, 'trace2':trace2,})
