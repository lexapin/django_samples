from django.conf.urls import url

from . import views

app_name = 'test'
urlpatterns = [
    url(r'^$', views.TestGroupListView.as_view(), name='groups'),
    url(r'^(?P<group_id>[0-9]+)/', views.TestUnitListView.as_view(), name='group'),
]