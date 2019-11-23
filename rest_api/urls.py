from django.conf.urls import url, include

from rest_api import views

auth_urlpatterns = [
    # authentication
    url(r"^login/$", views.Login.as_view(), name="login"),
]
urlpatterns = [
    url(r"^auth/", include((auth_urlpatterns, "auth"), namespace="auth")),
    ]
