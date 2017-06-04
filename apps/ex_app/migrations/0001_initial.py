# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-04 15:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trips',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('founder', models.CharField(max_length=45, null=True)),
                ('destination', models.CharField(max_length=45)),
                ('description', models.CharField(max_length=255)),
                ('start_date', models.CharField(max_length=45)),
                ('end_date', models.CharField(max_length=45)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('user_name', models.CharField(max_length=45)),
                ('email', models.CharField(max_length=60)),
                ('password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='trips',
            name='user',
            field=models.ManyToManyField(related_name='trip_user', to='ex_app.Users'),
        ),
    ]