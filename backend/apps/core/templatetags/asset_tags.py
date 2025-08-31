import json
from django.contrib.staticfiles import finders
from django.utils.safestring import mark_safe
from django import template

register = template.Library()

_manifest_cache = None


@register.simple_tag
def asset_tags(path):
    global _manifest_cache
    if _manifest_cache is None:
        manifest_file = finders.find('manifest.json')
        if not manifest_file:
            return path
        with open(manifest_file, 'r') as f:
            _manifest_cache = json.load(f)

    hashed_path = _manifest_cache.get(path)
    if not hashed_path:
        return path  # fallback if not found

    if hashed_path.startswith('static/'):
        hashed_path = hashed_path[7:]

    return mark_safe(f"/static/{hashed_path}")
