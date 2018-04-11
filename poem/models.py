from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=150)
    intro = models.TextField(blank=True, null=True)
    dynasty = models.CharField(max_length=10, blank=True, null=True)
    weight = models.IntegerField()

    class Meta:
        db_table = 'poem_author'


#弃用Poem，Poetry和poem一张表
class Poem(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    dynasty = models.CharField(max_length=10,default='S')
    type = models.CharField(max_length=10, default='poem')
    author_name = models.CharField(max_length=150)
    weight = models.IntegerField()
    class Meta:
        db_table = 'poem_poems'


class Poetry(models.Model):
    title = models.CharField(max_length=150)
    yunlv_rule = models.TextField(default='')
    author = models.ForeignKey(Author,related_name='poetries',on_delete=models.CASCADE)
    content = models.TextField()
    dynasty = models.CharField(max_length=10)
    type = models.CharField(max_length=10, default='poetry')
    author_name = models.CharField(max_length=150)
    weight = models.IntegerField()

    class Meta:
        db_table = 'poem_poetry'



class User (AbstractUser):

    login_type = models.CharField(max_length=20, blank=False)
    weichat_id = models.CharField(max_length=100, null=True)
    weichat_session_key = models.CharField(max_length=100,null=True)
    nick_name = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    favourate_peotry = models.ManyToManyField(Poetry)
    favourate_author = models.ManyToManyField(Author)
    avataUrl=models.URLField(null=True)
    gender = models.IntegerField(null=True)


