from django.shortcuts import render, redirect
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView,DestroyAPIView,UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import *
from django.http import Http404, HttpResponse,JsonResponse
import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
import secrets
import string
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.conf import settings
import os
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from django.utils.timezone import now
from datetime import datetime, timedelta
import pytz
import math
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import requests
from django.contrib import auth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)






from django.contrib.auth import (
    authenticate,
    logout as django_logout,
    login as django_login,
)

# Create your views here.

def index(request):
    return render(request, 'index.html')

def successmsg(request):
    return render(request, 'success.html')

def new_result(request):
    return render(request, 'useradmin/sendresult.html')


def Dashboard(request):
    allappointment = len(Appointment.objects.all())
    confirmed=len(Appointment.objects.filter(confirmed=True))
    cancelled=len(Appointment.objects.filter(rejected=True))
    pending=len(Appointment.objects.filter(rejected=False,confirmed=False))
    
    kigali_timezone = pytz.timezone('Africa/Kigali')
    current_time_kigali = datetime.now(kigali_timezone).strftime('%Y-%m-%d - %H:%M')
    return render(
        request,
        "useradmin/dashboard.html",
        {
            "allappointment": allappointment,
            'cancelled':cancelled,
            'confirmed':confirmed,
            'pending':pending,
            'current_time_kigali': current_time_kigali,

        },
    )

def kdclogin(request):
    if request.method == "POST":
        user = authenticate(
            email=request.POST["email"], 
            password=request.POST["password"]
        )
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect("Dashboard")
        else:
            return render(
                request,
                "useradmin/login.html",
                {"error": "Your Email or Password are incorrect. "},
            )
    else:
        return render(request, "useradmin/login.html")
    
def kdclogout(request):
    django_logout(request)
    return redirect("kdclogin")
    

def add_appointment(request):
    if request.method == "POST":
        new_appointment = Appointment()
        new_appointment.names = request.POST["name"]
        new_appointment.email = request.POST["email"]
        new_appointment.phone = request.POST["phone"]
        new_appointment.date = request.POST["date"]
        new_appointment.appointment_type = request.POST["appointment_type"]
        new_appointment.insurance = request.POST.get("insurance")
        new_appointment.doctor = request.POST.get("doctor")
        new_appointment.message = request.POST["message"]
        new_appointment.save()
        return redirect("successmsg")
    else:
        return render(request, "index.html")
    
def cancel_page(request,appointmentID):
    appointment=Appointment.objects.get(id=appointmentID)
    return render(request,'useradmin/cancel.html',{'appointment':appointment})
    
def cancel(request,appointmentID):
    if request.method=="POST":
        appointment=Appointment.objects.get(id=appointmentID)
        appointment.rejected=True
        appointment.confirmed=False
        appointment.reason= request.POST['reason']
        appointment.save()
        payload={'details':f'Dear {appointment.names},\nWe are sorry to inform you that your appointment at {appointment.date},{appointment.time} has been cancelled due to {request.POST["reason"]}. For rescheduling  your appointment please call +250 782 742 943 / 252 604 144','phone':f'25{appointment.phone}'}
        headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOi8vdXBjb3VudHJ5LnRpY2tldC5ydy9hcGkvbW9iaWxlL2F1dGhlbnRpY2F0ZSIsImlhdCI6MTcwMjQwMTkzMSwiZXhwIjoxNzAyNDA1NTMxLCJuYmYiOjE3MDI0MDE5MzEsImp0aSI6IkM2dkY1b3V0cXplRGg4TG4iLCJzdWIiOiIzIiwicHJ2IjoiMjNiZDVjODk0OWY2MDBhZGIzOWU3MDFjNDAwODcyZGI3YTU5NzZmNyJ9.LqRhq-8muztNIOLwyl8MDV2xXEFnXfJilwJc4E6w7og'}
        r = requests.post('http://upcountry.ticket.rw/api/send-sms-kwetu',
                      headers=headers, data=payload, verify=False)
        return redirect('cancelled')


def confirm_page(request,appointmentID):
    appointment=Appointment.objects.get(id=appointmentID)
    appointments=Appointment.objects.filter(doctor=appointment.doctor,confirmed=True)
    return render(request,'useradmin/confirm.html',{'appointments':appointments,'appointment':appointment})
    
def confirm(request,appointmentID):
    if request.method=="POST":
        appointment=Appointment.objects.get(id=appointmentID)
        appointment.doctor=request.POST["doctor"]
        appointment.date=request.POST["date"]
        appointment.time=request.POST["time"]
        appointment.rejected=False
        appointment.confirmed=True
        appointment.save()
        payload={'details':f'Dear {appointment.names},\nWe are to inform you that your appointment at {appointment.date},{appointment.time} has been confirmed.please call +250 782 742 943 / 252 604 144','phone':f'25{appointment.phone}'}
        headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOi8vdXBjb3VudHJ5LnRpY2tldC5ydy9hcGkvbW9iaWxlL2F1dGhlbnRpY2F0ZSIsImlhdCI6MTcwMjQwMTkzMSwiZXhwIjoxNzAyNDA1NTMxLCJuYmYiOjE3MDI0MDE5MzEsImp0aSI6IkM2dkY1b3V0cXplRGg4TG4iLCJzdWIiOiIzIiwicHJ2IjoiMjNiZDVjODk0OWY2MDBhZGIzOWU3MDFjNDAwODcyZGI3YTU5NzZmNyJ9.LqRhq-8muztNIOLwyl8MDV2xXEFnXfJilwJc4E6w7og'}
        r = requests.post('http://upcountry.ticket.rw/api/send-sms-kwetu',
                      headers=headers, data=payload, verify=False)
        return redirect('appointments_list')
   

def appointments_list(request):
    appointments = Appointment.objects.all()
    search_query = request.GET.get("search", "")
    if search_query:
        appointments = Appointment.objects.filter(Q(names__icontains=search_query))
        
    paginator = Paginator(appointments, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "useradmin/appointment.html", {"appointments": appointments, "page_obj": page_obj})

def cancelled(request):
    appointments = Appointment.objects.filter(rejected=True)
    search_query = request.GET.get("search", "")
    if search_query:
        appointments = Appointment.objects.filter(Q(names__icontains=search_query))
    paginator = Paginator(appointments, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "useradmin/cancelled.html", {"appointments": appointments, "page_obj": page_obj})

def reminder(request,Appointmentid):
    appointment=Appointment.objects.get(id=Appointmentid)
    payload={'details':f' Dear {appointment.names},\nThis is to remind you that you have an appointment on {appointment.date} at kdc. Please call us for any cancellation or delay through +250 782 742 943 / 252 604 144 ','phone':f'25{appointment.phone}'}
    headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOi8vdXBjb3VudHJ5LnRpY2tldC5ydy9hcGkvbW9iaWxlL2F1dGhlbnRpY2F0ZSIsImlhdCI6MTcwMjQwMTkzMSwiZXhwIjoxNzAyNDA1NTMxLCJuYmYiOjE3MDI0MDE5MzEsImp0aSI6IkM2dkY1b3V0cXplRGg4TG4iLCJzdWIiOiIzIiwicHJ2IjoiMjNiZDVjODk0OWY2MDBhZGIzOWU3MDFjNDAwODcyZGI3YTU5NzZmNyJ9.LqRhq-8muztNIOLwyl8MDV2xXEFnXfJilwJc4E6w7og'}
    r = requests.post('http://upcountry.ticket.rw/api/send-sms-kwetu',
                      headers=headers, data=payload, verify=False)
    return redirect('appointments_list')

def send_result(request):
    if request.method == "POST":
        new_result = Result()
        new_result.name = request.POST["name"]
        new_result.phonenumber = request.POST["phone"]
        new_result.fileupload = request.FILES.get("file")
        new_result.save()
        payload={'details':f'Dear {new_result.name},\n Here is your result http://127.0.0.1:8000/{new_result.fileupload.url}.','phone':f'25{new_result.phonenumber}'}
        headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOi8vdXBjb3VudHJ5LnRpY2tldC5ydy9hcGkvbW9iaWxlL2F1dGhlbnRpY2F0ZSIsImlhdCI6MTcwMjQwMTkzMSwiZXhwIjoxNzAyNDA1NTMxLCJuYmYiOjE3MDI0MDE5MzEsImp0aSI6IkM2dkY1b3V0cXplRGg4TG4iLCJzdWIiOiIzIiwicHJ2IjoiMjNiZDVjODk0OWY2MDBhZGIzOWU3MDFjNDAwODcyZGI3YTU5NzZmNyJ9.LqRhq-8muztNIOLwyl8MDV2xXEFnXfJilwJc4E6w7og'}
        r = requests.post('http://upcountry.ticket.rw/api/send-sms-kwetu',
                      headers=headers, data=payload, verify=False)
        return redirect("result_list")
    else:
        return render(request, "useradmin/dashboard.html")
    
    
def result_list(request):
    results = Result.objects.all()
    search_query = request.GET.get("search", "")
    if search_query:
        results = Result.objects.filter(Q(name__icontains=search_query))
    paginator = Paginator(results, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "useradmin/result.html", {"results": results, "page_obj": page_obj})


def resendresult(request,Resultid):
    result=Result.objects.get(id=Resultid)
    payload={'details':f'Dear {result.name},\nHere is your result http://localhost:8000/{result.fileupload.url}.','phone':f'25{result.phonenumber}'}
    headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOi8vdXBjb3VudHJ5LnRpY2tldC5ydy9hcGkvbW9iaWxlL2F1dGhlbnRpY2F0ZSIsImlhdCI6MTcwMjQwMTkzMSwiZXhwIjoxNzAyNDA1NTMxLCJuYmYiOjE3MDI0MDE5MzEsImp0aSI6IkM2dkY1b3V0cXplRGg4TG4iLCJzdWIiOiIzIiwicHJ2IjoiMjNiZDVjODk0OWY2MDBhZGIzOWU3MDFjNDAwODcyZGI3YTU5NzZmNyJ9.LqRhq-8muztNIOLwyl8MDV2xXEFnXfJilwJc4E6w7og'}
    r = requests.post('http://upcountry.ticket.rw/api/send-sms-kwetu',
                      headers=headers, data=payload, verify=False)
    return redirect('result_list')


def reminder(request,Appointmentid):
    appointment=Appointment.objects.get(id=Appointmentid)
    payload={'details':f' Dear {appointment.names},\nThis is to remind you that you have an appointment on {appointment.date},{appointment.time} at Kigali dematology center. Please call us for any cancellation or delay through +250 782 742 943 / 252 604 144 ','phone':f'25{appointment.phone}'}
    headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOi8vdXBjb3VudHJ5LnRpY2tldC5ydy9hcGkvbW9iaWxlL2F1dGhlbnRpY2F0ZSIsImlhdCI6MTcwMjQwMTkzMSwiZXhwIjoxNzAyNDA1NTMxLCJuYmYiOjE3MDI0MDE5MzEsImp0aSI6IkM2dkY1b3V0cXplRGg4TG4iLCJzdWIiOiIzIiwicHJ2IjoiMjNiZDVjODk0OWY2MDBhZGIzOWU3MDFjNDAwODcyZGI3YTU5NzZmNyJ9.LqRhq-8muztNIOLwyl8MDV2xXEFnXfJilwJc4E6w7og'}
    r = requests.post('http://upcountry.ticket.rw/api/send-sms-kwetu',headers=headers, data=payload, verify=False)
    return redirect('appointments_list')