from django.contrib import admin
from .models import Poem,Poetry,Author

# Register your models here.

admin.site.register(Poem)
admin.site.register(Author)
admin.site.register(Poetry)