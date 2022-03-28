from staticpages.loader import StaticpagesLoader


def test_loader_resolve_registry():
    """
    Registry items should be resolved as expected according to defined options and given
    arguments.
    """
    loader = StaticpagesLoader(
        template_basepath="prefix/path",
        name_base="plop-",
    )

    resolved = loader.resolve_registry(
        registry=[
            "foo",
            {
                "template": "nope",
                "template_path": "plif/plaf.html",
                "re_path": r"plouf/$",
                "name": "plof",
            },
        ],
    )

    assert resolved == [
        {
            "path": "foo/",
            "template": "prefix/path/foo.html",
            "name": "foo",
            "urlname": "plop-foo",
            "is_index": False,
            "is_regex": False,
            "extra": None,
        },
        {
            "path": r"plouf/$",
            "template": "prefix/path/plif/plaf.html",
            "name": "plof",
            "urlname": "plop-plof",
            "is_index": False,
            "is_regex": True,
            "extra": None,
        },
    ]


def test_loader_resolve_registry_empty(settings):
    """
    Registry resolver should not fail even without arguments and empty registry list in
    settings.
    """
    settings.STATICPAGES = []

    loader = StaticpagesLoader()

    resolved = loader.resolve_registry()

    assert resolved == []


def test_loader_resolve_registry_defaults(settings):
    """
    Registry items should be resolved as expected according to defined options and use
    default values from settings for non defined arguments.
    """
    settings.STATICPAGES = ["foo"]
    settings.STATICPAGES_DEFAULT_TEMPLATEPATH = "ping"
    settings.STATICPAGES_DEFAULT_NAME_BASE = "plop-"
    settings.STATICPAGES_DEFAULT_URLPATH = "moo"

    loader = StaticpagesLoader()

    resolved = loader.resolve_registry()

    assert resolved == [
        {
            "path": "moo/foo/",
            "template": "ping/foo.html",
            "name": "foo",
            "urlname": "plop-foo",
            "is_index": False,
            "is_regex": False,
            "extra": None,
        },
    ]
