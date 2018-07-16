from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

from django.contrib.auth.models import User
from .models import TestGroup, TestUnit, Question, Answer

def get_user():
    return User.objects.get(username='fomin')


def users(request):
    return HttpResponse(get_user())


def index(request):
    context = {
        'test_groups': TestGroup.objects.all(),
    }
    print(TestGroup.objects.all())
    return render(request, "tests/index.html", context)