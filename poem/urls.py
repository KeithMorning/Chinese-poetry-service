from django.urls import path,re_path
from django.conf.urls import url,include
from rest_framework import routers
from poem import views
from . import router
from rest_framework_jwt.views import obtain_jwt_token

proetries_list = views.PoetryViewSet.as_view({
    'get':'list'
})

proetries_detail = views.PoetryViewSet.as_view({
    'get':'retrieve'
})

proetries_random = views.PoetryViewSet.as_view({
    'get':'random'
})


routers = router.DocumentedRouter()
routers.register(r'users',views.UserViewSet)
routers.register(r'poetries',views.PoetryViewSet)
routers.register(r'authors',views.AuthorViewSet)


urlpatterns = [
    url('',include(routers.urls)),
    url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework')),
    url(r'^api-token-auth/',obtain_jwt_token),
    url(r'^weichatOAuth',views.WeichatLoginView),
    url(r'^favour-poetry',views.favourite_poetry),
    url(r'^favour-author',views.favourite_author),
    url(r'^myfavour/(?P<userid>[0-9])/',views.get_user_favourite),
]