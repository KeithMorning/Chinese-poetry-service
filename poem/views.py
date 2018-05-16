from django.core import serializers
from django.core.serializers.json import Serializer as Buildin_Serializer
from django.http import HttpResponse,JsonResponse
from rest_framework import viewsets,status
from rest_framework.decorators import api_view,detail_route,action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes
from rest_framework import permissions
import simplejson
from django.utils.decorators import method_decorator

from django.db.models import FilteredRelation,Q,Count
from .models import User
from .serializers import Poetry,Author
from .serializers import UserSerializer,PoemSerializer,AuthorSerializer,PoetrySerializer
from .myPagination import mypagination
from .weichat_tools import get_session_info,to_weichat_jwt,random_passwd,get_user_info
from . import apps
from .custom_join import join_to


class Serializer(Buildin_Serializer):
    def get_dump_object(self,obj):
        return self._current
# Create your views here.


@permission_classes((IsAuthenticated,))
def favourite_author(request):
    if request.method != 'POST':
        return JsonResponse({"success":False,'error':'Not a valid request'})

    json_data = simplejson.loads(request.body)
    print(json_data)
    author_id = json_data.get('author_id',None)
    user_id = json_data.get('user_id',None)
    favour = json_data.get('favour',None)


    if author_id == None:
        return JsonResponse({"success": False, 'error': 'author_id is null'})

    author = Author.objects.filter(pk = author_id).first()
    if author == None:
        return JsonResponse({"success": False, 'error': 'can not find this author'})

    if user_id == None:
        return JsonResponse(author_id)

    user = User.objects.filter(pk=user_id).first()
    if (user == None):
        print("can't find this user")
        return JsonResponse({"success": False, 'error': 'can not find user'})

    if favour == 1:
        author.weight = author.weight+1
        author.save()
        author.favour_user.add(user)
    else:
        author.weight = author.weight+1
        author.save()
        author.favour_user.remove(user)

    author.save()

    return JsonResponse({"success":True})






@csrf_exempt
@permission_classes((permissions.IsAuthenticated,))
def favourite_poetry(request):
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
        poetry.favour_user.add(user)
    else:
        poetry.weight = poetry.weight - 1
        poetry.favour_user.remove(user)

    poetry.save()

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
    if user == None:
        return JsonResponse({"success": False, 'error': 'can not find user'})

    peotry_set = user.poetry_set.all()
    authors_set = user.author_set.all()

    poetries = map(lambda p:PoetrySerializer(p).data,peotry_set)
    poetries = list(poetries)

    authors = map(lambda a:AuthorSerializer(a).data,authors_set)
    authors = list(authors)


    return JsonResponse({'poetries':poetries,'authors':authors})


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PoetryViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Poetry.objects.all().order_by('id')
    serializer_class = PoetrySerializer
    pagination_class = mypagination

    def get_queryset(self):
        user_id = self.request.user.id
        user = User.objects.get(pk=user_id)
        fav_poetry = user.poetry_set.all()
        quertys_set = Poetry.objects.filter(~Q(favour_user=user_id))
        quertys_set = quertys_set | fav_poetry
        quertys_set = quertys_set.order_by('-weight','id').\
            extra(select={'isFav':'CASE when user_id='+str(user_id)+' then 1 else 0 END'}).distinct('weight','id')
        print(quertys_set.query)
        return quertys_set

    @detail_route(['GET'])
    def random(self,request):
        count = Poetry.objects.count()
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
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user_id = self.request.user.id
        user = User.objects.get(pk=user_id)
        fav_author = user.author_set.all()

        quertys_set = Author.objects.exclude(id__in=fav_author)
        quertys_set = quertys_set | fav_author
        quertys_set = quertys_set.order_by('-weight','id').extra(
            select={'isFav': 'CASE when user_id=' + str(user_id) + ' then 1 else 0 END',}).distinct('weight','id')

        dynasty = self.request.query_params.get('dynasty', None)

        if dynasty is not None:
            quertys_set = quertys_set.filter(dynasty=dynasty)

        print(quertys_set.query)
        return quertys_set

    @detail_route(['GET'])
    def poetry(self,request,pk):
        user_id = self.request.user.id
        user = User.objects.get(pk=user_id)
        fav_poetry = user.poetry_set.all()
        quertys_set = Poetry.objects.filter(~Q(favour_user=user_id))
        quertys_set = quertys_set | fav_poetry
        quertys_set = quertys_set.order_by('-weight','id').extra(
            select={'isFav': 'CASE when user_id=' + str(user_id) + ' then 1 else 0 END'}).filter(Q(author=pk)).distinct('weight','id')
        print(quertys_set.query)
        poetries_result = PoetrySerializer(quertys_set, many=True)
        return Response(poetries_result.data)

    @action(methods=['GET'],detail=True,serializer_class=PoetrySerializer)
    def poetry_list(self,request,pk):
        user_id = self.request.user.id
        user = User.objects.get(pk=user_id)
        fav_poetry = user.poetry_set.all()
        quertys_set = Poetry.objects.filter(~Q(favour_user=user_id))
        quertys_set = quertys_set | fav_poetry
        quertys_set = quertys_set.order_by('-weight','id').extra(
            select={'isFav': 'CASE when user_id=' + str(user_id) + ' then 1 else 0 END'}).filter(Q(author=pk)).distinct('weight','id')
        page = self.paginate_queryset(quertys_set)
        if page is not None:
            serializer = self.get_serializer(page,many=True)
            return self.get_paginated_response(serializer.data)

        poetries_result = PoetrySerializer(quertys_set, many=True)
        return Response(poetries_result.data)







