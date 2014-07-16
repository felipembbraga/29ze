from django.utils.functional import SimpleLazyObject
from django.middleware.csrf import rotate_token
from models import Eleicao, LocalVotacao


SESSION_KEY='_eleicao_eleicao_id'

def definir_eleicao_padrao(request, eleicao=None):
    """
    Persist a user id and a backend in the request. This way a user doesn't
    have to reauthenticate on every request. Note that data set during
    the anonymous session is retained when the user logs in.
    """
    if eleicao is None:
        eleicao = Eleicao.objects.get(atual=True)
    if SESSION_KEY in request.session:
        if request.session[SESSION_KEY] != eleicao.pk:
            request.session.flush()
    else:
        request.session.cycle_key()
    request.session[SESSION_KEY] = eleicao.pk
    if hasattr(request, 'eleicao_atual'):
        request.eleicao_atual = eleicao
    rotate_token(request)
    
    
def get_eleicao(request):
    """
    Returns the user model instance associated with the given request session.
    If no user is retrieved an instance of `AnonymousUser` is returned.
    """

    try:
        eleicao_id = request.session[SESSION_KEY]
        eleicao = Eleicao.objects.get(pk=int(eleicao_id))
    except (KeyError):
        eleicao =  Eleicao.objects.get(atual=True)
    return eleicao

def get_eleicao_persistente(request):
    if not hasattr(request, '_cached_eleicao'):
        request._cached_eleicao = get_eleicao(request)
    return request._cached_eleicao


class EleicaoMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
        #if not hasattr(request, 'eleicao_atual'):
        #    definir_eleicao_padrao(request)
            
        request.eleicao_atual = SimpleLazyObject(lambda: get_eleicao_persistente(request))
        
class FormAgregarSecaoMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_func.func_name != 'secao_agregar' and view_func.func_name != 'local_detalhar':
            request.formClass = None
            return
        from forms import SecaoAgregarForm
        classForm = SecaoAgregarForm
        id_local = request.POST.get('id-local') and request.POST.get('id-local') or (len(view_args) > 0 and view_args[0] or None)
        try:
            local = LocalVotacao.objects.get(pk=int(id_local))
        except:
            request.formClass = None
            return
        classForm.base_fields['pk_secao'].choices = local.secao_set.secao_pai().values_list('pk', 'num_secao')
        
        request.formClass = classForm
