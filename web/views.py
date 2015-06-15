from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
import json
from django.views.decorators.csrf import csrf_exempt
from push_notifications.models import GCMDevice,APNSDevice

from rest_framework import viewsets
from serializers import *

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden
from web.models import *
from push_notifications.models import GCMDevice,APNSDevice

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

def getFinalTop(request):
    if request.method == 'GET':
        categorys = Category.objects.all()
        dishes = []
        for category in categorys:
            query = 'SELECT web_restaurantdish.* FROM\
                        (SELECT DISTINCT restaurantdish_id, category_id, SUM(evaluation) as sum \
                        FROM web_evaluation GROUP BY restaurantdish_id ORDER BY sum DESC LIMIT 5)\
                        as tb_evaluations, web_restaurantdish WHERE web_restaurantdish.id =tb_evaluations.restaurantdish_id AND tb_evaluations.category_id ='+ str(category.id)

            for d in RestaurantDish.objects.raw(query):
                dishes.append((category.name,d))

        response = render_to_response(
            'json/win.json',
            {'dishes': dishes},
            context_instance=RequestContext(request)
        )
        response['Content-Type'] = 'application/json; charset=utf-8'
        response['Cache-Control'] = 'no-cache'
        return response


def get_user(email, username):
    mail = User.objects.filter(email=email.lower())
    nick = User.objects.filter(username = username.lower())
    return not(len(mail)>0 or len(nick)>0)


@csrf_exempt
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        password = request.POST['password']
        exist = get_user(email, username)
        if exist:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            #user = authenticate(username=user, password=password)
            #login
            response = { 'id' : user.id }
            response['status'] = 'ok'
            return HttpResponse(json.dumps(response))
        else:
            #messages
            response = {'error':'ya existe el nombre de usuario o esta registrado'}

        return HttpResponseBadRequest(json.dumps(response))
    elif request.method == "GET":
        return HttpResponse(json.dumps({}))

@never_cache
@csrf_exempt
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
                'email': user.mail,
                'firstname': user.first_name,
                'lastname': user.lastname,
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

def push_notifications_view(request):
    if request.method == "POST":
        if 'code' in request.POST:
            code = request.POST['code']

            devices = GCMDevice.objects.all()
            devices.send_message("Pruebaaaaa !!!")
            message = "message sent to android devices"


            #if code == 'android':
            #    print 'code == android'
            #    devices = GCMDevice.objects.all()
            #    devices.send_message({"message": "Hi Android!"})
            #    message = "message sent to android devices"

            #elif code == 'ios':
            #    print 'code == ios'
            #    devices = APNSDevice.objects.all()
            #    devices.send_message("Hi iOS!")
            #    message = "message sent to ios devices"

            #elif code == 'simple':
            #    print 'code == simple'

            #    device = APNSDevice.objects.get(registration_id='mi apns token')
            #    device.send_message(None, extra={"foo": "bar"})
            #    message = "simple message sent"

    return render_to_response('main.html', locals(), context_instance=RequestContext(request))


class GCMDeviceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows words to be viewed or edited.
    """
    queryset = GCMDevice.objects.all()
    serializer_class = GCMDeviceSerializer

