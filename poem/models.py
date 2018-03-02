from django.db import models

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Author(models.Model):
    name = models.CharField(max_length=150)
    intro = models.TextField(blank=True, null=True)
    dynasty = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'poetry_author'


class PoetryAuthor(models.Model):
    name = models.CharField(max_length=150)
    intro = models.TextField(blank=True, null=True)
    dynasty = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'poetry_author'


class Poem(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    dynasty = models.CharField(max_length=10,default='S')
    author_name = models.CharField(max_length=150)
    class Meta:
        db_table = 'poems'


class Poetry(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    content = models.TextField()
    dynasty = models.CharField(max_length=10)
    author_name = models.CharField(max_length=150)

    class Meta:
        db_table = 'poetry'


