from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden
from web.models import *
# Create your views here.

#@login_required
def getTop(request):
    if request.method == 'GET':
        try:
            category = request.GET['category']
        except:
            category = None
        if category is None:
            query = 'SELECT web_restaurantdish.* FROM\
                    (SELECT DISTINCT restaurantdish_id, SUM(evaluation) as sum \
                    FROM web_evaluation GROUP BY restaurantdish_id ORDER BY sum DESC LIMIT 5)\
                    as tb_evaluations, web_restaurantdish WHERE web_restaurantdish.id =tb_evaluations.restaurantdish_id  '
        else:
            query = 'SELECT web_restaurantdish.* FROM\
                    (SELECT DISTINCT restaurantdish_id, category_id, SUM(evaluation) as sum \
                    FROM web_evaluation GROUP BY restaurantdish_id ORDER BY sum DESC LIMIT 5)\
                    as tb_evaluations, web_restaurantdish WHERE web_restaurantdish.id =tb_evaluations.restaurantdish_id AND tb_evaluations.category_id ='+ category
                    

        dishes = RestaurantDish.objects.raw(query) 
        response = render_to_response(
            'json/dishes.json',
            {'dishes': dishes},
            context_instance=RequestContext(request)
        )
        response['Content-Type'] = 'application/json; charset=utf-8'
        response['Cache-Control'] = 'no-cache'
        return response

def get_user(email, username):
    mail = User.objects.get(email=email.lower())
    nick = User.objects.get(username = username.lower())
    return not(mail is None) or not(nick is None)


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        password = request.POST['password']
        exist = get_user(email, username)
        if exist is None:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            user = authenticate(username=user, password=password)
            #login
            response = { 'user' : user }
            response['status'] = 'ok'
            return HttpResponse(json.dumps(response))
        else:
            #messages
            response = {'error':'ya existe el nombre de usuario o esta registrado'} 

        return HttpResponseBadRequest(json.dumps(response))
    elif request.method == "GET":
        return HttpResponse(json.dumps({}))

@never_cache
def login(request):
    #if not request.is_ajax() or request.method != 'GET':
    #    return
    try:
        username = request.POST['username']
        password = request.POST['password']
    except:
        return HttpResponseBadRequest('Bad parameters')

    from django.contrib.auth import authenticate, login

    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            response_content = {
                'username': user.username,
            }
            response =  HttpResponse(json.dumps(response_content))
            response['Content-Type'] = 'application/json; charset=utf-8'
            response['Cache-Control'] = 'no-cache'
            return response
        else:
            # Return a 'disabled account' error message
            return HttpResponseBadRequest('Usuario ha sido supendido')
    else:
        # Return an 'invalid login' error message.
        return HttpResponseBadRequest('Usuario o clave incorrecto')

        
from django.contrib.auth import logout
@never_cache
def logout(request):
    logout(request)
    return redirect('/')

@never_cache
def getRestaurants(request):

    if request.method == "GET":
        restaurants = Restaurant.objects.all()
 
        response = render_to_response(
            'json/restaurants.json',
            {'restaurants': restaurants},
            context_instance=RequestContext(request)
        )
        response['Content-Type'] = 'application/json; charset=utf-8'
        response['Cache-Control'] = 'no-cache'
        return response

