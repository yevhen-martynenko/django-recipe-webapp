from rest_framework.renderers import BaseRenderer
import json


class PlainTextRenderer(BaseRenderer):
    media_type = 'text/plain'
    format = 'txt'

    def render(self, data, media_type=None, renderer_context=None):
        content = json.dumps(data, ensure_ascii=False, indent=4)
        return content.encode('utf-8')
