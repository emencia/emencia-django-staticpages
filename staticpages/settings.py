"""
Default application settings
----------------------------

These are the default settings you can override in your own project settings
right after the line which load the default app settings.

"""
STATICPAGES = []
"""
List of page definition to mount as urls.

It should be something like this: ::

    STATICPAGES = [
        ...
        (r'foo/$', "foo/index.html", 'foo-index'),
        (r'foo/part1/$', "foo/part1.html", 'foo-part1'),
        (r'foo/part2/$', "foo/part2.html", 'foo-part2'),
        ...
    ]

For each page item, the first item should be the url pattern, the second is the
template to use and the last one will be the url name.
"""
