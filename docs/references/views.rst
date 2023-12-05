.. _references_views_intro:

=====
Views
=====

Implemented view is a basic view which inherits from
``django.views.generic.TemplateView`` to add some additional attribute and extend the
template context.

If needed you can define another class based view to use with loader argument
``view_class``.

.. automodule:: staticpages.views
    :members: StaticPageView
