from django.conf.urls import url, patterns
from views import carro_importar, caminhao_importar

urlpatterns = patterns('',
    url(r'^veiculos/importar/carro/$',carro_importar, name='importar_fipe' ),
    url(r'^veiculos/importar/caminhao/$',caminhao_importar, name='importar_fipe_caminhao' ),
    
    
)