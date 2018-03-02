from django.core import serializers
from django.core.serializers.json import Serializer as Buildin_Serializer
from django.http import HttpResponse
from rest_framework import viewsets

from poem.change import changeSql
from .models import Poem
from .serializers import Poetry,Author
from .serializers import UserSerializer,PoemSerializer,User,AuthorSerializer,PoetrySerializer


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

class PoemViewSet(viewsets.ModelViewSet):

    queryset = Poem.objects.all()
    serializer_class = PoemSerializer


class PoetryViewSet(viewsets.ModelViewSet):

    queryset = Poetry.objects.all()
    serializer_class = PoetrySerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


