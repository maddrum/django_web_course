# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-28 07:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0005_auto_20180928_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='match_status',
            field=models.CharField(choices=[('home', 'Home Team Wins'), ('away', 'Guest Team Wins'), ('tie', 'Tie'), ('ns', 'Not Started')], default='ns', max_length=10),
        ),
        migrations.AlterField(
            model_name='userpredictions',
            name='predicted_match_state',
            field=models.CharField(choices=[('home', 'Home Team Wins'), ('away', 'Guest Team Wins'), ('tie', 'Tie'), ('ns', 'Not Started')], max_length=10),
        ),
    ]
