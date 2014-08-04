from django.conf.urls import include, url, patterns
from views import carro_importar

urlpatterns = patterns('',
    url(r'^veiculos/importar/$',carro_importar, name='importar_fipe' ),
    
    
)