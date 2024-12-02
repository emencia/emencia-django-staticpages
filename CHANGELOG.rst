
=========
Changelog
=========

Development
-----------

Minor release without any incompatible changes, you should be able to safely migrate.

* Added support for **Django 5.0** and **Django 5.1**;
* Added minimal version for all requirements;
* Updated script to freeze local dependencies;


Version 0.6.0 - 2023/12/06
--------------------------

You should be able to safely migrate to this version without any changes if you are
fullfilling requirements.

* Added official support for Django 4.1 and 4.2;
* Dropped support for Django<4.0;
* Added official support for Python 3.11;
* Dropped official support for Python<3.10;
* Restructured package configuration
* Refactored documentation with Sphinx theme Furo;
* Added a logo;


Version 0.5.1 - 2022/09/18
--------------------------

Added official support for Django 4.0.


Version 0.5.0 - 2022/04/04
--------------------------

**Complete refactoring**

To modernize this application, a lot of work was required thus this version is totally
incompatible with previous version usages.

* Dropped support for Python3.6;
* Added official support for Python 3.7 to 3.9;
* Added official support for Django 2.2 to 3.2;
* Restructured packaging;
* Added full test coverage;
* Implement new ways to define staticpages;

The 0.5.x branch will be the last to support Python3.7.


Version 0.4.0 - 2014/10/01
--------------------------

**Last version with Python3.6 and Django<2.2 version**

In these old times, there was no changelog. Application was using a totally different
strategy where you explicitely define all page url options (url regex path, url path,
url name).

0.4.0 was the last release from this era and was compatible with Python 3.6 and
Django prior 2.0 version.
