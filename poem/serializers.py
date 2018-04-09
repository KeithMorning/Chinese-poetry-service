from django.contrib.auth.models import  Group
from .models import Poem, Poetry, Author,User

from  rest_framework import serializers,reverse


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups','weichat_id','nick_name','login_type')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class PoemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poem
        fields = ('id', 'title', 'content', 'author', 'dynasty', 'author_name','weight')




class PoetrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Poetry
        fields = ('id', 'title', 'content', 'author', 'dynasty', 'author_name','weight')


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('id', 'name', 'intro', 'dynasty','weight')
