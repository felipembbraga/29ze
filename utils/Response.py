from django.http import HttpResponse
import json

class NotifyResponse(HttpResponse):
    def __init__(self, content='', theme='erro', redirect_url='', lista='', mimetype='application/json', *args, **kwargs):
        notify = {
                  'theme': theme,
                  'title': str(content),
                  'list':lista,
                  'redirect_url':redirect_url
                  }
        super(NotifyResponse, self).__init__(json.dumps(notify), mimetype, *args, **kwargs)