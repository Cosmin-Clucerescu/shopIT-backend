"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

SchemaView = get_schema_view(
    openapi.Info(title="ShopIT API", default_version="v1"), public=True, permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    urls.path("admin/", admin.site.urls, name="admin"),
    url(r"^api/", include(("rest_api.urls", "api"), namespace="api")),
    url(r"^docs(?P<format>\.json|\.yaml)$", SchemaView.without_ui(cache_timeout=0), name="schema-json"),
    url(r"^docs/$", SchemaView.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    urls.path("", RedirectView.as_view(url="docs/", permanent=True)),
]
