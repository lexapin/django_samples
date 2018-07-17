from django.conf.urls import url

from . import views

app_name = 'test'
urlpatterns = [
    url(r'^$', views.test_groups, name='groups'),
    url(r'^(?P<group_id>[0-9]+)/', views.group_tests, name='group'),
]