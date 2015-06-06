# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Restaurant(models.Model):
    name = models.CharField(max_length=64)
    place = models.CharField(max_length=128)
    latitude = models.FloatField()
    longitude = models.FloatField()

   
    class Meta:
        verbose_name = 'Restaurante'
        verbose_name_plural = 'Restaurantes'

class Text(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        abstract = True

class Dish(Text):
    restaurant = models.ManyToManyField(Restaurant, through = 'RestaurantDish', through_fields = ('dish','restaurant'))



class RestaurantDish(models.Model):
    restaurant = models.ForeignKey(Restaurant)
    dish = models.ForeignKey(Dish)
    price = models.DecimalField(max_digits = 10, decimal_places = 3)
    


class Category(Text):
    pass

class Evaluation(models.Model):
    user = models.ForeignKey(User, related_name = 'evaluations')
    restaurantdish = models.ForeignKey(RestaurantDish, related_name = 'evaluations')
    category = models.ForeignKey(Category, related_name = 'evaluations')
    evaluation = models.PositiveSmallIntegerField()



    



