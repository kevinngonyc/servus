from django.shortcuts import get_object_or_404, render
from django.core import serializers
from .models import *

# Create your views here.

from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

def users(request):
	users = serializers.serialize("json", User.objects.all())
	return HttpResponse(users, content_type="application/json")

def user(request, user_id):
	u = get_object_or_404(User, pk=user_id)
	user = serializers.serialize("json", u)
	return HttpResponse(user, content_type="application/json")