
def eleicao_atual(request):
    """
    Returns context variables required by apps that use Django's authentication
    system.

    If there is no 'user' attribute in the request, uses AnonymousUser (from
    django.contrib.auth).
    """
    if hasattr(request, 'eleicao_atual'):
        eleicao = request.eleicao_atual
    else:
        return {}
    return {
        'eleicao_atual': eleicao,
    }
