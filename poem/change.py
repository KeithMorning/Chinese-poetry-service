

from poem.models import PoetryAuthor,Poem



filename = "./poem/poems_author.sql"

def changeSql():

    raw = open(filename,'r').read()
    sqls = raw.split('\n')
    for sql in sqls:
        a = sql.split(",")
        if a.__len__()<2:
            continue
        id = a[0]
        name = a[1]
        name = name.strip()
        #查找是否已存在poery中author
        poetry_authors = PoetryAuthor.objects.filter(name=name,dynasty='S')
        if poetry_authors.count()>1:#查到作者，
            poetry_author = poetry_authors[0]
            #查找该作者的poem
            print('find author %s'%(name))
            poems = Poem.objects.filter(author=id)
            for poem in poems:
                poem.author_id = poetry_author.id;
                poem.save()
                print('1：modify poem %s author:%s' %(poem.title,poetry_author.name))
        else:
            #没有查找用现有的作者
            intro = a[2]
            #大于31 的格式不对
            intro = intro.strip()
            if intro != "" and int(id)>31:
                intro = name + '，' + intro

            if intro == "":
                intro = "无传。"


            tempauthor = PoetryAuthor(name=name,intro=intro,dynasty='S')
            tempauthor.save()
            print('create new author %s' %(tempauthor.name))

            poems = Poem.objects.filter(author=id)
            for poem in poems:
                poem.author_id = tempauthor.id;
                poem.save()
                print('2：modify poem %s author is %s seq: %s' % (poem.title,tempauthor.name,id))

