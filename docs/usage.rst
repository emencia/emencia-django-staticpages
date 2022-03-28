.. _usage_intro:

=====
Usage
=====

Once installed you can configure some static pages to mount on urls in different ways.


The basic way
*************

This is the simpliest method to configure your static pages, more appropriated when
for basic needing: each page has its own template with a basic name and all pages are
in the same path directory.

So you got page templates in directory ``templates/staticpages/`` : ::

    templates/
    └── staticpages
        ├── bar.html
        ├── foo.html
        └── index.html

.. Note::
    Eventually if you need to store your templates in another directory, like
    ``templates/prototypes/samples/`` you can define it from settings: ::

        STATICPAGES_DEFAULT_TEMPLATEPATH = "prototypes/samples"

In your settings, you will just have to list their template names: ::

    STATICPAGES = [
        "index",
        "foo",
        "bar",
    ]

And finally mount them in your root ``urls.py`` like so: ::

    from staticpages.loader import StaticpagesLoader

    staticpages_loader = StaticpagesLoader()

    urlpatterns = [
        *staticpages_loader.build_urls(),
    ]

Your pages will be reachable on urls ``/``, ``/foo/`` and ``/bar/``.

.. Note::
    Note how ``index`` item have been resolved to ``/`` and not ``/index/``, this is
    from default behavior which assert than ``index`` is an index page, you can change
    this from settings ``STATICPAGES_INDEX_NAME``.


The explicit way
****************

The basic way is the quickest method to do but if you need to manage multiple pages
from various template directories or with specific path or different template names,
you will need to define a page with a dictionnary of options.


Options format
--------------

Here is a sample of all possible options for a page: ::

    {
        "path": "foo/",
        "re_path": r"foo/$",
        "template": "foo",
        "template_path": "foo.html",
        "name": "foo",
        "extra": "anything anykind",
    }

.. _usage_options_specs:

Specifications
..............

``path``
    Optional page url path that will be used to mount page on urls. So if
    ``foo/`` is given and you mount your pages on root urls, the page will be
    reachable from ``/foo/``.

    If not given, path will be resolved from template name suffixed by an
    ending slash.

``re_path``
    Optional page url regex path. Works exactly like ``path`` but is marked as
    a regex path to be mounted with Django function ``re_path()`` instead of
    ``path()``.

    If this option is given ``path`` is ignored.

``template``
    Template name without any leading path and ending file extension suffix
    (aka: ``foo``, not ``bar/foo.html``).

    If ``template_path`` is not given, this option is required. It will be used
    to resolve ``name`` or ``path`` options if they are not given.

``template_path``
    Full relative template path. If ``template`` option is not given, this one
    is required.

    If this option is given the ``name`` option is required since we can not resolve
    correctly an url name from a real path. And also the ``template`` option
    will be ignored.

    Using this option is a way to explicitely define a full template path
    instead of ``template`` option magic.

``name``
    Optional page url name used to mount url, it can be used to reverse it to
    page url with Django function ``django.urls.reverse``.

    This option becomes required if ``template_path`` option has been given.

    It must be a valid url name so no space or any special characters, only letters,
    numbers, ``-`` and ``_``. If you need to pass a display name to use in template,
    use the ``extra`` option to do so.

``extra``
    Extra data to pass to view in its options.


Defining page with options
--------------------------

So you got page templates in directory ``templates/staticpages/`` : ::

    templates/
    └── staticpages
        ├── page.html
        ├── index.html
        └── ping
            └── pong.html

In your settings, you will define them like so: ::

    STATICPAGES = [
        "index",
        {
            "template": "page",
        },
        {
            "template_path": "page.html",
            "name": "foo",
        },
        {
            "template_path": "ping/pong.html",
            "name": "ping-pong",
            "extra": "Ping-pong is magic!",
        },
    ]

.. Note::
    Note how you can mix both template name (a string) and option formats (dictionnary)
    in the same list. Because sometime you may have only a single page which needs
    options and vice versa.

And finally mount them in your root ``urls.py`` like so: ::

    from staticpages.loader import StaticpagesLoader

    staticpages_loader = StaticpagesLoader()

    urlpatterns = [
        *staticpages_loader.build_urls(),
    ]

Resulting in:

* The first item will be the index using ``index.html`` template and mounted on ``/``
  url;
* The second item is for demonstration purpose, it works exactly like the string format
  and will results to an url ``/page/`` using the ``page.html`` template;
* The third will results to an url ``/foo/`` using the ``page.html`` template;
* The fourth will results to an url ``/ping-pong/`` using the ``ping/pong.html``
  template which will have context variable ``page_extra`` with value
  ``Ping-pong is magic!``;

Loader options
**************

If you need to load different static pages from different applications, you won't be
able to manage them all from the settings.

To resolve this situation, Loader accept some arguments to override settings, see
:ref:`loader_docstring_args` documentation for details. Obviously you will need to use
different loader instance for each application to be able to provided different
arguments.

Static page template
********************

There is no ready to use template shipped with application since it is very basic
without any specific logic, you just have some template variables available that you
can use like you want.

But here is a basic sample: ::

    <!DOCTYPE html>
    <head>{% spaceless %}
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{% block head_title %}Staticpages sample{% endblock head_title %}</title>
    {% endspaceless %}
    </head>

    <body>{% spaceless %}
        {% block content %}
            {% comment %}Make a basic title using page name{% endcomment %}
            <h1>Sample {{ page_options.name }}</h1>

            {% comment %}Make a basic paragraph using page url name{% endcomment %}
            <p>{{ page_options.urlname }}</p>

            {% comment %}Use 'is_index' value as condition to list pages or not{% endcomment %}
            {% if page_options.is_index %}
                <ul class="menu">
                {% for item in staticpages %}
                    {% comment %}Do not list index page in the menu{% endcomment %}
                    {% if not item.is_index %}
                    <li>{{ item.name }}</li>
                    {% endif %}
                {% endfor %}
                </ul>
            {% endif %}

            {% comment %}Display 'extra' content if not empty{% endcomment %}
            {% if page_options.extra %}
                <div class="extra">{{ page_options.extra }}</div>
            {% endif %}

        {% endblock content %}
    {% endspaceless %}</body>
    </html>

.. _usage_template_context:

Template context variables
--------------------------

The variable ``page_options`` will contains the following items.

``name``
    The page name which is ever the template name or the url name depending provided
    options.

``urlname``
    The url name with possible prefix depending settings and loader arguments.

``template``
    The full template path.

``path``
    The url path or url regex path depending provided options.

``is_regex``
    A boolean to indicate if ``path`` is a regex path (True) or not (False)

``is_index``
    A boolean to mark a page as an index page. At this stage it only have an
    informational meaning which can be used in a template to distinguish a page from
    non index ones.

``extra``
    Some extra data you may want to pass to template. You can put anything you need in
    this variable.

There will be also a variable ``staticpages`` that is a list of all static pages
options related to a same loader instance (multiple loader instances won't share all
static pages).
