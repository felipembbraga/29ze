#-*-coding:utf-8-*-

from django.db import models
from django.contrib.auth.models import User, Group, Permission

# Create your models here.z

class PermissaoManager(models.Manager):
    pass

class Permissao(Permission):
    objects = PermissaoManager()
    class Meta:
        proxy = True
        verbose_name=u'Permissão'
        verbose_name_plural=u'Permissões'
        permissions = (
            ('adicionar_permissoes', u'Adicionar Permissões'),
            ('alterar_permissoes', u'Alterar Permissões'),
            ('deletar_permissoes', u'Deletar Permissões'),
        )
