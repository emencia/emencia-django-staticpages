from django.conf import settings

try:
    from django.conf.urls.defaults import patterns
except ImportError:
    from django.conf.urls import patterns

from . import build_urls


# Mount page urls
urlpatterns = patterns('', *build_urls(settings.STATICPAGES))
