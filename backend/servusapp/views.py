from django.shortcuts import get_object_or_404, render
from django.core import serializers
from django.forms.models import model_to_dict
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotAuthenticated
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser
from rest_framework.decorators import api_view

from .models import *
import json

# Create your views here.

from django.http import Http404, HttpResponse, QueryDict, JsonResponse
from django.core.exceptions import ObjectDoesNotExist


def users(request):
    qstring_dict = QueryDict(query_string=request.META["QUERY_STRING"])
    if qstring_dict:
        u = User.objects.filter(**delist_dict(qstring_dict))
    else:
        u = User.objects.all()
    users = serializers.serialize("json", u)
    return HttpResponse(users, content_type="application/json")


def user(request, user_id):
    try:
        u = User.objects.get(pk=user_id)
        _user = serializers.serialize("json", [u, ])
    except ObjectDoesNotExist:
        raise Http404("User does not exist")
    return HttpResponse(_user, content_type="application/json")


def delist_dict(qstring_dict):
    delisted_dict = {}
    for key in qstring_dict:
        delisted_dict[key] = qstring_dict[key]
    return delisted_dict

def login(request):
    try:
        print(request.body)
        user = json.loads(request.body)
        uid = user.get("id", None)
    except:
        return JsonResponse({"msg":"Missing User Dump"}, status=500)
    try:
        u = User.objects.get(username=uid)
    except ObjectDoesNotExist:
        u = register(user)
    return JsonResponse({
        "username": u.username
    })

def register(user):
    print("user created")
    print(user)
    u = User(
        first_name=user["givenName"], 
        last_name=user["familyName"],
        username=user["id"],
        password=make_password(user["id"]),
        email=user["email"],)
    u.save()
    return u

@api_view(['POST','GET'])
def me(request):
    if isinstance(request.user, AnonymousUser):
        return HttpResponse('Unauthorized', status=401)
    return JsonResponse({
        "first_name": request.user.first_name,
        "last_name": request.user.last_name
    })

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)