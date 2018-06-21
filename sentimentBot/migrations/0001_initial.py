# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-21 14:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TwitchChannel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='TwitchChatWordPositivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('positivity', models.FloatField()),
                ('word', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='TwitchEmote',
            fields=[
                ('twitchchatwordpositivity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sentimentBot.TwitchChatWordPositivity')),
                ('channel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sentimentBot.TwitchChannel')),
            ],
            bases=('sentimentBot.twitchchatwordpositivity',),
        ),
    ]
