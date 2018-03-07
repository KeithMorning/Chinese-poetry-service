from django.urls import path,re_path
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
    re_path(r'^poems/(?:id=(?P<id>\d+))?$',views.PoemDetailView,name='Poem'),
    re_path(r'^poems/(?:authorid=(?P<id>\d+))?$',views.AuthorPoemes.as_view()),
    url(r'^poetries/$', views.PoetryDetailView, name='Poetries random'),
    re_path(r'^poetries/(?:id=(?P<id>\d+))?$', views.PoetryDetailView),
    re_path(r'^poetries/(?:authorid=(?P<id>\d+))?$',views.AuthorPoetries.as_view()),
    url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework')),
]