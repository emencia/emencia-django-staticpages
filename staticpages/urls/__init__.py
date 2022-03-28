try:
    from django.conf.urls.defaults import url
except ImportError:
    from django.conf.urls import url

from ..views import StaticPageView


def build_urls(registry):
    """
    Build url objects from given registry list.

    Returns:
        list: A list of ``url`` objects.
    """
    urls = []

    for url_entry, template_name, url_name in registry]:
        urls.append(url(
            url_entry,
            StaticPageView.as_view(template_name=template_name),
            name=url_name,
        ))

    return urls
