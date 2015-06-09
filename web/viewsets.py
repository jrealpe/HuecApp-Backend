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

    def get_queryset(self):
        queryset = RestaurantDish.objects.all()
        restaurant = self.request.query_params.get('restaurant', None)
        if restaurant is not None:
            queryset = queryset.filter(restaurant=restaurant)
        return queryset

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class EvaluationViewSet(viewsets.ModelViewSet):
    serializer_class = EvaluationSerializer
    queryset = Evaluation.objects.all()

    def get_queryset(self):
        queryset = Evaluation.objects.all()
        restaurantdish = self.request.query_params.get('restaurantdish', None)
        user = self.request.query_params.get('username', None)
        if user is not None:
            queryset = queryset.filter(user__username = username)
        if restaurantdish is not None:
            queryset = queryset.filter(restaurantdish = restaurantdish)
        return queryset

