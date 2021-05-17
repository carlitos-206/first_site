import re
from django.contrib.messages.api import error
from django.shortcuts import render,redirect, HttpResponse
from .models import Register, Trip
from django.contrib import messages
import bcrypt
def index(request):
    return render(request, 'log_register.html')
def register(request):
    if request.method =='POST':
        errors = Register.objects.register_validation(request.POST)
        if len(errors) >0:
            for key, value in errors.items():
                messages.error(request, value)      
            return redirect('/')
        pw_hash=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = Register.objects.create(
            first_name=request.POST['first_name'], 
            last_name=request.POST['last_name'], 
            email=request.POST['email'], 
            password=pw_hash
            )
        request.session['register_id'] = new_user.id
        return redirect("/dashboard")
    return redirect('/')
def dashboard(request):
    if 'register_id' not in request.session:
        return redirect('/')
    this_user = Register.objects.filter(id=request.session['register_id'])
    context = {
        'user': this_user[0],
        'all_trips':Trip.objects.all()
    }
    return render(request, 'inside.html', context)
def login(request):
    if request.method=='GET':
        return redirect('/')
    if request.method == "POST":
        # errors = Register.objects.authenticate(request.POST)
        if not Register.objects.authenticate(request.POST['email'], request.POST['password']):
            messages.error(request, 'Invalid info')
            return redirect('/')
        # if len(errors) != 0:
        #     for key, value in errors.items():
        #         messages.error(request, value)
        #     return redirect('/')
        this_user = Register.objects.filter(email=request.POST['email'])
        request.session['register_id'] = this_user[0].id
    return redirect('/dashboard')

def logout(request):
    request.session.flush()
    return redirect('/')

#----TripViews---
def tripform(request):
    this_user = Register.objects.filter(id=request.session['register_id'])
    context = {
        'user': this_user[0],
        'all_trips':Trip.objects.all()
    }
    return render(request, 'tripform.html', context)
def add(request):
    errors=Trip.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/addTripForm')
    else:
        Trip.objects.create(
            name=request.POST['trip'],
            plan=request.POST['plan'],
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date']
        )
    user = Register.objects.get(id=request.session['register_id'])
    return redirect ('/dashboard')

def destroyTrip(request, trip_id):
    one_trip=Trip.objects.get(id=trip_id)
    one_trip.delete()
    return redirect('/dashboard')

def editTrip(request, trip_id):
    one_trip=Trip.objects.get(id=trip_id)
    context={
        'this_trip': one_trip
    }
    return render(request,'edit.html',context)
def update(request, trip_id):
    errors=Trip.objects.basic_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/{trip_id}/edit')
    else:
        this_user = Register.objects.filter(id=request.session['register_id'])
        update_trip=Trip.objects.get(id=trip_id)
        update_trip.name =request.POST['trip']
        update_trip.start_date=request.POST['start_date'],
        update_trip.end_date=request.POST['end_date'],
        update_trip.plan=request.POST['plan']
    return redirect('/dashboard')
def tripInfo(request, trip_id):
    user = Register.objects.get(id=request.session['register_id'])
    one_trip=Trip.objects.get(id=trip_id)
    context={
        'trip': one_trip,
        'this_user':user
    }
    return render(request, 'show.html', context)

# Create your views here.
