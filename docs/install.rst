.. _intro_install:

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
        "staticpages",
    )

Then load default application settings in your settings file: ::

    from staticpages.settings import *

Then mount applications URLs: ::

    urlpatterns = [
        ...
        path("", include("staticpages.urls")),
    ]

And finally apply database migrations.

Settings
********

.. automodule:: staticpages.settings
   :members:
