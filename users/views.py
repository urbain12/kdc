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
import math
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q


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


def Dashboard(request):
    alllist = len(Appointment.objects.all())
    return render(
        request,
        "admin/dashboard.html",
        {
            "alllist": alllist,
        },
    )

def kdclogin(request):
    if request.method == "POST":
        user = authenticate(
            email=request.POST["email"], password=request.POST["password"]
        )
        if user is not None:
            django_login(request, user)
            return redirect("Dashboard")
        else:
            return render(
                request,
                "admin/login.html",
                {"error": "Your Email or Password are incorrect. "},
            )
    else:
        return render(request, "admin/login.html")
    
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
        new_appointment.message = request.POST["message"]
        new_appointment.save()
        return redirect("successmsg")
    else:
        return render(request, "index.html")
    


def appointments_list(request):
    appointments = Appointment.objects.all()
    search_query = request.GET.get("search", "")
    if search_query:
        appointments = Appointment.objects.filter(Q(names__icontains=search_query))
    paginator = Paginator(appointments, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "admin/dashboardapp.html", {"appointments": appointments, "page_obj": page_obj})