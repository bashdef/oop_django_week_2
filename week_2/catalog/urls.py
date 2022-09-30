from django.urls import path
from . import views
from django.urls import re_path as url
from .models import Application

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^application/$', views.ApplicationList.as_view(), name='application'),
    url(r'^application/create/$', views.ApplicationCreate.as_view(), name='application-create'),
    url(r'^application/(?P<pk>\d+)/delete/$', views.ApplicationDelete.as_view(), name='application-delete'),
    url(r'^application/(?P<pk>\d+)/edit_status/$', views.edit_status, name='edit-status')
]
