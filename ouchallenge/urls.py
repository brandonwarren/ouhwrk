"""ouchallenge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

import pricer

urlpatterns = [
    #url(r'^item-price-service/$', pricer.views.item_price, name='item-price-service'),
    url(r'^item-price-service/$', 'pricer.views.item_price', name='item-price-service'),    # new vers
    url(r'^item-price-service2/$', 'pricer.views.item_price2', name='item-price-service2'), # orig vers
    url(r'^admin/', admin.site.urls),
]
