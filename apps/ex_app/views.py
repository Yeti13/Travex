# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import Users, Trips
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'ex_app/index.html')

def login(request):
    if request.method == 'POST':
        response = Users.objects.login(request.POST)
        if not response[0]:
            for error in response[1]:
                messages.error(request, error[1])
            return redirect('/')
        else:
            request.session['user'] = {
                "id": response[1].id,
                "name": response[1].name,
                "user_name": response[1].user_name,
            }
            return redirect('/home')

def register(request):
    if request.method == 'POST':
        response = Users.objects.register(request.POST)
        if not response[0]:
            for error in response[1]:
                messages.error(request, error[1])
            return redirect('/')
        else:
            request.session['user'] = {
                "id": response[1].id,
                "name": response[1].name,
                "user_name": response[1].user_name,
            }
            return redirect('/home')

def create(request):
    return render(request, 'ex_app/create.html')

def submit(request):
    if request.method == 'POST':
        user_id = Users.objects.get(id=request.session['user']['id'])
        founder = request.session['user']['name']
        response = Trips.objects.create_new(request.POST, user_id, founder)
        if not response[0]:
            for error in response[1]:
                messages.error(request, error[1])
            return redirect('/create')
        else:
            return redirect('/home')

def details(request, id):
    context = {
        'trip_details': Trips.objects.get(id=id),
        'trip_users': Users.objects.filter(trip_user=id)
    }
    return render(request, 'ex_app/details.html', context)

def join(request, id):
    user_id = Users.objects.get(id=request.session['user']['id'])
    response = Trips.objects.join(id, user_id)
    return redirect('/home')

def logout(request):
    request.session.clear()
    return redirect('/')

def home(request):
    usertest = Users.objects.all()
    for user in usertest:
        print user.id
    print "*****"
    test = Trips.objects.all()
    for t in test:
        print t.user
    print "*****"
    context = {
        'my_trips': Trips.objects.filter(user=request.session['user']['id']),
        'all_trips': Trips.objects.exclude(user=request.session['user']['id']),
        'trip_users': Users.objects.all()
    }
    return render(request, 'ex_app/home.html', context)
