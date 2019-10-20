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
from django.views.generic.dates import DayArchiveView

from .models import Control, Done, Move
from .views import index, by_storage, by_product, done, stockKorr, priemka, vidacha, control, comment, dateDone, dateControl, to, move, dateMove



urlpatterns = [
    path('', index, name='index'),
	path('storage/<int:storage_id>/to/<int:storage_to>', to, name='to'),
    path('storage/<int:storage_id>', by_storage, name='by_storage'),
    path('product/<int:product_id>', by_product, name='by_product'),
    path('done/', done, name='done'),
    path('move/', move, name='move'),
    path('stockkorr/<int:product_id>', stockKorr, name='stockkorr'),
    path('priemka/<int:storage_id>/', priemka, name='priemka'),
    path('vidacha/<int:storage_id>/', vidacha, name='vidacha'),
    path('control/', control, name='control'),
    path('comment/<int:check_id>', comment, name='comment'),
	path('control/<int:year>/<int:month>/<int:day>/', DayArchiveView.as_view(model=Control, date_field='time', month_format='%m')),
	path('control/date/', dateControl, name='date_control'),
    path('done/<int:year>/<int:month>/<int:day>/', DayArchiveView.as_view(model=Done, date_field='time', month_format='%m')),
    path('done/date/', dateDone, name='date_done'),
    path('move/date/', dateMove, name='date_move'),
    path('move/<int:year>/<int:month>/<int:day>/', DayArchiveView.as_view(model=Move, date_field='time', month_format='%m')),



]
