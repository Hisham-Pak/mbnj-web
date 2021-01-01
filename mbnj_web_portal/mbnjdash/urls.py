from django.urls import path, re_path
from mbnjdash import views

#TEMPLATE TAGGING
app_name = 'mbnjdash'

urlpatterns =[
        path('mbnjdash/dashboard/', views.dashboard, name='dashboard'),

]
