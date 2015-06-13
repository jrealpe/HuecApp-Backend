from rest_framework import serializers
from web.models import *

from push_notifications.models import GCMDevice

class GCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GCMDevice
        #field = ('name','is_active'.'user','device_id','registration_id')
        field = ('objects','device_id','registration_id')

#class UsuarioSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Usuario
#        fields = ('id','username', 'password',)
class RestaurantSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Restaurant
        fields = ('id', 'name', 'place', 'longitude', 'latitude', 'image_restaurant')

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('id', 'name')

class RestaurantDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantDish
        fields = ('id', 'restaurant', 'dish', 'price', 'image_dish')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ('id', 'user', 'restaurantdish', 'category', 'evaluation')



