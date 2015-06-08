from rest_framework import serializers
from web.models import *

#class UsuarioSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Usuario
#        fields = ('id','username', 'password',)
class RestaurantSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Restaurant
        fields = ('id', 'name', 'place', 'longitude', 'latitude')

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('id', 'name')

class RestaurantDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantDish
        fields = ('id', 'restaurant', 'dish', 'price')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ('id', 'user', 'restaurantdish', 'category', 'evaluation')



