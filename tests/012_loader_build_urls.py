import pytest

from staticpages.loader import StaticpagesLoader
from staticpages.views import StaticPageView


class DummyPageView(StaticPageView):
    """
    Just a dummy view which inherits from StaticPageView to respect signature
    """
    pass


@pytest.mark.parametrize("item, template_basepath, name_base, url_basepath, expected", [
    (
        {
            "template": "foo",
        },
        None,
        None,
        None,
        {
            "name": "foo",
            "pattern": "foo/",
            "template_name": "foo.html",
            "page_options": {
                "name": "foo",
                "path": "foo/",
                "template": "foo.html",
                "urlname": "foo",
                "is_index": False,
                "is_regex": False,
                "extra": None,
            },
            "staticpages": ["one", "two"],
        },
    ),
    (
        {
            "template_path": "plip/plop.html",
            "name": "plup",
        },
        None,
        None,
        None,
        {
            "name": "plup",
            "pattern": "plup/",
            "template_name": "plip/plop.html",
            "page_options": {
                "name": "plup",
                "path": "plup/",
                "template": "plip/plop.html",
                "urlname": "plup",
                "is_index": False,
                "is_regex": False,
                "extra": None,
            },
            "staticpages": ["one", "two"],
        },
    ),
    (
        {
            "template_path": "machin.html",
            "name": "index",
        },
        None,
        None,
        None,
        {
            "name": "index",
            "pattern": "",
            "template_name": "machin.html",
            "page_options": {
                "name": "index",
                "path": "",
                "template": "machin.html",
                "urlname": "index",
                "is_index": True,
                "is_regex": False,
                "extra": None,
            },
            "staticpages": ["one", "two"],
        },
    ),
    (
        {
            "template": "foo",
        },
        "to/templates",
        "base-",
        "statics",
        {
            "name": "base-foo",
            "pattern": "statics/foo/",
            "template_name": "to/templates/foo.html",
            "page_options": {
                "name": "foo",
                "path": "statics/foo/",
                "template": "to/templates/foo.html",
                "urlname": "base-foo",
                "is_index": False,
                "is_regex": False,
                "extra": None,
            },
            "staticpages": ["one", "two"],
        },
    ),
])
def test_loader_build_url(item, template_basepath, name_base, url_basepath, expected):
    """
    Page item should create a correct UrlPattern with expected options.
    """
    loader = StaticpagesLoader(
        template_basepath=template_basepath,
        name_base=name_base,
        url_basepath=url_basepath,
    )

    resolved = loader.resolve_item(item)
    url = loader.build_url(resolved, ["one", "two"])

    # Build a dict of relevant values to compare to expection
    results = {
        "name": url.name,
        "pattern": str(url.pattern),
        "template_name": url.callback.view_initkwargs["template_name"],
        "page_options": url.callback.view_initkwargs["page_options"],
        "staticpages": url.callback.view_initkwargs["staticpages"],
    }

    assert results == expected


def test_loader_build_url_view():
    """
    If view class is given as argument it should be used to build item UrlPattern.
    """
    # Let the default view class to be used
    loader = StaticpagesLoader()
    resolved = loader.resolve_item({"template": "foo"})
    url = loader.build_url(resolved, ["one", "two"])
    assert url.callback.view_class == StaticPageView

    # Explicitely use StaticPageView class
    loader = StaticpagesLoader(view_class=StaticPageView)
    resolved = loader.resolve_item({"template": "bar"})
    url = loader.build_url(resolved, ["one", "two"])
    assert url.callback.view_class == StaticPageView

    # Use a custom dummy view class
    loader = StaticpagesLoader(view_class=DummyPageView)
    resolved = loader.resolve_item({"template": "ping"})
    url = loader.build_url(resolved, ["one", "two"])
    assert url.callback.view_class == DummyPageView


def test_loader_build_urls_defaults(settings):
    """
    A list of UrlPattern should be correctly created from defaults (from settings).
    """
    settings.STATICPAGES = ["index", "foo"]
    settings.STATICPAGES_DEFAULT_TEMPLATEPATH = "ping"
    settings.STATICPAGES_DEFAULT_NAME_BASE = "plop-"
    settings.STATICPAGES_DEFAULT_URLPATH = "moo"

    loader = StaticpagesLoader()

    urls = loader.build_urls()

    index_url = urls[0]
    assert str(index_url.pattern) == "moo/"
    assert index_url.name == "plop-index"
    assert index_url.callback.view_initkwargs["template_name"] == "ping/index.html"

    foo_url = urls[1]
    assert str(foo_url.pattern) == "moo/foo/"
    assert foo_url.name == "plop-foo"
    assert foo_url.callback.view_initkwargs["template_name"] == "ping/foo.html"


def test_loader_build_urls(settings):
    """
    A list of UrlPattern should be correctly created from given registry.
    """
    loader = StaticpagesLoader()
    urls = loader.build_urls(["index", "foo"])

    index_url = urls[0]
    assert str(index_url.pattern) == ""
    assert index_url.name == "index"
    assert index_url.callback.view_initkwargs["template_name"] == "index.html"

    foo_url = urls[1]
    assert str(foo_url.pattern) == "foo/"
    assert foo_url.name == "foo"
    assert foo_url.callback.view_initkwargs["template_name"] == "foo.html"
