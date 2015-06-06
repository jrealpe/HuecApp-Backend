from django.contrib import admin

from models import Restaurant, Dish, RestaurantDish, Category, Evaluation

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Dish)
admin.site.register(RestaurantDish)
admin.site.register(Category)
admin.site.register(Evaluation)
