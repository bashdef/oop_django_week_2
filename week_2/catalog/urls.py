from django.urls import path
from . import views
from django.urls import re_path as url

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^application/$', views.ApplicationListView.as_view(), name='application'),
    url(r'^application/create/$', views.ApplicationCreateView.as_view(), name='application-create'),
]
