from django.conf.urls import url

from rest_api import views

urlpatterns = [url("login/", views.LoginView.as_view())]
