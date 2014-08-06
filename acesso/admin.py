#-*- coding: utf-8 -*-
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import Http404
from forms import AddOrgaoPublicoForm, ChangeOrgaoPublicoForm
from models import Permissao, OrgaoPublico

class OrgaoPublicoAdmin(UserAdmin):
    filter_horizontal=[]
    list_display=['sigla', 'nome_secretaria', 'responsavel']
    list_filter=[]
    ordering=['nome_secretaria']
    add_form = AddOrgaoPublicoForm
    form = ChangeOrgaoPublicoForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'nome_secretaria', "endereco", "responsavel", 'data_expiracao', 'password1', 'password2')}
        ),
    )
    fieldsets = (
        (None, {
            'fields': ('nome_secretaria', 'username', 'password')}
        ),
        ('Representantes', {
            'fields': ('responsavel', 'responsavel_info')}
        ),
        ('Dados Adicionais', {
            'fields': ('endereco', 'tel_residencial', 'tel_comercial', 'tel_celular', 'email')}
        ),
        ('Acesso', {
            'fields': ('data_expiracao','atualizar')}
        ),
    )
    
    def sigla(self, obj):
        return unicode(obj.username)
    sigla.short_description=u'sigla'
    
    def add_view(self, request, form_url='', extra_context=None):
        # It's an error for a user to have add permission but NOT change
        # permission for users. If we allowed such users to add users, they
        # could create superusers, which would mean they would essentially have
        # the permission to change users. To avoid the problem entirely, we
        # disallow users from adding users if they don't have change
        # permission.
        if not self.has_change_permission(request):
            if self.has_add_permission(request) and settings.DEBUG:
                # Raise Http404 in debug mode so that the user gets a helpful
                # error message.
                raise Http404(
                    'Your user does not have the "Change user" permission. In '
                    'order to add users, Django requires that your user '
                    'account have both the "Add user" and "Change user" '
                    'permissions set.')
            raise PermissionDenied
        if extra_context is None:
            extra_context = {}
        
        return super(UserAdmin, self).add_view(request, form_url,
                                               extra_context)
# Register your models here.

admin.site.register(Permissao)
admin.site.register(OrgaoPublico, OrgaoPublicoAdmin)