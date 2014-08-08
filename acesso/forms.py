#-*- coding: utf-8 -*-
'''
Created on 05/08/2014

@author: felipe
'''
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
from models import OrgaoPublico

import datetime
import warnings

class OrgaoPublicoForm(forms.ModelForm):
    class Meta:
        model = OrgaoPublico
        fields = ("nome_secretaria", "endereco", "responsavel", "responsavel_info", "tel_residencial", "tel_celular", "tel_comercial", "email")
        widgets = {
            'nome_secretaria' : forms.HiddenInput()
        }
        
    def __init__(self, *args, **kwargs):
        super(OrgaoPublicoForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            
            if not isinstance(self.fields[key].widget, forms.CheckboxInput):
                self.fields[key].widget.attrs.update({'class': 'form-control'})
            if key in ('email', 'tel_comercial', 'tel_celular'):
                continue
            if 'tel' in key:
                self.fields[key].widget.attrs['class'] += ' telefone'
            self.fields[key].required=True
        
class AddOrgaoPublicoForm(forms.ModelForm):
    error_messages = {
        'duplicate_username': u'Um órgão público já foi cadastrado com esse nome',
        'password_mismatch': u'As senhas estão incompatíveis',
    }
    username = forms.RegexField(label='sigla', max_length=30,
        regex=r'^[\w_]+$',
        help_text=u'No máximo 30 caracteres, sendo aceitos apenas letras, numeros e underlines, sem espaco',
        error_messages={
            'invalid': u'''Coloque apenas letras, números e underline'''})
    password1 = forms.CharField(label='senha',
        widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar a senha',
        widget=forms.PasswordInput,
        help_text='Repita a senha')

    class Meta:
        model = OrgaoPublico
        fields = ("nome_secretaria", "username", "endereco", "responsavel", 'data_expiracao')

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            OrgaoPublico.objects.get(username=username)
        except OrgaoPublico.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        op = super(AddOrgaoPublicoForm, self).save(commit=False)
        op.set_password(self.cleaned_data["password1"])
        if commit:
            op.save()
            
            
        return op


class ChangeOrgaoPublicoForm(forms.ModelForm):
    username = forms.RegexField(label='sigla', max_length=30,
        regex=r'^[\w_]+$',
        help_text=u'No máximo 30 caracteres, sendo aceitos apenas letras, numeros e underlines, sem espaco',
        error_messages={
            'invalid': u'''Coloque apenas letras, números e underline'''})
    password = ReadOnlyPasswordHashField(label='Senha',
        help_text='''Senha criptografada. Para trocar a senha acesse <a href="password/">aqui</a>.''')

    class Meta:
        model = OrgaoPublico
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ChangeOrgaoPublicoForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
class LoginVeiculosForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.ModelChoiceField(queryset=OrgaoPublico.objects.all().order_by('nome_secretaria'),
                                 label=u'Órgão Público',
                                 widget=forms.Select(attrs={'class':'form-control'}))
    password = forms.CharField(label="Senha",
                               widget=forms.PasswordInput(attrs={'class':'form-control'}))

    error_messages = {
        'invalid_login': u'Usuário e/ou senha incorretos',
        'inactive': 'Conta inativa',
        'expired': 'acesso expirado',
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(LoginVeiculosForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user_cache = authenticate(username=username.username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
            elif not self.user_cache.data_expiracao > datetime.date.today():
                raise forms.ValidationError(
                    self.error_messages['expired'],
                    code='expired',
                )
        return self.cleaned_data

    def check_for_test_cookie(self):
        warnings.warn("check_for_test_cookie is deprecated; ensure your login "
                "view is CSRF-protected.", DeprecationWarning)

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

