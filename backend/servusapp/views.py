from django.shortcuts import get_object_or_404, render
from django.core import serializers
from django.forms.models import model_to_dict
from django.middleware.csrf import get_token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password

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
        user = serializers.serialize("json", [u, ])
    except User.DoesNotExist:
        raise Http404("User does not exist")
    return HttpResponse(user, content_type="application/json")


def delist_dict(qstring_dict):
    delisted_dict = {}
    for key in qstring_dict:
        delisted_dict[key] = qstring_dict[key]
    return delisted_dict

def login(request):
    csrf_token = get_token(request)
    try:
        user = json.loads(request.body)
        uid = user.get("id", None)
    except:
        return JsonResponse({"msg":"Missing User Dump"}, status=500)
    try:
        u = User.objects.get(username=uid)
    except User.DoesNotExist:
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

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)