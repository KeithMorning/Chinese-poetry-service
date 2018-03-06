from django.core import serializers
from django.core.serializers.json import Serializer as Buildin_Serializer
from django.http import HttpResponse,JsonResponse
from rest_framework import viewsets,status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from poem.change import changeSql
from .models import Poem
from .serializers import Poetry,Author
from .serializers import UserSerializer,PoemSerializer,User,AuthorSerializer,PoetrySerializer
from .myPagination import mypagination

import random


class Serializer(Buildin_Serializer):
    def get_dump_object(self,obj):
        return self._current

# Create your views here.
def index(request):

    poem = Poem.objects.first()
    data = serializers.serialize('json',[poem,])
    changeSql()
    return HttpResponse(data,content_type="application/json")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# class PoemViewSet(viewsets.ModelViewSet):
#
#     queryset = Poem.objects.all()
#     serializer_class = PoemSerializer
@api_view(['GET'])
def PoemDetailView(request,pk=None,format=None):
    if pk == None:
        count = Poem.objects.count()
        pk = random.randint(0,count)


    try:
        p = Poem.objects.get(pk=pk)
    except Poem.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        poemserial = PoemSerializer(p)
        return Response(poemserial.data)


@api_view(['GET'])
def PoetryDetailView(request,pk=None,format = None):

    if pk == None:
        count = Poetry.objects.count()
        pk = random.randint(0,count)


    try:
        p = Poetry.objects.get(pk=pk)
    except Poetry.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        poetryserial = PoetrySerializer(p)
        return Response(poetryserial.data)
#
# class PoetryViewSet(viewsets.ModelViewSet):
#
#     queryset = Poetry.objects.all()
#     serializer_class = PoetrySerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    pagination_class = mypagination


