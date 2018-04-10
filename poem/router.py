from rest_framework import routers
from django.conf.urls import url
from rest_framework.response import Response
from rest_framework.reverse import reverse
from collections import OrderedDict
from django.urls.exceptions import NoReverseMatch


class ApiListView(routers.APIRootView):
    """
    `authors/13175/poem/` 获取对应作者的词
    `favorate-poetry` 为POST方法，body = {'poetry_id':3,'user_id':2}
    `favorate-poem` 为POST 方法， body = {'poem_id':11,'user_id':3}
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
        ret['author-T'] = uri + "authors?dynasty=T"
        ret['author-poetry'] = uri+"authors/1/poetry/"
        ret['author-poem'] = uri + "authors/13175/poem/"
        ret['weichatOAuth'] = uri + "weichatOAuth"
        ret['favorate-poetry'] = uri + 'favorate-poetry'
        ret['favorate-poem'] = uri + 'favorate-poem'
        return Response(ret)



class DocumentedRouter(routers.DefaultRouter):
    APIRootView = ApiListView

