"""mysite URL Configuration

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
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin', admin.site.urls),
    path('', views.home),
    path('home', views.home),
    path('buy', views.buy),
    path('sitzone', views.sitzone),
    path('standzone', views.standzone),
    path('payment', views.payment),
    path('addpayment', views.addpayment),
    path('paymentbill', views.paymentbill),
    path('addreserve', views.addreserve),
    path('success', views.success),   
    path('search', views.search),
    path('search_user', views.search_user),
    #path('searchsuccess', views.searchsuccess),
    path('contact', views.contact),
 

]
