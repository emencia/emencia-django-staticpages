import pytest

from staticpages.exceptions import StaticpagesResolverError
from staticpages.loader import StaticpagesLoader


def test_loader_foo():
    """
    Either template or template_path option is required.
    """
    loader = StaticpagesLoader()

    with pytest.raises(StaticpagesResolverError):
        loader.resolve_item({"name": "plup"})


def test_loader_validate_item_fail_template():
    """
    Either template or template_path option is required.
    """
    loader = StaticpagesLoader()

    with pytest.raises(StaticpagesResolverError):
        loader.validate_item({"name": "plup"})


def test_loader_validate_item_fail_name():
    """
    name argument is required if template_path is given.
    """
    loader = StaticpagesLoader()

    with pytest.raises(StaticpagesResolverError):
        loader.validate_item({
            "template_path": "plip/plop.html",
            "template": "foo",
        })


@pytest.mark.parametrize("item, expected", [
    (
            {
                "template": "foo",
            },
            {
                "path": "foo/",
                "template": "foo.html",
                "name": "foo",
                "urlname": "foo",
                "is_index": False,
                "is_regex": False,
                "extra": None,
            },
    ),
    (
            {
                "template_path": "plip/plop.html",
                "name": "plup",
            },
            {
                "path": "plup/",
                "template": "plip/plop.html",
                "name": "plup",
                "urlname": "plup",
                "is_index": False,
                "is_regex": False,
                "extra": None,
            },
    ),
    (
            {
                "re_path": r"ping/$",
                "template": "bar",
                "name": "pong",
            },
            {
                "path": r"ping/$",
                "template": "bar.html",
                "name": "pong",
                "urlname": "pong",
                "is_index": False,
                "is_regex": True,
                "extra": None,
            },
    ),
    (
            {
                "template": "bar",
                "template_path": "plif/plaf.html",
                "re_path": r"plouf/$",
                "name": "plof",
                "extra": "free for use",
            },
            {
                "path": r"plouf/$",
                "template": "plif/plaf.html",
                "name": "plof",
                "urlname": "plof",
                "is_index": False,
                "is_regex": True,
                "extra": "free for use",
            },
    ),
])
def test_loader_resolve_item_no_args(item, expected):
    """
    Item should be correctly resolved from given data.
    """
    loader = StaticpagesLoader()

    resolved = loader.resolve_item(item)

    assert resolved == expected


@pytest.mark.parametrize("item, expected", [
    (
            {
                "template": "index",
            },
            {
                "path": "",
                "template": "prefix/path/index.html",
                "name": "index",
                "urlname": "index",
                "is_index": True,
                "is_regex": False,
                "extra": None,
            },
    ),
    (
            {
                "template": "foo",
            },
            {
                "path": "foo/",
                "template": "prefix/path/foo.html",
                "name": "foo",
                "urlname": "foo",
                "is_index": False,
                "is_regex": False,
                "extra": None,
            },
    ),
    (
            {
                "template_path": "plip/plop.html",
                "name": "plup",
            },
            {
                "path": "plup/",
                "template": "prefix/path/plip/plop.html",
                "name": "plup",
                "urlname": "plup",
                "is_index": False,
                "is_regex": False,
                "extra": None,
            },
    ),
])
def test_loader_resolve_item_template_basepath(item, expected):
    """
    Item should be correctly resolved from given data and template path should always
    be augmented with 'template_basepath' argument value.
    """
    loader = StaticpagesLoader(template_basepath="prefix/path")

    resolved = loader.resolve_item(item)

    assert resolved == expected


@pytest.mark.parametrize("item, expected", [
    (
            {
                "template": "foo",
            },
            {
                "path": "foo/",
                "template": "foo.html",
                "name": "foo",
                "urlname": "plop-foo",
                "is_index": False,
                "is_regex": False,
                "extra": None,
            },
    ),
    (
            {
                "template_path": "plip/plop.html",
                "name": "plup",
            },
            {
                "path": "plup/",
                "template": "plip/plop.html",
                "name": "plup",
                "urlname": "plop-plup",
                "is_index": False,
                "is_regex": False,
                "extra": None,
            },
    ),
])
def test_loader_resolve_item_name_base(item, expected):
    """
    Item should be correctly resolved from given data and url name is prefixed with
    'name_base' argument value if given.
    """
    loader = StaticpagesLoader(name_base="plop-")

    resolved = loader.resolve_item(item)

    assert resolved == expected


@pytest.mark.parametrize("item, expected", [
    (
            {
                "template": "index",
            },
            {
                "path": "plop/",
                "template": "index.html",
                "name": "index",
                "urlname": "index",
                "is_index": True,
                "is_regex": False,
                "extra": None,
            },
    ),
    (
            {
                "template_path": "plip/plap.html",
                "name": "plup",
            },
            {
                "path": "plop/plup/",
                "template": "plip/plap.html",
                "name": "plup",
                "urlname": "plup",
                "is_index": False,
                "is_regex": False,
                "extra": None,
            },
    ),
])
def test_loader_resolve_item_url_basepath(item, expected):
    """
    Item url path should be prefixed with 'url_basepath' argument value if not empty.
    """
    loader = StaticpagesLoader(url_basepath="plop")

    resolved = loader.resolve_item(item)

    assert resolved == expected


@pytest.mark.parametrize("item, expected", [
    (
            {
                "template": "index",
            },
            {
                "path": "",
                "template": "index.html",
                "name": "index",
                "urlname": "plop-index",
                "is_index": True,
                "is_regex": False,
                "extra": None,
            },
    ),
    (
            {
                "template_path": "plip/plop.html",
                "name": "index",
            },
            {
                "path": "",
                "template": "plip/plop.html",
                "name": "index",
                "urlname": "plop-index",
                "is_index": True,
                "is_regex": False,
                "extra": None,
            },
    ),
])
def test_loader_resolve_item_index(item, expected):
    """
    Item should have 'is_index' as True if its resolved name (without name prefix)
    match the value of setting 'STATICPAGES_INDEX_NAME' and path shortened to a
    simple '/' (but with possible path prefix)
    """
    loader = StaticpagesLoader(name_base="plop-")

    resolved = loader.resolve_item(item)

    assert resolved == expected


@pytest.mark.parametrize("item, expected", [
    (
            {
                "template": "index",
            },
            {
                "path": "plop/",
                "template": "index.html",
                "name": "index",
                "urlname": "index",
                "is_index": True,
                "is_regex": False,
                "extra": None,
            },
    ),
    (
            {
                "template": "ping",
            },
            {
                "path": "plop/ping/",
                "template": "ping.html",
                "name": "ping",
                "urlname": "ping",
                "is_index": False,
                "is_regex": False,
                "extra": None,
            },
    ),
])
def test_loader_resolve_item_index_url_basepath(item, expected):
    """
    Index url should be correctly prefix with value from 'url_basepath' argument.
    """
    loader = StaticpagesLoader(url_basepath="plop")

    resolved = loader.resolve_item(item)

    assert resolved == expected
