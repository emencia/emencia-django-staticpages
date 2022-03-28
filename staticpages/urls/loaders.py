try:
    from django.conf.urls.defaults import url
except ImportError:
    from django.conf.urls import url

from ..views import StaticPageView


def mount_staticpages(*args):
    """
    Mount pages from the given list

    DEPRECATED: Almost duplicated code with "build_urls". Instead "build_urls" should
    be adapted to implement *args and page_map keyword arg passing.
    """
    urls = []

    for url_pattern, template_name, url_name in args:
        urls.append(url(
            url_pattern,
            StaticPageView.as_view(template_name=template_name, page_map=args),
            name=url_name
        ))

    return urls
