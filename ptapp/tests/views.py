from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse

# Create your views here.

from django.contrib.auth.models import User
from .models import TestGroup, TestUnit, Question, Answer

def get_user():
    return User.objects.get(username='fomin')


def test_groups(request):
    context = {
        'list_name': 'Наборы тестов',
        'button_text': 'Перейти к тестам',
        'list_object': ((obj, reverse('test:group', args=(obj.id,))) for obj in TestGroup.objects.all()),
    }

    return render(request, "tests/list_view.html", context)


def group_tests(request, group_id):
    tg = TestGroup.objects.get(id=group_id)
    context = {
        'list_name': 'Тесты по теме \"%s\"'%tg.name,
        'button_text': 'Выполнить тест',
        'list_object': ((obj, reverse('test:groups')) for obj in tg.testunit_set.all()),
    }
    return render(request, "tests/list_view.html", context)