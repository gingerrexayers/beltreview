from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add$', views.add, name='add'),
    url(r'^create$', views.create, name='create'),
    url(r'^(?P<id>\d+)$', views.show, name='show'),
    url(r'^(?P<id>\d+)/add$', views.addtoexisting, name='addtoexisting'),
    url(r'^(?P<id>\d+)/delete$', views.delete, name='delete')
]
