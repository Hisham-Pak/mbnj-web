from django import forms
from django.contrib.auth.models import User
from django.contrib.admin.widgets import AdminDateWidget

'''
from mbnjattend.models import (Course, Faculty, Grade, Information,
                                Performance, Roster, Student, Transaction)
'''
from mbnjattend.models import (Course, Grade, Information,
                                Profile, Roster, Transaction)
'''
class NewStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ()
'''
class NewUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ( 'first_name', 'last_name','username', 'email', 'password',)

class NewProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'usertype', 'userid', 'useridtype')


class AbsenceForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Profile.objects.all(), label='Student')
    date = forms.DateField(widget = forms.SelectDateWidget(), label='Absence Date')
    comment = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":50}), required=False)
