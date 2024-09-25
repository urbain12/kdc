from django.urls import path, include
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', index, name='index'),
    path('successmsg/', successmsg, name='successmsg'),
    path('Dashboard/', Dashboard, name='Dashboard'),
    path('new_result/', new_result, name='new_result'),
    path('kdclogin/', kdclogin, name='kdclogin'),
    path('kdclogout/', kdclogout, name='kdclogout'),
    path('add_appointment/', add_appointment, name='add_appointment'),
    path('send_result/', send_result, name='send_result'),
    path('appointments_list/', appointments_list, name='appointments_list'),
    path('cancel/<int:appointmentID>',cancel,name="cancel"),
    path('cancel_page/<int:appointmentID>',cancel_page,name="cancel_page"),
    path('cancelled/',cancelled,name="cancelled"),
    path('reminder/<int:Appointmentid>',reminder,name="reminder"),
    path('confirm/<int:appointmentID>',confirm,name="confirm"),
    path('result_list/', result_list, name='result_list'),
    path('resend/<int:Resultid>',resendresult,name="resend"),
    path('confirm_page/<int:appointmentID>',confirm_page,name="confirm_page"),

]