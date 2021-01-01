from django.urls import path, re_path
from mbnjattend import views

#TEMPLATE TAGGING
app_name = 'mbnjattend'

urlpatterns =[
        path('mbnjattend/<int:pk>/submit/', views.attend_submit, name='submit'),
        path('mbnjattend/<int:pk>/', views.check_attend, name='attend_check'),
        #path('mbnjattend/<int:year>/', views.select_year, name='year'),
        #path('mbnjattend/dashboard/', views.dashboard, name='dashboard'),
        path('mbnjattend/absence', views.absence, name='absence'),
        path('mbnjattend/', views.select_class, name='sel_class'),
]
