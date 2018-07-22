from django.conf.urls import url

from . import views

app_name = 'interview'
urlpatterns = [
    url(r'^test/(?P<testunit_id>[0-9]+)/', views.open_interview, name='open'),
    url(r'^(?P<pk>[0-9]+)/question', views.QuestionView.as_view(), name='question'),
    url(r'^(?P<interview_id>[0-9]+)/report', views.report, name='report'),
]