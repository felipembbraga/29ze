#-*-coding:utf-8-*-
from django.contrib.admin import *


class CustomAdminSite(AdminSite):
    site_header = u'Administração da 29ª Zona Eleitoral'
    site_title = u'Administração da 29ª Zona Eleitoral'
    index_title = u'Administração'

site = CustomAdminSite()

