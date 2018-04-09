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
routers.register(r'poems',views.PoemViewSet)
routers.register(r'authors',views.AuthorViewSet)


urlpatterns = [
    url('',include(routers.urls)),
    url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework')),
    url(r'^api-token-auth/',obtain_jwt_token),
    url(r'^weichatOAuth',views.WeichatLoginView),
]