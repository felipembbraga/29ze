from models import Permissao
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType

# Register your models here.

admin.site.register(Permissao)
