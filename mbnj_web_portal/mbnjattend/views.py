from django.shortcuts import render
from django.db import transaction
from django.db.models import Avg
from datetime import datetime, date, time
import pytz

from mbnjattend.models import (Course, Grade, Information,
                                Profile, Roster, Schoolyear, Transaction)

from mbnjattend.forms import NewProfileForm, NewUserForm, AbsenceForm
# Create your views here.
from django.views.generic import (ListView, CreateView, DetailView,
                                  UpdateView, TemplateView)
from mbnjattend import forms, models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import redirect

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


def index(request):
    user = request.user
    return render(request, 'index.html',)

@login_required
@user_passes_test(is_faculty)
#@permission_required('profile.teacher_view')
def load_attend(request):
    years = Schoolyear.objects.all()
    return render(request, 'mbnjattend/attend_splash.html', {'years':years})

@login_required
def absence(request):
    form = forms.AbsenceForm()
    if request.method == 'POST':
        form =forms.AbsenceForm(request.POST)
        if form.is_valid():
            return render(request, 'mbnjattend/submit_absence.html')
    return render(request, 'mbnjattend/absence.html', {'form':form})


@login_required
@user_passes_test(is_faculty)
def check_attend(request, pk):
    year = Schoolyear.objects.filter(curyear=True)[0]
    roster = Roster.objects.filter(course=pk)
    today_min = datetime.combine(date.today(), datetime.min.time()).replace(tzinfo=pytz.UTC)
    today_max = datetime.combine(date.today(), datetime.max.time()).replace(tzinfo=pytz.UTC)
    print(today_min, today_max)
    stu_list = []
    abs_list = []
    tar_list = []
    par_list = []
    inf_list = []
    for r in roster:

        trans = Transaction.objects.filter(student=r.student,
                                           transdate__range=(today_min, today_max))
        try:
            if trans[0].type == 'absent':
                abs_list.append('checked')
                tar_list.append(None)
                par_list.append(None)
            if trans[0].type == 'tardy':
                tar_list.append('checked')
                abs_list.append(None)
                par_list.append(None)
            if trans[0].type == 'partial':
                par_list.append('checked')
                abs_list.append(None)
                tar_list.append(None)
            if trans[0].status == 'informed':
                inf_list.append('checked')
            else:
                inf_list.append(None)
        except:
            abs_list.append(None)
            tar_list.append(None)
            par_list.append(None)
            inf_list.append(None)

        student = Profile.objects.get(id=r.student.id)
        stu_list.append(student)
    zipped = zip(stu_list, abs_list, tar_list, par_list, inf_list)
    #print(len(stu_list), len(abs_list), len(tar_list), len(par_list), len(inf_list))
    return render(request, 'mbnjattend/attend_check.html',
                                {'zipped':zipped, 'student':stu_list,
                                 'year':year.hijriyear, 'id':pk})


def user_register(request):
    print('I got to register page')
    registered = False
    if request.method == 'POST':
        user_form = NewUserForm(data=request.POST)
        if user_form.is_valid():
            print('both forms valid')
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            print('The user id is ', user.id)
            #profile_form.user = user
            registered = True
            print(registered)
        else:
            print('error found')
            print(user_form.errors)
    else:
        print('I got lost here')
        user_form = NewUserForm()
    return render(request, 'register.html', { 'user_form':user_form,
                                              'registered':registered} )


def user_login(request):
    print('I got into user login')
    if request.method == 'POST':
        username=request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                return HttpResponse('Account is not active')
        else:
            print('Someone tried to login and failed')
            print('Username: {} and password {}'.format(username, password))
            return HttpResponse('Invalid login details supplied!')
    else:
        return render(request, 'login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return redirect('index')


@login_required
@user_passes_test(is_faculty)
def attend_submit(request, pk):
    if request.method == 'POST':
        absent = request.POST.getlist('absent[]')
        partial = request.POST.getlist('partial[]')
        tardy = request.POST.getlist('tardy[]')
        informed = request.POST.getlist('informed[]')

        roster = Roster.objects.filter(course=pk)
        print('The roster is ', roster)
        today_min = datetime.combine(date.today(), datetime.min.time()).replace(tzinfo=pytz.UTC)
        today_max = datetime.combine(date.today(), datetime.max.time()).replace(tzinfo=pytz.UTC)

        print(request.user, absent, informed, partial, tardy)
        for stu in roster:
            stid = str(stu.student.id)
            inf='informed' if stid in informed else None
            print(inf)
            if stid in absent:
                attype = 'absent'
            elif stid in partial:
                attype = 'partial'
            elif stid in tardy:
                attype = 'tardy'
            else:
                attype = 'present'

            if attype != 'present':
                profile = Profile.objects.get(id=stu.student.id)
                print(stu.student.id,attype)
                #add code to check if user is an admin
                year = Schoolyear.objects.get(curyear=True)
                t = Transaction.objects.filter(student=profile,
                                            transdate__range=(today_min, today_max))
                if t:
                    t[0].type = attype
                    t[0].status=inf
                    t[0].transdate= datetime.now().replace(tzinfo=pytz.UTC)
                    t[0].save()
                else:
                    t = Transaction.objects.create(type=attype,
                                               status=inf,
                                               student=profile,
                                               admin=request.user,
                                               transdate=datetime.now().replace(tzinfo=pytz.UTC),
                                               hijriyear=year)
        print('transactions added successfully')
    return render(request,'mbnjattend/submit.html')


@login_required
@user_passes_test(is_faculty)
def select_class(request):
    year = Schoolyear.objects.get(curyear = True)
    courses = Course.objects.filter(hijriyear__hijriyear=year.hijriyear)
    return render(request, 'mbnjattend/courses.html',{'year':year, 'courses':courses})
