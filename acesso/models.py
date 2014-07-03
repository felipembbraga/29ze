#-*-coding:utf-8-*-

from django.db import models
from django.contrib.auth.models import User, Group, Permission

# Create your models here.z

class Usuario(User):
    class Meta:
        proxy = True
        verbose_name=u'Usuário'
        verbose_name_plural=u'Usuários'
        permissions = (
            ('adicionar_usuarios', u'Adicionar Usuários'),
            ('alterar_usuarios', u'Alterar Usuários'),
            ('deletar_usuarios', u'Deletar Usuários'),
        )
                
class Grupo(Group):
    class Meta:
        proxy = True
        permissions = (
            ('adicionar_grupos', u'Adicionar Grupos'),
            ('alterar_grupos', u'Alterar Grupos'),
            ('deletar_grupos', u'Deletar Grupos'),
        )

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
