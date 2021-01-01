import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mbnjadmin.settings')
import django
django.setup()
from mbnjattend.models import (Course, Grade, Information,
                                Profile, Roster, Schedule, Schoolyear, Transaction)
from mbnjdash.models import (Announcement, Performance)
from django.contrib.auth.models import Group, User
from datetime import datetime
import pytz
import csv

fp = r'C:\Users\MiM\Documents\Murtaza\Masjid\madrassah\mbnjDB'

def add_groups():
    Group.objects.create(name='committee')
    Group.objects.create(name='moallims')
    Group.objects.create(name='teachers')
    Group.objects.create(name='parents')
    Group.objects.create(name='students')

    print('add_groups_complete')


def add_years():
    Schoolyear.objects.create(hijriyear='1442', gregyear='2020', curyear=False)
    Schoolyear.objects.create(hijriyear='1441', gregyear='2019', curyear=True)
    Schoolyear.objects.create(hijriyear='1440', gregyear='2018', curyear=False)
    Schoolyear.objects.create(hijriyear='1439', gregyear='2017', curyear=False)

    print('add_years_complete')


def add_grades():
    csv_file = open(fp + r'\grades.csv', 'r')
    csv_rdr = csv.reader(csv_file)
    hdr = next(csv_rdr)
    #print('Header-->' + str(hdr))
    for row in csv_rdr:
        #print(row[0], row[1])
        Grade.objects.create(name=row[0], desc=row[1])

    print('add_grades complete')

def add_courses():
    csv_file = open(fp + r'\courses.csv', 'r')
    csv_rdr = csv.reader(csv_file)
    hdr = next(csv_rdr)
    #print('Header-->' + str(hdr))
    for row in csv_rdr:
        #print(row[0], row[1])
        hy = Schoolyear.objects.filter(curyear=True)[0]
        grd = Grade.objects.get(name=row[2])
        Course.objects.create(name=row[0], hijriyear=hy,
                                grade=grd)

    print('add_courses_complete')

def add_stu_users():
    csv_file = open(fp + r'\UpdateFrmStudents.csv', 'r')
    csv_rdr = csv.reader(csv_file)
    hdr = next(csv_rdr)

    for row in csv_rdr:
        user = User.objects.create_user(username=row[6], email=row[9],
                                        password=row[7], first_name=row[1],
                                        last_name=row[2])

    print('add_stu_users_complete')

def add_profile():
    csv_file = open(fp + r'\UpdateFrmStudents.csv', 'r')
    csv_rdr = csv.reader(csv_file)
    hdr = next(csv_rdr)

    for row in csv_rdr:
        user = User.objects.get(username=row[6])
        Profile.objects.create(user=user, usertype="student",
                                userid=row[0], useridtype=row[1],
                                address=row[10], city=row[11],
                                state=row[12], zipcode=row[13],
                                gender=row[14], phone=row[15],
                                status=row[16], dob=row[17],
                                rollnbr=row[18])

    print('add_profile_complete')

def add_roster():
    csv_file = open(fp + r'\UpdateFrmStudents.csv', 'r')
    csv_rdr = csv.reader(csv_file)
    hdr = next(csv_rdr)

    for row in csv_rdr:
        student = Profile.objects.get(user__username=row[6])
        nm=row[4]
        grd = row[5]
        grade = Grade.objects.get(name=grd)
        name=int(nm) if nm.isnumeric() else nm.replace("0","")
        course = Course.objects.get(name=name,grade=grade)
        Roster.objects.create(student=student, course=course)

    print('add_roster_complete')

def add_schedule():
    csv_file = open(fp + r'\Schedule.csv', 'r')
    csv_rdr = csv.reader(csv_file)
    hdr = next(csv_rdr)

    for row in csv_rdr:
        date = row[0]
        hyear=row[3]
        year = Schoolyear.objects.get(hijriyear=1441)
        Schedule.objects.create(date=date, hijriyear=year)

print('add_schedule_complete')

def add_attendance():
    csv_file = open(fp + r'\Attendance.csv', 'r')
    csv_rdr = csv.reader(csv_file)
    hdr = next(csv_rdr)

    for row in csv_rdr:
        inf = "informed" if row[4]==True else None
        attype = "absent" if row[3]=="A" else "present"
        if row[5] == True:
            attype = "tardy"
        if row[6] == True:
            attype = "partial"

        if attype != "present":
            try:
                student = Profile.objects.get(userid=str(row[2]))
                admin = User.objects.get(username='manaqibm')
                year = Schoolyear.objects.get(curyear=True)

                Transaction.objects.create(type=attype,
                                        status=inf,
                                        student=student,
                                        admin=admin,
                                        transdate = datetime.strptime(row[1], '%Y-%m-%d').replace(tzinfo=pytz.UTC),
                                        hijriyear=year)
                print(row, 'Transaction successful')
            except:
                print(row, 'something failed')
    print('add_attendance_complete')

if __name__ == '__main__':
    #add_groups()
    #add_years()
    #add_grades()
    #add_courses()
    #add_stu_users()
    #add_profile()
    #add_roster()
    #add_attendance()
    #add_schedule()
