.. _install_intro:

=======
Install
=======

Install package in your environment : ::

    pip install emencia-django-staticpages

For development usage see :ref:`install_development`.


Configuration
*************

Add it to your installed Django apps in settings : ::

    INSTALLED_APPS = (
        ...
        "staticpages.apps.staticpagesConfig",
    )

Then load default application settings in your settings file: ::

    from staticpages.settings import *

See :ref:`usage_intro` to learn how to define pages and mount their urls.
