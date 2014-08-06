from models import OrgaoPublico

class OrgaoBackend(object):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, username=None, password=None, **kwargs):
        try:
            op = OrgaoPublico.objects.get_by_natural_key(username)
            if op.check_password(password):
                return op
            return None
        except OrgaoPublico.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            OrgaoPublico().set_password(password)

    def get_user(self, user_id):
        
        try:
            return OrgaoPublico.objects.get(pk=user_id)
        except OrgaoPublico.DoesNotExist:
            return None

