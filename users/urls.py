from django.urls import path, include
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', index, name='index'),
    path('successmsg/', successmsg, name='successmsg'),
    path('Dashboard/', Dashboard, name='Dashboard'),
    path('kdclogin/', kdclogin, name='kdclogin'),
    path('kdclogout/', kdclogout, name='kdclogout'),
    path('add_appointment/', add_appointment, name='add_appointment'),
    path('appointments_list/', appointments_list, name='appointments_list'),

]