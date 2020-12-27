"""URL_Shortener URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from logics.views import shorten_url, login_view, registration_view, get_url_from_hash, get_hash_from_url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', registration_view, name='register'),
    path('login/', login_view, name='login'),
    path('shorten/', shorten_url, name='shorten_url'),
    path('hash2url/', get_url_from_hash, name='url_from_hash'),
    path('url2hash/', get_hash_from_url, name='hash_from_url'),
]
