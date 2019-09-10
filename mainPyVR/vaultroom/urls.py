"""mainPyVR URL Configuration

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
from django.urls import path

from .views import index, by_storage, by_product, done, stockKorr

urlpatterns = [
    path('', index, name='index'),
    path('storage/<int:storage_id>', by_storage, name='by_storage'),
    path('product/<int:product_id>', by_product, name='by_product'),
    path('done/', done, name='done'),
    path('stockkorr/<int:product_id>', stockKorr, name='stockkorr'),
]
