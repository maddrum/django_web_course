# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-28 07:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0006_auto_20180928_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpredictions',
            name='predicted_match_state',
            field=models.CharField(choices=[('home', 'Home Team Wins'), ('away', 'Guest Team Wins'), ('tie', 'Tie')], default='home', max_length=10),
        ),
    ]