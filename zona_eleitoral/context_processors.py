
def base_url(request):
    """
    Returns context variables required by apps that use Django's authentication
    system.

    If there is no 'user' attribute in the request, uses AnonymousUser (from
    django.contrib.auth).
    """
    return {
        'base_url': request.path.replace(request.path_info, '')
    }
