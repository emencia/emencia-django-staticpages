import pytest

from staticpages.utils.tests import html_pyquery


@pytest.mark.urls("sandbox.staticpages_testapp.base_urls")
@pytest.mark.parametrize("url, name, urlname, pages, extra", [
    (
        "/",
        "index",
        "index",
        ["foo"],
        None,
    ),
    (
        "/foo/",
        "foo",
        "foo",
        None,
        "free for use",
    ),
    (
        "/sub/",
        "index",
        "index",
        None,
        None,
    ),
    (
        "/sub/plif/",
        "plif",
        "plif",
        None,
        None,
    ),
])
def test_loader_build_urls(client, url, name, urlname, pages, extra):
    """
    A list of UrlPattern should be correctly created from given registry.

    Urls are created and mounted from 'test_mount_urls' url map used just for this test.

    Some very basic display logic have been done in the template to show some data to
    check against.
    """
    response = client.get(url)

    assert response.status_code == 200

    dom = html_pyquery(response)

    # print()
    # print(response.content.decode("UTF-8"))
    # print()

    assert dom.find("h1").text() == "Sample {}".format(name)
    assert dom.find("p").text() == urlname

    # If expected 'staticpages' variable is given, check the dummy menu list correctly
    # its items
    if pages is not None:
        assert [item.text for item in dom.find("ul.menu > li")] == pages

    # If expected 'staticpages' variable is given, check the dummy menu list correctly
    # its items
    if extra is not None:
        assert dom.find("div.extra").text() == extra
