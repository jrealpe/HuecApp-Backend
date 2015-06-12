# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('evaluation', models.PositiveSmallIntegerField()),
                ('category', models.ForeignKey(related_name='evaluations', to='web.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('place', models.CharField(max_length=128)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
            ],
            options={
                'verbose_name': 'Restaurante',
                'verbose_name_plural': 'Restaurantes',
            },
        ),
        migrations.CreateModel(
            name='RestaurantDish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(max_digits=10, decimal_places=3)),
                ('dish', models.ForeignKey(to='web.Dish')),
                ('restaurant', models.ForeignKey(to='web.Restaurant')),
            ],
        ),
        migrations.AddField(
            model_name='evaluation',
            name='restaurantdish',
            field=models.ForeignKey(related_name='evaluations', to='web.RestaurantDish'),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='user',
            field=models.ForeignKey(related_name='evaluations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dish',
            name='restaurant',
            field=models.ManyToManyField(to='web.Restaurant', through='web.RestaurantDish'),
        ),
    ]
