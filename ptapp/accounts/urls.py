from django.contrib.auth.views import (
    LoginView, LogoutView,
)

from django.conf.urls import url

from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^signup/', views.signup, name='signup'),
    url(r'^login/', LoginView.as_view(template_name='accounts/signin.html'), name='signin'),
    url(r'^logout/', LogoutView.as_view(), name='signout'),
]