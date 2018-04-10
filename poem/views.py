from django.core import serializers
from django.core.serializers.json import Serializer as Buildin_Serializer
from django.http import HttpResponse,JsonResponse
from rest_framework import viewsets,status
from rest_framework.decorators import api_view,detail_route
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes
from rest_framework import permissions
import simplejson

from .models import Poem,User
from .serializers import Poetry,Author
from .serializers import UserSerializer,PoemSerializer,AuthorSerializer,PoetrySerializer
from .myPagination import mypagination
from .weichat_tools import get_session_info,to_weichat_jwt,random_passwd,get_user_info
from . import apps


class Serializer(Buildin_Serializer):
    def get_dump_object(self,obj):
        return self._current
# Create your views here.

@csrf_exempt
@permission_classes((permissions.IsAuthenticated,))
def favorite_poetry(request):
    if request.method != 'POST':
        return JsonResponse({"success":False,'error':'Not a valid request'})
    json_data = simplejson.loads(request.body);
    print(json_data)
    poetry_id = json_data.get('poetry_id',None)
    user_id = json_data.get('user_id',None)
    favour = json_data.get('favour',None)
    if poetry_id == None:
        return JsonResponse({"success":False,'error':'poetry_id is null'})

    if user_id == None:
        return JsonResponse({"success":False,'error':'user_id is null'})
    user = User.objects.filter(pk=user_id).first()
    if(user == None):
        print("can't find this user")
        return JsonResponse({"success": False, 'error': 'can not find user'})

    poetry = Poetry.objects.filter(pk=poetry_id).first()
    if(poetry == None):
        print("can't find the poetry")
        return JsonResponse({"success": False, 'error': 'can not find poetry'})

    if favour == 1:
        poetry.weight = poetry.weight + 1
        poetry.save()
        user.favorate_peotry.add(poetry)
    else:
        poetry.weight = poetry.weight - 1
        poetry.save()
        user.favorate_peotry.remove(poetry)


    user.save()
    return JsonResponse({"success":True})

@csrf_exempt
@permission_classes((permissions.IsAuthenticated,))
def favorite_poem(request):
    if request.method != 'POST':
        return JsonResponse({"success":False,'error':'Not a valid request'})
    json_data = simplejson.loads(request.body);
    print(json_data)
    poem_id = json_data.get('poem_id', None)
    user_id = json_data.get('user_id', None)
    favour = json_data.get('favour', None)

    if poem_id == None:
        return JsonResponse({"success":False,'error':'poem id is null'})

    if user_id == None:
        return JsonResponse({"success":False,'error':'user_id is null'})
    user = User.objects.filter(pk=user_id).first()
    if(user == None):
        print("can't find this user");
        return JsonResponse({"success": False, 'error': 'can not find user'})

    poem = Poem.objects.filter(pk=poem_id).first()
    if(poem == None):
        print("can't find the poetry")
        return JsonResponse({"success": False, 'error': 'can not find poem'})

    if favour == 1:
        poem.weight = poem.weight + 1
        poem.save()
        user.favorate_poem.add(poem)
    else:
        poem.weight = poem.weight - 1
        poem.save()
        user.favorate_poem.remove(poem)


    user.save()
    return JsonResponse({"success":True})



@csrf_exempt
@permission_classes((permissions.AllowAny,))
def WeichatLoginView(request):

    json_data = simplejson.loads(request.body);
    print(json_data)

    code = json_data.get('code',None)
    encryptedData = json_data.get('encryptedData',None)
    iv = json_data.get('iv',None)
    loginType = json_data.get('loginType')
    session_key,openid = get_session_info(code,apps.APP_ID,appsecret=apps.APP_SECRET)
    users = User.objects.filter(username=openid)
    if users == None or users.count()==0:
        user = User(username=openid,password=random_passwd(),email='n@n.com')
        user.save()
    user = users.first()
    user_info = get_user_info(session_key,apps.APP_ID,encryptedData,iv)
    user.nick_name = user_info['nickName']
    user.avataUrl = user_info['avatarUrl']
    user.gender = user_info['gender']
    user.location = user_info['province']
    user.login_type = loginType;
    user.save()

    print(user_info)
    jwt = token = to_weichat_jwt(user)
    return JsonResponse({'jwt':jwt,'userId':user.id})

@csrf_exempt
def get_user_favourite(request,userid=None):
    user =  User.objects.filter(pk=userid).first()
    peotry_set = user.favorate_peotry.all()
    poem_set = user.favorate_poem.all()

    poetries = map(lambda p:PoetrySerializer(p).data,peotry_set)
    poetries = list(poetries);
    poems = map(lambda p:PoemSerializer(p).data,poem_set)
    poems = list(poems)

    return JsonResponse({'poetries':poetries,'poems':poems})


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









