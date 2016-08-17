from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^download_media/$', views.download_media, name='download_media'),
    url(r'^verify/$', views.verify, name='verify'),
    url(r'^record/$', views.record, name='record'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^$', views.index, name='index'),
]