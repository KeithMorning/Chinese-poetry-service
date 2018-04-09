from django.core import serializers
from django.core.serializers.json import Serializer as Buildin_Serializer
from django.http import HttpResponse,JsonResponse
from rest_framework import viewsets,status
from rest_framework.decorators import api_view,detail_route
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from .models import Poem,User
from .serializers import Poetry,Author
from .serializers import UserSerializer,PoemSerializer,AuthorSerializer,PoetrySerializer
from .myPagination import mypagination
from .weichat_tools import get_user_info,to_weichat_jwt,random_passwd
from . import apps


class Serializer(Buildin_Serializer):
    def get_dump_object(self,obj):
        return self._current
# Create your views here.

def WeichatLoginView(resquest):
    code = resquest.GET.get('code',None)
    session_key,openid = get_user_info(code,apps.APP_ID,appsecret=apps.APP_SECRET)
    users = User.objects.filter(username=openid)
    if users == None or users.count()==0:
        user = User(username=openid,password=random_passwd(),email='n@n.com')
        user.save()
    user = users.first()
    jwt = token = to_weichat_jwt(user)
    return JsonResponse({'jwt':jwt})


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PoemViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Poem.objects.all()
    serializer_class = PoemSerializer
    pagination_class = mypagination

    @detail_route(['GET'])
    def random(self,request):

        count = Poem.objects.count()
        id = random.randint(0, count)

        try:
            p = Poem.objects.get(pk=id)
        except Poem.DoesNotExist:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'GET':
            poemserial = PoemSerializer(p)
            return Response(poemserial.data)

class PoetryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Poetry.objects.all().order_by('id')
    serializer_class = PoetrySerializer
    pagination_class = mypagination

    @detail_route(['GET'])
    def random(self,request):
        count = Poem.objects.count()
        pk = random.randint(0, count)

        try:
            p = Poetry.objects.get(pk=pk)
        except Poetry.DoesNotExist:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'GET':
            poetryserial = PoetrySerializer(p)
            return Response(poetryserial.data)



class AuthorViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = AuthorSerializer
    pagination_class = mypagination
    queryset = Author.objects.all()

    def get_queryset(self):
        queryset = Author.objects.all()
        dynasty = self.request.query_params.get('dynasty', None)
        if dynasty is not None:
            return queryset.filter(dynasty=dynasty)
        return queryset

    @detail_route(['GET'])
    def poetry(self,request,pk):
        poetries = Poetry.objects.filter(author=pk)
        poetries_result = PoetrySerializer(poetries, many=True)
        return Response(poetries_result.data)

    @detail_route(['GET'])
    def poem(self,request,pk):
        poems = Poem.objects.filter(author=pk)
        poems_result = PoemSerializer(poems, many=True)
        return Response(poems_result.data)









