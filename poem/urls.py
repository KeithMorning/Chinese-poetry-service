from django.urls import path
from django.conf.urls import url,include
from rest_framework import routers
from poem import views

routers = routers.DefaultRouter()
routers.register(r'users',views.UserViewSet)
#routers.register(r'poetries',views.PoetryViewSet)
routers.register(r'authors',views.AuthorViewSet)


urlpatterns = [
    path(r'test',views.index,name = 'index'),
    url('',include(routers.urls)),
    url(r'^poems/$',views.PoemDetailView,name='Poem random'),
    url(r'^poems/(?P<pk>[0-9]+)/$',views.PoemDetailView),
    url(r'^poetries/$', views.PoetryDetailView, name='Poem random'),
    url(r'^poetries/(?P<pk>[0-9]+)/$', views.PoetryDetailView),
    url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework')),
]