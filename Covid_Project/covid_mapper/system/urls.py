"""covid_mapper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.urls import path, include
from rest_framework import routers
from system.views import *

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='User')
router.register(r'groups', GroupViewSet)
router.register(r'lists', ListViewSet, basename='List')
router.register(r'listLocations', ListLocationViewSet, basename = 'ListLocation')
router.register(r'locations', LocationViewSet, basename = 'Location')


urlpatterns = [
    # path('', views.index, name = "index"),
    url(r'^user/', include(router.urls)),
    url(r'^user/current/$', getUID),
    url(r'^register/', include('rest_auth.registration.urls')),
    url(r'^verification/email/$', send_verification_email),
    url(r'^', include('rest_auth.urls')),
    url(r'^allauth/', include('allauth.urls')),
]
