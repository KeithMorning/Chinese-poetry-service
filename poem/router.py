from rest_framework import routers
from django.conf.urls import url
from rest_framework.response import Response
from rest_framework.reverse import reverse
from collections import OrderedDict
from django.urls.exceptions import NoReverseMatch


class ApiListView(routers.APIRootView):
    """
    * `authors/1/poetry/` 获取对应作者的作品

    * `author-poetry-list` 分页获取对应作者的作品

    * `favour-poetry` 为 POST 方法，`POST body = {'poetry_id':3,'user_id':2,'favour':1}` 1 收藏，0 取消收藏

    * `favour-author` 为 POST 方法，用于收藏作者 `POST body 为 {'author_id':122,'user_id':3,`favour`:1}`

    * `myfavour` GET 方法，获取用户收藏列表，结构为 `myfavour/2`, 2 为user_id
    """

    def get(self, request, *args, **kwargs):
        # Return a plain {"name": "hyperlink"} response.
        ret = OrderedDict()
        namespace = request.resolver_match.namespace
        for key, url_name in self.api_root_dict.items():
            if namespace:
                url_name = namespace + ':' + url_name
            try:
                ret[key] = reverse(
                    url_name,
                    args=args,
                    kwargs=kwargs,
                    request=request,
                    format=kwargs.get('format', None)
                )
            except NoReverseMatch:
                # Don't bail out if eg. no list routes exist, only detail routes.
                continue
        uri = request.build_absolute_uri();
        ret['author-T'] = uri + "authors/?dynasty=T"
        ret['author-poetry'] = uri+"authors/1/poetry/"
        ret['author-poetry-list'] = uri + "authors/1/poetry_list/"
        ret['weichatOAuth'] = uri + "weichatOAuth"
        ret['favour-poetry'] = uri + 'favour-poetry'
        ret['favour-author'] = uri + 'favour-author'
        ret['myfavour'] = uri + 'myfavour/2'
        return Response(ret)



class DocumentedRouter(routers.DefaultRouter):
    APIRootView = ApiListView

