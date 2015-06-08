from web.models import *
from web.serializers import *
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import generics

class RestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()

class DishViewSet(viewsets.ModelViewSet):
    serializer_class = DishSerializer
    queryset = Dish.objects.all()


class RestaurantDishViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantDishSerializer
    queryset = RestaurantDish.objects.all()

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class EvaluationViewSet(viewsets.ModelViewSet):
    serializer_class = EvaluationSerializer
    queryset = Evaluation.objects.all()


