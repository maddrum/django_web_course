# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-27 12:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0003_auto_20180927_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchcomments',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_match', to='bets.Match'),
        ),
        migrations.AlterField(
            model_name='matchcomments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userextrainfo',
            name='favourite_team',
            field=models.CharField(default='No favourite team', max_length=255),
        ),
        migrations.AlterField(
            model_name='userpredictions',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prediction_match', to='bets.Match'),
        ),
        migrations.AlterField(
            model_name='userpredictions',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prediction_user', to=settings.AUTH_USER_MODEL),
        ),
    ]