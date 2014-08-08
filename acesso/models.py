#-*-coding:utf-8-*-

from django.db import models
from django.contrib.auth.models import User, Group, Permission
from eleicao.models import Eleicao
from django.db.models.signals import post_save
from django.dispatch import receiver

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

class OrgaoPublico(User):
    nome_secretaria = models.CharField(u'Nome do órgão', max_length=100)
    endereco = models.CharField(u'Endereço do Órgão', max_length=100, null=True, blank=True)
    responsavel = models.CharField(u'Responsável do Órgão', max_length=100, help_text='Ex.: Secretário, Superintendente, Presidente')
    responsavel_info = models.CharField(u'Responsável pela informação', max_length=100, null=True, blank=True, help_text='Ex.: Chefe do Transporte')
    tel_residencial = models.CharField(u'Telefone Residencial', max_length=15, null=True, blank=True)
    tel_celular = models.CharField(u'Telefone Celular', max_length=15, null=True, blank=True)
    tel_comercial = models.CharField(u'Telefone Comercial', max_length=15, null=True, blank=True)
    data_expiracao = models.DateField()
    atualizar = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = u'Órgao público'
        verbose_name_plural = u'Órgaos públicos'
        
    def is_orgao(self):
        return True
    
    def __unicode__(self):
        return self.nome_secretaria
    
@receiver(post_save, sender=OrgaoPublico)
def orgao_publico_post_save(signal, instance, sender, **kwargs):
    
    try:
        grupo = Group.objects.get(name='orgao_publico')
        instance.groups.add(grupo)
    except Group.DoesNotExist:
        instance.groups.create(name='orgao_publico')

