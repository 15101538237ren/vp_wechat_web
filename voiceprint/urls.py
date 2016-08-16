from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^record/$', views.record, name='record'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^$', views.index, name='index'),
]