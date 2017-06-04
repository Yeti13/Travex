# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
import datetime

# Create your models here.
EMAILREG = re.compile(r'^[a-zA-Z0-9.+-_]+@[a-zA-Z0-9._-]+\.[a-zA-Z]*$')
PASSWORD_REGEX = re.compile(r'^(?=.*[^a-zA-Z])(?=.*[a-z])(?=.*[A-Z])\S{8,255}$')

class UserManager(models.Manager):

    def login(self, data):
        error = []
        user = Users.objects.get(email=data['logmail'])
        if data['logmail'] != user.email or bcrypt.hashpw(data['passlog'].encode(), user.password.encode()) != user.password:
            error.append(["login", "Invalid email or password."])
        if error:
            print error
            return [False, error]
        else:
            return[True, user]

    def register(self, data):
        error = []
        # validate name and username
        if len(data['name']) < 1:
            error.append(["name", "First name is required."])
        if len(data['user_name']) < 1:
            error.append(["user_name", "Last name is required."])
        uName_check = Users.objects.filter(user_name=data['user_name'])
        if uName_check:
            error.append(["user_name", "Username already registered."])
        # validate email
        if len(data['email']) < 1:
            error.append(["email", "Email is required."])
        elif not EMAILREG.match(data['email']):
            error.append(["email", "Invalid email."])
        DB_check = Users.objects.filter(email=data['email'])
        if DB_check:
            error.append(["email", "Email already registered."])
        # validate password
        if len(data['password']) < 1:
            error.append(["password", "Password is required."])
        elif not PASSWORD_REGEX.match(data['password']):
            error.append(["password", "Invalid password."])

        if data['password'] != data['confirm']:
            error.append(["confirm", "Password and password confirmation must match."])
        if error:
            return [False, error]

        else:
            hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt())
            user = Users(name=data['name'], user_name=data['user_name'], email=data['email'], password=hashed)
            user.save()

            return [True, user]

class Users(models.Model):
    name = models.CharField(max_length=45)
    user_name = models.CharField(max_length=45)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class TripManager(models.Manager):

    def create_new(self, data, user_id, founder):
        error = []
        if len(data['destination']) < 1 or len(data['description']) < 1 or len(data['start']) < 1 or len(data['end']) < 1:
            error.append(["new_trip", "All fields are required."])
        if data['end'] < data['start']:
            error.append(["new_trip", "End date cannot be before Start date."])
            print error
        if error:
            return [False, error]
        else:
            newTrip = Trips.objects.create(founder=founder, destination=data['destination'], description=data['description'], start_date=data['start'], end_date=data['end'])
            newTrip.save()
            newTrip.user.add(user_id.id)
            newTrip.save()
            return [True, newTrip]

    def join(self, id, user_id):
        trip_join = Trips.objects.get(id=id)
        user_join = Users.objects.get(id=user_id.id)
        trip_join.user.add(user_join)

class Trips(models.Model):
    founder = models.CharField(max_length=45, null=True)
    destination = models.CharField(max_length=45)
    description = models.CharField(max_length=255)
    start_date = models.CharField(max_length=45)
    end_date = models.CharField(max_length=45)
    user = models.ManyToManyField(Users, related_name="trip_user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return 'dest: %s | desc: %s | user: %s' % (self.destination, self.description, self.user)

    objects = TripManager()
