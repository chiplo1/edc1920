"""edc1920 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from projeto1 import views
from edc1920 import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name=''),
    path('distritos/', views.distritos, name='distritos'),
    path('distritoDetail/', views.distritoDetail, name='distritoDetail'),
    path('municipioDetail/', views.municipioDetail, name='municipioDetail'),
    path('interesseDetail/', views.interesseDetail, name='interesseDetail'),
    path('validateXML/', views.validateXML, name='validateXML'),  ## TEST ONLY
    path('interesses/', views.interesses, name='interesses'),
    path('sobre/', views.sobre, name='sobre'),
    path('rssFeed/', views.rssFeed, name='rssFeed'),
    path('labelList/', views.labelList, name='labelList')
]

