from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.admin import UserAdmin

# Create your models here.

class ProfileBase(type):
    def __new__(cls, name, bases, attrs):
        module = attrs.pop('__module__')
        parents = [b for b in bases if isinstance(b,ProfileBase)]
        if parents:
            fileds = []
            for obj_name, obj in attrs.items():
                if isinstance(obj,models.Field):fileds.append(obj_name)
                User.add_to_class(obj_name,obj)
            UserAdmin.fieldsets = list(UserAdmin.fieldsets)
            UserAdmin.fieldsets.append((name,{'fields':fileds}))
        return super(ProfileBase,cls).__new__(cls,name,bases,attrs)


class ProfileUser(object):
    __metaclass = ProfileBase


class Author(models.Model):
    name = models.CharField(max_length=150)
    intro = models.TextField(blank=True, null=True)
    dynasty = models.CharField(max_length=10, blank=True, null=True)
    weight = models.IntegerField()

    class Meta:
        db_table = 'poetry_author'


class PoetryAuthor(models.Model):
    name = models.CharField(max_length=150)
    intro = models.TextField(blank=True, null=True)
    dynasty = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'poetry_author_bak'


class Poem(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    dynasty = models.CharField(max_length=10,default='S')
    author_name = models.CharField(max_length=150)
    weight = models.IntegerField()
    class Meta:
        db_table = 'poems'


class Poetry(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(Author,related_name='poetries',on_delete=models.CASCADE)
    content = models.TextField()
    dynasty = models.CharField(max_length=10)
    author_name = models.CharField(max_length=150)
    weight = models.IntegerField()

    class Meta:
        db_table = 'poetry'



class Profile(ProfileUser):
    login_type = models.CharField(max_length=20,blank=False)
    weichat_id = models.CharField(max_length=100,null=True)
    nick_name = models.CharField(max_length=100,blank=True)
    create_date = models.DateField(null=True,blank=True)
    location = models.CharField(max_length=100,blank=True)
    favorate_peotry = models.ManyToManyField(to=Poetry)
    favorate_poem = models.ManyToManyField(to=Poem)
    #avatar = models.BinaryField(m)

